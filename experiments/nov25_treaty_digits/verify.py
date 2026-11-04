#!/usr/bin/env python3
"""Verify the conditional Article XII numeral assignments across Nov25–28.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Standard library only.
The published key remains attributed to Lasry, Niebel, Kopal and Wacker.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import math
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIOR = ROOT / "experiments/nov25_letter_constraint"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_prior():
    spec = importlib.util.spec_from_file_location("nov25_letter", PRIOR / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def changes(native, edition, mapping):
    return [{"frame_index": i, "source_index": mapping[i], "from": a, "to": b,
             "kind": "fill" if a == "?" else "observed_substitution"}
            for i, (a, b) in enumerate(zip(native, edition)) if a != b]


def normalized_german(text):
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(a, b).replace(a.upper(), b.upper())
    return re.sub(r"[^A-Z0-9?]", "", text.upper())


def run():
    data = json.loads((HERE / "inputs.json").read_text())
    for dep in data["dependencies"]:
        assert digest(ROOT / dep["path"]) == dep["sha256"], dep["path"]
    base = load_prior()
    prior_input = json.loads((PRIOR / "inputs.json").read_text())
    prior = base.run()
    assert prior == json.loads((PRIOR / "certificates.json").read_text())
    key = prior_input["key"]
    ranks, published = key["column_rank_order"], key["square"]
    partial = list(prior["conditional_partial_square"])
    assignments = data["hypothesis"]["assignments"]
    for pair, value in assignments.items():
        cell = 6 * base.CO.index(pair[0]) + base.CO.index(pair[1])
        assert partial[cell] == "?" and value not in partial
        partial[cell] = value
    partial = "".join(partial)
    remaining = "".join(sorted(set(base.ALPHABET) - (set(partial) - {"?"})))
    assert remaining == "03456789QY"
    anchor = data["hypothesis"]["anchor"]
    anchor_positions = set(anchor["plaintext_indices"])
    records, inventory, removed = [], [], []
    totals = Counter()
    for rec in base.normalized_records(prior_input):
        native = rec["ciphertext"]
        raw = base.read(native, ranks, published)
        assert raw["plaintext"] == rec["raw"]
        assert base.read(rec["edition_ciphertext"], ranks, published)["plaintext"] == rec["edition"]
        revised = list(rec["edition_ciphertext"])
        if rec["id"] == anchor["record_id"]:
            assert "".join(raw["plaintext"][i] for i in sorted(anchor_positions)) == anchor["baseline_labels"]
            for index in sorted(anchor_positions):
                pos = raw["positions"][index]
                assert pos["pair"] in assignments and "?" not in pos["pair"]
                assert all(rec["mapping"][i] is not None for i in pos["frame_indices"])
                for i in pos["frame_indices"]:
                    if revised[i] != native[i]:
                        removed.append({"record_id": rec["id"], "plaintext_index": index,
                                        "frame_index": i, "source_index": rec["mapping"][i],
                                        "source": native[i], "prior_edition": revised[i]})
                    revised[i] = native[i]
        revised = "".join(revised)
        decoded = base.read(revised, ranks, partial)
        raw_decoded = base.read(native, ranks, partial)
        prior_changes = changes(native, rec["edition_ciphertext"], rec["mapping"])
        revised_changes = changes(native, revised, rec["mapping"])
        prior_count = Counter(c["kind"] for c in prior_changes)
        revised_count = Counter(c["kind"] for c in revised_changes)
        assert {(c["frame_index"], c["to"]) for c in revised_changes} <= {
            (c["frame_index"], c["to"]) for c in prior_changes}
        rec_inventory = []
        for p in raw["positions"]:
            if p["pair"] not in assignments:
                continue
            index = p["index"]
            revised_pair = "".join(revised[i] for i in p["frame_indices"])
            retained = revised_pair == p["pair"]
            if retained:
                assert decoded["plaintext"][index] == assignments[p["pair"]]
            elif rec["id"] not in {"p218_A2", "p220_C1", "p220_C3"}:
                raise AssertionError((rec["id"], index, revised_pair))
            item = {"record_id": rec["id"], "plaintext_index": index,
                    "pair": p["pair"], "source_indices": [rec["mapping"][i] for i in p["frame_indices"]],
                    "original_label": p["domain"], "conditional_value": assignments[p["pair"]],
                    "raw_context": raw["plaintext"][max(0, index - 12):index + 13],
                    "conditional_raw_context": raw_decoded["plaintext"][max(0, index - 12):index + 13],
                    "edition_context": decoded["plaintext"][max(0, index - 12):index + 13],
                    "retained_in_edition": retained,
                    "is_article_anchor": rec["id"] == anchor["record_id"] and index in anchor_positions}
            inventory.append(item)
            rec_inventory.append(item)
        totals["source_records"] += 1
        totals["plaintext_positions"] += len(rec["raw"])
        totals["raw_anchor_pair_occurrences"] += len(rec_inventory)
        totals["retained_numeric_occurrences"] += sum(i["retained_in_edition"] for i in rec_inventory)
        totals["inconvenient_raw_occurrences"] += sum(not i["retained_in_edition"] for i in rec_inventory)
        records.append({"id": rec["id"], "raw_baseline": rec["raw"],
                        "conditional_raw": raw_decoded["plaintext"],
                        "conditional_edition": decoded["plaintext"],
                        "conditional_edition_domains": [p["domain"] for p in decoded["positions"]],
                        "prior_edit_cost": dict(prior_count), "conditional_edit_cost": dict(revised_count),
                        "conditional_coordinate_changes": revised_changes,
                        "raw_roundtrip_witness": base.witness(native, ranks, partial),
                        "edition_roundtrip_witness": base.witness(revised, ranks, partial)})
    totals["removed_observed_coordinate_substitutions"] = len(removed)
    totals["remaining_square_completions"] = math.factorial(partial.count("?"))
    assert dict(totals) == data["expected"], (dict(totals), data["expected"])
    index = {r["id"]: r for r in records}
    checked_fields = []
    for field in data["case_fields"]:
        start, end = field["range"]
        value = index[field["record_id"]]["conditional_edition"][start:end]
        assert value == field["conditional"], (field, value)
        assert "`" + value + "`" in (ROOT / field["case_path"]).read_text(), field
        checked_fields.append(field)
    display = data["live_reading"]
    case = (ROOT / display["case_path"]).read_text()
    assert case.count(display["caption"]) == 1
    after = case.split(display["caption"], 1)[1]
    quote = []
    for line in after.lstrip().splitlines():
        if line.startswith(">"):
            quote.append(line[1:].strip())
        elif line.strip():
            break
    german = " ".join(quote)
    combined = "".join(index[r]["conditional_edition"] for r in display["record_ids"])
    assert normalized_german(german) == combined.replace("X", ""), german
    assert len({r[view]["square"] for r in records for view in
                ("raw_roundtrip_witness", "edition_roundtrip_witness")}) == 1
    return {"schema": "adfgvx-nov25-treaty-digits-certificate-v1",
            "prepared_by": data["prepared_by"], "input_sha256": digest(HERE / "inputs.json"),
            "published_square": published, "prior_partial_square": prior["conditional_partial_square"],
            "conditional_partial_square": partial, "remaining_cell_domain": remaining,
            "summary": dict(totals), "removed_prior_substitutions": removed,
            "all_observed_assignment_occurrences": inventory, "records": records,
            "checked_case_fields": checked_fields, "checked_german_reading": german,
            "limits": data["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = run()
    target = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
