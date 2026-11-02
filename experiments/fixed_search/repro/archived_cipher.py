"""Independent, erasure-preserving ADFGVX arithmetic and audit utilities.

Rank convention: ranks[c] is the one-based transmission order of column c.
All indices in machine-readable audit records are zero-based.
"""
from __future__ import annotations

import json
from pathlib import Path

SYMBOLS = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"


def validate_ranks(ranks):
    if sorted(ranks) != list(range(1, len(ranks) + 1)):
        raise ValueError("Ranks must be a permutation of 1,...,width")


def transposition_indices(length, ranks):
    """Indices of the interim stream, in transmitted order."""
    validate_ranks(ranks)
    width = len(ranks)
    return [p for col in sorted(range(width), key=ranks.__getitem__)
            for p in range(col, length, width)]


def transpose(interim, ranks):
    return "".join(interim[p] for p in transposition_indices(len(interim), ranks))


def untranspose(ciphertext, ranks):
    result = [""] * len(ciphertext)
    for symbol, target in zip(ciphertext, transposition_indices(len(ciphertext), ranks)):
        result[target] = symbol
    return "".join(result)


def decode(interim, square):
    if len(square) != 36:
        raise ValueError("The square must contain 36 cells")
    result = []
    for i in range(0, len(interim) - 1, 2):
        a, b = interim[i:i+2]
        if a not in SYMBOLS or b not in SYMBOLS:
            result.append("?")
        else:
            ch = square[6*SYMBOLS.index(a) + SYMBOLS.index(b)]
            result.append("?" if ch in "+-?" else ch)
    return "".join(result)


def encode(plaintext, square):
    known = [c for c in square if c not in "+-?"]
    if len(set(known)) != len(known):
        raise ValueError("A substitution square must be injective")
    return "".join(SYMBOLS[square.index(c)//6] + SYMBOLS[square.index(c)%6]
                   for c in plaintext)


def decrypt(ciphertext, ranks, square):
    return decode(untranspose(ciphertext, ranks), square)


def encrypt(plaintext, ranks, square):
    return transpose(encode(plaintext, square), ranks)


def cell_stream(ciphertext, ranks):
    interim = untranspose(ciphertext, ranks)
    return "".join(ALPHABET[6*SYMBOLS.index(interim[i])+SYMBOLS.index(interim[i+1])]
                   if interim[i] in SYMBOLS and interim[i+1] in SYMBOLS else "?"
                   for i in range(0, len(interim)-1, 2))


def plaintext_domains(ciphertext, ranks, square):
    """All square-cell possibilities, without guessing any received erasure."""
    interim = untranspose(ciphertext, ranks)
    domains = []
    for i in range(0, len(interim)-1, 2):
        a, b = interim[i:i+2]
        rows = [SYMBOLS.index(a)] if a in SYMBOLS else range(6)
        cols = [SYMBOLS.index(b)] if b in SYMBOLS else range(6)
        domains.append("".join(sorted({square[6*r+c] for r in rows for c in cols})))
    return domains


def load_data():
    messages = json.loads((DATA / "messages.json").read_text())
    keys = json.loads((DATA / "keys.json").read_text())
    return messages, keys


def self_check():
    for width in range(1, 25):
        ranks = list(range(width, 0, -1))
        for length in range(0, 3*width+3):
            stream = "".join(SYMBOLS[(i*i+3*i)//2 % 6] for i in range(length))
            assert untranspose(transpose(stream, ranks), ranks) == stream
    text = "EXACTROUNDTRIP1918"
    ranks = [3, 1, 5, 2, 4]
    assert decrypt(encrypt(text, ranks, ALPHABET), ranks, ALPHABET) == text
    return True


if __name__ == "__main__":
    print("Independent arithmetic self-check:", self_check())
