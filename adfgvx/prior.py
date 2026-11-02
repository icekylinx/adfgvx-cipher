#!/usr/bin/env python3
"""Independently verify the exact arithmetic in prior_readings.json.

The certificate separates received-coordinate edits, pre-transposition sender
errors, editorial wording, and unresolved Polybius cells. No guessed word is
used to complete an erasure during verification. All offsets are zero based.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

SYMBOLS = "ADFGVX"
PLAINTEXT_SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def apply_edits(source, edits):
    out, cursor = [], 0
    for e in sorted(edits, key=lambda x: (x["start"], x["end"])):
        a, b = e["start"], e["end"]
        assert cursor <= a <= b <= len(source), (cursor, e)
        assert source[a:b] == e["removed"], (e, source[a:b])
        out.extend((source[cursor:a], e["inserted"]))
        cursor = b
    out.append(source[cursor:])
    return "".join(out)


def transpose(stream, ranks):
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    return "".join(stream[c::len(ranks)] for c in sorted(range(len(ranks)), key=ranks.__getitem__))


def untranspose(ciphertext, ranks):
    width, n = len(ranks), len(ciphertext)
    out, offset = [None] * n, 0
    for c in sorted(range(width), key=ranks.__getitem__):
        length = len(range(c, n, width))
        out[c::width] = ciphertext[offset:offset + length]
        offset += length
    assert offset == n and all(x is not None for x in out)
    return "".join(out)


def domains(stream, square):
    known = [x for x in square if x in PLAINTEXT_SYMBOLS]
    assert len(square) == 36 and len(known) == len(set(known))
    unassigned = set(PLAINTEXT_SYMBOLS) - set(known)
    result = []
    for i in range(0, len(stream) - 1, 2):
        first, second = stream[i:i + 2]
        rows = [SYMBOLS.index(first)] if first in SYMBOLS else range(6)
        cols = [SYMBOLS.index(second)] if second in SYMBOLS else range(6)
        possible = set()
        for r in rows:
            for c in cols:
                value = square[6 * r + c]
                possible.update(value if value in PLAINTEXT_SYMBOLS else unassigned)
        result.append("".join(sorted(possible)))
    return result


def encode_known_plaintext(plaintext, square):
    return "".join(SYMBOLS[square.index(x) // 6] + SYMBOLS[square.index(x) % 6] for x in plaintext)


def compute_variant(source, key, variant):
    ciphertext = apply_edits(source, variant.get("ciphertext_edits", []))
    before = untranspose(ciphertext, key["column_rank_order"])
    after = apply_edits(before, variant.get("intermediate_edits", []))
    d = domains(after, key["square"])
    raw = "".join(x if len(x) == 1 else "?" for x in d)
    result = {
        "corrected_ciphertext": ciphertext,
        "corrected_ciphertext_length": len(ciphertext),
        "intermediate_stream_before_edits": before,
        "intermediate_stream_after_edits": after,
        "raw_partial_plaintext": raw,
        "plaintext_domains": d,
        "decoded_plaintext_length": len(d),
        "fixed_plaintext_characters": sum(len(x) == 1 for x in d),
        "unpaired_intermediate_suffix": after[2 * len(d):],
        "coordinate_transposition_roundtrip": transpose(before, key["column_rank_order"]) == ciphertext,
    }
    # A full plaintext encryption is certified only when every letter is
    # uniquely fixed and the paired stream uses directly attested square cells.
    full = "?" not in raw and all(x in key["square"] for x in raw)
    result["all_decoded_letters_reencode_to_paired_stream"] = (
        encode_known_plaintext(raw, key["square"]) == after[:2 * len(d)] if full else None
    )
    result["ordinary_complete_adfgvx_roundtrip"] = (
        not variant.get("intermediate_edits")
        and not result["unpaired_intermediate_suffix"]
        and full
        and transpose(encode_known_plaintext(raw, key["square"]), key["column_rank_order"]) == ciphertext
    )
    return result


def compare_reading(plaintext, result):
    if len(plaintext) != result["decoded_plaintext_length"]:
        return {
            "length_compatible": False,
            "proposed_plaintext_length": len(plaintext),
            "model_plaintext_length": result["decoded_plaintext_length"],
        }
    conflicts = [
        {"plaintext_index": i, "proposed": x, "allowed": d}
        for i, (x, d) in enumerate(zip(plaintext, result["plaintext_domains"]))
        if x != "?" and x not in d
    ]
    return {
        "length_compatible": True,
        "contradictory_plaintext_positions": conflicts,
        "compatible_with_each_position_domain": not conflicts,
        "caveat": "Positionwise compatibility does not assign globally coupled unknown square cells or prove a proposed wording.",
    }


def verify(path):
    document = json.loads(Path(path).read_text())
    checked = []
    source_scope_checks = []
    for entry in document["messages"]:
        for variant in entry["verified_variants"]:
            result = compute_variant(entry["analysis_ciphertext"], entry["key"], variant)
            assert result == variant["verification"], (entry["id"], variant["id"])
            assert result["coordinate_transposition_roundtrip"]
            assert result["all_decoded_letters_reencode_to_paired_stream"] is not False
            checked.append({
                "message_id": entry["id"],
                "variant": variant["id"],
                "plaintext_length": result["decoded_plaintext_length"],
                "fixed_characters": result["fixed_plaintext_characters"],
                "ordinary_complete_roundtrip": result["ordinary_complete_adfgvx_roundtrip"],
                "unpaired_suffix": result["unpaired_intermediate_suffix"],
            })
        for reading in entry["published_readings"]:
            comparison = reading.get("comparison")
            if comparison is None:
                continue
            target = next(v for v in entry["verified_variants"] if v["id"] == reading["compared_with_variant"])
            assert comparison == compare_reading(reading["compact_plaintext"], target["verification"])
        for variant in entry["verified_variants"]:
            stages = variant.get("staged_repair")
            if not stages:
                continue
            first = next(v for v in entry["verified_variants"] if v["id"] == stages["first_stage_variant"])
            before = first["verification"]["corrected_ciphertext"]
            after = variant["verification"]["corrected_ciphertext"]
            assert len(before) == len(after)
            expected = [{"index":i,"observed":a,"replacement":b,"kind":"erasure fill" if a=="?" else "known-symbol correction"} for i,(a,b) in enumerate(zip(before,after)) if a!=b]
            assert expected == stages["additional_changes_in_first_stage_coordinates"]
        scope = entry.get("source_scope_comparison")
        if scope is not None:
            source_key = {**entry["key"], "square": scope["source_conservative_square"]}
            for variant in entry["verified_variants"]:
                result = compute_variant(entry["analysis_ciphertext"], source_key, variant)
                i = scope["ambiguous_plaintext_position"]
                pairs = [result["intermediate_stream_after_edits"][j:j + 2]
                         for j in range(0, 2 * result["decoded_plaintext_length"], 2)]
                assert result["decoded_plaintext_length"] == scope["plaintext_length"]
                assert result["fixed_plaintext_characters"] == scope["fixed_plaintext_letters"]
                assert result["plaintext_domains"][i] == scope["domain"]
                assert pairs[i] == scope["coordinate_pair"]
                assert pairs.count(scope["coordinate_pair"]) == 1
                assert scope["unused_coupled_coordinate_pair"] not in pairs
                assert result["coordinate_transposition_roundtrip"]
                source_scope_checks.append({
                    "message_id": entry["id"], "variant": variant["id"],
                    "raw_partial_plaintext": result["raw_partial_plaintext"],
                    "fixed_characters": result["fixed_plaintext_characters"],
                    "ambiguous_plaintext_position": i,
                    "domain": result["plaintext_domains"][i],
                })
    return {"messages": len(document["messages"]), "verified_variants": len(checked),
            "checks_passed": True, "variants": checked,
            "source_scope_comparisons": source_scope_checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", default=str(Path(__file__).resolve().parent.parent / "data" / "prior_readings.json"))
    parser.add_argument("--output")
    args = parser.parse_args()
    result = verify(args.certificate)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text)
