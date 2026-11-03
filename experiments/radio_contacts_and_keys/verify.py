#!/usr/bin/env python3
"""Verify seven radio-contact, key-availability and neighboring source records.

Prepared by icekylinx and GPT-6 Astra Pro. The published key retains credit
to Lasry, Niebel, Kopal and Wacker. Default verification uses standard Python.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO = "ADFGVX"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def undo(cipher, ranks):
    width = len(ranks)
    columns, source_indices, offset = {}, {}, 0
    for column in sorted(range(width), key=lambda c: ranks[c]):
        height = len(cipher) // width + (column < len(cipher) % width)
        columns[column] = cipher[offset:offset + height]
        source_indices[column] = list(range(offset, offset + height))
        offset += height
    stream, origins = [], []
    for index in range(len(cipher)):
        col, row = index % width, index // width
        stream.append(columns[col][row])
        origins.append(source_indices[col][row])
    assert sorted(origins) == list(range(len(cipher)))
    return "".join(stream), origins


def transpose(stream, ranks):
    return "".join(stream[c::len(ranks)]
                   for c in sorted(range(len(ranks)), key=lambda c: ranks[c]))


def reading(stream, square):
    assert len(stream) % 2 == 0
    domains = []
    for index in range(0, len(stream), 2):
        a, b = stream[index:index + 2]
        domains.append("".join(sorted({square[6 * row + col]
                       for row in range(6) for col in range(6)
                       if (a == "?" or a == CO[row])
                       and (b == "?" or b == CO[col])})))
    return {"plaintext": "".join(d if len(d) == 1 else "?" for d in domains),
            "domains": domains, "plaintext_positions": len(domains),
            "fixed_positions": sum(len(d) == 1 for d in domains)}


def encode(text, square):
    return "".join(CO[square.index(c) // 6] + CO[square.index(c) % 6]
                   for c in text)


def locations(rows):
    result, number = [], 0
    for rownum, row in enumerate(rows, 1):
        for group_in_row, group in enumerate(row.split(), 1):
            number += 1
            result.extend({"printed_row_1based": rownum,
                           "group_in_row_1based": group_in_row,
                           "printed_group_1based": number,
                           "group_position_1based": j + 1}
                          for j in range(len(group)))
    return result


def rebuild(inputs, pdf=None):
    keys = {k["id"]: k for k in inputs["keys"]}
    for key in keys.values():
        square, ranks = key["square"], key["column_rank_order"]
        assert len(square) == len(set(square)) == 36
        assert set(square) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        assert sorted(ranks) == list(range(1, len(ranks) + 1))
    document = None
    if pdf:
        import fitz
        assert sha(pdf) == inputs["source"]["pdf_sha256"]
        document = fitz.open(pdf)
    for item in inputs["source"]["images"]:
        assert sha(HERE / item["path"]) == item["sha256"]
        if document is not None:
            pix = document[item["pdf_page_1based"] - 1].get_pixmap(
                matrix=fitz.Matrix(item["scale"], item["scale"]),
                clip=fitz.Rect(*item["clip_points"]))
            assert (pix.width, pix.height) == (item["width"], item["height"])
            assert hashlib.sha256(pix.samples).hexdigest() == item["pixel_sha256"]
    records = []
    for rec in inputs["records"]:
        key = keys[rec["key_id"]]
        square, ranks = key["square"], key["column_rank_order"]
        groups = " ".join(rec["rows"]).split()
        assert all(len(g) == 5 for g in groups[:-1])
        literal = "".join(groups)
        source = "".join(c if c in CO else "?" for c in literal)
        assert literal == rec["literal_source"] and source == rec["analysis_source"]
        assert len(source) == rec["advertised_length"]
        assert set(literal) <= set(CO + "-")
        assert rec["key_id"] == key["id"]
        stream, origins = undo(source, ranks)
        assert transpose(stream, ranks) == source
        raw = reading(stream, square)
        assert raw["plaintext"] == rec["expected_raw"]
        proposed = rec["editorial_text"]
        encoded = encode(proposed, square)
        assert len(encoded) == len(stream)
        witness = transpose(encoded, ranks)
        places = locations(rec["rows"])
        substitutions, fills = [], []
        for index, (before, after) in enumerate(zip(source, witness)):
            if before == after:
                continue
            pair = origins.index(index) // 2
            item = {"source_index": index, **places[index], "before": before,
                    "diplomatic_source_glyph": literal[index], "after": after,
                    "plaintext_index": pair, "raw_plaintext_symbol": raw["plaintext"][pair],
                    "proposed_plaintext_symbol": proposed[pair]}
            (fills if before == "?" else substitutions).append(item)
        edits = substitutions + fills
        assert sorted([[e["source_index"], e["before"], e["after"]] for e in edits]) == rec["expected_source_changes"]
        cost = {"known_coordinate_substitutions": len(substitutions),
                "source_erasure_fills": len(fills)}
        assert cost == rec["expected_cost"]
        repaired = list(source)
        for item in edits:
            repaired[item["source_index"]] = item["after"]
        assert "".join(repaired) == witness
        assert reading(undo(witness, ranks)[0], square)["plaintext"] == proposed
        numerals, repairs = [], {r["plaintext_index"]: r
                                for r in rec["explicit_numeral_spelling_repairs"]}
        for index, char in enumerate(raw["plaintext"]):
            if not char.isdigit():
                continue
            changed = char != proposed[index]
            if changed:
                assert repairs[index] == {"plaintext_index": index,
                                          "before": char, "after": proposed[index]}
            else:
                assert all(source[p] == witness[p] for p in origins[2 * index:2 * index + 2])
            numerals.append({"plaintext_index": index, "raw_label": char,
                             "editorial_label": proposed[index],
                             "explicit_spelling_repair": changed,
                             "coordinate_origins": origins[2 * index:2 * index + 2]})
        assert set(repairs) == {n["plaintext_index"] for n in numerals if n["explicit_spelling_repair"]}
        for field in rec["preserved_literal_fields"]:
            assert field in raw["plaintext"] and field in proposed
        records.append({"id": rec["id"], "key_id": key["id"], "source_slots": len(source),
                        "valid_received_coordinates": len(source) - source.count("?"),
                        "raw_reading": raw, "coordinate_origins": [origins[i:i + 2]
                                                  for i in range(0, len(origins), 2)],
                        "editorial_plaintext": proposed, "cost": cost,
                        "known_coordinate_substitutions": substitutions,
                        "source_erasure_fills": fills, "numeral_label_ledger": numerals,
                        "reencrypted_received_witness": witness,
                        "source_length_and_geometry_unchanged": True})
    totals = {"source_records": len(records), "source_slots": sum(r["source_slots"] for r in records),
              "valid_received_coordinates": sum(r["valid_received_coordinates"] for r in records),
              "plaintext_positions": sum(r["raw_reading"]["plaintext_positions"] for r in records),
              "raw_fixed_positions": sum(r["raw_reading"]["fixed_positions"] for r in records),
              "known_coordinate_substitutions": sum(r["cost"]["known_coordinate_substitutions"] for r in records),
              "source_erasure_fills": sum(r["cost"]["source_erasure_fills"] for r in records),
              "coordinate_insertions_or_removals": 0, "published_square_changes": 0}
    assert totals == {"source_records": 7, "source_slots": 1290,
                      "valid_received_coordinates": 1287, "plaintext_positions": 645,
                      "raw_fixed_positions": 642, "known_coordinate_substitutions": 13,
                      "source_erasure_fills": 3, "coordinate_insertions_or_removals": 0,
                      "published_square_changes": 0}
    return {"schema": "adfgvx-radio-contacts-and-keys-certificate-v1",
            "prepared_by": inputs["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
            "totals": totals, "records": records,
            "limits": ["Exact forward witnesses establish the stated local repair prices, not unique historical wording.",
                       "BRSLAU, MEGLICH and PERIDEN remain literal; no extra plaintext letters are inserted.",
                       "p150 A2 is a source-labeled second part; no missing first part is reconstructed.",
                       "OSKACHI availability does not identify an unobserved key, its period or a separate challenge cipher."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = rebuild(json.loads((HERE / "inputs.json").read_text()), args.pdf)
    output = HERE / "certificates.json"
    if args.verify:
        assert json.loads(output.read_text()) == result
    else:
        output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified" if args.verify else "written": True,
                      **result["totals"]}, indent=2))


if __name__ == "__main__":
    main()
