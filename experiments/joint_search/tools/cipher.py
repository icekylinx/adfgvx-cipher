"""Small independent ADFGVX arithmetic for the portable research suite."""
SYMBOLS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def validate(ranks):
    if not ranks or sorted(ranks) != list(range(1, len(ranks)+1)):
        raise ValueError('Column ranks must be a permutation of1..width')


def indices(length, ranks):
    validate(ranks)
    return [i for col in sorted(range(len(ranks)), key=ranks.__getitem__)
            for i in range(col, length, len(ranks))]


def untranspose(ciphertext, ranks):
    if any(ch not in SYMBOLS+'?' for ch in ciphertext):
        raise ValueError('Ciphertexts may contain only ADFGVX and ?')
    out = [''] * len(ciphertext)
    for ch, position in zip(ciphertext, indices(len(ciphertext), ranks)):
        out[position] = ch
    return ''.join(out)


def cells(ciphertext, ranks):
    if len(ciphertext) % 2:
        raise ValueError('Odd ciphertext length requires a separately declared corruption model')
    text = untranspose(ciphertext, ranks)
    return ''.join('?' if '?' in text[i:i+2] else ALPHABET[
        6*SYMBOLS.index(text[i])+SYMBOLS.index(text[i+1])]
        for i in range(0, len(text), 2))


def decrypt(ciphertext, ranks, square):
    if len(square) != 36 or sorted(square) != sorted(ALPHABET):
        raise ValueError('A complete square must be a permutation of the36-character alphabet')
    return ''.join('?' if ch == '?' else square[ALPHABET.index(ch)]
                   for ch in cells(ciphertext, ranks))


def encrypt(plaintext, ranks, square):
    if len(square) != 36 or sorted(square) != sorted(ALPHABET):
        raise ValueError('A complete square must be a permutation of the36-character alphabet')
    interim = ''.join(SYMBOLS[square.index(ch)//6]+SYMBOLS[square.index(ch)%6]
                      for ch in plaintext)
    return ''.join(interim[i] for i in indices(len(interim), ranks))


def mismatches(ciphertext, regenerated):
    if len(ciphertext) != len(regenerated):
        raise ValueError('Reencryption lengths differ')
    return [i for i, (a, b) in enumerate(zip(ciphertext, regenerated)) if a != '?' and a != b]
