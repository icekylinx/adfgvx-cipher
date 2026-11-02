"""Build independently documented German n-gram models from public-domain books.

The attacked and solved 1918 radiograms are excluded from training.
Cached source texts are intermediates and need not be distributed.
"""
import argparse
import array
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
IDS = [22367, 2407, 6099, 5323, 21000, 34811, 24571]


def fetch(book_id):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    path = ROOT / "data" / "corpus" / f"pg{book_id}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        data = urllib.request.urlopen(url, timeout=40).read()
        path.write_bytes(data)
    data = path.read_bytes()
    text = data.decode("utf-8-sig", "replace")
    title = re.search(r"^Title:\s*(.+)$", text, flags=re.M)
    language = re.search(r"^Language:\s*(.+)$", text, flags=re.M)
    metadata = {"id": book_id, "url": url, "sha256": hashlib.sha256(data).hexdigest(),
                "title": title.group(1).strip() if title else "not recorded",
                "language": language.group(1).strip() if language else "not recorded"}
    start = re.search(r"\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", text, re.S)
    end = re.search(r"\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK", text)
    if start:
        text = text[start.end(): end.start() if end else len(text)]
    elif end:
        text = text[:end.start()]
    return metadata, text


def streams(text):
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    text = text.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE").replace("ß", "ss").upper()
    # The X is a literal separator in the historical alphabet. Two independently
    # specified textual conventions are mixed; no candidate text is inserted.
    plain = re.sub(r"[^A-Z0-9]", "", text)
    sentence = re.sub(r"[.!?;:\n]+", "X", text)
    sentence = re.sub(r"[^A-Z0-9]", "", sentence)
    sentence = re.sub("XX+", "X", sentence)
    word = "X".join(re.findall(r"[A-Z0-9]+", text))
    return [(plain, 5), (sentence, 3), (word, 1)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--download-only", action="store_true")
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=3) as pool:
        source = list(pool.map(fetch, IDS))
    meta = [m for m, _ in source]
    (ROOT / "data" / "corpus_sources.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2), flush=True)
    if args.download_only:
        return
    counts = Counter()
    mono = Counter()
    for m, text in source:
        if m["language"].lower() != "german":
            print("Excluded non-German source", m["id"], flush=True)
            continue
        for stream, weight in streams(text):
            c = Counter(stream[i:i+4] for i in range(len(stream)-3))
            for gram, count in c.items():
                counts[gram] += count*weight
            for ch, count in Counter(stream).items():
                mono[ch] += count*weight
    total = sum(counts.values())
    floor = math.log10(0.01/total)
    table = array.array("f", [floor] * (36**4))
    for gram, count in counts.items():
        z = 0
        for ch in gram:
            z = z*36 + ALPHABET.index(ch)
        table[z] = math.log10(count/total)
    path = ROOT / "data" / "german36_quad.bin"
    with path.open("wb") as f:
        table.tofile(f)
    info = {"alphabet": ALPHABET, "entries": len(table), "total_weighted_windows": total,
            "distinct_windows": len(counts), "floor": floor,
            "mixture_weights": {"letters_and_digits": 5, "sentence_X": 3, "word_X": 1},
            "training_includes_challenge_plaintexts": False,
            "monograms": dict(mono), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    (ROOT / "data" / "german36_model.json").write_text(json.dumps(info, indent=2))
    print(json.dumps(info, indent=2), flush=True)


if __name__ == "__main__":
    main()
