#!/usr/bin/env python3
"""Reproduce source-preserving readings and explicitly separate editorial repairs.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
Only the Python standard library is required. The source transcription and key
are inputs; arithmetic verification does not independently establish either.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path

COORDS = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def order(length, ranks):
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    return [p for c in sorted(range(len(ranks)), key=ranks.__getitem__)
            for p in range(c, length, len(ranks))]


def decode_record(record, key):
    source = "".join(record["source_groups"])
    assert len(source) % 2 == 0
    assert set(source) <= set(COORDS + "?")
    ranks, square = key["column_rank_order"], key["square"]
    assert len(square) == 36
    known = square.replace("?", "")
    assert len(set(known)) == len(known) and set(known) <= set(ALPHABET)
    unused = "".join(sorted(set(ALPHABET) - set(known)))
    permutation = order(len(source), ranks)
    inverse = [0] * len(source)
    interim = [""] * len(source)
    for transmitted, position in enumerate(permutation):
        inverse[position] = transmitted
        interim[position] = source[transmitted]
    assert "".join(interim[p] for p in permutation) == source
    domains, cells, pairs = [], [], []
    for p in range(0, len(source), 2):
        a, b = interim[p:p + 2]
        rows = [COORDS.index(a)] if a in COORDS else range(6)
        cols = [COORDS.index(b)] if b in COORDS else range(6)
        possible = [6 * r + c for r in rows for c in cols]
        cells.append(possible)
        symbols = set()
        for cell in possible:
            symbols.update(unused if square[cell] == "?" else square[cell])
        domains.append("".join(sorted(symbols)))
        pairs.append([inverse[p], inverse[p + 1]])
    plaintext = "".join(d if len(d) == 1 else "?" for d in domains)
    canonical_square = list(square)
    fill = iter(unused)
    for i, char in enumerate(square):
        if char == "?":
            canonical_square[i] = next(fill)
    # This completion exists only to check a complete roundtrip. Its arbitrary
    # unused-symbol order is not published as a recovered historical key.
    canonical_square = "".join(canonical_square)
    canonical_interim = "".join(c if c in COORDS else "A" for c in interim)
    canonical_text = "".join(canonical_square[6 * COORDS.index(canonical_interim[p])
        + COORDS.index(canonical_interim[p + 1])] for p in range(0, len(source), 2))
    recoded = "".join(COORDS[canonical_square.index(c) // 6]
                      + COORDS[canonical_square.index(c) % 6] for c in canonical_text)
    transmitted = "".join(recoded[p] for p in permutation)
    assert all(a == "?" or a == b for a, b in zip(source, transmitted))
    editorial = []
    edited = list(source)
    for proposal in record.get("editorial_readings", []):
        p, char = proposal["plaintext_index"], proposal["proposed_symbol"]
        assert char in known, "Editorial target must already have an established cell"
        cell = square.index(char)
        desired = COORDS[cell // 6] + COORDS[cell % 6]
        replacements = []
        for offset, new in zip(pairs[p], desired):
            if source[offset] != new:
                replacements.append({"ciphertext_offset": offset,
                    "source": source[offset], "proposed": new,
                    "group_1based": offset // 5 + 1,
                    "within_group_1based": offset % 5 + 1})
                assert edited[offset] in (source[offset], new)
                edited[offset] = new
        editorial.append({**proposal, "source_plaintext": plaintext[p],
                          "source_domain": domains[p],
                          "coordinate_replacements": replacements})
    editorial_plaintext = list(plaintext)
    for proposal in editorial:
        editorial_plaintext[proposal["plaintext_index"]] = proposal["proposed_symbol"]
    if editorial:
        # Re-decode each edited position directly, while checking that all other
        # source coordinates remain literally unchanged.
        for p, offsets in enumerate(pairs):
            if p not in {e["plaintext_index"] for e in editorial}:
                assert all(edited[t] == source[t] for t in offsets)
            elif all(edited[t] in COORDS for t in offsets):
                cell = 6 * COORDS.index(edited[offsets[0]]) + COORDS.index(edited[offsets[1]])
                assert square[cell] == editorial_plaintext[p]
    raw_ocr = record.get("ocr_ciphertext")
    ocr_changes = []
    if raw_ocr is not None:
        for tag, a, b, c, d in difflib.SequenceMatcher(None, raw_ocr, source,
                                                     autojunk=False).get_opcodes():
            if tag != "equal":
                ocr_changes.append({"kind": tag, "ocr_offsets": [a, b],
                    "source_offsets": [c, d], "ocr": raw_ocr[a:b], "source": source[c:d]})
    return {"id": record["id"], "key_id": key["id"],
        "source_coordinate_count": len(source),
        "observed_coordinate_count": sum(c in COORDS for c in source),
        "plaintext_positions": len(plaintext),
        "source_fixed_positions": sum(len(d) == 1 for d in domains),
        "source_plaintext": plaintext,
        "plaintext_domains": domains,
        "plaintext_cell_domains": cells,
        "plaintext_to_ciphertext_offsets": pairs,
        "source_ciphertext_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "ocr_changes": ocr_changes,
        "editorial_plaintext": "".join(editorial_plaintext),
        "editorial_readings": editorial,
        "editorial_coordinate_cost": sum(a != b for a, b in zip(source, edited)),
        "all_observed_coordinates_preserved_by_base_reading": True,
        "complete_roundtrip_under_demonstration_only_completion": True}


def build(inputs):
    keys = {k["id"]: k for k in inputs["keys"]}
    rows = [decode_record(record, keys[record["key_id"]]) for record in inputs["records"]]
    return {"schema": "adfgvx-source-reading-package-v1",
        "title": inputs["title"], "authors": "icekylinx and GPT-6 Astra Pro",
        "results": rows,
        "summary": {"message_parts": len(rows),
            "source_coordinates": sum(r["source_coordinate_count"] for r in rows),
            "observed_coordinates": sum(r["observed_coordinate_count"] for r in rows),
            "plaintext_positions": sum(r["plaintext_positions"] for r in rows),
            "source_fixed_positions": sum(r["source_fixed_positions"] for r in rows),
            "editorial_coordinate_replacements": sum(r["editorial_coordinate_cost"] for r in rows)},
        "limits": ["The source transcription and historical key are supplied evidence, not inferred by this verifier.",
            "A singleton is fixed relative to the stated source transcription and key; a source copying error can still yield a wrong letter.",
            "Editorial readings are proposed source-coordinate changes and are never folded into the preserved source ciphertext.",
            "Unknown square-cell domains share one global injective square and are not independent choices.",
            "The complete roundtrip uses a deterministic arbitrary completion only as an arithmetic witness, not a historical claim."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_text())
    for image in inputs.get("source_images", []):
        assert sha256(args.inputs.parent / image["path"]) == image["sha256"]
    result = build(inputs)
    if args.verify:
        assert json.loads(args.output.read_text()) == result
        print(json.dumps({"verified": True, **result["summary"]}, indent=2))
    else:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
