#!/usr/bin/env python3
"""Reconcile p171 C and p172 E using only their observed coordinate values.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Prior key: Lasry, Niebel, Kopal and Wacker. No new key assignments.
"""
from pathlib import Path
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.withdrawal_recovery.verify import reading, repair, sha
from experiments.operational_recovery.verify import global_witness


def check_pdf(path, inputs):
    import fitz
    assert sha(path) == inputs["source"]["pdf_sha256"]
    doc = fitz.open(path)
    for image in inputs["source_images"]:
        pix = doc[image["pdf_page_1based"] - 1].get_pixmap(
            matrix=fitz.Matrix(image["render_scale"], image["render_scale"]),
            clip=fitz.Rect(*image["crop_rectangle_pdf_points"]))
        saved = fitz.Pixmap(str(HERE / image["path"]))
        assert (pix.width, pix.height, pix.n, pix.samples) == (
            saved.width, saved.height, saved.n, saved.samples)


def finite_alignments(c, e, minimum):
    rows = []
    for offset in range(1 - len(e), len(c)):
        comparisons = [(c[j + offset], value) for j, value in enumerate(e)
                       if 0 <= j + offset < len(c) and c[j + offset] != "?" and value != "?"]
        if len(comparisons) < minimum:
            continue
        agree = sum(a == b for a, b in comparisons)
        rows.append({"e_start_relative_to_c": offset,
                     "jointly_observed_pairs": len(comparisons), "agree": agree,
                     "disagree": len(comparisons) - agree})
    best = max(Fraction(r["agree"], r["jointly_observed_pairs"]) for r in rows)
    leaders = [r for r in rows if Fraction(r["agree"], r["jointly_observed_pairs"]) == best]
    return rows, leaders


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    for image in inputs["source_images"]:
        assert sha(HERE / image["path"]) == image["sha256"]
    assert sha(HERE / "prior_candidates.json") == inputs["prior_credit"]["prior_candidates_sha256"]
    key = inputs["key"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    ranks, square = key["column_rank_order"], key["square"]
    assert ranks == published["column_rank_order"] and square == published["square"]
    records = []
    for rec in inputs["records"]:
        literal = "".join("".join(rec["source_rows"]).split())
        assert set(literal) <= set("ADFGVX-")
        assert len(literal) == rec["literal_source_slots"]
        prefix = rec["modeled_missing_leading_coordinates"]
        mapping = [None] * prefix + list(range(len(literal)))
        cipher = "?" * prefix + literal.replace("-", "?")
        assert len(cipher) == rec["modeled_total_coordinates"]
        raw = reading(cipher, ranks, square)
        assert raw["plaintext"] == rec["expected_raw_under_model"]
        edition = repair(cipher, "?" * prefix + literal,
                         {"text": rec["editorial_template"], "pair_overrides": []},
                         ranks, square, raw)
        for field in ["known_coordinate_substitutions", "erasure_fills"]:
            for change in edition[field]:
                index = change.pop("source_position_0based")
                change["working_coordinate_index"] = index
                change["source_coordinate_index"] = mapping[index]
                change["kind"] = "modeled_lost_prefix" if mapping[index] is None else "received_slot"
        raw["global_witness_not_original_reading"] = global_witness(cipher, ranks, square, raw)
        edition["reading"]["global_witness_not_original_reading"] = global_witness(
            edition["ciphertext"], ranks, square, edition["reading"])
        records.append({"id": rec["id"], "source_literal": literal,
                        "source_slots": len(literal), "analysis_frame": cipher,
                        "frame_to_source_indices": mapping, "raw": raw, "edition": edition})
    c, e = [r["analysis_frame"] for r in records]
    selected = records[0]["edition"]["ciphertext"]
    assert selected == records[1]["edition"]["ciphertext"]
    assert records[0]["edition"]["reading"]["plaintext"] == inputs["shared_editorial_plaintext"]
    assert records[1]["edition"]["reading"]["plaintext"] == inputs["shared_editorial_plaintext"]
    assert "INSP1IN" in inputs["shared_editorial_plaintext"]
    assert [r["raw"]["fixed_positions"] for r in records] == [122, 115]
    assert [len(r["edition"]["known_coordinate_substitutions"]) for r in records] == [6, 5]
    assert [len(r["edition"]["erasure_fills"]) for r in records] == [4, 10]
    assert selected[:10] == c[:10] == "DGAAVFADFD"
    assert all(a != "?" or b != "?" for a, b in zip(c, e))
    assert all(value in (c[i], e[i]) for i, value in enumerate(selected))
    conflicts = [i for i, (a, b) in enumerate(zip(c, e)) if a != "?" and b != "?" and a != b]
    assert len(conflicts) == 11
    positions = records[0]["raw"]["source_position_pairs_0based"]
    owner = {coord: index for index, pair in enumerate(positions) for coord in pair}
    conflict_rows = [{"c_source_index": i, "e_source_index": i - 10,
                      "c_observed": c[i], "e_observed": e[i], "selected": selected[i],
                      "selected_from": "p171_C" if selected[i] == c[i] else "p172_E",
                      "plaintext_position": owner[i]}
                     for i in conflicts]
    support_counts = Counter()
    pair_support = []
    for i, pair in enumerate(positions):
        supporters = [r["id"] for r in records
                      if all(r["analysis_frame"][p] == selected[p] for p in pair)]
        category = "+".join(supporters) if supporters else "coordinate_union_only"
        support_counts[category] += 1
        pair_support.append({"plaintext_position": i, "character": inputs["shared_editorial_plaintext"][i],
                             "coordinate_pair": "".join(selected[p] for p in pair),
                             "working_coordinate_indices": pair,
                             "whole_pair_observed_in": supporters,
                             "each_selected_coordinate_observed_in": [
                                 [r["id"] for r in records if r["analysis_frame"][p] == selected[p]]
                                 for p in pair]})
    assert dict(support_counts) == {"p171_C+p172_E": 102, "p171_C": 14,
                                   "p172_E": 9, "coordinate_union_only": 1}
    digest = hashlib.sha256()
    count, selected_bits = 0, None
    for bits in itertools.product((0, 1), repeat=len(conflicts)):
        candidate = list(selected)
        for index, choose_e in zip(conflicts, bits):
            candidate[index] = e[index] if choose_e else c[index]
        candidate = "".join(candidate)
        cost = sum(a != "?" and a != b for a, b in zip(c, candidate))
        cost += sum(a != "?" and a != b for a, b in zip(e, candidate))
        assert cost == len(conflicts)
        digest.update((candidate + "\n").encode())
        count += 1
        if candidate == selected:
            selected_bits = list(bits)
    assert count == 2048 and selected_bits is not None
    comparisons, leaders = finite_alignments(
        c, records[1]["source_literal"],
        inputs["alignment_model"]["minimum_known_coordinate_overlap_for_finite_alignment_comparison"])
    assert len(leaders) == 1 and leaders[0]["e_start_relative_to_c"] == 10
    assert leaders[0]["jointly_observed_pairs"] == 238 and leaders[0]["agree"] == 227
    return {"schema": "adfgvx-namur-order-witnesses-certificate-v1",
            "prepared_by": inputs["prepared_by"], "prior_credit": inputs["prior_credit"],
            "inputs_sha256": sha(HERE / "inputs.json"),
            "summary": {"physical_source_witnesses": 2, "distinct_shared_plaintext_bodies": 1,
                        "literal_source_slots": 494, "modeled_working_coordinates": 504,
                        "shared_plaintext_positions": 126, "summed_witness_plaintext_positions": 252,
                        "raw_fixed_positions_across_witnesses": 237,
                        "edition_fixed_positions_across_witnesses": 252,
                        "known_coordinate_substitutions": 11,
                        "printed_erasure_fills": 4,
                        "modeled_missing_prefix_coordinates": 10,
                        "modeled_missing_prefix_fills": 10,
                        "unwitnessed_coordinate_values_in_shared_reconstruction": 0,
                        "whole_plaintext_pairs_observed_in_at_least_one_witness": 125,
                        "coordinate_union_only_pairs": 1,
                        "source_deletions": 0, "source_reordering": 0, "key_changes": 0},
            "records": records, "shared_editorial_plaintext": inputs["shared_editorial_plaintext"],
            "shared_reconstructed_ciphertext": selected,
            "complete_observed_conflict_inventory": conflict_rows,
            "whole_pair_support_counts": dict(support_counts), "plaintext_pair_support": pair_support,
            "minimum_reconciliation": {"assumptions": inputs["alignment_model"],
                                       "observed_conflicts_lower_bound": 11,
                                       "selected_total_known_substitutions": 11,
                                       "minimum_known_substitution_common_streams": count,
                                       "enumerated_common_streams": count,
                                       "ordered_stream_digest_sha256": digest.hexdigest(),
                                       "selected_choice_bits": selected_bits,
                                       "limits": "The minimum is for reconciliation of these two aligned streams as one message. There are2048 minimum-cost common coordinate streams, not a unique plaintext. No original-length exclusion or statistical significance is claimed."},
            "finite_coordinate_alignment_comparison": {"minimum_jointly_known_overlap": 200,
                                                       "evaluated_offsets": len(comparisons),
                                                       "all_leaders": leaders,
                                                       "all_offsets": comparisons},
            "limits": [
                "The ten missing E prefix coordinates are inferred under the same-message alignment; E has an unread length header and does not explicitly print a ten-coordinate gap.",
                "All chosen coordinate values are witnessed, but choosing among eleven conflicts uses the proposed readable body. Minimal repair count does not prove uniquely historical wording.",
                "The anomalous INSP1IN and literal HPTVXX are preserved. No separator correction or key relabelling is introduced.",
                "The two receiving timestamps are retained even though their order does not establish an actual relay sequence.",
                "The source name WEIHER is supported by E's observed coordinate. Identification with a particular historical officer is not certified here.",
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    if args.pdf:
        check_pdf(args.pdf, json.loads((HERE / "inputs.json").read_text()))
    result = run()
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"],
                      "finite_alignment_offsets": result["finite_coordinate_alignment_comparison"]["evaluated_offsets"],
                      "minimum_common_streams": result["minimum_reconciliation"]["enumerated_common_streams"]}, indent=2))


if __name__ == "__main__":
    main()
