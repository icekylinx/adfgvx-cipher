#!/usr/bin/env python3
"""Verify a separately priced p137 staff-vocabulary proposal and its limits.

Prepared by icekylinx and GPT-6 Astra Pro. The primary zero-substitution
edition, published period keys and all original source images stay unchanged.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.transylvania_situation_report.verify import (
    C, frame, inspect, literal_of, masked_encryption, repair)
from experiments.november_radio_service.verify import encode, inverse, reading, transpose
from data.reviews.check_reading_presentation import displays, expected_legend


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_key(data, record):
    if "key" in data:
        return data["key"]
    keys = data["keys"]
    return (next(k for k in keys if k["id"] == record["key_id"])
            if isinstance(keys, list) else keys[record["key_id"]])


def allocation_costs(rec, key, template, visual=None):
    stencil = masked_encryption(template, key)
    costs = []
    for first in range(38):
        last = 37 - first
        literal, model, origins = frame(rec, [(190, first), (215, last)], visual)
        changes = [(i, a, b) for i, (a, b) in enumerate(zip(model, stencil))
                   if b != "?" and a != b]
        costs.append({"first_missing_run": first, "last_missing_run": last,
                      "observed_substitutions": sum(a in C for _, a, _ in changes),
                      "printed_mask_fills": sum(a == "?" and origins[i] is not None
                                                for i, a, b in changes),
                      "missing_coordinate_fills": sum(a == "?" and origins[i] is None
                                                      for i, a, b in changes)})
    best = min(x["observed_substitutions"] for x in costs)
    return {"scope": "All 38 original interference allocations; '?' in the fixed optional target is unconstrained.",
            "all_costs": costs, "minimum_observed_substitutions": best,
            "all_minimum_first_run_lengths": [x["first_missing_run"] for x in costs
                                               if x["observed_substitutions"] == best],
            "fixed_target_chosen_retrospectively": True}


def complete_witness(candidate, key, mapping):
    # Each source coordinate belongs to one pair; the fixed square is unchanged.
    plaintext = "".join(p["domain"][0] for p in candidate["positions"])
    witness = transpose(encode(plaintext, key["square"]), key["column_rank_order"])
    assert all(a == "?" or a == b for a, b in zip(candidate["ciphertext"], witness))
    assert inspect(witness, key, mapping)["raw"] == plaintext
    return {"plaintext": plaintext, "model_ciphertext": witness,
            "limit": "Arbitrary mathematical completion of the ten unasserted labels; not historical plaintext."}


def check_image(item, document=None):
    assert sha(ROOT / item["path"]) == item["sha256"]
    if document is not None:
        import fitz
        clip = item.get("clip_points", item.get("crop_pdf_points"))
        scale = item.get("scale", item.get("render_scale"))
        pix = document[item["pdf_page_1based"] - 1].get_pixmap(
            matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(*clip))
        saved = fitz.Pixmap(str(ROOT / item["path"]))
        assert (pix.width, pix.height, pix.n) == (saved.width, saved.height, saved.n)
        assert pix.samples == saved.samples


def rebuild(inp, pdf=None):
    live = json.loads((ROOT / inp["live_input_path"]).read_text())
    rec = next(r for r in live["records"] if r["id"] == "p137_A5")
    key = live["key"]
    assert rec == inp["record_snapshot"] and key == inp["key_snapshot"]
    literal, model, mapping = frame(rec)
    assert len(literal) == 215 and literal.count("-") == 4
    assert len(model) == 252 and mapping == list(range(215)) + [None] * 37
    assert rec["model"]["primary_run_lengths"] == [0, 37]
    raw = inspect(model, key, mapping)
    assert raw["raw"] == rec["expected_raw"]
    assert raw["fixed_positions"] == 85
    native_source = "".join(c if c in C else "?" for c in literal)
    native_mid, native_origins = inverse(native_source, key["column_rank_order"])
    native = reading(native_mid, native_origins, key["square"])
    assert native["unpaired_coordinate"] is not None
    primary = repair(rec["readable_candidate"], model, key, mapping, literal)
    assert primary["fixed_positions"] == 106
    assert primary["known_coordinate_substitutions"] == []
    assert len(primary["erased_coordinate_fills"]) == 21
    prop = inp["proposal"]
    target = list(rec["readable_candidate"])
    for word in prop["new_word_spans"]:
        a = word["start"]
        target[a:a + len(word["text"]) ] = word["text"]
    target = "".join(target)
    assert target == prop["editorial_text"] and len(target) == 126
    assert target[:64] == rec["readable_candidate"][:64]
    assert target[96:] == rec["readable_candidate"][96:]
    assert target[75] == "?" and target[96:100] == prop["preserved_numeral_field"] == "?B6?"
    optional = repair(target, model, key, mapping, literal)
    edits = optional["known_coordinate_substitutions"]
    fills = optional["erased_coordinate_fills"]
    assert [[e["source_index"], e["from"], e["to"]] for e in edits] == prop["expected_observed_changes"]
    assert len(edits) == prop["expected_total_observed_substitutions"] == 3
    printed_fills = [e for e in fills if e["source_index"] is not None]
    missing_fills = [e for e in fills if e["source_index"] is None]
    assert len(printed_fills) == prop["expected_total_printed_mask_fills"] == 3
    assert len(missing_fills) == prop["expected_total_missing_coordinate_fills"] == 28
    old_fills = {e["model_index"]: e for e in primary["erased_coordinate_fills"]}
    new_fills = {e["model_index"]: e for e in fills}
    assert all(new_fills[i] == e for i, e in old_fills.items())
    additions = [e for e in fills if e["model_index"] not in old_fills]
    assert all(e["source_index"] is None for e in additions)
    assert [[e["model_index"], e["to"]] for e in additions] == prop["expected_additional_missing_coordinate_fills"]
    assert optional["fixed_positions"] == prop["expected_fixed_positions"] == 116
    unknowns = [p for p in optional["positions"] if p["raw"] == "?"]
    assert [p["plaintext_index"] for p in unknowns] == prop["preserved_unknown_positions"]
    assert len(unknowns) == 10
    numeral = raw["positions"][98]
    assert numeral["raw"] == target[98] == "6"
    assert all(model[i] == optional["ciphertext"][i] for i in numeral["model_indices"])
    math_witness = complete_witness(optional, key, mapping)
    comparisons = allocation_costs(rec, key, target)
    assert comparisons["minimum_observed_substitutions"] == 3
    assert comparisons["all_minimum_first_run_lengths"] == [0]
    # Evaluate the visibly unsettled glyph as a source variant, never a free edit.
    visual = inp["visual_alternative"]
    assert visual["source_index"] == 68 and literal[68] == visual["original_transcript"] == "F"
    assert visual["alternative"] == "V"
    _, alternate_model, alternate_mapping = frame(rec, visual=(68, "V"))
    assert alternate_mapping == mapping
    assert [i for i, (a, b) in enumerate(zip(model, alternate_model)) if a != b] == [68]
    alternate_raw = inspect(alternate_model, key, mapping)
    alternate = repair(target, alternate_model, key, mapping, literal)
    assert len(alternate["known_coordinate_substitutions"]) == 2
    assert [e["source_index"] for e in alternate["known_coordinate_substitutions"]] == [201, 202]
    assert alternate["erased_coordinate_fills"] == fills
    assert alternate["ciphertext"] == optional["ciphertext"]
    alternate_costs = allocation_costs(rec, key, target, visual=(68, "V"))
    assert alternate_costs["minimum_observed_substitutions"] == 2
    assert alternate_costs["all_minimum_first_run_lengths"] == [0]
    witnesses = []
    images = [inp["source"]["image"]]
    for item in inp["independent_witnesses"]:
        data = json.loads((ROOT / item["live_input_path"]).read_text())
        record = next(r for r in data["records"] if r["id"] == item["id"])
        witness_key = get_key(data, record)
        assert record == item["record_snapshot"] and witness_key == item["key_snapshot"]
        images.append(item["image"])
        if item["id"] == "p184_B1":
            text = "".join("".join(record["source_rows"]).split())
            reading_ = inspect(text, witness_key, list(range(len(text))))
            assert reading_["raw"] == record["expected_raw"]
            span = "MACKENSENXWIRTSCHAFTSSTABXMINERALOELABTEILUNG"
            start = reading_["raw"].index(span)
            letters = reading_["positions"][start:start + len(span)]
            assert all(len(p["domain"]) == 1 and all(c in C for c in p["pair"])
                       for p in letters)
            witnesses.append({"id": item["id"], "role": "Independent raw vocabulary",
                              "unmodified_raw": reading_["raw"], "span": span,
                              "start_plaintext_index": start, "letter_ledger": letters,
                              "observed_substitutions": 0, "mask_fills": 0})
        else:
            assert item["id"] == "p122_B"
            phrase = "OBERKOMMANDO M VERWALTUNGSSTAB"
            assert phrase in record["header_literal"]
            witnesses.append({"id": item["id"], "role": "Independent clear header vocabulary",
                              "literal_header": record["header_literal"], "bound_phrase": phrase,
                              "not_a_decrypted_body_claim": True})
    document = None
    if pdf:
        import fitz
        assert sha(pdf) == inp["source"]["pdf_sha256"]
        document = fitz.open(pdf)
    for img in images:
        check_image(img, document)
    case = inp["primary_case"]
    text = (ROOT / case["path"]).read_text()
    fences, quotes = displays(text)
    assert [line for line in text.splitlines() if re.match(r"^#{1,6} ", line)] == case["headings"]
    assert [x["sha256"] for x in fences] == case["fence_sha256"]
    # The later full-part quotation has its own coordinate verifier. Keep the
    # original display snapshot exact while accounting for that added layer.
    completion_caption = "**Readable German — conditional complete part-5 proposal:**"
    later = [x for x in quotes if x["caption"] == completion_caption]
    assert len(later) == 1
    assert later[0]["sha256"] == "9353511f9012e3673af64a6c9c4c4e7742907cfbd933757c2f416e5a1e954030"
    quotes = [x for x in quotes if x["caption"] != completion_caption]
    assert [x["sha256"] for x in quotes] == case["quote_sha256"]
    page = HERE / "README.md"
    text = page.read_text()
    assert text.count(expected_legend(page)) == 1
    fences, quotes = displays(text)
    assert all(x["role_from_caption"] for x in fences + quotes)
    assert re.findall(r"```text\n(.*?)\n```", text, flags=re.S) == [raw["raw"], rec["readable_candidate"], target]
    quote = "".join(line[2:] for line in text.splitlines() if line.startswith("> "))
    assert re.sub(r"[^A-Z0-9?]", "", quote.upper()) == target
    return {"schema": "adfgvx-p137-optional-staff-vocabulary-certificate-v1",
            "prepared_by": inp["prepared_by"],
            "native_literal_215_slot_reading": native,
            "conditional_252_slot_ciphertext": model,
            "conditional_model_to_source_indices": mapping,
            "unchanged_conditional_raw": raw,
            "unchanged_primary_edition": primary,
            "optional_staff_vocabulary": optional,
            "additional_missing_coordinate_fills": additions,
            "remaining_unknown_positions": unknowns,
            "preserved_literal_numeral": numeral,
            "arbitrary_nonhistorical_complete_witness": math_witness,
            "all_original_interference_allocations": comparisons,
            "unadopted_visual_V_alternative": {"source_override": visual,
                                              "raw": alternate_raw,
                                              "optional_reading": alternate,
                                              "all_allocations": alternate_costs},
            "independent_vocabulary_witnesses": witnesses,
            "primary_case_displays_unchanged": True,
            "new_physical_records": 0,
            "limits": inp["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    result = rebuild(inputs, args.pdf)
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text()), "Rebuilt certificate differs"
        print("VERIFIED optional p137 vocabulary: +3 substitutions, +10 lost-coordinate fills, 116/126 fixed; ten unknowns and both F/V alternatives retained")
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print("Wrote " + str(path.relative_to(ROOT)))


if __name__ == "__main__":
    main()
