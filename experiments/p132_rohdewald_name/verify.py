#!/usr/bin/env python3
"""Price the optional Rohdewald spelling against the unchanged p132 A source.

Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = "ADFGVX"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rebuild():
    inp = read(HERE / "inputs.json")
    for path, expected in inp["dependencies"].items():
        assert sha(ROOT / path) == expected, path
    baseline = read(ROOT / inp["source_input"])
    rec = next(r for r in baseline["records"] if r["id"] == "p132_A")
    key = next(k for k in baseline["keys"] if k["id"] == rec["key_id"])
    square, ranks = key["square"], key["column_rank_order"]
    assert len(square) == len(set(square)) == 36
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    literal = "".join("".join(rec["rows"]).split())
    assert literal == rec["literal_source"] and len(literal) == 242
    source = "".join(c if c in CO else "?" for c in literal)
    assert source == rec["analysis_source"] and source.count("?") == 1
    width = len(ranks)
    heights = [len(source) // width + (i < len(source) % width)
               for i in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[i])
              for i in range(width)]
    origins = [starts[i % width] + i // width for i in range(len(source))]
    assert sorted(origins) == list(range(len(source)))

    def decode(cipher):
        stream = "".join(cipher[i] for i in origins)
        return "".join("?" if "?" in stream[i:i + 2] else
                       square[6 * CO.index(stream[i]) + CO.index(stream[i + 1])]
                       for i in range(0, len(stream), 2))

    def witness(text):
        stream = "".join(CO[square.index(c) // 6] + CO[square.index(c) % 6]
                         for c in text)
        cipher = "".join(stream[i::width] for i in
                         sorted(range(width), key=lambda i: ranks[i]))
        assert len(cipher) == len(source) and decode(cipher) == text
        return cipher

    def changes(a, b):
        return [[i, x, y] for i, (x, y) in enumerate(zip(a, b)) if x != y]

    raw = decode(source)
    assert raw == rec["expected_unmodified_raw"] and raw.count("?") == 1
    original = rec["editorial_text"]
    proposed = original.replace(inp["original_name"], inp["proposed_name"])
    assert original.count(inp["original_name"]) == 1
    assert len(raw) == len(original) == len(proposed) == 121
    old_witness, new_witness = witness(original), witness(proposed)
    baseline_edits = changes(source, old_witness)
    assert baseline_edits == rec["expected_source_changes"]
    extra = changes(old_witness, new_witness)
    assert extra == inp["expected_additional_changes"]
    assert all(source[i] == before and before in CO for i, before, after in extra)
    all_edits = changes(source, new_witness)
    observed = [e for e in all_edits if e[1] in CO]
    fills = [e for e in all_edits if e[1] == "?"]
    assert len(extra) == 4 and len(observed) == 10 and len(fills) == 1
    assert sorted(baseline_edits + extra) == all_edits
    assert fills == [e for e in baseline_edits if e[1] == "?"]
    text_edits = changes(original, proposed)
    assert text_edits == [[78, "H", "O"], [79, "Y", "H"]]
    for field in inp["preserved_literal_fields"]:
        assert field in raw and field in original and field in proposed
    for i, c in enumerate(raw):
        if c.isdigit():
            assert proposed[i] == c
            assert all(source[j] == new_witness[j] for j in origins[2 * i:2 * i + 2])
    ledger = []
    for i, before, after in text_edits:
        positions = origins[2 * i:2 * i + 2]
        ledger.append({"plaintext_index": i, "before": before, "after": after,
                       "source_indices": positions,
                       "observed_pair": "".join(source[j] for j in positions),
                       "proposed_pair": "".join(new_witness[j] for j in positions)})
    return {"schema": "adfgvx-p132-rohdewald-certificate-v1",
            "prepared_by": inp["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
            "raw_positions": 121, "raw_fixed_positions": 120,
            "new_raw_fixed_positions": 0, "new_physical_records": 0,
            "optional_plaintext": proposed, "name_letter_changes": ledger,
            "additional_observed_changes": extra,
            "total_cost": {"observed_substitutions": len(observed),
                           "source_mask_fills": len(fills), "key_changes": 0,
                           "added_or_removed_source_slots": 0},
            "all_source_changes": all_edits,
            "forward_received_witness": new_witness,
            "exact_forward_roundtrip": True,
            "historical_identification": None,
            "historical_source": inp["historical_source"], "limits": inp["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = rebuild()
    path = HERE / "certificate.json"
    if args.verify:
        assert result == read(path), "Rebuilt certificate differs"
        print("VERIFIED p132 optional ROHDEWALD: +4 observed changes; total 10 + 1 mask fill; no raw gain")
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print("Wrote " + str(path.relative_to(ROOT)))


if __name__ == "__main__":
    main()
