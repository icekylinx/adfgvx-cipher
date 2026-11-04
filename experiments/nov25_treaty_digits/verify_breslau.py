#!/usr/bin/env python3
"""Propagate the optional VI Army Corps identification in the Nov25–28 key.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def run(historical_pdf=None):
    spec = importlib.util.spec_from_file_location("treaty_digits", HERE / "verify.py")
    treaty = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(treaty)
    data = json.loads((HERE / "breslau_inputs.json").read_text())
    dep = data["prior_certificate"]
    assert treaty.digest(ROOT / dep["path"]) == dep["sha256"]
    prior = treaty.run()
    assert prior == json.loads((ROOT / dep["path"]).read_text())
    historical = data["historical_source"]
    for crop in historical["crops"]:
        assert treaty.digest(ROOT / crop["path"]) == crop["sha256"]
    if historical_pdf:
        import fitz
        assert historical_pdf.stat().st_size == historical["pdf_bytes"]
        assert treaty.digest(historical_pdf) == historical["pdf_sha256"]
        doc = fitz.open(historical_pdf)
        for crop in historical["crops"]:
            original = doc[crop["pdf_page_1based"] - 1].get_pixmap(
                matrix=fitz.Matrix(crop["scale"], crop["scale"]),
                clip=fitz.Rect(crop["clip_points"]))
            stored = fitz.Pixmap(str(ROOT / crop["path"]))
            assert (original.width, original.height, original.samples) == (
                stored.width, stored.height, stored.samples)
    base = treaty.load_prior()
    manifest = json.loads((treaty.PRIOR / "inputs.json").read_text())
    ranks, square = manifest["key"]["column_rank_order"], manifest["key"]["square"]
    hypothesis = data["assignment"]
    partial = list(prior["conditional_partial_square"])
    pair = hypothesis["pair"]
    cell = 6 * base.CO.index(pair[0]) + base.CO.index(pair[1])
    assert square[cell] == hypothesis["original_label"]
    assert partial[cell] == "?" and hypothesis["value"] not in partial
    partial[cell] = hypothesis["value"]
    partial = "".join(partial)
    prior_records = {r["id"]: r for r in prior["records"]}
    records, occurrences = [], []
    for rec in base.normalized_records(manifest):
        earlier = prior_records[rec["id"]]
        edition = list(rec["ciphertext"])
        for change in earlier["conditional_coordinate_changes"]:
            assert edition[change["frame_index"]] == change["from"]
            edition[change["frame_index"]] = change["to"]
        edition = "".join(edition)
        native = base.read(rec["ciphertext"], ranks, square)
        decoded = base.read(edition, ranks, partial)
        for pos in native["positions"]:
            if pos["pair"] != pair:
                continue
            i = pos["index"]
            edited_pair = "".join(edition[j] for j in pos["frame_indices"])
            retained = edited_pair == pair
            assert retained or (rec["id"], i) == ("p220_C1", 25)
            occurrences.append({"record_id": rec["id"], "plaintext_index": i,
                                "pair": pair, "source_indices": [rec["mapping"][j] for j in pos["frame_indices"]],
                                "baseline_context": rec["raw"][max(0, i - 12):i + 13],
                                "conditional_edition_context": decoded["plaintext"][max(0, i - 12):i + 13],
                                "retained_in_edition": retained,
                                "prior_coordinate_changes": [c for c in earlier["conditional_coordinate_changes"]
                                                             if c["frame_index"] in pos["frame_indices"]]})
        records.append({"id": rec["id"], "conditional_edition": decoded["plaintext"],
                        "conditional_edit_cost": earlier["conditional_edit_cost"],
                        "roundtrip_witness": base.witness(edition, ranks, partial)})
    anchors = [o for o in occurrences if o["record_id"] == hypothesis["record_id"]
               and o["plaintext_index"] == hypothesis["plaintext_index"]]
    assert len(anchors) == 1 and anchors[0]["retained_in_edition"]
    summary = {"reviewed_records": len(records), "observed_raw_occurrences": len(occurrences),
               "retained_edition_occurrences": sum(o["retained_in_edition"] for o in occurrences),
               "inconvenient_raw_occurrences": sum(not o["retained_in_edition"] for o in occurrences),
               "additional_coordinate_changes": 0,
               "remaining_square_completions": math.factorial(partial.count("?"))}
    assert summary == data["expected"], summary
    by_id = {r["id"]: r for r in records}
    for field in data["case_fields"]:
        start, end = field["range"]
        assert by_id[field["record_id"]]["conditional_edition"][start:end] == field["conditional"], field
        assert "`" + field["conditional"] + "`" in (ROOT / field["case_path"]).read_text(), field
    return {"schema": "adfgvx-nov25-breslau-extension-certificate-v1",
            "prepared_by": data["prepared_by"], "input_sha256": treaty.digest(HERE / "breslau_inputs.json"),
            "prior_partial_square": prior["conditional_partial_square"],
            "conditional_partial_square": partial,
            "remaining_cell_domain": "".join(sorted(set(base.ALPHABET) - (set(partial) - {"?"}))),
            "summary": summary, "all_observed_assignment_occurrences": occurrences,
            "records": records, "checked_case_fields": data["case_fields"], "limits": data["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--historical-pdf", type=Path)
    args = parser.parse_args()
    result = run(args.historical_pdf)
    target = HERE / "breslau_certificate.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
