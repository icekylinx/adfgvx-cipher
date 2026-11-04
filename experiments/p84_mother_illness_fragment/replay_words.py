#!/usr/bin/env python3
"""Recheck independent dictionary words at p84's selected clause starts.

This enumerates lexical possibilities, not authenticated historical wording.
icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lexicon", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    provenance = json.loads((HERE / "search_provenance.json").read_text())["independent_lexicon"]
    assert hashlib.sha256(args.lexicon.read_bytes()).hexdigest() == provenance["lexicon_sha256"]
    with args.lexicon.open() as stream:
        count, _ = map(int, stream.readline().split())
        words = dict((word, float(score)) for word, score in
                     (stream.readline().split() for _ in range(count)))
    assert count == provenance["distinct_words"] == 53465
    for entry in provenance["words_used"]:
        assert words[entry["word"]] == entry["log10_unigram_frequency"]
    spec = importlib.util.spec_from_file_location("p84_illness_verifier", HERE / "verify.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    rebuilt, _ = verifier.build()
    results = []
    frames = sorted(rebuilt["records"] + rebuilt["alternative_frames"],
                    key=lambda row: row["insert_before_source"])
    for frame in frames:
        domains = [set(position["domain"]) for position in frame["positions"]]
        starts = []
        for start in (68, 74, 80, 85, 90):
            compatible = [(word, score) for word, score in words.items()
                          if 3 <= len(word) <= len(domains) - start
                          and all(letter in domains[start + offset]
                                  for offset, letter in enumerate(word))]
            compatible.sort(key=lambda row: (-len(row[0]), -row[1], row[0]))
            used = [entry["word"] for entry in provenance["words_used"]
                    if entry["plaintext_start"] == start]
            starts.append(dict(plaintext_start=start,
                               compatible_dictionary_words=len(compatible),
                               longest_examples=[word for word, _ in compatible[:15]],
                               proposed_words={word: all(letter in domains[start + offset]
                                                         for offset, letter in enumerate(word))
                                               for word in used}))
        results.append(dict(insert_before_source=frame["insert_before_source"], starts=starts))
    for frame in results:
        at = frame["insert_before_source"]
        for entry in frame["starts"]:
            if entry["plaintext_start"] == 90:
                assert entry["proposed_words"]["KOMM"] == (at in (77, 78, 79))
    result = dict(lexicon_sha256=provenance["lexicon_sha256"],
                  distinct_words=count, frames=results,
                  native_copy_claim=False, historical_uniqueness_claim=False,
                  limit="The starts and composed clause were selected after domain inspection.")
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
