#!/usr/bin/env python3
"""p187 C four-edit audit -- icekylinx and GPT-6 Astra Pro.

Original body reading: Ayush Agarwal (@AyushAg1002), 2026-10-28,
https://github.com/dbourdeau/cyphersolver/issues/181.
"""
from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt
from experiments.withdrawal_recovery.verify import reading, repair, sha
from experiments.operational_recovery.verify import global_witness


def run():
    inputs = json.loads((HERE / "companion_inputs.json").read_text())
    source, key = inputs["source"], inputs["key"]
    assert sha(HERE / source["crop"]) == source["crop_sha256"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"] if k["id"] == key["id"])
    assert key["square"] == published["square"] and key["column_rank_order"] == published["column_rank_order"]
    ranks, square = key["column_rank_order"], key["square"]
    cipher = "".join("".join(inputs["source_rows"]).split())
    assert len(cipher) == inputs["advertised_length"] == 134 and set(cipher) <= set("ADFGVX")
    raw = reading(cipher, ranks, square)
    reference = inputs["prior_canonical_record"]
    prior = next(r for r in json.loads((ROOT / reference["path"]).read_text())["messages"]
                 if r["id"] == reference["id"])
    assert prior["prior_credit"] == inputs["prior_credit"]
    assert cipher == prior["source_ciphertext_literal_letters"]
    assert square == prior["key"]["square"] and ranks == prior["key"]["column_rank_order"]
    assert raw["plaintext"] == prior["source_verification"]["plaintext"]
    assert raw["domains"] == prior["source_verification"]["plaintext_domains"]
    proposal = repair(cipher, cipher, inputs["editorial_recipe"], ranks, square, raw)
    assert len(proposal["known_coordinate_substitutions"]) == 4 and not proposal["erasure_fills"]
    assert raw["fixed_positions"] == 65 and proposal["reading"]["fixed_positions"] == 67
    assert encrypt(proposal["reading"]["plaintext"], ranks, square) == proposal["ciphertext"]
    raw["global_witness"] = global_witness(cipher, ranks, square, raw)
    proposal["reading"]["global_witness"] = global_witness(proposal["ciphertext"], ranks, square, proposal["reading"])
    return {"schema": "adfgvx-p187-connection-check-certificate-v1", "prepared_by": inputs["prepared_by"],
            "inputs_sha256": sha(HERE / "companion_inputs.json"), "source_ciphertext": cipher,
            "prior_credit": inputs["prior_credit"], "our_contribution": inputs["our_contribution"],
            "prior_canonical_record": reference, "prior_source_key_plaintext_and_domains_match": True,
            "raw": raw, "edition": proposal, "exact_roundtrip_with_unchanged_partial_square": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = run()
    if args.pdf:
        assert sha(args.pdf) == json.loads((HERE / "companion_inputs.json").read_text())["source"]["pdf_sha256"]
    path = HERE / "companion_certificate.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, "source_coordinates": 134,
                      "raw_fixed_positions": 65, "plaintext_positions": 67,
                      "known_coordinate_substitutions": 4, "insertions_or_erasures": 0}, indent=2))


if __name__ == "__main__":
    main()
