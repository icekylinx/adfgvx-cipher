#!/usr/bin/env python3
"""Verify November 3 medical, radio and withdrawal source records.

Prepared by icekylinx and GPT-6 Astra Pro. The published key retains credit
to Lasry, Niebel, Kopal and Wacker. Default verification uses standard Python.
"""
import argparse
import hashlib
import json
from pathlib import Path
from functools import lru_cache
from itertools import combinations
from math import comb, fsum, isclose

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


def deletion_alignment(source, target):
    """Exact price and all minimizers for fixed target and arbitrary deletions."""
    missing = len(source) - len(target)
    assert missing >= 0

    @lru_cache(None)
    def best(j, removed):
        i = j + removed
        if j == len(target):
            assert len(source) - i == missing - removed
            return 0, 1
        choices = []
        if removed < missing:
            choices.append(best(j, removed + 1))
        cost, count = best(j + 1, removed)
        choices.append((cost + (source[i] != target[j]), count))
        minimum = min(c for c, n in choices)
        return minimum, sum(n for c, n in choices if c == minimum)

    optimum, count = best(0, 0)
    maps = []

    def walk(j, removed, positions):
        if j == len(target):
            maps.append(positions + list(range(j + removed, len(source))))
            return
        minimum, _ = best(j, removed)
        i = j + removed
        if removed < missing and best(j, removed + 1)[0] == minimum:
            walk(j, removed + 1, positions + [i])
        if best(j + 1, removed)[0] + (source[i] != target[j]) == minimum:
            walk(j + 1, removed, positions)

    walk(0, 0, [])
    assert len(maps) == count == len({tuple(m) for m in maps})
    return {'minimum_substitutions': optimum, 'minimum_layout_count': count,
            'minimum_deleted_source_indices': sorted(maps),
            'total_possible_layouts': comb(len(source), missing),
            'states': [{'target_index': j, 'deleted_count': removed,
                        'minimum_remaining_substitutions': best(j, removed)[0],
                        'optimal_suffix_paths': best(j, removed)[1]}
                       for j in range(len(target) + 1) for removed in range(missing + 1)]}


