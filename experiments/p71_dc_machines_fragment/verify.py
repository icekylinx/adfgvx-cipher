#!/usr/bin/env python3
"""Verify a conditional fragment, retaining every observed half-pair."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, untranspose
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect
from data.reviews.check_reading_presentation import displays as classify_displays, expected_legend

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
COORDINATES = "ADFGVX"


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def verify(pdf: Path | None) -> tuple[dict, dict]:
    data = json.loads((HERE / "inputs.json").read_text())
    source = data["record"]
    literal = "".join("".join(source["source_rows"]).split())
    assert literal == source["literal_source"]
    assert digest(literal.encode()) == source["literal_sha256"]
    assert len(literal) == source["source_slot_count"] == 85
    assert sum(c in COORDINATES for c in literal) == 85
    assert source["mask_source_indices"] == []
    assert source["advertised_coordinate_length"] == 192
    assert data["records"] == [{
        "id": source["id"], "source_rows": source["source_rows"],
        "source_slots": 85, "advertised_length": 192,
        "header": "; ".join(source["header_lines"]),
        "printed_page": 71, "pdf_page_1based": 74,
    }]
    assert source["annotations"] == [{
        "text": "(interference)", "source_boundary": 85,
        "placement": "Immediately after the final five-coordinate group.",
    }]
    key = data["key"]
    registered = json.loads((ROOT / "data/keys.json").read_text())["keys"]
    assert key == next(k for k in registered if k["id"] == "Oct4-6")
    assert len(set(key["square"])) == 36 and "?" not in key["square"]
    ranks, square = key["column_rank_order"], key["square"]
    frame = literal + "?" * 107
    mapping = list(range(85)) + [None] * 107
    common_raw = inspect(frame, key, mapping)
    assert data["frame"]["observed_source_indices"] == list(range(85))
    assert data["frame"]["added_unobserved_tail_indices"] == list(range(85, 192))
    assert data["frame"]["coordinate_length"] == len(frame) == 192
    middle = untranspose(frame, ranks)
    # Unique tags provide a source map without relying on a plaintext proposal.
    tags = untranspose("".join(chr(0x1000 + i) for i in range(192)), ranks)
    pair_maps = [
        [ord(c) - 0x1000 for c in tags[2 * i:2 * i + 2]] for i in range(96)
    ]
    assert sorted(i for pair in pair_maps for i in pair) == list(range(192))
    domains = []
    for i in range(96):
        pair = middle[2 * i:2 * i + 2]
        allowed = []
        for char in ALPHABET:
            cell = square.index(char)
            encoded = COORDINATES[cell // 6] + COORDINATES[cell % 6]
            if all(a == "?" or a == b for a, b in zip(pair, encoded)):
                allowed.append(char)
        domains.append("".join(allowed))
    raw = decrypt(frame, ranks, square)
    assert raw == "?" * 96
    assert common_raw["raw"] == raw and common_raw["fixed_positions"] == 0
    assert [set(p["domain"]) for p in common_raw["positions"]] == [set(d) for d in domains]
    observation_counts = [sum(i < 85 for i in pair) for pair in pair_maps]
    assert observation_counts.count(1) == 85
    assert observation_counts.count(0) == 11
    assert observation_counts.count(2) == 0
    context = data["context"]
    first = json.loads((ROOT / context["package"]).read_text())["records"]
    first = next(r for r in first if r["id"] == context["record_id"])
    packed = json.dumps(first, sort_keys=True, separators=(",", ":")).encode()
    assert digest(packed) == context["record_sha256"]
    assert context["editorial_template"] == first["editorial_template"]
    assert context["editorial_note"] == first["editorial_note"]

    candidates = []
    for candidate in data["candidates"]:
        prefix = candidate["prefix"]
        assert len(prefix) == 47
        assignments = {}
        observed_support, unobserved_fills = [], []
        for i, char in enumerate(prefix):
            assert char in domains[i]
            cell = square.index(char)
            encoded = COORDINATES[cell // 6] + COORDINATES[cell % 6]
            for half, (index, value) in enumerate(zip(pair_maps[i], encoded)):
                assert index not in assignments
                assignments[index] = value
                record = {"plaintext_index": i, "pair_half": half,
                          "frame_index": index, "coordinate": value}
                if index < 85:
                    assert literal[index] == value
                    observed_support.append(record)
                else:
                    unobserved_fills.append(record)
        assert len(assignments) == 94
        assert len(observed_support) == 43
        assert len(unobserved_fills) == 51
        wholly_unobserved = [i for i in range(47) if observation_counts[i] == 0]
        assert wholly_unobserved == [8, 19, 30, 41]
        partial_frame = "".join(assignments.get(i, "?") for i in range(192))
        assert decrypt(partial_frame, ranks, square) == prefix + "?" * 49
        for i, observed in enumerate(literal):
            assert partial_frame[i] in ("?", observed)
        filled_frame = "".join(assignments.get(i, value) for i, value in enumerate(frame))
        assert filled_frame[:85] == literal
        assert decrypt(filled_frame, ranks, square) == prefix + "?" * 49
        unresolved_added = [i for i in range(85, 192) if i not in assignments]
        assert len(unresolved_added) == 56
        common_edited = inspect(filled_frame, key, mapping)
        assert common_edited["raw"] == prefix + "?" * 49
        assert common_edited["fixed_positions"] == 47
        full_witness = filled_frame.replace("?", "A")
        full_plaintext = decrypt(full_witness, ranks, square)
        assert full_witness[:85] == literal
        assert encrypt(full_plaintext, ranks, square) == full_witness
        assert full_plaintext[:47] == prefix
        added_events = [{"model_index": event["frame_index"], "source_index": None,
                         "printed": None, "from": "?", "to": event["coordinate"]}
                        for event in unobserved_fills]
        layer = {
            "template": prefix + "?" * 49, "ciphertext": filled_frame, **common_edited,
            "known_coordinate_substitutions": [], "printed_mask_fills": [],
            "inserted_slot_fills": added_events,
            "full_global_witness": {"square": square, "ciphertext": full_witness,
                                    "plaintext": full_plaintext, "roundtrip_verified": True,
                                    "all_observed_source_coordinates_retained": True,
                                    "historical_fill_claim": False},
        }
        candidates.append({
            "id": candidate["id"], "prefix": prefix,
            "display_stream": prefix + "?" * 49,
            "proposed_plaintext_positions": 47,
            "unread_plaintext_positions": 49,
            "observed_coordinate_substitutions": 0,
            "source_mask_fills": 0,
            "inserted_slot_fills": 51,
            "native_complete_pairs_in_prefix": 0,
            "single_observation_positions_in_prefix": 43,
            "wholly_unobserved_positions_in_prefix": wholly_unobserved,
            "observed_support": observed_support,
            "unobserved_slot_fills": unobserved_fills,
            "remaining_unassigned_added_slots": unresolved_added,
            "remaining_observed_coordinates_outside_prefix": 42,
            "partial_reencryption_witness": partial_frame,
            "observed_source_plus_conditional_fills": filled_frame,
            "edited_layer": layer,
        })
    assert [c["id"] for c in candidates] == ["series_connection", "retention_alternative"]
    different_positions = [i for i, (a, b) in enumerate(zip(
        candidates[0]["prefix"], candidates[1]["prefix"])) if a != b]
    assert different_positions == [38, 39]
    displays = data["display_blocks"]
    assert displays == {"source": "\n".join(source["source_rows"]), "raw": raw,
                        "conditional": candidates[0]["display_stream"],
                        "alternative": candidates[1]["display_stream"]}
    markdown = (ROOT / data["case"]).read_text()
    assert markdown.count(expected_legend(ROOT / data["case"])) == 1
    classified_fences, classified_quotes = classify_displays(markdown)
    assert [r["role_from_caption"] for r in classified_fences] == [
        "source_transcription", "raw_output", "edited_output", "edited_output"]
    assert [r["role_from_caption"] for r in classified_quotes] == ["readable_german"]
    fences = re.findall(r"```text\n(.*?)\n```", markdown, flags=re.S)
    assert fences == [displays[k] for k in ("source", "raw", "conditional", "alternative")]
    assert len(re.findall(r"^```", markdown, flags=re.M)) == 8
    quotes = re.findall(r"^> (.*)$", markdown, flags=re.M)
    assert quotes == [data["candidates"][0]["readable_german"]]
    fold = lambda text: re.sub("[^A-Z0-9]", "", text.upper()).replace("X", "")
    assert fold(quotes[0]) == fold(candidates[0]["prefix"])
    for required in ("0/96 plaintext positions", "51 fills of added unobserved-tail slots",
                     "8, 19, 30 and 41", "remaining 56 added coordinate slots",
                     "equally compatible", "conditional lexical reading"):
        assert required in markdown, required
    evidence = verify_source_evidence(pdf, data["source"], data["source_images"], HERE)
    summary = {"physical_records": 1, "printed_source_slots": 85,
               "valid_source_coordinates": 85, "printed_masks": 0,
               "added_unknown_slots": 107, "modeled_coordinates": 192,
               "plaintext_positions": 96, "raw_fixed_positions": 0,
               "conditional_proposed_positions": 47, "unread_positions": 49,
               "observed_coordinate_substitutions": 0,
               "source_mask_fills": 0, "added_slot_fills": 51}
    return {
        "schema": "adfgvx-p71-dc-machines-fragment-certificate-v1",
        "authors": data["authors"], "input_sha256": digest((HERE / "inputs.json").read_bytes()),
        "indexing": data["indexing"], "summary": summary,
        "records": [{"id": source["id"], "literal_source": literal, "source_slots": 85,
                     "ciphertext": frame, "model_to_source_indices": mapping,
                     "excluded_source_indices": [], **common_raw,
                     "readable_candidate": candidates[0]["edited_layer"],
                     "equally_compatible_alternative": candidates[1]["edited_layer"]}],
        "source_slots": 85, "observed_coordinates": 85, "source_masks": 0,
        "frame_slots": 192, "added_unobserved_tail_slots": 107,
        "plaintext_positions": 96, "raw_fixed_positions": 0,
        "one_observation_positions": 85, "wholly_unobserved_positions": 11,
        "raw_stream": raw, "plaintext_domains": domains,
        "plaintext_pair_to_frame_indices": pair_maps,
        "candidates": candidates,
        "alternative_differing_plaintext_positions": different_positions,
        "markdown_checked_text_fences": 4,
        "markdown_checked_readable_quotations": 1,
        "historical_uniqueness_established": False,
    }, evidence


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--write", action="store_true", help="Freeze the recomputed certificate.")
    parser.add_argument("--verify", action="store_true", help="Verify the frozen certificate (the default).")
    args = parser.parse_args()
    assert not (args.write and args.verify), "Choose --write or --verify"
    certificate, evidence = verify(args.pdf)
    path = HERE / "certificates.json"
    if args.write:
        path.write_text(json.dumps(certificate, indent=2) + "\n")
    else:
        assert certificate == json.loads(path.read_text()), "Certificate differs"
    print(json.dumps({"verified": not args.write, **certificate["summary"],
                      "source_evidence": evidence["summary"]}, indent=2))


if __name__ == "__main__":
    main()
