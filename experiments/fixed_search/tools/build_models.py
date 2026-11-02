"""Rebuild hash-pinned German models without distributing corpora or binaries.

Existing cached books may be shared with the other experiment packages.
Downloads require --download and are accepted only at the recorded hashes.
"""
from __future__ import annotations
import argparse
import array
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def streams(text):
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    text = text.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE").replace("ß", "ss").upper()
    plain = re.sub(r"[^A-Z0-9]", "", text)
    sentence = re.sub(r"[.!?;:\n]+", "X", text)
    sentence = re.sub(r"[^A-Z0-9]", "", sentence)
    sentence = re.sub("XX+", "X", sentence)
    word = "X".join(re.findall(r"[A-Z0-9]+", text))
    return [(plain, 5), (sentence, 3), (word, 1)]


def load_book(source, directories, download=False, cache=None):
    filename = f"pg{source['id']}.txt"
    candidates = [Path(folder) / filename for folder in directories]
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        if not download or cache is None:
            raise FileNotFoundError(f"Missing {filename}; supply --corpus-directory or --download --cache-directory")
        path = Path(cache) / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        data = urllib.request.urlopen(source["url"], timeout=45).read()
        if hashlib.sha256(data).hexdigest() != source["sha256"]:
            raise ValueError(f"Downloaded source hash changed: {source['url']}")
        path.write_bytes(data)
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != source["sha256"]:
        raise ValueError(f"Source hash does not match the recorded book: {path}")
    text = data.decode("utf-8-sig", "replace")
    language = re.search(r"^Language:\s*(.+)$", text, re.M)
    if language is None or language.group(1).strip().lower() != "german":
        raise ValueError(f"Expected the recorded German source: {path}")
    start = re.search(r"\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", text, re.S)
    end = re.search(r"\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK", text)
    if start:
        text = text[start.end():end.start() if end else len(text)]
    elif end:
        text = text[:end.start()]
    return text


def write_array(file, values):
    if sys.byteorder == "big":
        values.byteswap()
    values.tofile(file)


def build(sources, args, kind, expected):
    q4, q6 = Counter(), Counter()
    indices = {c: i for i, c in enumerate(ALPHABET)}
    directories = args.corpus_directory + ([args.cache_directory] if args.cache_directory else [])
    for source in sources:
        text = load_book(source, directories, args.download, args.cache_directory)
        for stream, stream_weight in streams(text):
            weight = stream_weight * (source.get("domain_weight", 1) if kind == "military" else 1)
            code = 0
            for i, character in enumerate(stream):
                code = (code * 36 + indices[character]) % (36 ** 6)
                if i >= 3:
                    q4[code % (36 ** 4)] += weight
                if kind == "military" and i >= 5:
                    q6[code] += weight
        print(json.dumps({"model": kind, "processed_book": source["id"]}), flush=True)
    total4 = sum(q4.values())
    floor4 = math.log10(0.01 / total4)
    quad = array.array("f", [floor4]) * (36 ** 4)
    for code, count in q4.items():
        quad[code] = math.log10(count / total4)
    quad_name = "german36_quad.bin" if kind == "general" else "german_military36_quad.bin"
    quad_path = args.output / quad_name
    with quad_path.open("wb") as file:
        write_array(file, quad)
    quad_hash = hashlib.sha256(quad_path.read_bytes()).hexdigest()
    expected_quad = expected["sha256"] if kind == "general" else expected["quad"]["sha256"]
    if quad_hash != expected_quad:
        raise AssertionError(("Quadgram rebuild mismatch", quad_hash, expected_quad))
    report = {"model": kind, "quad_sha256": quad_hash, "weighted_quad_windows": total4,
              "quad_types": len(q4), "hash_matches_archived_model": True}
    if kind == "military":
        total6 = sum(q6.values())
        floor6 = math.log10(0.01 / total6)
        size = 1
        while size < 2 * len(q6):
            size *= 2
        keys = array.array("I", [0]) * size
        values = array.array("f", [floor6]) * size
        for code, count in q6.items():
            key = code + 1
            h = ((key ^ (key >> 16)) * 0x7FEB352D) & 0xFFFFFFFF
            h = ((h ^ (h >> 15)) * 0x846CA68B) & 0xFFFFFFFF
            h ^= h >> 16
            slot = h & (size - 1)
            while keys[slot]:
                slot = (slot + 1) & (size - 1)
            keys[slot] = key
            values[slot] = math.log10(count / total6)
        six_path = args.output / "german_military36_sixgram.bin"
        with six_path.open("wb") as file:
            file.write(struct.pack("<8sIIf", b"G6HASH2\0", size, len(q6), floor6))
            write_array(file, keys)
            write_array(file, values)
        six_hash = hashlib.sha256(six_path.read_bytes()).hexdigest()
        if six_hash != expected["six"]["sha256"]:
            raise AssertionError(("Six-gram rebuild mismatch", six_hash, expected["six"]["sha256"]))
        report.update(six_sha256=six_hash, weighted_six_windows=total6, six_types=len(q6))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provenance", type=Path, default=ROOT / "data/model_provenance.json")
    parser.add_argument("--corpus-directory", type=Path, action="append", default=[])
    parser.add_argument("--cache-directory", type=Path)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--kind", choices=["general", "military", "all"], default="all")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.download and args.cache_directory is None:
        parser.error("--download requires --cache-directory")
    args.output.mkdir(parents=True, exist_ok=True)
    provenance = json.loads(args.provenance.read_text())
    reports = []
    if args.kind in ["general", "all"]:
        general = [s for s in provenance["general_sources"] if s["language"].lower() == "german"]
        reports.append(build(general, args, "general", provenance["general_model"]))
    if args.kind in ["military", "all"]:
        reports.append(build(provenance["military_model"]["sources"], args, "military", provenance["military_model"]))
    (args.output / "rebuild_report.json").write_text(json.dumps(reports, indent=2) + "\n")
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
