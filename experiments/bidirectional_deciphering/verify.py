#!/usr/bin/env python3
"""Verify p138 B's conditional source edition and a finite p132 B comparison.

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


def source_variant(rec, key, variant):
    source = rec["analysis_source"]
    square, ranks = key["square"], key["column_rank_order"]
    extra = variant["extra_transmitted_index"]
    assert source[extra] == variant["extra_coordinate"]
    working = source[:extra] + source[extra + 1:]
    source_map = [i for i in range(len(source)) if i != extra]
    stream, working_origins = undo(working, ranks)
    origins = [source_map[i] for i in working_origins]
    raw = reading(stream, square)
    assert raw["plaintext"] == variant["expected_raw"]
    assert raw["unpaired_coordinate"] is None and raw["fixed_positions"] == 51
    proposed = variant["editorial_text"]
    transmitted = transpose(encode(proposed, square), ranks)
    assert len(transmitted) == len(working) == 104
    witness = transmitted[:extra] + source[extra] + transmitted[extra:]
    places = locations(rec["rows"])
    edits, fills = [], []
    for i, (before, after) in enumerate(zip(source, witness)):
        if before == after:
            continue
        assert i != extra
        index = origins.index(i) // 2
        change = {"source_index": i, **places[i], "before": before, "after": after,
                  "diplomatic_source_glyph": rec["literal_source"][i],
                  "plaintext_index": index, "raw_plaintext_symbol": raw["plaintext"][index],
                  "proposed_plaintext_symbol": proposed[index]}
        (fills if before == "?" else edits).append(change)
    assert sorted([[c["source_index"], c["before"], c["after"]] for c in edits + fills]) == rec["expected_source_changes"]
    cost = {"known_coordinate_substitutions": len(edits), "source_erasure_fills": len(fills),
            "extraneous_transmitted_coordinates": 1}
    assert cost == rec["expected_cost"]
    repaired = list(source)
    for c in edits + fills:
        repaired[c["source_index"]] = c["after"]
    assert "".join(repaired) == witness and len(witness) == 105
    assert witness[extra] == source[extra]
    decoded = undo(witness[:extra] + witness[extra + 1:], ranks)[0]
    assert reading(decoded, square)["plaintext"] == proposed
    return {"id": variant["id"], "status": variant["status"],
            "extra_transmitted_coordinate": {"source_index": extra, "coordinate": source[extra],
                                              **places[extra], "retained_in_full_source_witness": True},
            "working_source_slots": 104, "working_raw_reading": raw,
            "coordinate_origins": [origins[i:i + 2] for i in range(0, len(origins), 2)],
            "editorial_plaintext": proposed, "cost": cost,
            "known_coordinate_substitutions": edits, "source_erasure_fills": fills,
            "reencrypted_full_source_witness": witness}


def p132_comparison(inputs):
    meta = inputs["companion"]
    source_file, cert_file = HERE / meta["frozen_inputs_path"], HERE / meta["frozen_certificates_path"]
    assert sha(source_file) == meta["frozen_inputs_sha256"]
    assert sha(cert_file) == meta["frozen_certificates_sha256"]
    frozen = json.loads(source_file.read_text())
    rec = next(r for r in frozen["records"] if r["id"] == "p132_B")
    key = next(k for k in frozen["keys"] if k["id"] == rec["key_id"])
    assert key == inputs["key"]
    square, ranks, source = key["square"], key["column_rank_order"], rec["analysis_source"]
    stream, origins = undo(source, ranks)
    assert len(stream) == 155
    front, back = reading(stream, square), reading(stream[1:], square)
    encoded = encode(rec["editorial_text"], square)
    assert len(encoded) == 154
    rows = []
    for leading in range(78):
        gap = 2 * leading
        joined = front["domains"][:leading] + back["domains"][leading:]
        direct = reading(stream[:gap] + stream[gap + 1:], square)
        assert joined == direct["domains"]
        complete = encoded[:gap] + stream[gap] + encoded[gap:]
        witness = transpose(complete, ranks)
        substitutions = sum(a != "?" and a != b for a, b in zip(source, witness))
        paired_fills = sum(a == "?" and b != "?" for a, b in zip(source, witness))
        rows.append({"leading_forward_labels": leading, "trailing_backward_labels": 77 - leading,
                     "unpaired_interim_index": gap, "unpaired_source_index": origins[gap],
                     "unpaired_received_coordinate": stream[gap],
                     "raw_plaintext": direct["plaintext"],
                     "known_coordinate_substitutions_for_prior_template": substitutions,
                     "source_erasure_fills_for_paired_labels": paired_fills,
                     "unpaired_source_erasure": stream[gap] == "?"})
    minimum = min(r["known_coordinate_substitutions_for_prior_template"] for r in rows)
    best = [r for r in rows if r["known_coordinate_substitutions_for_prior_template"] == minimum]
    assert minimum == 3 and [r["leading_forward_labels"] for r in best] == [27, 28]
    assert all(r["raw_plaintext"] == rec["expected_working_raw"] for r in best)
    balanced = [r for r in rows if r["leading_forward_labels"] in [38, 39]]
    assert [r["known_coordinate_substitutions_for_prior_template"] for r in balanced] == [20, 22]
    old = json.loads(cert_file.read_text())
    prior = next(r for r in old["records"] if r["id"] == "p132_B")
    assert [v["removal_index"] for v in prior["equivalent_removal_variants"]] == [54, 55, 56, 57]
    return {"source_record": "p132_B", "comparison_count": len(rows),
            "forward_plaintext": front["plaintext"], "backward_phase_plaintext": back["plaintext"],
            "prior_editorial_template": rec["editorial_text"], "rows": rows,
            "minimum_known_coordinate_substitutions": minimum,
            "best_forward_label_counts": [27, 28], "balanced_splits": balanced,
            "prior_extra_V_positions_retained": [54, 55, 56, 57],
            "interpretation": "Flexible opposite-end pairing is algebraically the prior one-unpaired-interim-coordinate model. Literal balanced halves do not reproduce its low-cost reading. No reduction in the prior repair cost or geometry assumptions is established."}


def rebuild(inputs, pdf=None):
    key, rec = inputs["key"], inputs["record"]
    assert len(key["square"]) == len(set(key["square"])) == 36
    assert sorted(key["column_rank_order"]) == list(range(1, 18))
    document = None
    if pdf:
        import fitz
        assert sha(pdf) == inputs["source"]["pdf_sha256"]
        document = fitz.open(pdf)
    for image in inputs["source"]["images"]:
        assert sha(HERE / image["path"]) == image["sha256"]
        if document is not None:
            pix = document[image["pdf_page_1based"] - 1].get_pixmap(
                matrix=fitz.Matrix(image["scale"], image["scale"]),
                clip=fitz.Rect(*image["clip_points"]))
            assert (pix.width, pix.height) == (image["width"], image["height"])
            assert hashlib.sha256(pix.samples).hexdigest() == image["pixel_sha256"]
    groups = " ".join(rec["rows"]).split()
    assert len(groups) == 21 and all(len(g) == 5 for g in groups)
    literal = "".join(groups)
    assert literal == rec["literal_source"]
    source = "".join(c if c in CO else "?" for c in literal)
    assert source == rec["analysis_source"] and len(source) == rec["advertised_length"] == 105
    assert literal[8] == "R" and source.count("?") == 1
    unmodified, origins = undo(source, key["column_rank_order"])
    raw = reading(unmodified, key["square"])
    assert raw["plaintext"] == rec["expected_105_slot_raw"]
    assert rec["raw_unpaired_coordinate"] == {"interim_index": 104, "source_index": origins[-1],
                                              "coordinate": unmodified[-1]}
    variants = [source_variant(rec, key, v) for v in rec["variants"]]
    assert len({v["reencrypted_full_source_witness"] for v in variants}) == 1
    assert len({v["editorial_plaintext"][:-3] for v in variants}) == 1
    preferred = variants[0]["editorial_plaintext"]
    encrypted = transpose(encode(preferred, key["square"]), key["column_rank_order"])
    prices = []
    for extra in range(105):
        witness = encrypted[:extra] + source[extra] + encrypted[extra:]
        prices.append({"extra_transmitted_index": extra,
                       "known_coordinate_substitutions_for_NKJ_template": sum(a != "?" and a != b
                                                                               for a, b in zip(source, witness)),
                       "paired_source_erasure_fills": sum(a == "?" and b != "?" for a, b in zip(source, witness))})
    minimum = min(p["known_coordinate_substitutions_for_NKJ_template"] for p in prices)
    assert minimum == 2
    assert [p["extra_transmitted_index"] for p in prices
            if p["known_coordinate_substitutions_for_NKJ_template"] == minimum] == [104]
    return {"schema": "adfgvx-bidirectional-deciphering-certificate-v1",
            "prepared_by": inputs["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
            "source_record": "p138_B", "source_slots": 105, "valid_received_coordinates": 104,
            "unmodified_105_slot_reading": raw, "conditional_working_slots": 104,
            "conditional_raw_fixed_positions": 51, "conditional_plaintext_positions": 52,
            "equally_priced_variants": variants, "shared_instructional_body": preferred[:-3],
            "known_coordinate_substitutions_per_variant": 2, "source_erasure_fills_per_variant": 1,
            "extraneous_transmitted_coordinates_per_variant": 1,
            "fixed_NKJ_template_prices": prices,
            "p132_finite_comparison": p132_comparison(inputs),
            "limits": ["Both full variants reconstruct one identical repaired 105-slot source witness. The external NKJ 472 footer favors the NKJ ending but does not establish unique historical geometry.",
                       "Uniqueness at 104 is only for the retrospective fixed NKJ-ending template; the NMJ variant has the same total cost under its own text.",
                       "The p132 comparison is a specific interpretation of opposite-end pairing. The source instruction does not identify a mathematical implementation or an exactly balanced split."]}


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
    print(json.dumps({"verified" if args.verify else "written": True, "source_records": 1,
                      "source_slots": 105, "equally_priced_variants": 2,
                      "substitutions_per_variant": 2, "source_erasure_fills_per_variant": 1,
                      "extraneous_transmitted_coordinates_per_variant": 1,
                      "p132_split_comparisons": 78, "p132_best_splits": [27, 28],
                      "p132_balanced_split_substitutions": [20, 22]}, indent=2))


if __name__ == "__main__":
    main()
