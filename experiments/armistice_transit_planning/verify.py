#!/usr/bin/env python3
"""Certify p125-p126's transit report and adjacent receipt message.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Published period key:
Lasry, Niebel, Kopal and Wacker. Standard library by default; PyMuPDF
is required only for the optional --pdf source-render check.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transpose(stream, ranks):
    return "".join(stream[col::len(ranks)]
                   for col in sorted(range(len(ranks)), key=lambda col: ranks[col]))


def inverse(cipher, ranks):
    width, length = len(ranks), len(cipher)
    heights = [length // width + (col < length % width) for col in range(width)]
    bases = [sum(heights[other] for other in range(width)
                 if ranks[other] < ranks[col]) for col in range(width)]
    origins = [bases[index % width] + index // width for index in range(length)]
    assert sorted(origins) == list(range(length))
    stream = "".join(cipher[index] for index in origins)
    assert transpose(stream, ranks) == cipher
    return stream, origins


def reading(stream, origins, square):
    domains, pairs = [], []
    for i in range(0, len(stream) - 1, 2):
        a, b = stream[i:i + 2]
        rows = range(6) if a == "?" else [CO.index(a)]
        cols = range(6) if b == "?" else [CO.index(b)]
        domains.append("".join(sorted(square[6 * row + col]
                                      for row in rows for col in cols)))
        pairs.append(origins[i:i + 2])
    return {"plaintext": "".join(d if len(d) == 1 else "?" for d in domains),
            "plaintext_positions": len(domains), "domains": domains,
            "raw_fixed_positions": sum(len(d) == 1 for d in domains),
            "source_coordinate_origins": pairs,
            "unpaired_coordinate": {"interim_index": len(stream) - 1,
                                     "source_index": origins[-1],
                                     "coordinate": stream[-1]} if len(stream) % 2 else None}


def encode(text, square):
    return "".join(CO[square.index(char) // 6] + CO[square.index(char) % 6]
                   for char in text)


def locations(rows):
    output, group_number = [], 0
    for row_number, row in enumerate(rows, 1):
        for row_group, group in enumerate(row.split(), 1):
            group_number += 1
            output.extend({"printed_row_1based": row_number,
                           "group_in_row_1based": row_group,
                           "printed_group_1based": group_number,
                           "group_position_1based": offset}
                          for offset in range(1, len(group) + 1))
    return output


def certify(rec, key):
    ranks, square = key["column_rank_order"], key["square"]
    groups = " ".join(rec["rows"]).split()
    literal = "".join(groups)
    assert literal == rec["literal_source"]
    assert all(len(group) == 5 for group in groups[:-1])
    received = "".join(char if char in CO else "?" for char in literal)
    assert received == rec["analysis_source"]
    assert len(received) == rec["advertised_length"]
    stream, origins = inverse(received, ranks)
    original = reading(stream, origins, square)
    assert original["plaintext"] == rec["expected_unmodified_raw"]
    model = rec["frame_model"]
    if model["kind"] == "one_pretransposition_coordinate_loss":
        assert len(stream) == 267 and model["inserted_unknown_coordinates"] == 1
        gap = model["insert_before_interim_index"]
        assert gap == 136
        stream = stream[:gap] + "?" + stream[gap:]
        origins = origins[:gap] + [None] + origins[gap:]
    else:
        assert model["kind"] == "identity"
    working = reading(stream, origins, square)
    assert working["unpaired_coordinate"] is None
    assert working["plaintext"] == rec["expected_working_raw"]
    proposal = rec["editorial_text"]
    assert len(proposal) * 2 == len(stream) and set(proposal) <= set(ALPHABET)
    proposed_stream = encode(proposal, square)
    edits, fills, inserted = [], [], []
    places = locations(rec["rows"])
    for i, (before, after) in enumerate(zip(stream, proposed_stream)):
        source = origins[i]
        if before == after:
            continue
        change = {"interim_index": i, "source_index": source,
                  "plaintext_index": i // 2, "before": before, "after": after,
                  "raw_plaintext_symbol": working["plaintext"][i // 2],
                  "proposed_plaintext_symbol": proposal[i // 2]}
        if source is None:
            assert before == "?"
            inserted.append(change)
        else:
            change.update(places[source])
            change["diplomatic_source_glyph"] = literal[source]
            (fills if before == "?" else edits).append(change)
    edits.sort(key=lambda item: item["source_index"])
    fills.sort(key=lambda item: item["source_index"])
    # Reproduce the transmitted geometry. A5's one proposed coordinate is
    # removed BEFORE the original 267-slot transposition, never from ciphertext.
    outgoing_stream = "".join(char for char, source in zip(proposed_stream, origins)
                              if source is not None)
    witness = transpose(outgoing_stream, ranks)
    repaired = list(received)
    for change in edits + fills:
        assert repaired[change["source_index"]] == change["before"]
        repaired[change["source_index"]] = change["after"]
    assert "".join(repaired) == witness and len(witness) == len(received)
    again, again_origins = inverse(witness, ranks)
    for change in inserted:
        index = change["interim_index"]
        again = again[:index] + change["after"] + again[index:]
        again_origins = again_origins[:index] + [None] + again_origins[index:]
    assert reading(again, again_origins, square)["plaintext"] == proposal
    assert sorted([[c["source_index"], c["before"], c["after"]]
                   for c in edits + fills]) == rec["expected_source_changes"]
    cost = {"substitutions": len(edits), "source_erasure_fills": len(fills),
            "interim_insertions": len(inserted)}
    assert cost == rec["expected_cost"]
    numerals = []
    for index, char in enumerate(working["plaintext"]):
        if char.isdigit():
            assert proposal[index] == char
            positions = working["source_coordinate_origins"][index]
            assert all(source is not None and received[source] == witness[source]
                       for source in positions)
            numerals.append({"plaintext_index": index, "raw_label": char,
                             "source_coordinate_origins": positions})
    return {"id": rec["id"], "source_slots": len(received),
            "valid_received_coordinates": len(received) - received.count("?"),
            "literal_sha256": hashlib.sha256(literal.encode()).hexdigest(),
            "unmodified_source_reading": original,
            "working_reading_is_conditional": bool(inserted),
            "working_reading": working, "editorial_plaintext": proposal,
            "proposed_positions_directly_supported_under_stated_geometry": sum(
                domain == char for domain, char in zip(working["domains"], proposal)),
            "known_coordinate_substitutions": edits, "source_erasure_fills": fills,
            "interim_insertions": inserted, "cost": cost,
            "preserved_numerals_under_stated_geometry": numerals,
            "reencrypted_transmitted_witness": witness,
            "exact_roundtrip_under_stated_geometry": True}


def rebuild(inputs, pdf=None):
    key = inputs["key"]
    assert len(key["square"]) == 36 and set(key["square"]) == set(ALPHABET)
    assert sorted(key["column_rank_order"]) == list(range(1, 18))
    document = None
    if pdf:
        import fitz
        assert digest(pdf) == inputs["source"]["pdf_sha256"]
        document = fitz.open(pdf)
    for image in inputs["source"]["images"]:
        assert digest(HERE / image["path"]) == image["sha256"]
        if document is not None:
            pix = document[image["pdf_page_1based"] - 1].get_pixmap(
                matrix=fitz.Matrix(image["scale"], image["scale"]),
                clip=fitz.Rect(*image["clip_points"]))
            assert (pix.width, pix.height) == (image["width"], image["height"])
            assert hashlib.sha256(pix.samples).hexdigest() == image["pixel_sha256"]
    records = [certify(rec, key) for rec in inputs["records"]]
    exact = [r for r in records if not r["working_reading_is_conditional"]]
    totals = {"source_records": len(records),
              "source_slots": sum(r["source_slots"] for r in records),
              "valid_received_coordinates": sum(r["valid_received_coordinates"] for r in records),
              "exact_frame_records": len(exact),
              "exact_frame_positions": sum(r["working_reading"]["plaintext_positions"] for r in exact),
              "exact_frame_raw_fixed_positions": sum(r["working_reading"]["raw_fixed_positions"] for r in exact),
              "conditional_records": 1,
              "conditional_positions": records[4]["working_reading"]["plaintext_positions"],
              "conditional_raw_fixed_positions": records[4]["working_reading"]["raw_fixed_positions"],
              "known_coordinate_substitutions": sum(r["cost"]["substitutions"] for r in records),
              "source_erasure_fills": sum(r["cost"]["source_erasure_fills"] for r in records),
              "conditional_interim_insertions": sum(r["cost"]["interim_insertions"] for r in records),
              "transmitted_coordinate_insertions_or_deletions": 0,
              "reordered_source_blocks": 0, "published_square_changes": 0}
    assert totals == {"source_records": 7, "source_slots": 1537,
                      "valid_received_coordinates": 1533, "exact_frame_records": 6,
                      "exact_frame_positions": 635, "exact_frame_raw_fixed_positions": 633,
                      "conditional_records": 1, "conditional_positions": 134,
                      "conditional_raw_fixed_positions": 131,
                      "known_coordinate_substitutions": 10, "source_erasure_fills": 4,
                      "conditional_interim_insertions": 1,
                      "transmitted_coordinate_insertions_or_deletions": 0,
                      "reordered_source_blocks": 0, "published_square_changes": 0}
    return {"schema": "adfgvx-armistice-transit-planning-certificate-v1",
            "prepared_by": inputs["prepared_by"], "inputs_sha256": digest(HERE / "inputs.json"),
            "totals": totals, "records": records,
            "limits": ["A5's 267-slot source and odd unmodified reading are preserved independently of the proposed pretransposition omission.",
                       "A5's 134-position reading is conditional on that geometry; its tail is not a direct exact-frame decipherment.",
                       "The editorial template is retrospective, not an independent historical crib.",
                       "PUNKT, BESONDRER, DRINGD and the elliptical GEMELDETEN clause are retained; omitted grammar is not supplied as recovered plaintext.",
                       "All numerical labels in exact frames and the A5 prefix retain their published-square values without historical reassignment.",
                       "Exact re-encryption certifies consistency and costs, not unique historical wording or error mechanism."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = rebuild(json.loads((HERE / "inputs.json").read_text()), args.pdf)
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["totals"]}, indent=2))


if __name__ == "__main__":
    main()
