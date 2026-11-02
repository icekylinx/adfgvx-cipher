"""Exact dictionary and contiguous-phrase searches for the recorded column keys.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Inputs are the existing hash-pinned normalized wordlist and ten source books.
Books, normalized streams, and compiled executables stay outside the repository.
"""

from argparse import ArgumentParser
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import random
import re
import subprocess

from analyze import HERE, ROOT, P153, stable_ranks


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def normalized(text, mode):
    text = text.upper()
    for original, replacement in (("Ä", "AE"), ("Ö", "OE"), ("Ü", "UE")):
        text = text.replace(original, replacement if mode == "expanded" else replacement[0])
    return re.sub("[^A-Z]", "", text)


def targets():
    keys = json.loads((ROOT / "data/keys.json").read_text())["keys"]
    answer = [{"id": key["id"], "ranks": key["column_rank_order"]} for key in keys]
    p153 = next(key for key in answer if key["id"] == P153)
    answer.append({"id": P153 + "-pair-swapped", "ranks": [p153["ranks"][i ^ 1] for i in range(18)]})
    return answer


def write_targets(rows, path):
    lines = [str(len(rows))]
    for row in rows:
        assert re.fullmatch(r"[A-Za-z0-9-]+", row["id"])
        ranks = row["ranks"]
        lines.append(f"{row['id']} {len(ranks)} " + " ".join(map(str, ranks)))
    path.write_text("\n".join(lines) + "\n")


def run_scanner(binary, target_path, files):
    completed = subprocess.run([str(binary), str(target_path), *map(str, files)],
                               check=True, capture_output=True, text=True)
    return [json.loads(line) for line in completed.stdout.splitlines()]


def scanner_control(binary, target_path, rows, work_dir):
    rng = random.Random(15320261102)
    words = ["VIKINGSCROWNHOTEL", "TRUPPENVERSCHIEBUNG"]
    # An arbitrary distinct-letter witness is available for every numeric key.
    words.extend("".join(chr(64 + rank) for rank in row["ranks"]) for row in rows)
    text = ("Z" * 30).join(words) + "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(2048))
    path = work_dir / "synthetic-controls.letters"
    path.write_text(text)
    observed = run_scanner(binary, target_path, [path])
    actual = sorted((row["target"], row["offset"], row["word"])
                    for row in observed if row["type"] == "match")
    expected = []
    for row in rows:
        width = len(row["ranks"])
        for offset in range(len(text) - width + 1):
            word = text[offset:offset + width]
            if stable_ranks(word) == tuple(row["ranks"]):
                expected.append((row["id"], offset, word))
    assert actual == sorted(expected)
    assert {row[0] for row in actual} == {row["id"] for row in rows}
    return {"seed": 15320261102, "reference": "Independent Python sorting of every fixture window",
            "synthetic_characters": len(text), "matches": len(actual),
            "target_keys_with_a_confirmed_fixture_match": len(rows),
            "scanner_matches_reference_exactly": True}


