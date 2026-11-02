#!/usr/bin/env python3
"""Build the coordinate-marginal ranking model used by the reported searches.

This is a language-ranking heuristic. It does not complete a partial square,
certify a proposed plaintext, or preserve dependencies between repeated unknown
square cells. Input is the checksummed upstream German log10 quadgram table.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
UPSTREAM_SHA256 = 'a39714514cd2884605b1b04a2f65565fcf33aec1f7162bcd1b472c7108601009'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_quad26(path):
    if digest(path) != UPSTREAM_SHA256:
        raise ValueError('The upstream quadgram file does not match the reported experiment.')
    values = np.fromfile(path, dtype='<f4')
    if values.size != 26 ** 4 or not np.isfinite(values).all():
        raise ValueError('Expected 26**4 finite little-endian float32 log10 values.')
    return values.reshape((26,) * 4)


def build(square, quad26):
    """Return float32 quad correlations, single correlations and log marginals.

    Patterns are indexed by 7*row+column; coordinate index 6 denotes unknown.
    A fixed square cell contributes one letter. Each unassigned square cell is
    averaged uniformly over the unused alphabet for scoring only. Missing row
    or column coordinates sum compatible cell masses. Digit mass is 3% total.
    """
    square = square.replace('+', '?')
    known = [c for c in square if c in ALPHABET]
    unused = [c for c in ALPHABET if c not in square]
    if len(square) != 36 or len(known) != len(set(known)):
        raise ValueError('A square must contain 36 cells with injective known symbols.')
    if set(square) - set(ALPHABET + '?') or square.count('?') != len(unused):
        raise ValueError('Unassigned square cells must be represented by question marks.')
    q = 10. ** quad26.astype(float)
    q /= q.sum()
    letters = sum(q.sum(axis=tuple(j for j in range(4) if j != i))
                  for i in range(4)) / 4
    p = np.concatenate([.97 * letters, np.full(10, .003)])
    joint = np.einsum('a,b,c,d->abcd', p, p, p, p)
    joint[:26, :26, :26, :26] = q * (.97 ** 4)
    cells = np.zeros((36, 36))
    for i, c in enumerate(square):
        if c in ALPHABET:
            cells[i, ALPHABET.index(c)] = 1
        else:
            for candidate in unused:
                cells[i, ALPHABET.index(candidate)] = 1 / len(unused)
    masks = np.zeros((49, 36))
    for row in range(7):
        for column in range(7):
            for cell in range(36):
                if (row == 6 or cell // 6 == row) and (column == 6 or cell % 6 == column):
                    masks[7 * row + column] += cells[cell]
    values = np.einsum('ia,abcd->ibcd', masks, joint, optimize=True)
    values = np.einsum('jb,ibcd->ijcd', masks, values, optimize=True)
    values = np.einsum('kc,ijcd->ijkd', masks, values, optimize=True)
    values = np.einsum('ld,ijkd->ijkl', masks, values, optimize=True)
    marginal = masks @ p
    quad = np.log(np.maximum(values, 1e-30))
    for axis in range(4):
        shape = [1] * 4
        shape[axis] = 49
        quad -= np.log(np.maximum(marginal, 1e-30)).reshape(shape)
    coordinate = np.zeros((2, 7))
    for cell in range(36):
        mass = float(cells[cell] @ p)
        coordinate[0, cell // 6] += mass
        coordinate[1, cell % 6] += mass
    coordinate[:, 6] = 1
    independent = np.outer(coordinate[0], coordinate[1]).ravel()
    single = np.log(np.maximum(marginal, 1e-30) / np.maximum(independent, 1e-30))

    # Retain the original loop's accumulation order for the probability term.
    log_probability = []
    for row in range(7):
        for column in range(7):
            probability = 0.
            for cell, c in enumerate(square):
                if (row == 6 or cell // 6 == row) and (column == 6 or cell % 6 == column):
                    probability += (p[ALPHABET.index(c)] if c in ALPHABET else
                                    sum(p[ALPHABET.index(x)] for x in unused) / len(unused))
            log_probability.append(np.log(max(probability, 1e-30)))
    return (quad.astype('<f4'), single.astype('<f4'),
            np.asarray(log_probability, dtype='<f4'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quad26', required=True, type=Path)
    parser.add_argument('--square', required=True)
    parser.add_argument('--output-prefix', required=True, type=Path)
    args = parser.parse_args()
    args.output_prefix.parent.mkdir(parents=True, exist_ok=True)
    outputs = {}
    arrays = build(args.square, load_quad26(args.quad26))
    for label, values in zip(['quad49', 'single49', 'probability49'], arrays):
        path = Path(str(args.output_prefix) + '_' + label + '.bin')
        values.tofile(path)
        outputs[label] = {'path': str(path), 'sha256': digest(path),
                          'bytes': path.stat().st_size}
    print(json.dumps({'upstream_sha256': UPSTREAM_SHA256, 'square': args.square,
                      'outputs': outputs, 'scores_are_heuristic': True}, indent=2))


if __name__ == '__main__':
    main()
