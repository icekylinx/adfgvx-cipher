#!/usr/bin/env python3
"""Replay two conditional completions against their unchanged received sources.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
The arithmetic here is independent of the shared cipher implementation.
"""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = "ADFGVX"


def read(path):
    return json.loads((ROOT / path).read_text())


def source_order(size, ranks):
    width = len(ranks)
    return sorted(range(size), key=lambda i: (ranks[i % width], i // width))


def decode(cipher, key):
    middle = [None] * len(cipher)
    origins = [None] * len(cipher)
    for source, original in enumerate(source_order(len(cipher), key["column_rank_order"])):
        middle[original], origins[original] = cipher[source], source
    rows = []
    for i in range(0, len(middle), 2):
        pair = "".join(middle[i:i + 2])
        domain = "".join(sorted(key["square"][6 * a + b]
                               for a in range(6) for b in range(6)
                               if pair[0] in ("?", CO[a]) and pair[1] in ("?", CO[b])))
        rows.append({"position": i // 2, "pair": pair,
                     "source_indices": origins[i:i + 2], "domain": domain})
    return "".join(r["domain"] if len(r["domain"]) == 1 else "?" for r in rows), rows


def encode(text, key):
    middle = "".join(CO[key["square"].index(c) // 6] + CO[key["square"].index(c) % 6]
                     for c in text)
    return "".join(middle[i] for i in source_order(len(middle), key["column_rank_order"]))


def changes(before, after):
    assert len(before) == len(after)
    return [{"source_index": i, "before": a, "after": b,
             "kind": "substitution" if a in CO else "mask_fill"}
            for i, (a, b) in enumerate(zip(before, after)) if a != b]


def build():
    data = read(HERE.relative_to(ROOT) / "readings.json")
    keys = {k["id"]: k for k in read("data/keys.json")["keys"]}
    key = keys[data["key_id"]]
    assert len(set(key["square"])) == 36 and "?" not in key["square"]
    results = []
    for spec in data["records"]:
        base = next(r for r in read(spec["base_certificate"])["records"] if r["id"] == spec["id"])
        literal = "".join("".join(base["literal_printed_rows"]).split())
        assert literal == base["literal_source"]
        assert hashlib.sha256(literal.encode()).hexdigest() == spec["source_sha256"]
        native = "".join(c if c in CO else "?" for c in literal)
        assert native == base["ciphertext"] and len(native) % 2 == 0
        assert decode(native, key)[0] == base["raw"]
        layer = base
        for field in spec["base_layer"]:
            layer = layer[field]
        assert layer["template"] == spec["base_template"]
        old, domains = decode(layer["ciphertext"], key)
        assert old == spec["base_template"]
        target = spec["proposal"]
        witness = encode(target, key)
        assert decode(witness, key)[0] == target
        extra = changes(layer["ciphertext"], witness)
        total = changes(native, witness)
        for name, events in (("additional", extra), ("total", total)):
            assert sum(e["kind"] == "substitution" for e in events) == spec[f"expected_{name}_substitutions"]
            assert sum(e["kind"] == "mask_fill" for e in events) == spec[f"expected_{name}_fills"]
        new_letters = []
        for i, (a, b) in enumerate(zip(old, target)):
            if a != b:
                new_letters.append({**domains[i], "before": a, "proposal": b,
                                    "fits_surviving_pair": b in domains[i]["domain"]})
        quotation = spec["readable_german"]
        assert re.sub("[^A-Z0-9]", "", quotation.upper()) == target.replace("X", "")
        case = (ROOT / spec["case_path"]).read_text()
        assert "> " + quotation in case
        assert "\n" + target + "\n" in case
        results.append({"id": spec["id"], "source_slots": len(native),
                        "native_fixed_positions": len(base["raw"]) - base["raw"].count("?"),
                        "previous_proposal_fixed_positions": len(old) - old.count("?"),
                        "completed_proposal_positions": len(target),
                        "additional_changes": extra, "full_source_changes": total,
                        "changed_plaintext_positions": new_letters,
                        "ciphertext": witness, "plaintext": target})
    donors = []
    for spec in data["address_witnesses"]:
        record = next(r for r in read(spec["input_path"])["records"] if r["id"] == spec["id"])
        literal = "".join("".join(record["source_rows"]).split())
        source = "".join(c if c in CO else "?" for c in literal)
        raw, positions = decode(source, keys[spec["key_id"]])
        assert raw == record["expected_raw"]
        start, phrase = spec["plaintext_start"], spec["phrase"]
        assert raw[start:start + len(phrase)] == phrase
        span = positions[start:start + len(phrase)]
        assert all("?" not in p["pair"] for p in span)
        donors.append({"id": spec["id"], "key_id": spec["key_id"],
                       "phrase": phrase, "plaintext_start": start,
                       "observed_positions": span})
    return {"records": results, "independent_address_witnesses": donors,
            "newly_filled_plaintext_positions": sum(r["completed_proposal_positions"] - r["previous_proposal_fixed_positions"] for r in results),
            "new_observed_coordinate_substitutions": sum(e["kind"] == "substitution" for r in results for e in r["additional_changes"]),
            "new_source_mask_fills": sum(e["kind"] == "mask_fill" for r in results for e in r["additional_changes"]),
            "status": "Conditional readings; source masks and the place-name emendation remain explicit."}


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
