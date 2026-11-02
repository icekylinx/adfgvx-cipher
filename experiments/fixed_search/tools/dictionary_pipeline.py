"""Reproduce dictionary normalization, length-matched profiles and selection."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import heapq
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile

from build_models import load_book, streams

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from cipher import validate_ciphertext


def ranks(word):
    result = [0] * len(word)
    for rank, column in enumerate(sorted(range(len(word)), key=lambda i: (word[i], i)), 1):
        result[column] = rank
    return result


def normalize(args):
    provenance = json.loads((ROOT / "data/wordlist_provenance.json").read_text())
    source = next(x for x in provenance["upstream_files"] if x["local_name"] == "words")
    raw = args.raw.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == source["sha256"], "Raw wordlist hash changed"
    metadata = provenance["normalization"]
    words = raw.decode("utf-8").splitlines() + metadata["manual_context_words"] + metadata["injected_positive_controls"]
    candidates = set()
    for word in words:
        upper = word.upper()
        for table in [{"Ä": "AE", "Ö": "OE", "Ü": "UE"}, {"Ä": "A", "Ö": "O", "Ü": "U"}]:
            value = upper
            for old, new in table.items():
                value = value.replace(old, new)
            value = re.sub("[^A-Z]", "", value)
            if 8 <= len(value) <= 40:
                candidates.add(value)
    data = ("\n".join(sorted(candidates)) + "\n").encode()
    digest = hashlib.sha256(data).hexdigest()
    assert len(candidates) == metadata["unique_candidates"]
    assert digest == metadata["sha256"], (digest, metadata["sha256"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(json.dumps({"words": len(candidates), "sha256": digest, "maximum_length": max(map(len, candidates))}, indent=2))


def features(text):
    counts = Counter(text.replace("?", ""))
    n = sum(counts.values())
    profile = sorted(counts.values(), reverse=True) + [0] * (36 - len(counts))
    pairs = Counter(text[i:i + 2] for i in range(len(text) - 1) if "?" not in text[i:i + 2])
    m = sum(pairs.values())
    return [value / n for value in profile] + [sum(value * (value - 1) for value in pairs.values()) / (m * (m - 1))]


def profiles(args):
    args.output.mkdir(parents=True, exist_ok=True)
    sources = [s for s in json.loads((ROOT / "data/model_provenance.json").read_text())["general_sources"]
               if s["language"].lower() == "german"]
    texts = [streams(load_book(source, args.corpus_directory)) for source in sources]
    reports = []
    for mid in ["p73", "p170"]:
        expected_path = ROOT / "data/dictionary_profiles" / (mid + "_profile.txt")
        metadata = json.loads(expected_path.with_suffix(".json").read_text())
        n, erased = metadata["plaintext_length"], metadata["received_erased_symbols"]
        rng = random.Random(metadata["seed"])
        samples = []
        for variants in texts:
            for stream, weight in variants:
                for _ in range(200 * weight):
                    start = rng.randrange(len(stream) - n)
                    sample = list(stream[start:start + n])
                    missing = rng.randint((erased + 1) // 2, erased) if erased else 0
                    for i in rng.sample(range(n), missing):
                        sample[i] = "?"
                    samples.append(features("".join(sample)))
        means = [sum(row[i] for row in samples) / len(samples) for i in range(37)]
        variances = [sum((row[i] - means[i]) ** 2 for row in samples) / (len(samples) - 1) for i in range(37)]
        output = "\n".join(f"{a:.12g} {b:.12g}" for a, b in zip(means, variances)) + "\n"
        assert len(samples) == metadata["sample_count"] == 10800
        assert means == metadata["means"] and variances == metadata["variances"]
        assert output == expected_path.read_text()
        (args.output / expected_path.name).write_text(output)
        reports.append({"message": mid, "samples": len(samples), "sha256": hashlib.sha256(output.encode()).hexdigest(), "exact_match": True})
    print(json.dumps(reports, indent=2))


def select(args):
    expected = json.loads((ROOT / "data/dictionary_candidates.json").read_text())
    provenance = json.loads((ROOT / "data/wordlist_provenance.json").read_text())
    assert hashlib.sha256(args.words.read_bytes()).hexdigest() == provenance["normalization"]["sha256"]
    args.output.mkdir(parents=True, exist_ok=True)
    reports = []
    for mid in ["p73", "p170"]:
        ciphertext = expected["messages"][mid]["ciphertext"]
        validate_ciphertext(ciphertext)
        letters = len(ciphertext) // 2
        minimum_known_cells = letters - ciphertext.count("?")
        if 2 * minimum_known_cells - letters - 1 < 2:
            raise ValueError("Insufficient guaranteed observed adjacent cells for the archived IC scanner")
        with tempfile.TemporaryDirectory(prefix="adfgvx_dictionary_") as folder:
            inp = Path(folder) / "input.txt"
            inp.write_text("1\n" + ciphertext + "\n")
            scores = Path(folder) / "scores.tsv"
            with scores.open("w") as file:
                process = subprocess.run([str(args.scanner), str(ROOT / "data/dictionary_profiles" / (mid + "_profile.txt")),
                                          str(args.words), str(inp)], stdout=file, stderr=subprocess.PIPE, text=True, check=True)
            heaps = defaultdict(list)
            for line in scores.open():
                width, profile, ic, word = line.rstrip().split("\t")
                width, profile, ic = int(width), float(profile), float(ic)
                for metric, value in [("profile", profile), ("ic", ic)]:
                    item = (value, word, profile, ic)
                    heap = heaps[(width, metric)]
                    if len(heap) < 300:
                        heapq.heappush(heap, item)
                    elif item > heap[0]:
                        heapq.heapreplace(heap, item)
            rows = []
            for (width, metric), heap in heaps.items():
                seen = set()
                for _, word, profile, ic in sorted(heap, reverse=True):
                    order = tuple(ranks(word))
                    if order in seen:
                        continue
                    rank = len(seen)
                    seen.add(order)
                    rows.append({"k": width, "metric": metric, "rank": rank, "word": word,
                                 "ranks": list(order), "profile": profile, "ic": ic})
                    if len(seen) == 20:
                        break
            rows.sort(key=lambda row: (row["k"], row["metric"], row["rank"]))
            assert rows == expected["messages"][mid]["candidates"], mid + " selection differs"
            output = {"message": mid, "ciphertext": ciphertext, "candidates": rows,
                      "selection_matches_archived": True, "scanner_stderr": process.stderr}
            (args.output / (mid + "_selected.json")).write_text(json.dumps(output, indent=2) + "\n")
            reports.append({"message": mid, "selection_records": len(rows), "exact_match": True})
    print(json.dumps(reports, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("normalize")
    p.add_argument("--raw", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.set_defaults(function=normalize)
    p = sub.add_parser("profiles")
    p.add_argument("--corpus-directory", type=Path, action="append", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.set_defaults(function=profiles)
    p = sub.add_parser("select")
    p.add_argument("--words", type=Path, required=True)
    p.add_argument("--scanner", type=Path, default=ROOT / "bin/dictionary_profile")
    p.add_argument("--output", type=Path, required=True)
    p.set_defaults(function=select)
    args = parser.parse_args()
    args.function(args)


if __name__ == "__main__":
    main()
