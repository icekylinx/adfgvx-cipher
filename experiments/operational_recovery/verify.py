#!/usr/bin/env python3
"""Certify the source readings and optional interpretations on pp. 180/217/230.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.

The shared source-edition reader uses an independent physical-column inverse
and checks it against adfgvx.cipher. Relabel hypotheses are partial, injective
squares; unresolved cells are not silently retained with their baseline names.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from experiments.withdrawal_recovery.verify import AL, CO, reading, repair, sha


def check_square(square):
    assert len(square) == 36 and set(square) <= set(AL + "?")
    assert len(set(square) - {"?"}) == 36 - square.count("?")


def global_witness(source, ranks, square, value):
    """Exhibit one globally consistent completion, not a proposed plaintext."""
    unused = iter(sorted(set(AL) - set(square)))
    complete = "".join(next(unused) if c == "?" else c for c in square)
    assert set(complete) == set(AL)
    cipher = source.replace("?", "A")
    plaintext = decrypt(cipher, ranks, complete)
    assert encrypt(plaintext, ranks, complete) == cipher
    assert all(a == "?" or a == b for a, b in zip(source, cipher))
    assert all(c in domain for c, domain in zip(plaintext, value["domains"]))
    return {"square": complete, "ciphertext": cipher, "plaintext": plaintext,
            "is_proposed_reading": False}


def hypotheses(base_square, definition):
    ambiguous = definition["ambiguous_baseline_labels"]
    assert len(ambiguous) == len(set(ambiguous))
    assert set(ambiguous) <= set(base_square)
    square = ["?" if c in ambiguous else c for c in base_square]
    accumulated = {}
    output = []
    for layer in definition["layers"]:
        for old, new in layer["assignments"].items():
            assert old in ambiguous and old not in accumulated and new in AL
            assert new not in square
            cell = base_square.index(old)
            square[cell] = new
            accumulated[old] = new
        value = "".join(square)
        check_square(value)
        output.append({"id": layer["id"], "square": value,
                       "cumulative_assignments": dict(accumulated),
                       "remaining_symbols": "".join(sorted(set(AL) - set(value))),
                       "unknown_cells": value.count("?"),
                       "cell_assignments": [
                           {"baseline_label": old, "inferred_symbol": new,
                            "cell_0based": base_square.index(old),
                            "pair": CO[base_square.index(old) // 6] + CO[base_square.index(old) % 6]}
                           for old, new in accumulated.items()]})
    return output


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    published = {k["id"]: k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    all_hypotheses = {}
    for name, key in inputs["keys"].items():
        assert name == key["id"]
        assert key["square"] == published[name]["square"]
        assert key["column_rank_order"] == published[name]["column_rank_order"]
        check_square(key["square"])
        ranks = key["column_rank_order"]
        assert sorted(ranks) == list(range(1, len(ranks) + 1))
        if name in inputs["interpretation_layers"]:
            all_hypotheses[name] = hypotheses(key["square"], inputs["interpretation_layers"][name])
    history = inputs["historical_source"]
    assert sha(ROOT / history["path"]) == history["sha256"]
    records = []
    for rec in inputs["records"]:
        assert sha(HERE / rec["source_crop"]) == rec["source_crop_sha256"]
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set(CO + "-")
        source = literal.replace("-", "?")
        assert len(source) == rec["advertised_length"] and len(source) % 2 == 0
        key = inputs["keys"][rec["key_id"]]
        ranks, square = key["column_rank_order"], key["square"]
        raw = reading(source, ranks, square)
        edition = repair(source, literal, rec["editorial_recipe"], ranks, square, raw)
        raw["global_witness"] = global_witness(source, ranks, square, raw)
        edition["reading"]["global_witness"] = global_witness(edition["ciphertext"], ranks, square, edition["reading"])
        interpretations = []
        for hypothesis in all_hypotheses.get(rec["key_id"], []):
            conditional = {"id": hypothesis["id"], "square": hypothesis["square"]}
            for label, cipher in [("raw", source), ("edition", edition["ciphertext"])]:
                result = reading(cipher, ranks, hypothesis["square"])
                result["global_witness"] = global_witness(cipher, ranks, hypothesis["square"], result)
                conditional[label] = result
            interpretations.append(conditional)
        records.append({"id": rec["id"], "key_id": rec["key_id"],
                        "received_slots": len(source), "valid_coordinates": len(source) - source.count("?"),
                        "erased_slots": source.count("?"),
                        "advertised_length": rec["advertised_length"],
                        "source_ciphertext": source,
                        "source_sha256": hashlib.sha256(literal.encode()).hexdigest(),
                        "raw": raw, "edition": edition,
                        "optional_interpretations": interpretations})
    summary = {"source_records": len(records),
               "coordinate_slots": sum(r["received_slots"] for r in records),
               "raw_plaintext_positions": sum(r["raw"]["plaintext_positions"] for r in records),
               "raw_baseline_fixed_positions": sum(r["raw"]["fixed_positions"] for r in records),
               "known_coordinate_substitutions": sum(len(r["edition"]["known_coordinate_substitutions"]) for r in records),
               "erasure_fills": sum(len(r["edition"]["erasure_fills"]) for r in records),
               "no_ciphertext_edit_records": [r["id"] for r in records
                   if not r["edition"]["known_coordinate_substitutions"] and not r["edition"]["erasure_fills"]]}
    return {"schema": "adfgvx-operational-certificate-v1", "prepared_by": inputs["prepared_by"],
            "inputs_sha256": sha(HERE / "inputs.json"), "summary": summary,
            "optional_square_hypotheses": all_hypotheses, "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = run()
    if args.pdf:
        expected = json.loads((HERE / "inputs.json").read_text())["source"]["pdf_sha256"]
        assert sha(args.pdf) == expected
    target = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
