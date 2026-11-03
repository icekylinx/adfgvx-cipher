#!/usr/bin/env python3
"""Verify p132 radio service and p177 A document destruction.

Prepared by icekylinx and GPT-6 Astra Pro. Published keys retain credit to
Lasry, Niebel, Kopal and Wacker. Standard library only unless --pdf is used.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(cipher, ranks):
    width, length = len(ranks), len(cipher)
    heights = [length // width + (col < length % width) for col in range(width)]
    starts = [sum(heights[c] for c in range(width) if ranks[c] < ranks[col]) for col in range(width)]
    positions = [starts[i % width] + i // width for i in range(length)]
    assert sorted(positions) == list(range(length))
    return "".join(cipher[i] for i in positions), positions


def transpose(stream, ranks):
    return "".join(stream[col::len(ranks)]
                   for col in sorted(range(len(ranks)), key=lambda col: ranks[col]))


def reading(stream, origins, square):
    unused = set(ALPHABET) - set(square)
    domains, cells = [], []
    for i in range(0, len(stream) - 1, 2):
        a, b = stream[i:i + 2]
        possibilities, used_cells = set(), []
        for row in range(6):
            if a != "?" and a != CO[row]:
                continue
            for col in range(6):
                if b != "?" and b != CO[col]:
                    continue
                cell = 6 * row + col
                used_cells.append(cell)
                possibilities.update(unused if square[cell] == "?" else square[cell])
        domains.append("".join(sorted(possibilities)))
        cells.append(used_cells)
    return {"plaintext": "".join(d if len(d) == 1 else "?" for d in domains),
            "domains": domains, "possible_square_cells": cells,
            "plaintext_positions": len(domains),
            "fixed_positions": sum(len(d) == 1 for d in domains),
            "coordinate_origins": [origins[i:i + 2] for i in range(0, len(stream) - 1, 2)],
            "unpaired_coordinate": {"interim_index": len(stream) - 1,
                                     "source_index": origins[-1], "coordinate": stream[-1]}
                                    if len(stream) % 2 else None}


def encode(text, square):
    assert "?" not in text and all(char in square for char in text)
    return "".join(CO[square.index(char) // 6] + CO[square.index(char) % 6] for char in text)


def locations(rows):
    output, count = [], 0
    for rownum, row in enumerate(rows, 1):
        for group_in_row, group in enumerate(row.split(), 1):
            count += 1
            output.extend({"printed_row_1based": rownum, "group_in_row_1based": group_in_row,
                           "printed_group_1based": count, "group_position_1based": offset}
                          for offset in range(1, len(group) + 1))
    return output


def edition(rec, key, removal=None):
    source = rec["analysis_source"]
    ranks, square = key["column_rank_order"], key["square"]
    original, original_origins = inverse(source, ranks)
    assert transpose(original, ranks) == source
    stream, origins = original, original_origins
    extra = None
    if removal is not None:
        assert original[removal] == "V"
        extra = {"interim_index": removal, "source_index": origins[removal],
                 "coordinate": original[removal],
                 "treatment": "Extraneous to plaintext pairing, retained unchanged in the full transmitted witness."}
        stream = original[:removal] + original[removal + 1:]
        origins = original_origins[:removal] + original_origins[removal + 1:]
    raw = reading(stream, origins, square)
    assert raw["unpaired_coordinate"] is None
    assert raw["plaintext"] == rec["expected_working_raw"]
    text = rec["editorial_text"]
    proposed = encode(text, square)
    assert len(proposed) == len(stream)
    edits, fills = [], []
    places = locations(rec["rows"])
    for index, (before, after) in enumerate(zip(stream, proposed)):
        if before == after:
            continue
        source_index = origins[index]
        entry = {"working_interim_index": index, "source_index": source_index,
                 **places[source_index], "before": before, "after": after,
                 "diplomatic_source_glyph": rec["literal_source"][source_index],
                 "plaintext_index": index // 2, "raw_plaintext_symbol": raw["plaintext"][index // 2],
                 "proposed_plaintext_symbol": text[index // 2]}
        (fills if before == "?" else edits).append(entry)
    edits.sort(key=lambda item: item["source_index"])
    fills.sort(key=lambda item: item["source_index"])
    outgoing = proposed if extra is None else proposed[:removal] + extra["coordinate"] + proposed[removal:]
    witness = transpose(outgoing, ranks)
    repaired = list(source)
    for change in edits + fills:
        assert repaired[change["source_index"]] == change["before"]
        repaired[change["source_index"]] = change["after"]
    assert "".join(repaired) == witness and len(witness) == len(source)
    if extra is not None:
        assert witness[extra["source_index"]] == source[extra["source_index"]] == extra["coordinate"]
    recovered, recovered_origins = inverse(witness, ranks)
    if removal is not None:
        recovered = recovered[:removal] + recovered[removal + 1:]
        recovered_origins = recovered_origins[:removal] + recovered_origins[removal + 1:]
    assert reading(recovered, recovered_origins, square)["plaintext"] == text
    changes = sorted([[c["source_index"], c["before"], c["after"]] for c in edits + fills])
    assert changes == rec["expected_source_changes"]
    cost = {"substitutions": len(edits), "source_erasure_fills": len(fills),
            "interim_extra_coordinates": int(extra is not None)}
    assert cost == rec["expected_cost"]
    numerals = []
    exception = rec.get("explicit_raw_numeral_spelling_repair")
    for index, char in enumerate(raw["plaintext"]):
        if char.isdigit():
            changed = text[index] != char
            if changed:
                assert exception and index == exception["plaintext_index"]
                assert char == exception["before"] and text[index] == exception["after"]
            else:
                assert all(source[p] == witness[p] for p in raw["coordinate_origins"][index])
            numerals.append({"plaintext_index": index, "raw_label": char,
                             "editorial_label": text[index], "explicit_spelling_repair": changed,
                             "coordinate_origins": raw["coordinate_origins"][index]})
    for field in rec.get("preserved_uncertain_fields", []):
        assert field in raw["plaintext"] and field in text
    return {"working_reading": raw, "editorial_plaintext": text,
            "known_coordinate_substitutions": edits, "source_erasure_fills": fills,
            "extra_interim_coordinate": extra, "cost": cost,
            "numeral_label_ledger": numerals, "reencrypted_received_witness": witness,
            "exact_roundtrip_under_stated_geometry": True}


def rebuild(inputs, pdf=None):
    keys = {key["id"]: key for key in inputs["keys"]}
    for key in keys.values():
        known = key["square"].replace("?", "")
        assert len(key["square"]) == 36 and len(known) == len(set(known))
        assert set(known) <= set(ALPHABET)
        assert sorted(key["column_rank_order"]) == list(range(1, len(key["column_rank_order"]) + 1))
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
        groups = " ".join(rec["rows"]).split()
        assert all(len(g) == 5 for g in groups[:-1])
        literal = "".join(groups)
        assert literal == rec["literal_source"]
        source = "".join(char if char in CO else "?" for char in literal)
        assert source == rec["analysis_source"] and len(source) == rec["advertised_length"]
        key = keys[rec["key_id"]]
        original, original_origins = inverse(source, key["column_rank_order"])
        direct = reading(original, original_origins, key["square"])
        assert direct["plaintext"] == rec["expected_unmodified_raw"]
        model = rec["frame_model"]
        variants = []
        if model["kind"] == "one_extra_interim_coordinate":
            assert model["equivalent_removal_indices"] == [54, 55, 56, 57]
            for position in model["equivalent_removal_indices"]:
                variants.append({"removal_index": position, **edition(rec, key, position)})
            assert len({v["reencrypted_received_witness"] for v in variants}) == 1
            selected = next(v for v in variants if v["removal_index"] == model["representative_removal_index"])
            chosen = {k: v for k, v in selected.items() if k != "removal_index"}
        else:
            assert model["kind"] == "identity"
            chosen = edition(rec, key)
        records.append({"id": rec["id"], "key_id": key["id"],
                        "source_slots": len(source), "valid_received_coordinates": len(source) - source.count("?"),
                        "unmodified_source_reading": direct,
                        "working_reading_is_conditional": bool(variants),
                        **chosen, "equivalent_removal_variants": variants})
    exact = [r for r in records if not r["working_reading_is_conditional"]]
    totals = {"source_records": 4, "source_slots": sum(r["source_slots"] for r in records),
              "valid_received_coordinates": sum(r["valid_received_coordinates"] for r in records),
              "ordinary_frame_records": len(exact),
              "ordinary_frame_positions": sum(r["working_reading"]["plaintext_positions"] for r in exact),
              "ordinary_frame_fixed_positions": sum(r["working_reading"]["fixed_positions"] for r in exact),
              "conditional_positions": records[1]["working_reading"]["plaintext_positions"],
              "conditional_fixed_positions": records[1]["working_reading"]["fixed_positions"],
              "known_coordinate_substitutions": sum(r["cost"]["substitutions"] for r in records),
              "source_erasure_fills": sum(r["cost"]["source_erasure_fills"] for r in records),
              "conditional_extra_interim_coordinates": 1,
              "equivalent_extra_coordinate_positions": 4, "published_square_changes": 0}
    assert totals == {"source_records": 4, "source_slots": 781,
                      "valid_received_coordinates": 778, "ordinary_frame_records": 3,
                      "ordinary_frame_positions": 313, "ordinary_frame_fixed_positions": 311,
                      "conditional_positions": 77, "conditional_fixed_positions": 75,
                      "known_coordinate_substitutions": 11, "source_erasure_fills": 3,
                      "conditional_extra_interim_coordinates": 1,
                      "equivalent_extra_coordinate_positions": 4, "published_square_changes": 0}
    p177 = records[3]["unmodified_source_reading"]
    assert [d for d in p177["domains"] if len(d) != 1] == ["56789"]
    return {"schema": "adfgvx-november-radio-service-certificate-v1",
            "prepared_by": inputs["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
            "totals": totals, "records": records,
            "limits": ["p132 A's addressee/general-name fields remain unresolved raw strings despite ordinary-word repairs.",
                       "p132 B's extra-V mechanism is conditional. Four identical-V positions are indistinguishable and produce one source-shaped witness.",
                       "The local FU1NFTER-to-FUENFTER spelling repair is explicit and does not reassign the square's digit 1.",
                       "p132 C's NACHCHE5 and all reference labels remain literal.",
                       "p177 A changes two received coordinates; no erased coordinate or unknown square cell is filled.",
                       "Re-encryption certifies arithmetic consistency and cost, not historical uniqueness."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = rebuild(json.loads((HERE / "inputs.json").read_text()), args.pdf)
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["totals"]}, indent=2))


if __name__ == "__main__":
    main()