def frame_audit(inputs):
    rec = next(r for r in inputs['records'] if r['id'] == 'p117_C4')
    key = next(k for k in inputs['keys'] if k['id'] == rec['key_id'])
    source, candidate = rec['analysis_source'], rec['editorial_text']
    target = transpose(encode(candidate, key['square']), key['column_rank_order'])
    assert len(source) == 117 and len(target) == 112 and set(source) <= set(CO)
    one_block = []
    for start in range(113):
        frame = source[:start] + source[start + 5:]
        raw = reading(undo(frame, key['column_rank_order'])[0], key['square'])
        one_block.append({'start': start, 'excluded_coordinates': source[start:start + 5],
                          'raw_plaintext': raw['plaintext'],
                          'known_coordinate_substitutions_to_fixed_candidate':
                              sum(a != b for a, b in zip(frame, target))})
    minima = [r['start'] for r in one_block
              if r['known_coordinate_substitutions_to_fixed_candidate'] == 0]
    assert minima == list(range(16, 23))
    assert len({source[:i] + source[i + 5:] for i in minima}) == 1
    arbitrary = deletion_alignment(source, target)
    assert arbitrary['minimum_substitutions'] == 0
    assert arbitrary['minimum_layout_count'] == 14
    assert rec['excluded_source_indices'] in arbitrary['minimum_deleted_source_indices']
    controls = []
    for small_source, small_target in [('ADFGV', 'AFV'), ('AAAAA', 'AAA'),
                                       ('ADADAD', 'ADAD'), ('AGXVDF', 'AXVF'),
                                       ('ADXGVF', 'DDFF'), ('AAAA', 'XXXX')]:
        prices = []
        for removed in combinations(range(len(small_source)), len(small_source)-len(small_target)):
            frame = ''.join(c for j, c in enumerate(small_source) if j not in removed)
            prices.append((sum(a != b for a, b in zip(frame, small_target)), list(removed)))
        best_price = min(c for c, p in prices)
        expected = sorted(p for c, p in prices if c == best_price)
        exact = deletion_alignment(small_source, small_target)
        assert exact['minimum_substitutions'] == best_price
        assert exact['minimum_deleted_source_indices'] == expected
        controls.append({'source': small_source, 'target': small_target,
                         'bruteforce_layouts': len(prices), 'minimum': best_price,
                         'minimizers': expected})
    screen_ref = inputs['exploratory_screen']
    assert sha(HERE / screen_ref['path']) == screen_ref['sha256']
    screen = json.loads((HERE / screen_ref['path']).read_text())
    assert len(screen) == 230
    assert {(r['deleted_length'], r['start']) for r in screen} == {
        (width, start) for width in (1, 5) for start in range(118-width)}
    for row in screen:
        a, width = row['start'], row['deleted_length']
        frame = source[:a] + source[a+width:]
        assert row['removed'] == source[a:a+width]
        assert row['plaintext'] == reading(undo(frame, key['column_rank_order'])[0], key['square'])['plaintext']
    stream, origins = undo(source, key['column_rank_order'])
    return {'source_slots': 117, 'advertised_slots': 112,
            'literal_odd_frame_diagnostic': {
                **reading(stream[:-1], key['square']),
                'unpaired_coordinate': stream[-1], 'unpaired_source_index': origins[-1]},
            'single_five_slot_exclusion_prices': one_block,
            'single_block_zero_substitution_starts': minima,
            'complete_ciphertext_common_to_all_single_block_minima': target,
            'arbitrary_five_exclusion_exact_result': arbitrary,
            'independent_small_bruteforce_controls': controls,
            'exploratory_screen_candidates_reconstructed': len(screen),
            'limit': 'Minima are conditional on this selected plaintext and the stated exclusion families. Language ranking and exact forward fit do not prove a unique historical message or transmission error.'}


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
            if item.get('fresh_render_cache'):
                fitz.TOOLS.store_shrink(100)
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
        received = "".join(c if c in CO else "?" for c in literal)
        assert literal == rec["literal_source"] and received == rec["analysis_source"]
        excluded = rec.get("excluded_source_indices", [])
        assert excluded == sorted(set(excluded)) and all(0 <= i < len(received) for i in excluded)
        mapping = [i for i in range(len(received)) if i not in excluded]
        source = "".join(received[i] for i in mapping)
        assert len(source) == rec["advertised_length"]
        assert set(literal) <= set(CO + "-")
        assert rec["key_id"] == key["id"]
        stream, origins = undo(source, ranks)
        assert transpose(stream, ranks) == source
        raw = reading(stream, square)
        assert raw["plaintext"] == rec["expected_raw"]
        proposed = rec["editorial_text"]
        assert len(proposed) == len(raw["plaintext"])
        encoded = "".join(stream[2*i:2*i+2] if c == "?" else encode(c, square)
                          for i, c in enumerate(proposed))
        assert len(encoded) == len(stream)
        witness = transpose(encoded, ranks)
        places = locations(rec["rows"])
        substitutions, fills = [], []
        for working_index, (before, after) in enumerate(zip(source, witness)):
            if before == after:
                continue
            index = mapping[working_index]
            pair = origins.index(working_index) // 2
            item = {"source_index": index, "working_index": working_index, **places[index], "before": before,
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
            repaired[item["working_index"]] = item["after"]
        assert "".join(repaired) == witness
        edited = reading(undo(witness, ranks)[0], square)
        assert edited["plaintext"] == proposed
        # An arbitrary complete witness demonstrates consistency only. Values
        # chosen for still-unknown fields are never counted as recovered.
        complete = "".join(d[0] for d in edited["domains"])
        complete_cipher = transpose(encode(complete, square), ranks)
        assert all(a == "?" or a == b for a, b in zip(witness, complete_cipher))
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
                             "coordinate_origins": [mapping[p] for p in origins[2 * index:2 * index + 2]]})
        assert set(repairs) == {n["plaintext_index"] for n in numerals if n["explicit_spelling_repair"]}
        for field in rec["preserved_literal_fields"]:
            assert field in raw["plaintext"] and field in proposed
        records.append({"id": rec["id"], "key_id": key["id"], "source_slots": len(received), "analysis_frame_slots": len(source),
                        "valid_received_coordinates": len(received) - received.count("?"),
                        "excluded_source_indices": excluded,
                        "excluded_source_coordinates": "".join(received[p] for p in excluded),
                        "frame_to_source_indices": mapping,
                        "raw_reading": raw, "coordinate_origins": [[mapping[p] for p in origins[i:i + 2]]
                                                  for i in range(0, len(origins), 2)],
                        "editorial_plaintext": proposed, "editorial_domains": edited["domains"], "edited_fixed_positions": edited["fixed_positions"], "cost": cost,
                        "known_coordinate_substitutions": substitutions,
                        "source_erasure_fills": fills, "numeral_label_ledger": numerals,
                        "reencrypted_analysis_frame_witness": witness,
                        "arbitrary_complete_plaintext_witness": complete,
                        "arbitrary_complete_ciphertext_witness": complete_cipher,
                        "source_length_and_geometry_unchanged": not excluded})
    totals = {"source_records": len(records), "source_slots": sum(r["source_slots"] for r in records),
              "valid_received_coordinates": sum(r["valid_received_coordinates"] for r in records),
              "plaintext_positions": sum(r["raw_reading"]["plaintext_positions"] for r in records),
              "raw_fixed_positions": sum(r["raw_reading"]["fixed_positions"] for r in records),
              "known_coordinate_substitutions": sum(r["cost"]["known_coordinate_substitutions"] for r in records),
              "source_erasure_fills": sum(r["cost"]["source_erasure_fills"] for r in records),
              "excluded_observed_coordinates": sum(len(r["excluded_source_indices"]) for r in records),
              "inserted_coordinates": 0, "published_square_changes": 0,
              "analysis_frame_slots": sum(r["analysis_frame_slots"] for r in records)}
    totals["edited_fixed_positions"] = sum(r["edited_fixed_positions"] for r in records)
    assert totals == inputs["expected_totals"]
    return {"schema": "adfgvx-nov3-medical-radio-withdrawal-certificate-v1",
            "prepared_by": inputs["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
            "totals": totals, "records": records, "conditional_frame_audit": frame_audit(inputs),
            "limits": inputs["reading_policy"]}



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--book-model", type=Path,
                        help="Optionally recompute all230 archived language scores")
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    result = rebuild(inputs, args.pdf)
    maximum_score_error = None
    if args.book_model:
        from array import array
        import sys
        ref = inputs['exploratory_screen']
        assert sha(args.book_model) == ref['model_sha256']
        values = array('f')
        with args.book_model.open('rb') as source:
            values.fromfile(source, 37 ** 4)
            assert source.read() == b''
        if sys.byteorder != 'little':
            values.byteswap()
        indices = {c: i for i, c in enumerate(ref['model_alphabet'])}
        maximum_score_error = 0.0
        for row in json.loads((HERE / ref['path']).read_text()):
            text = row['plaintext']
            score = fsum(float(values[((indices[text[j]]*37 + indices[text[j+1]])*37
                                      + indices[text[j+2]])*37 + indices[text[j+3]]])
                         for j in range(len(text)-3)) / (len(text)-3)
            maximum_score_error = max(maximum_score_error, abs(score-row['score']))
            assert isclose(score, row['score'], rel_tol=0, abs_tol=1e-12)
    output = HERE / "certificates.json"
    if args.verify:
        assert json.loads(output.read_text()) == result
    else:
        output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified" if args.verify else "written": True,
                      **result["totals"],
                      "archived_model_scores_checked": 230 if args.book_model else 0,
                      "maximum_score_error": maximum_score_error}, indent=2))


if __name__ == "__main__":
    main()
