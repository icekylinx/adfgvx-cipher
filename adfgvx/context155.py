"""Verify the source-preserving p155 companion readings using only Python's stdlib.

Usage: python -m adfgvx.context155 [certificate.json]
No language model, downloaded corpus, or solver package is required.
"""
from pathlib import Path
import hashlib
import json
import sys

COORDS = "ADFGVX"
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def untranspose(ciphertext, ranks):
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    quotient, remainder = divmod(len(ciphertext), width)
    columns = [None] * width
    start = 0
    for column in sorted(range(width), key=ranks.__getitem__):
        size = quotient + (column < remainder)
        columns[column] = ciphertext[start:start + size]
        start += size
    return "".join(columns[column][row]
                   for row in range(quotient + bool(remainder))
                   for column in range(width)
                   if row < len(columns[column]))


def transpose(intermediate, ranks):
    return "".join(intermediate[column::len(ranks)]
                   for column in sorted(range(len(ranks)), key=ranks.__getitem__))


def domains(intermediate, square):
    assert len(square) == 36
    known = [character for character in square if character != "?"]
    assert len(set(known)) == len(known)
    unused = set(SYMBOLS) - set(known)
    assert len(unused) == square.count("?")
    assert len(intermediate) % 2 == 0
    result = []
    for start in range(0, len(intermediate), 2):
        row, column = intermediate[start:start + 2]
        row_options = COORDS if row == "?" else row
        column_options = COORDS if column == "?" else column
        choices = set()
        for first in row_options:
            for second in column_options:
                character = square[6 * COORDS.index(first) + COORDS.index(second)]
                choices.update(unused if character == "?" else character)
        result.append("".join(sorted(choices)))
    return result


def verify(data):
    ranks = data["key"]["column_rank_order"]
    square = data["key"]["square"]
    results = []
    for section in data["sections"]:
        literal = "".join(section["raw_group_lines"]).replace(" ", "")
        assert literal == section["raw_literal"]
        ciphertext = "".join(c if c in COORDS else "?" for c in literal)
        assert ciphertext == section["analysis_ciphertext"]
        assert len(ciphertext) == section["received_slots"]
        assert sum(c in COORDS for c in literal) == section["known_source_coordinates"]
        assert hashlib.sha256(literal.encode("ascii")).hexdigest() == section["raw_literal_sha256"]
        for variant in section["variants"]:
            gap = variant["insert_unknown_before_source_0based"]
            model = ciphertext if gap is None else ciphertext[:gap] + "?" + ciphertext[gap:]
            assert model == variant["model_ciphertext"]
            assert len(model) == section["advertised_length"]
            intermediate = untranspose(model, ranks)
            assert intermediate == variant["intermediate"]
            assert transpose(intermediate, ranks) == model
            recovered_domains = domains(intermediate, square)
            assert recovered_domains == variant["plaintext_domains"]
            plaintext = "".join(x if len(x) == 1 else "?" for x in recovered_domains)
            assert plaintext == variant["raw_plaintext"]
            inverse = {c: COORDS[i // 6] + COORDS[i % 6]
                       for i, c in enumerate(square) if c != "?"}
            partial_coordinates = "".join(inverse[c] if c != "?" else "??" for c in plaintext)
            reencrypted = transpose(partial_coordinates, ranks)
            covered = 0
            for observed, predicted in zip(model, reencrypted):
                if observed != "?" and predicted != "?":
                    assert observed == predicted
                    covered += 1
            assert covered == variant["known_ciphertext_coordinates_covered_by_fixed_plaintext"]
            assert sum(len(d) == 1 for d in recovered_domains) == variant["fixed_plaintext_slots"]
            results.append({"id": variant["id"], "plaintext_slots": len(plaintext),
                            "fixed_plaintext_slots": variant["fixed_plaintext_slots"],
                            "coordinate_roundtrip": True,
                            "fixed_plaintext_reencryption_compatible": True,
                            "known_source_coordinates_retained": section["known_source_coordinates"]})
    return {"status": "passed", "variants": results,
            "limits": "This checks source normalization, the stated key, and each explicitly hypothesized geometry. It does not establish the missing coordinate or choose a unique A2 insertion position."}


if __name__ == "__main__":
    filename = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "data/certificates/p155.json"
    print(json.dumps(verify(json.loads(filename.read_text())), indent=2))
