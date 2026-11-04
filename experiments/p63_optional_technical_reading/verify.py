#!/usr/bin/env python3
"""Replay p63 A's optional technical word under a surplus-DD interim model.

Prepared by icekylinx and GPT-6 Astra Pro. The published Oct4-6 key and
existing partial edition retain all earlier attribution and evidence.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from experiments.november_radio_service.verify import encode, inverse, reading, transpose
from data.reviews.check_reading_presentation import displays, expected_legend

CO = "ADFGVX"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def difference(source, witness, positions):
    reverse = {origin: i for i, pair in enumerate(positions)
               for origin in pair}
    observed, fills = [], []
    for i, (a, b) in enumerate(zip(source, witness)):
        if a == b:
            continue
        event = {"source_index": i, "before": a, "after": b,
                 "printed_group_1based": i // 5 + 1,
                 "group_position_1based": i % 5 + 1,
                 "native_plaintext_index": reverse[i]}
        (observed if a in CO else fills).append(event)
    return observed, fills


def all_pair_removals(interim, target):
    costs, minimum, ties, histogram = [], None, [], Counter()
    for a in range(len(interim) - 1):
        row = []
        for b in range(a + 1, len(interim)):
            stream = interim[:a] + interim[a + 1:b] + interim[b + 1:]
            cost = sum(x != "?" and x != y for x, y in zip(stream, target))
            row.append(cost)
            histogram[cost] += 1
            if minimum is None or cost < minimum:
                minimum, ties = cost, []
            if cost == minimum:
                ties.append([a, b])
        costs.append(row)
    adjacent = [row[0] for row in costs]
    amin = min(adjacent)
    return {"scope": "All unordered pairs of original intermediate indices, compared with one fixed retrospective 134-character target.",
            "trials": sum(histogram.values()),
            "cost_grid_definition": "Row a, entry j is the observed-coordinate cost of removing original interim indices a and a+1+j.",
            "observed_substitution_cost_grid": costs,
            "cost_histogram": {str(k): histogram[k] for k in sorted(histogram)},
            "minimum_observed_substitutions": minimum,
            "all_minimum_pairs": ties,
            "adjacent_pair_family": {"trials": len(adjacent),
                                     "costs_by_first_interim_index": adjacent,
                                     "minimum_observed_substitutions": amin,
                                     "all_minimum_first_indices": [i for i, n in enumerate(adjacent) if n == amin]},
            "retrospective_target_not_independent_evidence": True}


def normalized_readable(text):
    for before, after in [("Ä", "AE"), ("Ö", "OE"), ("Ü", "UE"), ("ß", "SS")]:
        text = text.replace(before, after).replace(before.lower(), after)
    return re.sub(r"[^A-Z0-9]", "", text.upper()).replace("X", "")


def rebuild(inp, pdf=None):
    live = json.loads((ROOT / inp["live_input_path"]).read_text())
    rec = next(r for r in live["records"] if r["id"] == "p63_A")
    key = live["key"]
    assert rec == inp["record_snapshot"] and key == inp["key_snapshot"]
    literal = "".join("".join(rec["rows"]).split())
    assert literal == rec["literal_source"] and len(literal) == 270
    assert len(literal) - sum(c in CO for c in literal) == 2
    source = "".join(c if c in CO else "?" for c in literal)
    assert source == rec["analysis_source"]
    interim, origins = inverse(source, key["column_rank_order"])
    assert transpose(interim, key["column_rank_order"]) == source
    native = reading(interim, origins, key["square"])
    assert native["plaintext"] == rec["literal_frame_raw"]
    assert native["plaintext_positions"] == 135 and native["fixed_positions"] == 133
    assert native["unpaired_coordinate"] is None
    prop = inp["proposal"]
    removed = prop["surplus_interim_indices"]
    assert removed == [86, 87]
    assert "".join(interim[i] for i in removed) == prop["surplus_interim_values"] == "DD"
    assert [origins[i] for i in removed] == prop["surplus_source_origins"] == [261, 16]
    assert native["plaintext"][43] == "W"
    keep = [i for i in range(270) if i not in removed]
    paired = "".join(interim[i] for i in keep)
    paired_origins = [origins[i] for i in keep]
    conditional = reading(paired, paired_origins, key["square"])
    assert conditional["plaintext"] == prop["conditional_raw"]
    assert conditional["plaintext_positions"] == 134 and conditional["fixed_positions"] == 132
    assert conditional["plaintext"] == native["plaintext"][:43] + native["plaintext"][44:]
    target = prop["editorial_text"]
    assert len(target) == 134 and "?" not in target
    begin, end = prop["technical_plaintext_span"]
    assert target[begin:end] == prop["technical_target"] == "MASCHINENTECHNISCHEN"
    goal = encode(target, key["square"])
    rebuilt_interim = goal[:86] + "DD" + goal[86:]
    witness = transpose(rebuilt_interim, key["column_rank_order"])
    assert len(witness) == 270
    assert all(witness[i] == source[i] == "D" for i in prop["surplus_source_origins"])
    back, back_origins = inverse(witness, key["column_rank_order"])
    assert back == rebuilt_interim and back_origins == origins
    assert reading(back[:86] + back[88:], paired_origins, key["square"])["plaintext"] == target
    edits, fills = difference(literal, witness, native["coordinate_origins"])
    assert len(edits) == prop["expected_total_observed_substitutions"] == 15
    assert len(fills) == prop["expected_total_source_mask_fills"] == 2
    assert prop["expected_surplus_interim_coordinates"] == 2
    assert prop["native_transmitted_source_exclusions"] == 0

    # Preserve the old primary template; its 21 unknowns are not silently accepted.
    primary_template = rec["editorial_template"]
    assert primary_template[37:58] == "?" * 21
    assert len(primary_template) == 135 and primary_template.count("?") == 21
    primary_stencil = []
    for c in primary_template:
        primary_stencil.extend("??" if c == "?" else encode(c, key["square"]))
    unchanged_word_interim = "".join(a if b == "?" else b for a, b in zip(interim, primary_stencil))
    primary_witness = transpose(unchanged_word_interim, key["column_rank_order"])
    previous_edits, previous_fills = difference(literal, primary_witness, native["coordinate_origins"])
    assert len(previous_edits) == 12 and len(previous_fills) == 2
    assert fills == previous_fills
    old_set = {(e["source_index"], e["before"], e["after"]) for e in previous_edits}
    new_set = {(e["source_index"], e["before"], e["after"]) for e in edits}
    assert old_set <= new_set
    additions = sorted(new_set - old_set)
    assert [list(x) for x in additions] == prop["expected_additional_observed_changes"]
    assert len(additions) == 3
    numeral_ledger = []
    for i, c in enumerate(native["plaintext"]):
        if not c.isdigit():
            continue
        assert i != 43
        j = i - (i > 43)
        changed = target[j] != c
        pair = native["coordinate_origins"][i]
        numeral_ledger.append({"native_plaintext_index": i,
                               "conditional_plaintext_index": j,
                               "raw_label": c, "optional_label": target[j],
                               "source_indices": pair,
                               "explicit_word_repair": changed,
                               "new_in_technical_proposal": i == 51})
        if not changed:
            assert all(literal[p] == witness[p] for p in pair)
    assert next(x for x in numeral_ledger if x["new_in_technical_proposal"])["optional_label"] == "N"
    assert "474D" in native["plaintext"] and "474D" in target
    grid = all_pair_removals(interim, goal)
    assert grid["trials"] == 36315
    assert grid["minimum_observed_substitutions"] == 15
    assert grid["all_minimum_pairs"] == [[86, 87]]
    assert grid["adjacent_pair_family"]["trials"] == 269
    assert grid["adjacent_pair_family"]["all_minimum_first_indices"] == [86]
    old_goal = encode(rec["unaccepted_full_conjecture"], key["square"])
    assert len(old_goal) == 270
    assert sum(a != "?" and a != b for a, b in zip(interim, old_goal)) == 28

    img = inp["source"]["image"]
    assert sha(ROOT / img["path"]) == img["sha256"]
    if pdf:
        import fitz
        assert sha(pdf) == inp["source"]["pdf_sha256"]
        document = fitz.open(pdf)
        pix = document[img["pdf_page_1based"] - 1].get_pixmap(
            matrix=fitz.Matrix(img["scale"], img["scale"]),
            clip=fitz.Rect(*img["clip_points"]))
        saved = fitz.Pixmap(str(ROOT / img["path"]))
        assert (pix.width, pix.height, pix.n) == (saved.width, saved.height, saved.n)
        assert pix.samples == saved.samples
        assert hashlib.sha256(pix.samples).hexdigest() == img["pixel_sha256"]
    case = inp["primary_case"]
    text = (ROOT / case["path"]).read_text()
    heading = "\n## " + case["section"] + "\n"
    assert text.count(heading) == 1
    text = text[text.index(heading) + 1:].split("\n## ", 1)[0]
    fences, quotes = displays(text)
    assert [line for line in text.splitlines() if re.match(r"^#{1,6} ", line)] == case["headings"]
    assert [x["sha256"] for x in fences] == case["fence_sha256"]
    assert [x["sha256"] for x in quotes] == case["quote_sha256"]
    page = HERE / "README.md"
    text = page.read_text()
    assert text.count(expected_legend(page)) == 1
    fences, quotes = displays(text)
    assert all(x["role_from_caption"] for x in fences + quotes)
    streams = re.findall(r"```text\n(.*?)\n```", text, flags=re.S)
    assert streams == [native["plaintext"], primary_template, conditional["plaintext"], target]
    quote = "\n".join(line[2:] for line in text.splitlines() if line.startswith("> "))
    assert normalized_readable(quote) == target.replace("X", "")

    return {"schema": "adfgvx-p63-optional-technical-reading-certificate-v1",
            "prepared_by": inp["prepared_by"],
            "literal_transmitted_source": literal,
            "native_135_position_reading": native,
            "unchanged_primary_partial_template": primary_template,
            "unchanged_primary_observed_substitutions": previous_edits,
            "unchanged_primary_mask_fills": previous_fills,
            "original_intermediate_stream": interim,
            "original_intermediate_to_source_indices": origins,
            "surplus_interim_coordinates": [{"interim_index": i,
                                              "source_index": origins[i],
                                              "literal_coordinate": interim[i],
                                              "retained_in_transmitted_witness": True}
                                             for i in removed],
            "conditional_intermediate_to_source_indices": paired_origins,
            "conditional_134_position_reading": conditional,
            "optional_editorial_plaintext": target,
            "observed_substitutions": edits,
            "source_mask_fills": fills,
            "additional_technical_word_changes": [list(x) for x in additions],
            "raw_numeral_ledger": numeral_ledger,
            "reinserted_270_coordinate_interim_witness": rebuilt_interim,
            "reencrypted_270_slot_received_witness": witness,
            "exact_forward_witness_after_reinsertion": True,
            "pair_removal_comparison": grid,
            "primary_case_displays_unchanged": True,
            "new_physical_records": 0,
            "limits": inp["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    result = rebuild(inputs, args.pdf)
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text()), "Rebuilt certificate differs"
        print("VERIFIED p63 optional technical reading: 15 substitutions, 2 dash fills, 2 surplus interim coordinates; unique fixed-target minimum among 36,315 pairs")
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print("Wrote " + str(path.relative_to(ROOT)))


if __name__ == "__main__":
    main()
