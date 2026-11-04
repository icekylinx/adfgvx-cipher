#!/usr/bin/env python3
"""Rebuild p84 C's conditional illness clause and every retained frame price.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import encrypt, decrypt, transposition_indices
from adfgvx.source_evidence import verify_source_evidence
from data.reviews.check_reading_presentation import displays, expected_legend

C = "ADFGVX"


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def order(length, ranks):
    """Assign a rectangular grid directly, then read ranked columns."""
    width = len(ranks)
    grid = [[None] * width for _ in range((length + width - 1) // width)]
    for index in range(length):
        grid[index // width][index % width] = index
    result = []
    for rank in range(1, width + 1):
        column = ranks.index(rank)
        result.extend(row[column] for row in grid if row[column] is not None)
    assert result == transposition_indices(length, ranks)
    return result


def analyze(wire, owners, key):
    permutation = order(len(wire), key["column_rank_order"])
    inverse = [0] * len(wire)
    for transmitted, interim in enumerate(permutation):
        inverse[interim] = transmitted
    positions = []
    for index in range(len(wire) // 2):
        model = inverse[2 * index:2 * index + 2]
        pair = "".join(wire[i] for i in model)
        cells = [cell for cell in range(36)
                 if (pair[0] == "?" or C[cell // 6] == pair[0])
                 and (pair[1] == "?" or C[cell % 6] == pair[1])]
        domain = "".join(sorted(key["square"][cell] for cell in cells))
        positions.append(dict(plaintext_index=index, pair=pair,
                              model_indices=model,
                              source_indices=[owners[i] for i in model],
                              domain=domain,
                              raw=domain if len(domain) == 1 else "?"))
    raw = "".join(position["raw"] for position in positions)
    assert raw == decrypt(wire, key["column_rank_order"], key["square"])
    return dict(raw=raw, fixed_positions=len(raw) - raw.count("?"),
                positions=positions)


def witness(wire, key, source, owners):
    full = wire.replace("?", "A")
    plaintext = decrypt(full, key["column_rank_order"], key["square"])
    assert encrypt(plaintext, key["column_rank_order"], key["square"]) == full
    retained = all(origin is None or source[origin] not in C
                   or full[index] == source[origin]
                   for index, origin in enumerate(owners))
    return dict(ciphertext=full, plaintext=plaintext, roundtrip_verified=True,
                all_observed_source_coordinates_retained=retained,
                unassigned_coordinate_choice="A only for a complete witness",
                historical_fill_claim=False)


def edit(template, wire, source, owners, key):
    raw = analyze(wire, owners, key)
    result = list(wire)
    changes, printed, inserted = [], [], []
    for position, letter in enumerate(template):
        if letter == "?":
            continue
        cell = key["square"].index(letter)
        wanted = C[cell // 6] + C[cell % 6]
        for model, value in zip(raw["positions"][position]["model_indices"], wanted):
            if wire[model] == value:
                continue
            origin = owners[model]
            row = dict(model_index=model, source_index=origin,
                       plaintext_index=position, before=wire[model], after=value,
                       literal_source_glyph=None if origin is None else source[origin])
            if wire[model] in C:
                changes.append(row)
            elif origin is None:
                inserted.append(row)
            else:
                assert source[origin] == "-"
                printed.append(row)
            result[model] = value
    edited = "".join(result)
    decoded = analyze(edited, owners, key)
    assert decoded["raw"] == template
    complete = witness(edited, key, source, owners)
    assert complete["all_observed_source_coordinates_retained"] == (not changes)
    return dict(template=template, ciphertext=edited, **decoded,
                observed_coordinate_substitutions=changes,
                printed_mask_fills=printed, inserted_slot_fills=inserted,
                full_global_witness=complete)


def build(pdf=None):
    data = load(HERE / "inputs.json")
    for path, digest in data["dependencies"].items():
        assert sha(ROOT / path) == digest, path
    record, key = data["record"], data["key"]
    assert key == next(row for row in load(ROOT / "data/keys.json")["keys"]
                       if row["id"] == "Oct28-31")
    audit = next(row for row in load(ROOT / "data/reviews/source_gap_audit_20261103.json")["records"]
                 if row["id"] == "p84_C")
    assert record["source_rows"] == audit["source_rows"]
    assert record["header_transcription"] == audit["header_transcription"]
    source = "".join("".join(record["source_rows"]).split())
    assert hashlib.sha256(source.encode()).hexdigest() == record["literal_sha256"] == audit["literal_sha256"]
    assert len(source) == 118 and source.count("-") == 7
    assert sum(c in C for c in source) == 111 and source[75:79] == "FDFG"
    evidence = verify_source_evidence(pdf, data["source"], data["source_images"], HERE)
    proposed = list(record["expected_raw"])
    for field in ("prior_word_fragment", "new_word_fragment"):
        fragment = record[field]
        proposed[fragment["start"]:fragment["start"] + len(fragment["word"])] = fragment["word"]
    assert "".join(proposed) == record["word_proposal"]
    alternative = record["equally_compatible_alternative"]
    alternative_text = list(record["word_proposal"])
    alternative_text[alternative["start"]:alternative["start"] + len(alternative["word"])] = alternative["word"]
    assert "".join(alternative_text) == alternative["template"]
    assert [i for i, (a, b) in enumerate(zip(record["word_proposal"], alternative["template"]))
            if a != b] == [69, 73]
    frames = []
    for at in record["frame"]["possible_insert_before_source_indices"]:
        owners = list(range(at)) + [None] + list(range(at, 118)) + [None] * 125
        assert len(owners) == 244
        assert [i for i in owners if i is not None] == list(range(118))
        wire = "".join(source[i] if i is not None and source[i] in C else "?" for i in owners)
        raw = analyze(wire, owners, key)
        assert raw["raw"] == record["expected_raw"] and raw["fixed_positions"] == 14
        primary = edit(record["word_proposal"], wire, source, owners, key)
        counterexample = edit(alternative["template"], wire, source, owners, key)
        span = raw["positions"][68:95]
        support = sum(sum(c in C for c in row["pair"]) for row in span)
        prices = dict(insert_before_source=at,
                      observed_substitutions=len(primary["observed_coordinate_substitutions"]),
                      printed_mask_fills=len(primary["printed_mask_fills"]),
                      inserted_slot_fills=len(primary["inserted_slot_fills"]),
                      new_span_support=support)
        assert prices == next(row for row in record["expected_frame_prices"]
                              if row["insert_before_source"] == at)
        assert primary["fixed_positions"] == counterexample["fixed_positions"] == 52
        assert all(len(primary[field]) == len(counterexample[field])
                   for field in ("observed_coordinate_substitutions", "printed_mask_fills", "inserted_slot_fills"))
        fully = [row["plaintext_index"] for row in span if "?" not in row["pair"]]
        half = [row["plaintext_index"] for row in span if row["pair"].count("?") == 1]
        absent = [row["plaintext_index"] for row in span if row["pair"] == "??"]
        assert fully == [74, 83, 92]
        if at in (78, 79):
            assert len(half) == 18 and absent == [71, 73, 80, 82, 89, 91]
        assert primary["full_global_witness"]["all_observed_source_coordinates_retained"] == (at in (77, 78, 79))
        frames.append(dict(id=f"short_group_{at}", insert_before_source=at,
                           ciphertext=wire, model_to_source_indices=owners,
                           **raw, full_roundtrip_witness=witness(wire, key, source, owners),
                           prices=prices, readable_candidate=primary,
                           equally_compatible_alternative=counterexample,
                           new_span_fully_observed_positions=fully,
                           new_span_half_observed_positions=half,
                           new_span_wholly_unobserved_positions=absent))
    representative = next(row for row in frames if row["insert_before_source"] == 78)
    text = (ROOT / data["case"]).read_text()
    assert text.count(expected_legend(ROOT / data["case"])) == 1
    fences, quotes = displays(text)
    assert all(row["role_from_caption"] is not None for row in fences + quotes)
    bodies = re.findall(r"```text\n(.*?)\n```", text, re.S)
    assert all(body in bodies for body in ("\n".join(record["source_rows"]), record["expected_raw"],
                                          record["word_proposal"], alternative["template"]))
    assert "> […] Deutsche Feldpost […] [Mutter schwer krank. Bitte komm.] […]" in text
    assert "> […] Deutsche Feldpost […] [Mittelschwer krank. Bitte komm.] […]" in text
    summary = dict(physical_sources=1, literal_source_slots=118,
                   observed_source_coordinates=111, printed_masks=7,
                   frame_slots=244, added_unknown_slots=126,
                   excluded_source_slots=0, retained_frames=5,
                   raw_fixed_positions=14, prior_edited_fixed_positions=28,
                   new_edited_fixed_positions=52, newly_proposed_positions=24,
                   unread_positions=70, representative_insert_before_source=78,
                   zero_observed_substitution_frames=[77, 78, 79],
                   minimum_fill_frames=[78, 79],
                   representative_observed_substitutions=0,
                   representative_printed_mask_fills=5,
                   representative_inserted_slot_fills=42,
                   new_span_observed_coordinates=24,
                   new_span_native_fixed_positions=[74, 83, 92],
                   new_span_half_supported_positions=18,
                   new_span_wholly_unobserved_positions=[71, 73, 80, 82, 89, 91],
                   alternative_differing_plaintext_positions=[69, 73],
                   independent_native_donor_claim=False,
                   historical_uniqueness_established=False)
    return dict(schema="adfgvx-p84-mother-illness-certificate-v1",
                authors=data["authors"], input_sha256=sha(HERE / "inputs.json"),
                search_provenance_sha256=sha(HERE / "search_provenance.json"),
                indexing="Zero based; ranges half open.", summary=summary,
                records=[dict(representative, id="p84_C")],
                alternative_frames=[row for row in frames if row["insert_before_source"] != 78],
                markdown_sha256=sha(ROOT / data["case"])) , evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result, evidence = build(args.pdf)
    path = HERE / "certificates.json"
    if args.verify:
        assert load(path) == result, "Certificate differs; inspect before regeneration"
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(dict(verified=True, **result["summary"], source_evidence=evidence), indent=2))


if __name__ == "__main__":
    main()
