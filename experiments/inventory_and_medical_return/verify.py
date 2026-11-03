#!/usr/bin/env python3
"""Verify p86 A and the two p104 C military service records independently.

Prepared by icekylinx and GPT-6 Astra Pro. The unchanged key retains credit
to Lasry, Niebel, Kopal and Wacker. Standard library unless --pdf is used.
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
    columns, offsets, position = {}, {}, 0
    width = len(ranks)
    for col in sorted(range(width), key=lambda c: ranks[c]):
        height = len(cipher) // width + (col < len(cipher) % width)
        columns[col] = cipher[position:position + height]
        offsets[col] = list(range(position, position + height))
        position += height
    origins = [offsets[i % width][i // width] for i in range(len(cipher))]
    assert sorted(origins) == list(range(len(cipher)))
    return "".join(columns[i % width][i // width] for i in range(len(cipher))), origins


def transpose(stream, ranks):
    return "".join(stream[c::len(ranks)]
                   for c in sorted(range(len(ranks)), key=lambda c: ranks[c]))


def reading(stream, square):
    domains = []
    for i in range(0, len(stream) - 1, 2):
        a, b = stream[i:i + 2]
        domains.append("".join(sorted({square[6 * row + col]
                       for row in range(6) for col in range(6)
                       if (a == "?" or a == CO[row])
                       and (b == "?" or b == CO[col])})))
    return {"plaintext": "".join(d if len(d) == 1 else "?" for d in domains),
            "domains": domains, "plaintext_positions": len(domains),
            "fixed_positions": sum(len(d) == 1 for d in domains),
            "unpaired_coordinate": stream[-1] if len(stream) % 2 else None}


def encode(text, square):
    return "".join(CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in text)


def locations(rows):
    answer, groupnum = [], 0
    for rownum, row in enumerate(rows, 1):
        for inrow, group in enumerate(row.split(), 1):
            groupnum += 1
            answer.extend({"printed_row_1based": rownum, "group_in_row_1based": inrow,
                           "printed_group_1based": groupnum, "group_position_1based": j + 1}
                          for j in range(len(group)))
    return answer


def edition(rec, key, missing=None):
    source, square, ranks = rec["analysis_source"], key["square"], key["column_rank_order"]
    working = source if missing is None else source[:missing] + "?" + source[missing:]
    source_map = list(range(len(source)))
    if missing is not None:
        source_map.insert(missing, None)
    stream, working_origins = undo(working, ranks)
    origins = [source_map[i] for i in working_origins]
    raw = reading(stream, square)
    assert raw["unpaired_coordinate"] is None
    target = rec["editorial_text"]
    completed = transpose(encode(target, square), ranks)
    assert len(completed) == len(working) == rec["advertised_length"]
    witness = completed if missing is None else completed[:missing] + completed[missing + 1:]
    assert len(witness) == len(source)
    places = locations(rec["rows"])
    changes = []
    for i, (before, after) in enumerate(zip(source, witness)):
        if before == after:
            continue
        index = origins.index(i) // 2
        changes.append({"source_index": i, **places[i], "before": before, "after": after,
                        "plaintext_index": index, "raw_plaintext_symbol": raw["plaintext"][index],
                        "proposed_plaintext_symbol": target[index]})
    assert [[c["source_index"], c["before"], c["after"]] for c in changes] == rec["expected_source_changes"]
    cost = {"known_coordinate_substitutions": len(changes), "source_erasure_fills": 0,
            "missing_transmitted_coordinates": int(missing is not None)}
    assert cost == rec["expected_cost"]
    repaired = list(source)
    for c in changes:
        repaired[c["source_index"]] = c["after"]
    assert "".join(repaired) == witness
    assert reading(undo(completed, ranks)[0], square)["plaintext"] == target
    insertion = None
    if missing is not None:
        assert completed[missing] == rec["geometry"]["inserted_coordinate"] == "A"
        plainindex = working_origins.index(missing) // 2
        insertion = {"reconstructed_transmitted_index": missing, "coordinate": completed[missing],
                     "source_group_local": missing in rec["geometry"]["source_short_group"]["source_local_insertion_indices"],
                     "plaintext_index": plainindex, "raw_domain": raw["domains"][plainindex],
                     "proposed_plaintext_symbol": target[plainindex]}
        assert raw["fixed_positions"] == 113 and raw["plaintext_positions"] == 114
    numerals = []
    for i, char in enumerate(raw["plaintext"]):
        if not char.isdigit():
            continue
        changed = target[i] != char
        if changed:
            assert rec["id"] == "p86_A" and char == "4" and target[i] == "E"
            assert raw["plaintext"][i - 3:i + 4] == "BER4ICH"
            assert rec["explicit_numeral_spelling_repairs"] == [
                {"before": "4", "after": "E", "raw_word": "BER4ICH", "proposed_word": "BEREICH"}]
        else:
            assert all(p is None or source[p] == witness[p] for p in origins[2 * i:2 * i + 2])
        numerals.append({"plaintext_index": i, "raw_label": char,
                         "editorial_label": target[i], "explicit_spelling_repair": changed,
                         "coordinate_origins": origins[2 * i:2 * i + 2]})
    for field in rec["preserved_literal_fields"]:
        assert field in raw["plaintext"] and field in target
    return {"missing_transmitted_index": missing, "working_source_slots": len(working),
            "working_raw_reading": raw,
            "coordinate_origins": [origins[i:i + 2] for i in range(0, len(origins), 2)],
            "editorial_plaintext": target, "known_coordinate_substitutions": changes,
            "missing_transmitted_coordinate": insertion, "cost": cost,
            "numeral_label_ledger": numerals, "complete_encoded_witness": completed,
            "repaired_received_witness": witness}


def rebuild(inputs, pdf=None):
    keys = {k["id"]: k for k in inputs["keys"]}
    for key in keys.values():
        assert set(key["square"]) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        assert len(key["square"]) == 36
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
        key = keys[rec["key_id"]]
        groups = " ".join(rec["rows"]).split()
        source = "".join(groups)
        assert source == rec["literal_source"] == rec["analysis_source"]
        assert set(source) <= set(CO)
        original, origins = undo(source, key["column_rank_order"])
        unmodified = reading(original, key["square"])
        assert unmodified["plaintext"] == rec["expected_unmodified_raw"]
        if unmodified["unpaired_coordinate"] is not None:
            unmodified["unpaired_source_index"] = origins[-1]
        variants, prices = [], []
        if rec["geometry"]["kind"] == "identity":
            assert all(len(g) == 5 for g in groups[:-1])
            assert len(source) == rec["advertised_length"]
            selected = edition(rec, key)
        else:
            assert rec["geometry"]["kind"] == "one_missing_transmitted_coordinate"
            assert len(source) == 227 and rec["advertised_length"] == 228
            short = rec["geometry"]["source_short_group"]
            assert groups[33] == short["literal"] == "GAGA"
            assert sum(map(len, groups[:33])) == short["source_start_0based"] == 165
            assert [(i + 1, len(g)) for i, g in enumerate(groups[:-1]) if len(g) != 5] == [(34, 4)]
            completed = transpose(encode(rec["editorial_text"], key["square"]), key["column_rank_order"])
            for missing in range(228):
                witness = completed[:missing] + completed[missing + 1:]
                prices.append({"missing_transmitted_index": missing, "inserted_coordinate": completed[missing],
                               "known_coordinate_substitutions": sum(a != b for a, b in zip(source, witness))})
            minimum = min(p["known_coordinate_substitutions"] for p in prices)
            tied = [p["missing_transmitted_index"] for p in prices if p["known_coordinate_substitutions"] == minimum]
            assert minimum == 3 and tied == rec["geometry"]["all_equal_minimum_insertions"] == [168, 169, 170]
            assert [i for i in tied if i in short["source_local_insertion_indices"]] == [168, 169]
            variants = [edition(rec, key, i) for i in tied]
            assert len({v["complete_encoded_witness"] for v in variants}) == 1
            assert len({v["repaired_received_witness"] for v in variants}) == 1
            selected = next(v for v in variants if v["missing_transmitted_index"] == rec["geometry"]["representative_insertion_index"])
        records.append({"id": rec["id"], "key_id": key["id"], "source_slots": len(source),
                        "valid_received_coordinates": len(source), "advertised_length": rec["advertised_length"],
                        "unmodified_source_reading": unmodified,
                        "conditional_missing_coordinate": bool(variants), "selected_edition": selected,
                        "equivalent_insertions": variants, "retrospective_template_prices": prices})
    totals = {"source_records": len(records), "source_slots": sum(r["source_slots"] for r in records),
              "valid_received_coordinates": sum(r["valid_received_coordinates"] for r in records),
              "ordinary_frame_positions": sum(r["selected_edition"]["working_raw_reading"]["plaintext_positions"]
                                              for r in records if not r["conditional_missing_coordinate"]),
              "conditional_raw_fixed_positions": 113, "conditional_plaintext_positions": 114,
              "known_coordinate_substitutions": sum(r["selected_edition"]["cost"]["known_coordinate_substitutions"] for r in records),
              "source_erasure_fills": 0, "missing_transmitted_coordinates": 1,
              "equivalent_minimum_insertion_positions": 3, "source_local_minimum_positions": 2,
              "retrospective_template_positions_priced": 228, "published_square_changes": 0}
    assert totals == {"source_records": 3, "source_slots": 665, "valid_received_coordinates": 665,
                      "ordinary_frame_positions": 219, "conditional_raw_fixed_positions": 113,
                      "conditional_plaintext_positions": 114, "known_coordinate_substitutions": 6,
                      "source_erasure_fills": 0, "missing_transmitted_coordinates": 1,
                      "equivalent_minimum_insertion_positions": 3, "source_local_minimum_positions": 2,
                      "retrospective_template_positions_priced": 228, "published_square_changes": 0}
    return {"schema": "adfgvx-inventory-medical-return-certificate-v1",
            "prepared_by": inputs["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
            "totals": totals, "records": records,
            "limits": ["p104 C1 remains conditional on one missing transmitted coordinate. Three identical-A positions yield the same full witness; only two lie inside or at the visibly short group's boundary.",
                       "The insertion comparison uses a retrospective plaintext template; it is not an independently supplied crib or a proof of historical uniqueness.",
                       "OSMAN office labels, numerical references, DTSCHXSTAAT, MARSH and RETTERL/KETTERL remain literal.",
                       "The medical statement is a historical message reading, not independent evidence about an identified person's health."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = rebuild(json.loads((HERE / "inputs.json").read_text()), args.pdf)
    path = HERE / "certificates.json"
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified" if args.verify else "written": True, **result["totals"]}, indent=2))


if __name__ == "__main__":
    main()
