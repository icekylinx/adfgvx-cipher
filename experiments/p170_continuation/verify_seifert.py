#!/usr/bin/env python3
"""Verify the source edition of station-control and Seifert service messages.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Uses independent column reconstruction, with no model, search or cipher imports.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
COORD = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def coordinate_map(length, ranks):
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    columns = []
    for col in range(len(ranks)):
        columns.append(list(range(col, length, len(ranks))))
    return [position for rank in range(1, len(ranks) + 1)
            for position in columns[ranks.index(rank)]]


def arithmetic(ciphertext, ranks, square):
    assert len(ciphertext) % 2 == 0
    assert len(square) == 36
    known = [c for c in square if c != "?"]
    assert len(set(known)) == len(known)
    unused = set(ALPHABET) - set(known)
    interim = [None] * len(ciphertext)
    for source, destination in enumerate(coordinate_map(len(ciphertext), ranks)):
        interim[destination] = ciphertext[source]
    domains, cells = [], []
    for pos in range(0, len(interim), 2):
        row, col = interim[pos:pos + 2]
        possibilities = [6 * r + c for r in range(6) for c in range(6)
                         if (row == "?" or COORD[r] == row)
                         and (col == "?" or COORD[c] == col)]
        chars = set()
        for cell in possibilities:
            chars.update(unused if square[cell] == "?" else [square[cell]])
        assert chars
        domains.append("".join(sorted(chars)))
        cells.append(possibilities)
    plaintext = "".join(domain if len(domain) == 1 else "?" for domain in domains)
    return plaintext, domains, cells


def encode(plaintext, ranks, square):
    interim = "".join(COORD[square.index(c) // 6] + COORD[square.index(c) % 6]
                      for c in plaintext)
    return "".join(interim[i] for i in coordinate_map(len(interim), ranks))


def verify(pdf=None):
    data = json.loads((HERE / "seifert_records.json").read_text())
    assert data["prepared_by"] == "icekylinx and GPT-6 Astra Pro"
    if pdf:
        assert digest(pdf) == data["source_pdf_sha256"]
    for crop in data["crops"]:
        assert digest(ROOT / crop["path"]) == crop["sha256"]
    keys = {k["id"]: k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    by_id = {r["id"]: r for r in data["records"]}
    assert len(by_id) == 9
    summary = []
    for record in data["records"]:
        raw = "".join("".join(record["raw_source_rows"]).split())
        assert raw == record["raw_source_compact"]
        cipher = "".join(c if c in COORD else "?" for c in raw)
        assert cipher == record["analysis_ciphertext"]
        assert record["received_slots"] == len(raw)
        assert record["valid_coordinates"] == sum(c in COORD for c in raw)
        assert record["masked_source_slots_0based"] == [i for i,c in enumerate(raw) if c not in COORD]
        ranks, square = record["column_rank_order"], record["partial_square"]
        key = keys[record["key_id"]]
        assert ranks == key["column_rank_order"] and square == key["square"]
        checked = {"id": record["id"], "received_slots": len(raw),
                   "valid_source_coordinates": record["valid_coordinates"], "editions": []}
        if len(cipher) % 2:
            assert record["raw_plaintext"] is None and record["id"] == "p169_A"
            assert len(cipher) == 185 and record["source"]["advertised_length"] == 184
            checked["raw_decode_refused_for_odd_length"] = True
        else:
            text, domains, _ = arithmetic(cipher, ranks, square)
            assert text == record["raw_plaintext"] and domains == record["raw_domains"]
            fixed = sum(len(d) == 1 for d in domains)
            assert fixed == record["fixed_plaintext_positions"]
            checked.update(plaintext_positions=len(domains), fixed_plaintext_positions=fixed)
            if "?" not in text:
                assert encode(text, ranks, square) == cipher
        for edition in record["editions"]:
            proposed = edition["ciphertext"]
            if edition["kind"] == "conditional_duplicate_coordinate_deletion":
                positions = edition["deleted_source_positions_0based"]
                assert positions in [[158], [159]]
                assert "".join(cipher[i] for i in positions) == edition["deleted_source_symbols"] == "G"
                assert proposed == "".join(c for i,c in enumerate(cipher) if i not in positions)
                checked["editions"].append({"id":edition["id"], "deleted_coordinates":1})
            else:
                assert len(proposed) == len(cipher)
                actual_fills = [{"ciphertext_position_0based":i,"raw_glyph":raw[i],"coordinate":b}
                                for i,(a,b) in enumerate(zip(cipher,proposed)) if a == "?"]
                actual_changes = [{"ciphertext_position_0based":i,"source_coordinate":a,"proposed_coordinate":b}
                                  for i,(a,b) in enumerate(zip(cipher,proposed)) if a != "?" and a != b]
                assert actual_fills == edition["fills"]
                assert actual_changes == edition["known_coordinate_substitutions"]
                checked["editions"].append({"id":edition["id"], "erasure_fills":len(actual_fills),
                                             "known_coordinate_substitutions":len(actual_changes)})
            text, _, _ = arithmetic(proposed, ranks, square)
            assert text == edition["plaintext"] and "?" not in text
            assert encode(text, ranks, square) == proposed
        if "identical_ciphertext_as" in record:
            assert cipher == by_id[record["identical_ciphertext_as"]]["analysis_ciphertext"]
            text, domains, cells = arithmetic(cipher, ranks, square)
            assert [(i,d) for i,d in enumerate(domains) if len(d)>1] == [(10,"56789")]
            cell = cells[10][0]
            assert len(cells[10]) == 1 and square[cell] == "?"
            attained = []
            unknown = [i for i,c in enumerate(square) if c == "?"]
            unused = sorted(set(ALPHABET) - set(square))
            for digit in "56789":
                complete = list(square); complete[cell] = digit
                for pos,c in zip([i for i in unknown if i != cell], [c for c in unused if c != digit]):
                    complete[pos] = c
                complete = "".join(complete)
                assert set(complete) == set(ALPHABET)
                candidate = text.replace("?",digit)
                assert encode(candidate,ranks,complete) == cipher
                attained.append(digit)
            checked["globally_attainable_hundreds_digits"] = attained
        summary.append(checked)
    assert by_id["p169_A"]["editions"][0]["ciphertext"] == by_id["p169_A"]["editions"][1]["ciphertext"]
    assert by_id["p172_A"]["raw_domains"][5] == "FIKNOS"
    assert by_id["p174_B"]["raw_domains"][22] == "156789ENVX"
    return {"status":"passed", "source_records":len(summary),
            "source_slots":sum(row["received_slots"] for row in summary),
            "source_pdf_hash_checked":bool(pdf), "source_crop_hashes_checked":len(data["crops"]),
            "records":summary,
            "scope":"Independent cipher arithmetic, exact edit accounting and global digit witnesses; source reading and historical interpretation still depend on the cited images and scholarship."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = verify(args.pdf)
    if args.json:
        print(json.dumps(report,indent=2))
    else:
        print(f"Station traffic: {report['source_records']} source records, {report['source_slots']} slots; all arithmetic and edit checks passed.")

if __name__ == "__main__":
    main()
