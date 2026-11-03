#!/usr/bin/env python3
"""Verify bounded parallel-witness comparisons without changing either edition.

Prepared by icekylinx and GPT-6 Astra Pro. The default is verification;
--write explicitly regenerates parallel_witnesses.json. Standard library only.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDINATES = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inverse(ciphertext, ranks, square):
    """Independent sorted-column inverse, retaining ciphertext origins."""
    width = len(ranks)
    assert len(set(ranks)) == width
    columns, origins, cursor = {}, {}, 0
    for column in sorted(range(width), key=lambda index: ranks[index]):
        height = (len(ciphertext) + width - 1 - column) // width
        columns[column] = ciphertext[cursor:cursor + height]
        origins[column] = list(range(cursor, cursor + height))
        cursor += height
    assert cursor == len(ciphertext) and len(ciphertext) % 2 == 0
    interim = "".join(columns[i % width][i // width] for i in range(len(ciphertext)))
    origin = [origins[i % width][i // width] for i in range(len(ciphertext))]
    unused = set(ALPHABET) - set(square)
    domains = []
    for first, second in zip(interim[::2], interim[1::2]):
        domain = set()
        for row, row_label in enumerate(COORDINATES):
            for column, column_label in enumerate(COORDINATES):
                if first in ("?", row_label) and second in ("?", column_label):
                    label = square[row * 6 + column]
                    domain.update(unused if label == "?" else label)
        assert domain
        domains.append("".join(sorted(domain)))
    return {
        "plaintext": "".join(value if len(value) == 1 else "?" for value in domains),
        "domains": domains,
        "interim": interim,
        "interim_source_indices": origin,
    }


def encode_template(plaintext, ranks, square):
    pairs = {
        label: COORDINATES[i // 6] + COORDINATES[i % 6]
        for i, label in enumerate(square) if label != "?"
    }
    interim = "".join("??" if label == "?" else pairs[label] for label in plaintext)
    return "".join(interim[column::len(ranks)]
                   for column in sorted(range(len(ranks)), key=lambda i: ranks[i]))


def differences(first, second):
    assert len(first) == len(second)
    return [{"position_0based": i, "first": a, "second": b}
            for i, (a, b) in enumerate(zip(first, second)) if a != b]


def text_comparison(first, second):
    """A diagnostic string alignment, not a historical or cipher proof."""
    left, right = first.replace("X", ""), second.replace("X", "")
    matcher = difflib.SequenceMatcher(None, left, right, autojunk=False)
    changes = []
    for operation, a, b, c, d in matcher.get_opcodes():
        if operation != "equal":
            changes.append({"operation": operation, "first_range_0based": [a, b],
                            "second_range_0based": [c, d],
                            "first": left[a:b], "second": right[c:d]})
    return {"first_literal_text": first, "second_literal_text": second,
            "comparison_form": "X removed for this textual comparison only; all other labels retained",
            "first_comparison_positions": len(left), "second_comparison_positions": len(right),
            "diagnostic_differences": changes,
            "limit": "SequenceMatcher diagnostics are not an optimal alignment certificate or a claim that the two transmissions are identical."}


def build():
    bound_files = {}

    def read(relative):
        data = (ROOT / relative).read_bytes()
        bound_files[relative] = {"sha256": digest(data), "size_bytes": len(data)}
        return json.loads(data)

    new_input_path = "experiments/nov8_radio_keys_and_reports/inputs.json"
    new_certificate_path = "experiments/nov8_radio_keys_and_reports/certificates.json"
    old_military_path = "experiments/p170_continuation/military_records.json"
    old_context_path = "experiments/p170_continuation/military_context.json"
    old_radio_input_path = "experiments/open_targets_continuation/inputs.json"
    old_radio_certificate_path = "experiments/open_targets_continuation/certificates.json"
    new = read(new_input_path)
    new_certificate = read(new_certificate_path)
    military = read(old_military_path)
    context = read(old_context_path)
    radio = read(old_radio_input_path)
    radio_certificate = read(old_radio_certificate_path)
    published = read("data/keys.json")
    assert new_certificate["inputs_sha256"] == bound_files[new_input_path]["sha256"]
    assert radio_certificate["source_input_sha256"] == bound_files[old_radio_input_path]["sha256"]
    keys = {key["id"]: key for key in published["keys"]}
    assert new["key"] == keys["Nov7-9"]
    images = []
    for base, specifications in [
        (HERE, new["source"]["images"]),
        (ROOT, military["crops"]),
        (ROOT / "experiments/open_targets_continuation",
         [image for image in radio["source_images"] if image["printed_page"] == 211]),
    ]:
        for image in specifications:
            path = base / image["path"]
            actual = digest(path.read_bytes())
            assert actual == image["sha256"]
            images.append({"path": path.relative_to(ROOT).as_posix(), "sha256": actual,
                           "printed_page": image["printed_page"]})

    new_records = {record["id"]: record for record in new["records"]}
    new_certificates = {record["id"]: record for record in new_certificate["records"]}
    old_records = {record["id"]: record for record in military["records"]}
    old_radio_inputs = {record["id"]: record for record in radio["messages"]}
    old_radio_certificates = {record["id"]: record for record in radio_certificate["results"]}
    first, second = new_records["p160_A2"], old_records["p170_B2"]
    key = new["key"]
    ranks, square = key["column_rank_order"], key["square"]
    assert second["column_rank_order"] == ranks and second["partial_square"] == square
    assert first["excluded_source_indices"] == [19, 26]
    source = "".join("".join(first["rows"]).split())
    assert source == first["literal_source"]
    analysis = "".join(c if c in COORDINATES else "?" for c in source)
    assert analysis == first["analysis_source"]
    new_origins = [i for i in range(len(source)) if i not in first["excluded_source_indices"]]
    first_frame = "".join(analysis[i] for i in new_origins)
    old_literal = "".join("".join(second["raw_source_rows"]).split())
    assert old_literal == second["raw_source_compact"]
    second_frame = "".join(c if c in COORDINATES else "?" for c in old_literal)
    assert second_frame == second["analysis_ciphertext"]
    assert len(first_frame) == len(second_frame) == 238
    first_raw = inverse(first_frame, ranks, square)
    second_raw = inverse(second_frame, ranks, square)
    assert first_raw["plaintext"] == first["expected_raw"]
    assert second_raw["plaintext"] == second["raw_geometry_plaintext"]
    aligned = []
    for i, (a, b) in enumerate(zip(first_frame, second_frame)):
        kind = "mask" if "?" in (a, b) else "agreement" if a == b else "disagreement"
        aligned.append({"frame_index_0based": i, "p160_source_index_0based": new_origins[i],
                        "p170_source_index_0based": i, "p160": a, "p170": b, "kind": kind})
    counts = {kind: sum(row["kind"] == kind for row in aligned)
              for kind in ("agreement", "disagreement", "mask")}
    assert counts == {"agreement": 230, "disagreement": 6, "mask": 2}
    assert [row["frame_index_0based"] for row in aligned if row["kind"] == "disagreement"] == [18, 46, 168, 185, 190, 191]
    assert [(row["frame_index_0based"], row["p160_source_index_0based"], row["p160"], row["p170"])
            for row in aligned if row["kind"] == "mask"] == [(25, 27, "X", "?"), (183, 185, "?", "D")]

    old_edited = next(edition["plaintext"] for edition in second["editions"]
                      if edition["id"] == "readable_same_length_emendation")
    current_witness = new_certificates["p160_A2"]["reencrypted_analysis_witness"]
    assert inverse(current_witness, ranks, square)["plaintext"] == first["editorial_text"]
    assert differences(first["editorial_text"], old_edited) == [
        {"position_0based": 67, "first": "E", "second": "D"},
        {"position_0based": 109, "first": "G", "second": "S"},
        {"position_0based": 113, "first": "E", "second": "T"},
    ]
    stencil = encode_template(old_edited, ranks, square)
    optional_witness = "".join(a if b == "?" else b for a, b in zip(current_witness, stencil))
    assert inverse(optional_witness, ranks, square)["plaintext"] == old_edited
    extra_changes = []
    for index, (before, after) in enumerate(zip(current_witness, optional_witness)):
        if before != after:
            assert analysis[new_origins[index]] != "?"
            extra_changes.append({"frame_index_0based": index,
                                  "p160_source_index_0based": new_origins[index],
                                  "p160_literal_coordinate": analysis[new_origins[index]],
                                  "main_edition_coordinate": before,
                                  "optional_coordinate": after})
    assert len(extra_changes) == 3
    optional_cost = {
        "known_coordinate_substitutions": sum(a != "?" and a != b for a, b in zip(first_frame, optional_witness)),
        "source_mask_fills": sum(a == "?" and b != "?" for a, b in zip(first_frame, optional_witness)),
        "excluded_observed_coordinates": 2, "excluded_source_masks": 0,
    }
    assert optional_cost == {"known_coordinate_substitutions": 7, "source_mask_fills": 1,
                             "excluded_observed_coordinates": 2, "excluded_source_masks": 0}
    compatibility = []
    missing_cells = [i for i, value in enumerate(square) if value == "?"]
    assert missing_cells == [26, 30]
    for labels in itertools.permutations("56"):
        completed = list(square)
        for cell, label in zip(missing_cells, labels):
            completed[cell] = label
        completed = "".join(completed)
        plaintext = inverse(optional_witness, ranks, completed)["plaintext"]
        assert "?" not in plaintext and encode_template(plaintext, ranks, completed) == optional_witness
        compatibility.append({"VF": labels[0], "XA": labels[1], "plaintext": plaintext})
    assert first_raw["interim"][128:130] == "VF"
    assert context["contextual_cell_assignments"] == {"VF": "6", "XA": "5"}

    p166_second = old_records["p166_A2"]["editions"][0]["plaintext"]
    p166_third = military["third_part_composite"]["editorial_emendation"]["plaintext"]
    p166_parallel = p166_second[p166_second.index("ALPENKORPS"):] + p166_third.split("XOXKXMX", 1)[0]
    old_radio_ids = ["p211_B_lower1", "p211_B_lower2", "p211_B_lower3"]
    for identity in old_radio_ids:
        record = old_radio_inputs[identity]
        certificate = old_radio_certificates[identity]
        old_key = keys[record["key_id"]]
        literal = "".join("".join(record["source_rows"]).split())
        cipher = "".join(c if c in COORDINATES else "?" for c in literal)
        assert literal == certificate["literal_ciphertext"] and cipher == certificate["analysis_ciphertext"]
        assert inverse(cipher, old_key["column_rank_order"], old_key["square"])["plaintext"] == record["expected_raw"]
        assert inverse(certificate["editorial"]["ciphertext"], old_key["column_rank_order"], old_key["square"])["plaintext"] == certificate["editorial"]["plaintext"]
    current_radio = "".join(new_records[identity]["editorial_text"] for identity in ("p160_C1", "p160_C2"))
    previous_radio = "".join(old_radio_certificates[identity]["editorial"]["plaintext"] for identity in old_radio_ids)
    semantic_fields = [
        ("First December date", "1XDEZEMBER", "ERSTERDEZEMBER"),
        ("First November key date", "ZEHNTERNOVEMBER", "ZEHNTERNOVEMBER"),
        ("Last December date", "21XDEZEMBER", "EINUNDZWANZIGSTERDEZEMBER"),
        ("Last November key date", "30XNOVEMBER", "DREISSIGSTERNOVEMBER"),
        ("Receipt request", "EMPFANGSBESTG", "EMPFANGSBESTAETIGUNG"),
        ("First reference", "NACHXCHEFX4XBX48929", "NACHRCHEFX4XB848727"),
        ("Final reference", "NACHCHEF4B498?9", "NACHRCHEFZ4XBX47857X"),
    ]
    fields = []
    for label, current, previous in semantic_fields:
        assert current in current_radio and previous in previous_radio
        fields.append({"field": label, "p160_literal": current, "p211_literal": previous,
                       "p160_joined_plaintext_start_0based": current_radio.index(current),
                       "p211_joined_plaintext_start_0based": previous_radio.index(previous)})

    return {
        "schema": "adfgvx-nov8-parallel-witness-comparison-v1",
        "authors": "icekylinx and GPT-6 Astra Pro",
        "scope": "Bounded comparisons of already declared source frames and edited candidates; no new source transcription, baseline-key assignment or replacement of either edition.",
        "source_files": bound_files,
        "source_images": images,
        "p160_A2_p170_B2": {
            "p160_header": first["header_literal"], "p170_header": second["source"]["header_transcription"],
            "key_id": key["id"], "square": square, "column_rank_order": ranks,
            "p160_frame": {"literal_slots": len(source), "excluded_observed_source_indices_0based": [19, 26],
                           "model_slots": len(first_frame), "sha256": digest(first_frame.encode())},
            "p170_frame": {"native_slots": len(second_frame), "sha256": digest(second_frame.encode())},
            "alignment_counts": counts,
            "disagreeing_coordinates": [row for row in aligned if row["kind"] == "disagreement"],
            "complementary_masks": [row for row in aligned if row["kind"] == "mask"],
            "mask_interpretation": [
                "The observed p160 source27 X supports p170 source25 X, selecting J at plaintext15 in UJVERBASZ, conditional on the p160 exclusion frame and the parallel relationship.",
                "The observed p170 source183 D supports p160 source185 D, selecting G at plaintext43 in BEREITGESTELLT under the same conditional alignment.",
            ],
            "p160_raw": first_raw["plaintext"], "p170_raw": second_raw["plaintext"],
            "raw_plaintext_differences": differences(first_raw["plaintext"], second_raw["plaintext"]),
            "p160_edited": first["editorial_text"], "p170_edited": old_edited,
            "edited_plaintext_differences": differences(first["editorial_text"], old_edited),
            "optional_copy_supported_interpretation": {
                "status": "Separate optional layer; main p160 RE and WERGCHEEZ remain unchanged.",
                "plaintext": old_edited, "ciphertext": optional_witness,
                "additional_observed_substitutions_beyond_main": extra_changes,
                "total_cost_against_p160_literal_source": optional_cost,
                "global_square_compatibility_witnesses": compatibility,
            },
            "same_key_context_reference": {
                "path": old_context_path, "p160_plaintext_index_0based": 64, "coordinate_cell": "VF",
                "baseline_domain": "56", "previous_contextual_preference": "6",
                "limit": "The earlier French operational-source identification is an optional historical layer. It is not applied here and does not independently establish this transmission's identity.",
            },
            "limits": [
                "The November8 and November9 headers differ; this is closely parallel traffic, not a certified identical transmission.",
                "The 230/6/2 alignment presupposes p160's declared two-coordinate exclusion model. No deletion geometry is inferred solely from this count.",
                "Six observed disagreements are retained; a parallel witness does not authorize overwriting its conflicting source coordinates.",
            ],
        },
        "p166_p167_related_context": {
            "source_record_ids": ["p166_A2", "p166_A3", "p167_A3"],
            "layer": "Previously edited p166 A2 plus previously source-supported and edited third-part composite, not untouched raw text.",
            "p166_second_part_edited": p166_second,
            "p166_p167_third_part_edited": p166_third,
            "body_comparison": text_comparison(first["editorial_text"], p166_parallel),
            "notable_differences": ["UJVERBASZ versus UMVERBASZXFRAGEZEICHEN", "RE versus RXD",
                                    "LINIE versus LINE", "WERGCHEEZ versus WERSCHETZ",
                                    "The p166/p167 version retains the separate O.K.M.1a No11319op footer."],
            "related_first_part": {"id": "p170_B1", "header": old_records["p170_B1"]["source"]["header_transcription"],
                                   "raw": old_records["p170_B1"]["raw_geometry_plaintext"],
                                   "limit": "Related earlier operational content, not identification of the physically missing p160 first part."},
        },
        "p160_C1_C2_p211_lower_B": {
            "p160_ids": ["p160_C1", "p160_C2"], "p160_key_id": "Nov7-9",
            "p160_headers": [new_records[identity]["header_literal"] for identity in ("p160_C1", "p160_C2")],
            "p160_frame_conditions": "C1 excludes observed source281 from309 slots; C2 is native144. Both use the declared edited layers.",
            "p211_ids": old_radio_ids, "p211_key_id": "Nov4-6",
            "p211_headers": [old_radio_inputs[identity]["header"] for identity in old_radio_ids],
            "p211_page_heading": old_radio_inputs[old_radio_ids[0]]["heading"],
            "p211_frame_conditions": "Three native frames214/184/134; first part has3 observed substitutions and third part1 invalid-glyph fill in the previously declared edited layer.",
            "body_comparison": text_comparison(current_radio, previous_radio),
            "literal_field_comparisons": fields,
            "limits": [
                "The keys, framing, dates, reference fields and some word forms differ. No cross-key coordinate alignment is performed.",
                "The same schedule is expressed partly with digits in p160 and with spelled ordinals in p211; the literal labels remain unchanged.",
                "The unequal footer references cannot supply p160's unresolved digit. Both5/6 baseline assignments remain possible.",
                "These are repeated key-use instructions, not evidence that all stations obeyed them and not recovery of a new secret key.",
            ],
        },
        "attribution": {
            "source_editions": "The existing p166/p167/p170 operational edition and p211 Ringbahn edition are by icekylinx and GPT-6 Astra Pro. Their already recorded body readings are prior context for the new physical witnesses.",
            "old_military_credit": military["prepared_by"],
            "old_radio_credit": radio["authors"],
            "published_key_provenance": {identity: keys[identity]["provenance"] for identity in ("Nov7-9", "Nov4-6")},
            "old_radio_prior_publication_statement": radio["prior_publication"],
            "new_contribution": "A second source-witness comparison, explicit disagreements, complementary masks and separately priced optional interpretation. No first historical decipherment or new period-key claim.",
            "counting": "The new p160/p161 physical records remain seven distinct additions; old p166/p167/p170/p211 records are not counted again.",
        },
        "navigation": ["cases/military/nov8_alpenkorps_report.md", "cases/military/nov9_operational_reports.md",
                       "cases/radio/ringbahn_key_reuse.md", "cases/radio/p211_key_schedule.md"],
        "provenance_limits": [
            "Repository input/certificate and crop bytes are hash-bound. This script does not render the external source PDF or redo the primary glyph audit.",
            "Cipher arithmetic is independently implemented here; prior source editions and declared editorial candidates remain its inputs.",
            "String-comparison differences have no statistical significance claim. Old editions, numeric uncertainties and repair costs remain unchanged.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--verify", action="store_true", help="Check the committed report (also the default).")
    mode.add_argument("--write", action="store_true", help="Explicitly regenerate only parallel_witnesses.json.")
    arguments = parser.parse_args()
    report = build()
    destination = HERE / "parallel_witnesses.json"
    if arguments.write:
        destination.write_text(json.dumps(report, indent=2) + "\n")
    else:
        assert report == json.loads(destination.read_text()), "Parallel-witness report differs from its bound inputs."
    print(json.dumps({"verified": not arguments.write,
                      "bound_source_files": len(report["source_files"]),
                      "bound_source_images": len(report["source_images"]),
                      "alignment_counts": report["p160_A2_p170_B2"]["alignment_counts"],
                      "additional_copy_interpretation_substitutions": 3,
                      "cross_key_coordinate_comparisons": 0,
                      "old_records_recounted": 0}, indent=2))


if __name__ == "__main__":
    main()
