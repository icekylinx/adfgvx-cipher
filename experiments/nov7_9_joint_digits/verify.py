#!/usr/bin/env python3
"""Check a cross-period reference and propagate one shared 5/6 assignment.

Independent column reconstruction; standard-library Python only.
Research and edition: icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = "ADFGVX"
ALPHABET = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")


def read(path):
    return json.loads((ROOT / path).read_text())


def at(value, path):
    for name in path:
        value = value[name]
    return value


def record(path, identifier=None, root_path=()):
    data = at(read(path), root_path)
    return next(r for r in data["records"] if r["id"] == identifier) if identifier else data


def source(spec):
    row = record(spec["inputs"], spec.get("record_id"), spec.get("input_root", ()))
    literal = "".join("".join(row[spec["rows_field"]]).split())
    assert hashlib.sha256(literal.encode()).hexdigest() == spec["source_sha256"]
    return literal


def untranspose(cipher, ranks):
    width, size = len(ranks), len(cipher)
    starts, cursor = {}, 0
    for col in sorted(range(width), key=lambda col: ranks[col]):
        starts[col] = cursor
        cursor += size // width + (col < size % width)
    origins = [starts[i % width] + i // width for i in range(size)]
    assert sorted(origins) == list(range(size))
    return "".join(cipher[i] for i in origins), origins


def transpose(interim, ranks):
    width = len(ranks)
    return "".join(interim[i] for i in sorted(range(len(interim)),
                   key=lambda i: (ranks[i % width], i // width)))


def pairs(interim, origins, square):
    assert len(interim) % 2 == 0
    unused = ALPHABET - set(square)
    rows = []
    for offset in range(0, len(interim), 2):
        pair = interim[offset:offset + 2]
        domain = set()
        for a in range(6):
            for b in range(6):
                if pair[0] in (CO[a], "?") and pair[1] in (CO[b], "?"):
                    label = square[6*a+b]
                    domain.update(unused if label == "?" else label)
        rows.append({"position": offset // 2, "pair": pair,
                     "source_indices": origins[offset:offset + 2],
                     "domain": "".join(sorted(domain))})
    text = "".join(r["domain"] if len(r["domain"]) == 1 else "?" for r in rows)
    return text, rows


def decode(cipher, ranks, square, mapping=None):
    interim, origins = untranspose(cipher, ranks)
    if mapping is not None:
        origins = [mapping[i] for i in origins]
    return pairs(interim, origins, square)


def full_square(base, assignment):
    result = list(base)
    for pair, label in assignment.items():
        index = CO.index(pair[0])*6 + CO.index(pair[1])
        assert result[index] == "?"
        result[index] = label
    result = "".join(result)
    assert set(result) == ALPHABET and len(result) == 36
    return result


def roundtrip(cipher, ranks, square):
    # A fills residual source masks only for this arithmetic check.
    witness = cipher.replace("?", "A")
    text, _ = decode(witness, ranks, square)
    encoded = "".join(CO[square.index(c)//6] + CO[square.index(c)%6] for c in text)
    assert transpose(encoded, ranks) == witness


def readable(spec, text):
    page = (ROOT / spec["case_path"]).read_text()
    assert spec["conditional_note"] in page, spec["id"]
    if "readable_german" not in spec:
        return
    quotes = [" ".join(line[2:] for line in match[0].splitlines())
              for match in re.finditer(r"(?:^>[^\n]*(?:\n|$))+", page, re.M)]
    assert spec["readable_german"] in quotes, spec["id"]
    labels = re.sub("[^A-Z0-9?]", "", spec["readable_german"].upper())
    assert labels == text.replace("X", ""), spec["id"]


def build():
    data = read(HERE.relative_to(ROOT) / "inputs.json")
    keys = {k["id"]: k for k in read("data/keys.json")["keys"]}
    key = keys["Nov7-9"]
    square = full_square(key["square"], data["assignment"])
    rival = full_square(key["square"], data["alternative_assignment"])
    reference = data["reference_comparison"]
    donor = reference["donor"]
    donor_source = source(donor)
    donor_key = keys[donor["key_id"]]
    interim, origins = untranspose(donor_source, donor_key["column_rank_order"])
    donor_outputs = []
    for omit in donor["excluded_interim_indices"]:
        assert interim[omit] == "X"
        retained = [i for i in range(len(interim)) if i != omit]
        text, positions = pairs("".join(interim[i] if interim[i] in CO else "?" for i in retained),
                                [origins[i] for i in retained], donor_key["square"])
        start = donor["reference_start"]
        assert text[start:start+5] == reference["number"]
        span = positions[start:start+5]
        assert all("?" not in p["pair"] for p in span)
        donor_outputs.append({"excluded_interim_index": omit, "observed_reference": span})
    target = reference["target"]
    target_source = source(target)
    clean_target = "".join(c if c in CO else "?" for c in target_source)
    target_raw, target_positions = decode(clean_target, key["column_rank_order"], key["square"])
    start = target["reference_start"]
    assert target_raw[start:start+5] == "4??10"
    observed = target_positions[start:start+5]
    assert all("?" not in p["pair"] for p in observed)
    selected_reference = decode(clean_target, key["column_rank_order"], square)[0][start:start+5]
    rival_reference = decode(clean_target, key["column_rank_order"], rival)[0][start:start+5]
    assert selected_reference == reference["number"] == "45610" and rival_reference == "46510"

    results = []
    for spec in data["records"]:
        literal = source(spec)
        base = record(spec["certificate"], spec.get("certificate_record_id"), spec.get("certificate_root", ()))
        cipher = at(base, spec["cipher_path"])
        if spec.get("cipher_is_interim"):
            cipher = transpose(cipher, key["column_rank_order"])
        if "mapping_path" in spec:
            mapping = at(base, spec["mapping_path"])
        elif "insert_before_source" in spec:
            mapping = list(range(len(literal)))
            mapping.insert(spec["insert_before_source"], None)
        else:
            mapping = list(range(len(literal)))
        assert len(mapping) == len(cipher)
        old, domains = decode(cipher, key["column_rank_order"], key["square"], mapping)
        assert old == spec["previous_plaintext"], spec["id"]
        selected, _ = decode(cipher, key["column_rank_order"], square, mapping)
        alternative, _ = decode(cipher, key["column_rank_order"], rival, mapping)
        gains = []
        for index, (before, after) in enumerate(zip(old, selected)):
            if before == after:
                continue
            p = domains[index]
            assert before == "?" and p["pair"] in data["assignment"] and p["domain"] == "56"
            support = all(i is not None and literal[i] == value for i, value in zip(p["source_indices"], p["pair"]))
            gains.append({**p, "selected": after, "alternative": alternative[index],
                          "both_original_coordinates_observed": support})
        assert len(gains) == spec["new_digit_positions"], spec["id"]
        assert selected == spec["selected_plaintext"]
        roundtrip(cipher, key["column_rank_order"], square)
        roundtrip(cipher, key["column_rank_order"], rival)
        readable(spec, selected)
        results.append({"id": spec["id"], "previous_plaintext": old,
                        "selected_plaintext": selected, "alternative_plaintext": alternative,
                        "positions": len(old), "fixed_before": len(old)-old.count("?"),
                        "fixed_after": len(selected)-selected.count("?"), "gained_positions": gains,
                        "new_coordinate_changes": 0, "new_source_mask_fills": 0})
    return {"schema": "adfgvx-nov7-9-joint-digit-certificate-v1", "authors": data["authors"],
            "reference": {"donor": donor_outputs, "target_observed_reference": observed,
                          "selected": selected_reference, "alternative": rival_reference,
                          "assumption": reference["assumption"]},
            "assignment": data["assignment"], "selected_square": square,
            "alternative_square": rival, "records": results,
            "new_conditional_digit_positions": sum(len(r["gained_positions"]) for r in results),
            "additional_coordinate_changes": 0, "additional_source_mask_fills": 0,
            "published_partial_key_changed": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build()
    path = HERE / "certificates.json"
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"Siegfried reference 45610: XA=5, VF=6 under the common-reference relation; "
          f"{result['new_conditional_digit_positions']} conditional positions in {len(result['records'])} records; "
          "no additional source edits or fills.")
