"""Portable ADFGVX arithmetic used by the archived fixed-search recipes."""
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SYMBOLS = "ADFGVX"


def validate_ranks(ranks):
    if not ranks or sorted(ranks) != list(range(1, len(ranks) + 1)):
        raise ValueError("Ranks must be a nonempty permutation of 1 through width")


def validate_ciphertext(ciphertext, even=True):
    if not ciphertext or set(ciphertext) - set(SYMBOLS + "?"):
        raise ValueError("Ciphertext must use only ADFGVX and ?")
    if even and len(ciphertext) % 2:
        raise ValueError("An ordinary complete coordinate stream must have even length")


def validate_square(square):
    if len(square) != 36 or set(square) != set(ALPHABET):
        raise ValueError("A fitted square must be a permutation of A-Z and 0-9")


def indices(length, ranks):
    validate_ranks(ranks)
    return [i for c in sorted(range(len(ranks)), key=ranks.__getitem__)
            for i in range(c, length, len(ranks))]


def transpose(interim, ranks):
    return "".join(interim[i] for i in indices(len(interim), ranks))


def untranspose(ciphertext, ranks):
    out = [""] * len(ciphertext)
    for symbol, position in zip(ciphertext, indices(len(ciphertext), ranks)):
        out[position] = symbol
    return "".join(out)


def whole_cells(interim):
    """Archived diagnostic: discard a final odd coordinate, mask partial pairs.

    Callers must record the abandoned suffix. This function is not an ordinary
    complete-message decoder and is used only by the historical fixed screen.
    """
    return "".join(ALPHABET[6 * SYMBOLS.index(a) + SYMBOLS.index(b)]
                   if a in SYMBOLS and b in SYMBOLS else "?"
                   for a, b in zip(interim[::2], interim[1::2]))


def decode(interim, square):
    validate_ciphertext(interim)
    validate_square(square)
    return "".join(square[ALPHABET.index(c)] if c != "?" else "?"
                   for c in whole_cells(interim))


def decode_cells(cells, square):
    validate_square(square)
    if set(cells) - set(ALPHABET + "?"):
        raise ValueError("Invalid cell alphabet")
    return "".join(square[ALPHABET.index(c)] if c != "?" else "?" for c in cells)
