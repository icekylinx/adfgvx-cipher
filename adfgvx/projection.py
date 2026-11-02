#!/usr/bin/env python3
"""Verify the p185 direct reading and the conservative p189 projection.

The p189 alignment may insert erased slots, but may not delete, substitute, or
fill any source position. Its geometry is inferred from an historical parallel.
This is a partial-decipherment certificate, not a complete p189 solution.
"""
from pathlib import Path
import json
import sys

SYMBOLS = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def untranspose(sequence, ranks):
    n, width = len(sequence), len(ranks)
    lengths = [n // width + (i < n % width) for i in range(width)]
    columns = {}
    position = 0
    for column in sorted(range(width), key=ranks.__getitem__):
        columns[column] = sequence[position:position + lengths[column]]
        position += lengths[column]
    return [columns[column][row] for row in range(max(lengths, default=0))
            for column in range(width) if row < lengths[column]]


def transpose(coordinates, ranks):
    return "".join("".join(coordinates[column::len(ranks)])
                   for column in sorted(range(len(ranks)), key=ranks.__getitem__))


def domains(ciphertext, ranks, square):
    coordinates = untranspose(ciphertext, ranks)
    indices = untranspose(list(range(len(ciphertext))), ranks)
    unused = ''.join(char for char in ALPHABET if char not in square)
    result = []
    for i in range(0, len(coordinates), 2):
        pair = ''.join(coordinates[i:i + 2])
        possible = set()
        for row in range(6):
            for column in range(6):
                if pair[0] not in ('?', SYMBOLS[row]) or pair[1] not in ('?', SYMBOLS[column]):
                    continue
                char = square[6 * row + column]
                possible.update(unused if char == '?' else char)
        result.append({'plaintext_index': i // 2, 'coordinate_pair': pair,
                       'ciphertext_indices': indices[i:i + 2],
                       'possible_characters': ''.join(sorted(possible)),
                       'unique_character': next(iter(possible)) if len(possible) == 1 else None})
    return result


def align_preserving_source(parallel, target):
    """All cheapest monotone injections of target into the parallel's slots.

    Erasures compare at cost zero; disagreement costs one; an inserted erased
    slot costs one. Source deletions are prohibited. No language model is used.
    """
    n, m = len(parallel), len(target)
    infinity = 10 ** 9
    table = [[infinity] * (m + 1) for _ in range(n + 1)]
    table[0][0] = 0
    for i in range(1, n + 1):
        for j in range(min(i, m) + 1):
            table[i][j] = table[i - 1][j] + 1
            if j:
                mismatch = int(target[j - 1] != '?' and target[j - 1] != parallel[i - 1])
                table[i][j] = min(table[i][j], table[i - 1][j - 1] + mismatch)
    paths = []

    def trace(i, j, reverse_map):
        if not i:
            assert not j
            paths.append(list(reversed(reverse_map)))
            return
        if j:
            mismatch = int(target[j - 1] != '?' and target[j - 1] != parallel[i - 1])
            if table[i][j] == table[i - 1][j - 1] + mismatch:
                trace(i - 1, j - 1, reverse_map + [j - 1])
        if table[i][j] == table[i - 1][j] + 1:
            trace(i - 1, j, reverse_map + [None])

    trace(n, m, [])
    return table[n][m], paths


def analyze(parallel, target, ranks, square):
    cost, mappings = align_preserving_source(parallel, target)
    analyses = []
    for mapping in mappings:
        aligned = ''.join('?' if source_index is None else target[source_index]
                          for source_index in mapping)
        character_domains = domains(aligned, ranks, square)
        analyses.append({'parallel_to_target_index': mapping,
                         'inserted_erasure_indices': [i for i, source_index in enumerate(mapping) if source_index is None],
                         'aligned_ciphertext': aligned,
                         'raw_partial_plaintext': ''.join(row['unique_character'] or '?' for row in character_domains),
                         'character_domains': character_domains})
    invariant = []
    for i in range(len(parallel) // 2):
        union = set().union(*(set(path['character_domains'][i]['possible_characters']) for path in analyses))
        invariant.append(''.join(sorted(union)))
    return {'cost': cost, 'path_count': len(mappings), 'paths': analyses,
            'all_path_character_domains': invariant,
            'all_path_invariant_plaintext': ''.join(chars if len(chars) == 1 else '?' for chars in invariant)}

