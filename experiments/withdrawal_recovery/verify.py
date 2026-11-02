#!/usr/bin/env python3
"""Source and edit certificate for the p163 withdrawal-order fragments.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The independent inverse below is checked against the separate project reader.
No language score, guessed source glyph, or completed baseline square is used.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

CO = "ADFGVX"
AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(ciphertext, ranks, square):
    """Read each physical column from an independently computed offset."""
    if len(ciphertext) % 2:
        raise ValueError("Odd coordinate stream has no complete plaintext frame")
    n, width = len(ciphertext), len(ranks)
    q, extra = divmod(n, width)
    lengths = [q + (col < extra) for col in range(width)]
    offsets = [sum(lengths[c] for c in range(width) if ranks[c] < ranks[col])
               for col in range(width)]
    source_for_interim = [offsets[i % width] + i // width for i in range(n)]
    assert sorted(source_for_interim) == list(range(n))
    missing = set(AL) - set(square)
    domains, positions = [], []
    for i in range(0, n, 2):
        p, q = source_for_interim[i:i + 2]
        row, col = ciphertext[p], ciphertext[q]
        rr = [CO.index(row)] if row in CO else range(6)
        cc = [CO.index(col)] if col in CO else range(6)
        chars = set()
        for r in rr:
            for c in cc:
                value = square[6 * r + c]
                chars.update(missing if value == "?" else value)
        domains.append("".join(sorted(chars)))
        positions.append([p, q])
    raw = "".join(d if len(d) == 1 else "?" for d in domains)
    return raw, domains, positions


def reading(ciphertext, ranks, square):
    raw, domains, positions = inverse(ciphertext, ranks, square)
    assert domains == plaintext_domains(ciphertext, ranks, square)
    assert raw == decrypt(ciphertext, ranks, square)
    return {"plaintext": raw, "fixed_positions": sum(len(d) == 1 for d in domains),
            "plaintext_positions": len(domains), "domains": domains,
            "source_position_pairs_0based": positions}


def repair(ciphertext, literal, recipe, ranks, square, raw):
    result = list(ciphertext)
    supplied_pairs = {}
    assert len(recipe["text"]) == len(raw["domains"])
    for i, char in enumerate(recipe["text"]):
        if char == "?":
            continue
        assert char in square, (i, char)
        cell = square.index(char)
        supplied_pairs[i] = CO[cell // 6] + CO[cell % 6]
    for override in recipe["pair_overrides"]:
        i, pair = override["plaintext_position_0based"], override["pair"]
        assert len(pair) == 2 and set(pair) <= set(CO)
        assert i not in supplied_pairs
        supplied_pairs[i] = pair
    for i, pair in supplied_pairs.items():
        for p, value in zip(raw["source_position_pairs_0based"][i], pair):
            result[p] = value
    result = "".join(result)
    substitutions, fills = [], []
    owner = {p: i for i, pair in enumerate(raw["source_position_pairs_0based"])
             for p in pair}
    for p, (a, b) in enumerate(zip(ciphertext, result)):
        if a == b:
            continue
        i = owner[p]
        entry = {"source_position_0based": p,
                 "plaintext_position_0based": i,
                 "observed": literal[p], "proposed": b}
        (fills if a == "?" else substitutions).append(entry)
    edition = reading(result, ranks, square)
    for i, char in enumerate(recipe["text"]):
        if char != "?":
            assert edition["domains"][i] == char
    return {"ciphertext": result, "reading": edition,
            "known_coordinate_substitutions": substitutions,
            "erasure_fills": fills,
            "remaining_erased_source_positions_0based": [
                i for i, c in enumerate(result) if c == "?"]}


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    key = inputs["key"]
    ranks, square = key["column_rank_order"], key["square"]
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    assert len(square) == 36
    assert len(set(square) - {"?"}) == 36 - square.count("?")
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    assert square == published["square"] and ranks == published["column_rank_order"]
    context = inputs["conditional_context"]
    context_path = ROOT / context["path"]
    assert sha(context_path) == context["sha256"]
    prior = json.loads(context_path.read_text())
    assert context["assignments"] == prior["contextual_cell_assignments"]
    contextual_square = list(square)
    for pair, char in context["assignments"].items():
        cell = 6 * CO.index(pair[0]) + CO.index(pair[1])
        assert square[cell] == "?"
        contextual_square[cell] = char
    contextual_square = "".join(contextual_square)
    assert contextual_square == prior["contextual_square"]
    assert set(contextual_square) == set(AL)
    records = []
    for rec in inputs["records"]:
        assert sha(HERE / rec["source_crop"]) == rec["source_crop_sha256"]
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set(CO + "-")
        ciphertext = literal.replace("-", "?")
        result = {"id": rec["id"], "received_slots": len(ciphertext),
                  "valid_coordinates": len(ciphertext) - ciphertext.count("?"),
                  "erased_slots": ciphertext.count("?"),
                  "advertised_length": rec["advertised_length"],
                  "source_ciphertext": ciphertext,
                  "source_sha256": hashlib.sha256(literal.encode()).hexdigest()}
        if len(ciphertext) % 2:
            try:
                inverse(ciphertext, ranks, square)
            except ValueError:
                result["status"] = "Unnumbered jammed fragment; no complete frame asserted"
            else:
                raise AssertionError("Odd stream must be rejected")
            records.append(result)
            continue
        result["raw"] = reading(ciphertext, ranks, square)
        result["edition"] = repair(ciphertext, literal, rec["editorial_recipe"],
                                   ranks, square, result["raw"])
        conditional = {}
        for label, source, base in [
                ("raw", ciphertext, result["raw"]),
                ("edition", result["edition"]["ciphertext"], result["edition"]["reading"])]:
            value = reading(source, ranks, contextual_square)
            value["new_singleton_positions"] = [
                {"position_0based": i, "base_domain": a, "conditional_character": b}
                for i, (a, b) in enumerate(zip(base["domains"], value["domains"]))
                if len(a) > 1 and len(b) == 1]
            # One global square and one global source filling certify consistency.
            # Filling residual unknown coordinates with A is only a witness.
            witness_source = source.replace("?", "A")
            witness_plaintext = decrypt(witness_source, ranks, contextual_square)
            assert encrypt(witness_plaintext, ranks, contextual_square) == witness_source
            assert all(a == "?" or a == b for a, b in zip(source, witness_source))
            assert all(ch in domain for ch, domain in zip(witness_plaintext, value["domains"]))
            value["global_witness_ciphertext"] = witness_source
            value["global_witness_plaintext"] = witness_plaintext
            value["witness_is_a_proposed_reading"] = False
            if "?" not in value["plaintext"]:
                assert encrypt(value["plaintext"], ranks, contextual_square) == source
                value["exact_roundtrip"] = True
            conditional[label] = value
        result["conditional_context"] = conditional
        records.append(result)
    readable = [r for r in records if "raw" in r]
    summary = {
        "source_records": len(records), "framed_records": len(readable),
        "visible_source_slots": sum(r["received_slots"] for r in records),
        "framed_coordinate_slots": sum(r["received_slots"] for r in readable),
        "raw_plaintext_positions": sum(r["raw"]["plaintext_positions"] for r in readable),
        "raw_fixed_positions": sum(r["raw"]["fixed_positions"] for r in readable),
        "known_coordinate_substitutions": sum(len(r["edition"]["known_coordinate_substitutions"]) for r in readable),
        "erasure_fills": sum(len(r["edition"]["erasure_fills"]) for r in readable),
        "conditional_raw_singleton_gain": sum(len(r["conditional_context"]["raw"]["new_singleton_positions"]) for r in readable),
        "conditional_edition_singleton_gain": sum(len(r["conditional_context"]["edition"]["new_singleton_positions"]) for r in readable)}
    return {"schema": "adfgvx-withdrawal-certificate-v1", "prepared_by": inputs["prepared_by"],
            "inputs_sha256": sha(HERE / "inputs.json"), "summary": summary,
            "conditional_square": contextual_square,
            "conditional_assignment_source": context["path"], "records": records}


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
