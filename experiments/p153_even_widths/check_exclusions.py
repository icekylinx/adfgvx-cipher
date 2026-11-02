#!/usr/bin/env python3
"""Independent necessary-condition proof excluding the six other even widths.

A repeated plaintext letter must repeat both coordinate components. Therefore
both columns in a physical pair must match the repetition pattern of that
pair's crib letters. This proof needs no square fitting or C search.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def matches(chunk, crib_column):
    if len(chunk) != len(crib_column):
        return False
    return all(crib_column[a] == '?' or crib_column[b] == '?' or crib_column[a] != crib_column[b]
               or chunk[a] == chunk[b] for a in range(len(chunk)) for b in range(a))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=HERE / 'historical_input.txt')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    crib, ciphertext, _, _ = args.input.read_text().split()
    assert len(crib) == 66 and len(ciphertext) == 132
    records = []
    # Every real transmitted column is a contiguous substring. Relaxing the
    # segmentation can only add possible columns, so fewer than two starts is
    # a valid exclusion without enumerating the actual segmentations.
    for width, physical_pair in [(14, 1), (16, 1), (20, 2), (24, 5)]:
        letters = crib[physical_pair::width // 2]
        starts = [i for i in range(len(ciphertext) - len(letters) + 1)
                  if matches(ciphertext[i:i + len(letters)], letters)]
        assert len(starts) < 2
        records.append({'width': width, 'method': 'Relaxation to every contiguous source substring',
                        'physical_pair_zero_based': physical_pair, 'crib_column': letters,
                        'required_distinct_columns': 2, 'possible_substring_starts': starts,
                        'excluded': True})
    # The two remaining widths need only 1 and 325 actual segmentations.
    for width in [22, 26]:
        q, remainder = divmod(132, width)
        witnesses = []
        for long_slots in combinations(range(width), remainder):
            long_set = set(long_slots)
            chunks = []
            offset = 0
            for slot in range(width):
                length = q + (slot in long_set)
                chunks.append(ciphertext[offset:offset + length])
                offset += length
            assert offset == 132
            for pair in range(width // 2):
                letters = crib[pair::width // 2]
                eligible = [i for i, chunk in enumerate(chunks) if matches(chunk, letters)]
                if len(eligible) < 2:
                    witnesses.append({'long_transmission_slots_zero_based': list(long_slots),
                                      'failing_physical_pair_zero_based': pair,
                                      'eligible_transmission_slots_zero_based': eligible})
                    break
            else:
                raise AssertionError('A segmentation survives this necessary-condition test')
        records.append({'width': width, 'method': 'Every actual segmentation fails a repeated-letter column requirement',
                        'segmentations': len(witnesses), 'witnesses': witnesses, 'excluded': True})
    result = {'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'all_six_other_even_widths_excluded': True, 'records': records,
              'scope': 'Conditional on the supplied first crib and ordinary transposition geometry. Repeated-letter constraints are necessary only; no historical plaintext probability or unrestricted uniqueness is claimed.'}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'excluded_widths': [row['width'] for row in records],
                      'proof_uses_no_C_engine_or_square_search': True}))


if __name__ == '__main__':
    main()
