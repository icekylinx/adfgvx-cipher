#!/usr/bin/env python3
"""Verify the optional p132 KOSPOLI spelling without changing its primary edition.

Prepared by icekylinx and GPT-6 Astra Pro. Published period keys remain
credited to George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker.
Standard library only, except optional PyMuPDF source-pixel verification.
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
from data.reviews.check_reading_presentation import displays, expected_legend

CO = "ADFGVX"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def live_key(document, record):
    if "keys" not in document:
        return document["key"]
    keys = document["keys"]
    if isinstance(keys, list):
        return next(key for key in keys if key["id"] == record["key_id"])
    return keys[record["key_id"]]


def literal(record):
    rows = record.get("rows", record.get("source_rows"))
    result = "".join("".join(rows).split())
    if "literal_source" in record:
        assert result == record["literal_source"]
    assert len(result) == record["advertised_length"]
    return result


def inverse(source, ranks):
    width = len(ranks)
    heights = [len(source) // width + (i < len(source) % width)
               for i in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[i])
              for i in range(width)]
    origins = [starts[i % width] + i // width for i in range(len(source))]
    assert sorted(origins) == list(range(len(source)))
    return "".join(source[i] for i in origins), origins


def transpose(stream, ranks):
    return "".join(stream[i::len(ranks)] for i in
                   sorted(range(len(ranks)), key=lambda i: ranks[i]))


def decode(source, key):
    square, ranks = key["square"], key["column_rank_order"]
    assert len(square) == len(set(square)) == 36 and "?" not in square
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    stream, origins = inverse(source, ranks)
    assert transpose(stream, ranks) == source and len(stream) % 2 == 0
    domains, pairs = [], []
    for i in range(0, len(stream), 2):
        pair = stream[i:i + 2]
        values = sorted({square[6 * r + c] for r in range(6) for c in range(6)
                         if (pair[0] not in CO or pair[0] == CO[r])
                         and (pair[1] not in CO or pair[1] == CO[c])})
        domains.append("".join(values))
        pairs.append({"plaintext_index": i // 2,
                      "source_indices": origins[i:i + 2],
                      "literal_coordinate_pair": pair,
                      "domain": "".join(values)})
    return {"raw": "".join(d if len(d) == 1 else "?" for d in domains),
            "positions": len(domains),
            "fixed_positions": sum(len(d) == 1 for d in domains),
            "letter_ledger": pairs}


def encode(text, key):
    square = key["square"]
    assert all(c in square for c in text)
    interim = "".join(CO[square.index(c) // 6] + CO[square.index(c) % 6]
                      for c in text)
    return transpose(interim, key["column_rank_order"])


def witness(text, source, key, raw):
    outgoing = encode(text, key)
    assert len(outgoing) == len(source)
    assert decode(outgoing, key)["raw"] == text
    origin_to_letter = {origin: pair["plaintext_index"]
                        for pair in raw["letter_ledger"]
                        for origin in pair["source_indices"]}
    observed, fills = [], []
    for i, (before, after) in enumerate(zip(source, outgoing)):
        if before == after:
            continue
        n = origin_to_letter[i]
        item = {"source_index": i, "printed_group_1based": i // 5 + 1,
                "group_position_1based": i % 5 + 1,
                "before": before, "after": after,
                "plaintext_index": n, "raw_label": raw["raw"][n],
                "proposed_label": text[n]}
        (observed if before in CO else fills).append(item)
    return {"plaintext": text, "received_witness": outgoing,
            "observed_substitutions": observed, "source_mask_fills": fills,
            "cost": {"observed_substitutions": len(observed),
                     "source_mask_fills": len(fills),
                     "inserted_source_slots": 0, "excluded_source_slots": 0,
                     "reordered_source_slots": 0, "key_changes": 0},
            "exact_forward_witness": True}


def rebuild(inputs, pdf=None):
    document = None
    if pdf:
        import fitz
        assert sha(pdf) == inputs["source"]["pdf_sha256"]
        document = fitz.open(pdf)
    records = {}
    for item in inputs["records"]:
        live = json.loads((ROOT / item["live_input_path"]).read_text())
        rec = next(r for r in live["records"] if r["id"] == item["id"])
        key = live_key(live, rec)
        assert rec == item["record_snapshot"] and key == item["key_snapshot"]
        source = literal(rec)
        reading = decode(source, key)
        expected = rec.get("expected_raw", rec.get("expected_unmodified_raw"))
        assert reading["raw"] == expected
        img = item["image"]
        assert sha(ROOT / img["path"]) == img["sha256"]
        if document is not None:
            rendered = document[img["pdf_page_1based"] - 1].get_pixmap(
                matrix=fitz.Matrix(img["scale"], img["scale"]),
                clip=fitz.Rect(*img["clip_points"]))
            saved = fitz.Pixmap(str(ROOT / img["path"]))
            assert (rendered.width, rendered.height, rendered.n) == (
                saved.width, saved.height, saved.n)
            assert rendered.samples == saved.samples
        records[item["id"]] = {"source": source, "key": key,
                                "record": rec, "reading": reading}
    main = records["p132_A"]
    raw = main["reading"]
    assert raw["positions"] == 121 and raw["fixed_positions"] == 120
    primary = witness(main["record"]["editorial_text"], main["source"],
                      main["key"], raw)
    assert primary["cost"]["observed_substitutions"] == 6
    assert primary["cost"]["source_mask_fills"] == 1
    proposal = inputs["proposal"]
    assert primary["plaintext"].count(proposal["original_field"]) == 1
    target = primary["plaintext"].replace(proposal["original_field"],
                                          proposal["proposed_field"])
    optional = witness(target, main["source"], main["key"], raw)
    for field in proposal["preserved_literal_fields"]:
        assert field in raw["raw"] and field in primary["plaintext"] and field in target
    extra = [[i, a, b] for i, (a, b) in enumerate(zip(
        primary["received_witness"], optional["received_witness"])) if a != b]
    assert extra == proposal["expected_additional_changes"]
    assert len(extra) == proposal["expected_additional_observed_substitutions"] == 2
    assert all(main["source"][i] == a and a in CO for i, a, b in extra)
    assert optional["cost"]["observed_substitutions"] == proposal[
        "expected_total_observed_substitutions"] == 8
    assert optional["cost"]["source_mask_fills"] == proposal[
        "expected_total_source_mask_fills"] == 1
    assert optional["source_mask_fills"] == primary["source_mask_fills"]
    numerals = []
    for i, c in enumerate(raw["raw"]):
        if c.isdigit():
            assert primary["plaintext"][i] == target[i] == c
            pair = raw["letter_ledger"][i]
            assert all(main["source"][j] == optional["received_witness"][j]
                       for j in pair["source_indices"])
            numerals.append(pair)
    witnesses = []
    for ident, spans in inputs["witness_spans"].items():
        entry = records[ident]
        reading = entry["reading"]
        bound = []
        for span in spans:
            assert reading["raw"].count(span) == 1
            begin = reading["raw"].index(span)
            letters = reading["letter_ledger"][begin:begin + len(span)]
            assert all(len(x["domain"]) == 1 and
                       all(c in CO for c in x["literal_coordinate_pair"])
                       for x in letters)
            bound.append({"span": span, "start_plaintext_index": begin,
                          "end_plaintext_index_exclusive": begin + len(span),
                          "letter_ledger": letters})
        witnesses.append({"id": ident, "key_id": entry["key"]["id"],
                          "literal_source": entry["source"],
                          "unmodified_raw": reading["raw"], "bound_spans": bound,
                          "applied_observed_substitutions": 0,
                          "applied_source_mask_fills": 0,
                          "relationship": "Independent wording attestation, not an identical-copy claim."})
    case = inputs["primary_case"]
    text = (ROOT / case["path"]).read_text()
    fences, quotes = displays(text)
    assert [x for x in text.splitlines() if re.match(r"^#{1,6} ", x)] == case["headings"]
    assert [x["sha256"] for x in fences] == case["fence_sha256"]
    assert [x["sha256"] for x in quotes] == case["quote_sha256"]
    page = HERE / "README.md"
    text = page.read_text()
    assert text.count(expected_legend(page)) == 1
    fences, quotes = displays(text)
    assert all(x["role_from_caption"] is not None for x in fences + quotes)
    streams = re.findall(r"```text\n(.*?)\n```", text, flags=re.S)
    assert streams == [raw["raw"], primary["plaintext"], target]
    assert "`GENERALMAJRHYDEWALD`" in text and "`PAFR53540`" in text
    return {"schema": "adfgvx-p132-optional-address-certificate-v1",
            "prepared_by": inputs["prepared_by"],
            "unmodified_p132_reading": raw,
            "unchanged_primary_edition": primary,
            "optional_address_proposal": optional,
            "additional_observed_changes": extra,
            "preserved_raw_numerals": numerals,
            "independent_raw_witnesses": witnesses,
            "new_physical_records": 0,
            "primary_case_headings_and_displays_unchanged": True,
            "name_identification_claim": None,
            "limits": inputs["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    result = rebuild(inputs, args.pdf)
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text()), "Certificate differs from rebuilt evidence"
        print("VERIFIED p132 optional KOSPOLI: +2 observed substitutions; primary 6+1 unchanged; 3 raw witnesses")
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print("Wrote " + str(path.relative_to(ROOT)))


if __name__ == "__main__":
    main()
