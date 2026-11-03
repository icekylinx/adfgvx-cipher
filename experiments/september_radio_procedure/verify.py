#!/usr/bin/env python3
"""Rebuild the three p60 radio-procedure source certificates.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The key is prior published work by Lasry, Niebel, Kopal and Wacker.
Default verification uses only Python's standard library and this package.
Optional PDF rendering additionally requires PyMuPDF.
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


def read(cipher, ranks, square):
    """Invert ranked ragged columns using their independently computed offsets."""
    width, length = len(ranks), len(cipher)
    assert length % 2 == 0
    heights = [length // width + (col < length % width) for col in range(width)]
    starts = [sum(heights[other] for other in range(width)
                  if ranks[other] < ranks[col]) for col in range(width)]
    origins = [starts[i % width] + i // width for i in range(length)]
    assert sorted(origins) == list(range(length))
    stream = "".join(cipher[i] for i in origins)
    domains = []
    for index in range(0, length, 2):
        a, b = stream[index:index + 2]
        rows = range(6) if a == "?" else [CO.index(a)]
        cols = range(6) if b == "?" else [CO.index(b)]
        domains.append("".join(sorted(square[6 * row + col]
                                      for row in rows for col in cols)))
    raw = "".join(domain if len(domain) == 1 else "?" for domain in domains)
    return raw, domains, [origins[i:i + 2] for i in range(0, length, 2)]


def encipher(text, ranks, square):
    """Forward route uses row-major coordinate pairs and sorted column slices."""
    flat = "".join(CO[square.index(char) // 6] + CO[square.index(char) % 6]
                   for char in text)
    width = len(ranks)
    return "".join(flat[col::width]
                   for col in sorted(range(width), key=lambda col: ranks[col]))


def locations(rows):
    result, group_number = [], 0
    for row_number, row in enumerate(rows, 1):
        for row_group, group in enumerate(row.split(), 1):
            group_number += 1
            result.extend({"printed_row_1based": row_number,
                           "group_in_row_1based": row_group,
                           "printed_group_1based": group_number,
                           "group_position_1based": offset}
                          for offset in range(1, len(group) + 1))
    return result


def certificate(rec, received, key):
    ranks, square = key["column_rank_order"], key["square"]
    raw, domains, origins = read(received, ranks, square)
    proposal = rec["editorial_text"]
    assert len(proposal) == len(raw) and set(proposal) <= set(ALPHABET)
    witness = encipher(proposal, ranks, square)
    owner = {source: index for index, pair in enumerate(origins) for source in pair}
    places = locations(rec["rows"])
    edits, fills = [], []
    for index, (before, after) in enumerate(zip(received, witness)):
        if before == after:
            continue
        position = owner[index]
        item = {"source_index": index, **places[index],
                "diplomatic_source_glyph": rec["literal_source"][index],
                "before": before, "after": after,
                "plaintext_index": position, "raw_plaintext_symbol": raw[position],
                "proposed_plaintext_symbol": proposal[position]}
        (fills if before == "?" else edits).append(item)
    repaired = list(received)
    for change in edits + fills:
        assert repaired[change["source_index"]] == change["before"]
        repaired[change["source_index"]] = change["after"]
    assert "".join(repaired) == witness
    assert read(witness, ranks, square)[0] == proposal
    # Every raw fixed numeral remains exactly as received, including repetitions.
    numerals = []
    for index, char in enumerate(raw):
        if char.isdigit():
            assert proposal[index] == char
            assert all(received[source] == witness[source] for source in origins[index])
            numerals.append({"plaintext_index": index, "raw_label": char,
                             "coordinate_origins": origins[index]})
    if "?" not in received:
        assert encipher(raw, ranks, square) == received
    return {"analysis_source": received,
            "source_slots": len(received),
            "valid_received_coordinates": len(received) - received.count("?"),
            "plaintext_positions": len(raw),
            "raw_plaintext": raw, "domains": domains,
            "raw_fixed_positions": sum(len(domain) == 1 for domain in domains),
            "proposed_positions_directly_supported": sum(domain == char for domain, char
                                                          in zip(domains, proposal)),
            "coordinate_origins": origins, "editorial_plaintext": proposal,
            "known_coordinate_substitutions": edits, "erasure_fills": fills,
            "cost": {"substitutions": len(edits), "fills": len(fills)},
            "preserved_raw_numerals": numerals, "reencrypted_witness": witness,
            "exact_roundtrip": True}


def rebuild(inputs, pdf=None):
    key = inputs["key"]
    assert len(key["square"]) == 36 and set(key["square"]) == set(ALPHABET)
    assert sorted(key["column_rank_order"]) == list(range(1, 23))
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
    records = []
    for rec in inputs["records"]:
        groups = " ".join(rec["rows"]).split()
        literal = "".join(groups)
        assert literal == rec["literal_source"]
        assert all(len(group) == 5 for group in groups[:-1])
        received = "".join(char if char in CO else "?" for char in literal)
        assert received == rec["analysis_source"]
        assert len(received) == rec["advertised_length"]
        cert = certificate(rec, received, key)
        assert cert["raw_plaintext"] == rec["expected_raw"]
        assert cert["cost"] == rec["expected_cost"]
        changes = sorted([[item["source_index"], item["before"], item["after"]]
                          for item in cert["known_coordinate_substitutions"] + cert["erasure_fills"]])
        assert changes == rec["expected_changes"]
        variants = []
        for variant in rec.get("conditional_visual_variants", []):
            alternative = list(received)
            for index, before, after in variant["source_replacements"]:
                assert alternative[index] == before
                alternative[index] = after
            alt = certificate(rec, "".join(alternative), key)
            assert alt["raw_plaintext"] == variant["expected_raw"]
            assert alt["cost"] == variant["expected_cost"]
            assert {str(i): d for i, d in enumerate(alt["domains"]) if len(d) > 1} == variant["expected_ambiguous_domains"]
            variants.append({"id": variant["id"], "included_in_totals": False,
                             "basis": variant["basis"], **alt})
        records.append({"id": rec["id"], "literal_source": literal,
                        "literal_sha256": hashlib.sha256(literal.encode()).hexdigest(),
                        **cert, "conditional_visual_variants": variants})
    assert {str(i): d for i, d in enumerate(records[0]["domains"]) if len(d) > 1} == {
        "79": "1EGNPZ", "87": "1EGNPZ"}
    assert records[2]["domains"][104] == "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    totals = {name: sum(rec[name] for rec in records) for name in [
        "source_slots", "valid_received_coordinates", "plaintext_positions",
        "raw_fixed_positions", "proposed_positions_directly_supported"]}
    totals.update({"records": len(records),
                   "known_coordinate_substitutions": sum(rec["cost"]["substitutions"] for rec in records),
                   "erasure_fills": sum(rec["cost"]["fills"] for rec in records),
                   "insertions": 0, "deletions": 0, "reordered_blocks": 0,
                   "published_square_changes": 0})
    assert totals == {"source_slots": 556, "valid_received_coordinates": 552,
                      "plaintext_positions": 278, "raw_fixed_positions": 275,
                      "proposed_positions_directly_supported": 272, "records": 3,
                      "known_coordinate_substitutions": 3, "erasure_fills": 4,
                      "insertions": 0, "deletions": 0, "reordered_blocks": 0,
                      "published_square_changes": 0}
    return {"schema": "adfgvx-september-radio-procedure-certificate-v1",
            "prepared_by": inputs["prepared_by"], "inputs_sha256": digest(HERE / "inputs.json"),
            "totals_scope": "Three physical source records under the conservative glyph transcription; the F visual variant is not counted again.",
            "totals": totals, "records": records,
            "limits": ["Erasure fills and three coordinate substitutions are editorial proposals, not direct source readings.",
                       "Exact re-encryption certifies arithmetic consistency and edit cost, not unique historical wording.",
                       "The uncertain B glyph may be a damaged F; that conditional reading is displayed separately.",
                       "All raw numerical labels and their repetitions remain unchanged."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = rebuild(json.loads((HERE / "inputs.json").read_text()), args.pdf)
    target = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["totals"]}, indent=2))


if __name__ == "__main__":
    main()