def search(wordlist, corpus_dir, work_dir):
    wordlist_provenance = json.loads((ROOT / "experiments/fixed_search/data/wordlist_provenance.json").read_text())
    expected_wordlist_hash = wordlist_provenance["normalization"]["sha256"]
    if digest(wordlist) != expected_wordlist_hash:
        raise ValueError("The normalized dictionary differs from the recorded source hash")
    rows = targets()
    index = defaultdict(list)
    for row in rows:
        index[tuple(row["ranks"])].append(row["id"])
    widths = {len(row["ranks"]) for row in rows}
    counts = Counter()
    word_matches = []
    words = wordlist.read_text().splitlines()
    for word in words:
        if len(word) not in widths:
            continue
        assert word.isascii() and word.isalpha() and word.isupper()
        counts[len(word)] += 1
        found = index.get(stable_ranks(word))
        if found:
            word_matches.append({"word": word, "targets": found})

    work_dir.mkdir(parents=True, exist_ok=True)
    sources = json.loads((ROOT / "experiments/joint_search/models/provenance.json").read_text())["sources"]
    normalized_inputs = []
    files = []
    # Match the original exploratory scan's lexicographic filename order.
    for source in sorted(sources, key=lambda row: f"pg{row['id']}.txt"):
        path = corpus_dir / f"pg{source['id']}.txt"
        if digest(path) != source["sha256"]:
            raise ValueError(f"Source hash mismatch: {path.name}")
        text = path.read_text(encoding="utf-8")
        for mode in ("expanded", "simple"):
            letters = normalized(text, mode)
            output = work_dir / f"pg{source['id']}_{mode}.letters"
            output.write_text(letters, encoding="ascii")
            files.append(output)
            normalized_inputs.append({
                "file": output.name, "source": source["url"], "title": source["title"],
                "source_sha256": source["sha256"], "normalization": mode,
                "letters": len(letters), "normalized_sha256": digest(output),
            })

    target_path = work_dir / "targets.txt"
    write_targets(rows, target_path)
    binary = work_dir / "scan_phrase_keys"
    subprocess.run(["cc", "-O3", "-std=c11", "-Wall", "-Wextra", "-Werror",
                    str(HERE / "scan_phrase_keys.c"), "-o", str(binary)], check=True)
    controls = scanner_control(binary, target_path, rows, work_dir)
    raw_results = run_scanner(binary, target_path, files)
    matches = [row for row in raw_results if row["type"] == "match"]
    summaries = [row for row in raw_results if row["type"] == "summary"]
    stream_lengths = {row["file"]: row["letters"] for row in normalized_inputs}
    for summary in summaries:
        expected_windows = sum(max(0, n - summary["width"] + 1) for n in stream_lengths.values())
        assert summary["windows"] == expected_windows
        assert summary["matches"] == sum(row["target"] == summary["target"] for row in matches)
    for match in matches:
        target = next(row for row in rows if row["id"] == match["target"])
        assert stable_ranks(match["word"]) == tuple(target["ranks"])
    return {
        "schema": "adfgvx-p153-exact-keyword-search-v1", "project": "ADFGVX Cipher",
        "authors": "icekylinx and GPT-6 Astra Pro",
        "target_keys": rows,
        "dictionary": {
            "source": "https://github.com/enz/german-wordlist",
            "normalization_reference": "experiments/fixed_search/data/wordlist_provenance.json",
            "normalized_sha256": expected_wordlist_hash,
            "total_normalized_entries": len(words),
            "examined_entries_by_width": {str(k): counts[k] for k in sorted(counts)},
            "matches": word_matches,
            "injected_positive_controls": wordlist_provenance["normalization"]["injected_positive_controls"],
            "control_caveat": "The dictionary's TRUPPENVERSCHIEBUNG entry was deliberately injected in the earlier experiment; this hit is not evidence of dictionary coverage.",
        },
        "phrases": {
            "normalization": "Uppercase (including sharp-s to SS), then AE/OE/UE or A/O/U for umlauts; retain A-Z only. Complete source files, including Gutenberg headers and footers, are used.",
            "scope": "Every contiguous letter window; windows may span words or punctuation and need not be linguistically valid phrases. No window crosses source-file boundaries.",
            "source_books": len(sources), "normalized_streams": len(normalized_inputs),
            "total_normalized_letters": sum(stream_lengths.values()),
            "inputs": normalized_inputs, "matches": matches, "per_target": summaries,
            "scanner_source_sha256": digest(HERE / "scan_phrase_keys.c"),
            "independent_fixture_check": controls,
        },
        "new_p153_keywords": 0,
        "interpretation": "A bounded negative search. A corpus match proves equality of numeric ranks, not original historical keyword authorship or plaintext correctness.",
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--wordlist", type=Path, required=True)
    parser.add_argument("--corpus-dir", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "keyword_search.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = search(args.wordlist, args.corpus_dir, args.work_dir)
    if args.verify:
        if json.loads(args.output.read_text()) != result:
            raise SystemExit("Stored keyword search differs from the fresh computation")
        print("Dictionary and phrase searches verified, including the independent scanner fixture")
    else:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(f"Wrote {args.output}; no p153 keyword match")


if __name__ == "__main__":
    main()
