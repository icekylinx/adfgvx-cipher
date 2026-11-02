"""Make segmentation_profile_batch inputs from rankings or complete widths."""
from pathlib import Path
from itertools import combinations
import argparse
import json


def all_segments(width):
    if width == 16:
        for aa in combinations(range(16), 4):
            amask = sum(1 << col for col in aa)
            remaining = [col for col in range(16) if col not in aa]
            for cc in combinations(remaining, 4):
                cmask = sum(1 << col for col in cc)
                bb = [col for col in remaining if col not in cc]
                yield amask, 65535^cmask, [col+1 for col in list(aa)+bb+list(cc)]
    elif width == 18:
        for aa in combinations(range(18), 6):
            mask = sum(1 << col for col in aa)
            bb = [col for col in range(18) if col not in aa]
            yield mask, 0, [col+1 for col in list(aa)+bb]
    else:
        raise ValueError('Complete enumeration is defined here only for widths16 and18')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--ranking', type=Path)
    group.add_argument('--all-width', type=int, choices=[16, 18])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.ranking:
        unique = {}
        for line in args.ranking.open():
            row = json.loads(line)
            if row.get('kind') != 'candidate': continue
            key = row['a_mask'], row['c_mask']
            if key not in unique:
                unique[key] = (row['a_mask'], 65535^row['c_mask'], row['matching_seed_ranks'])
        count = len(unique); rows = unique.values()
    else:
        count = 900900 if args.all_width == 16 else 18564
        rows = all_segments(args.all_width)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w') as stream:
        stream.write(str(count)+'\n')
        for mask1, mask2, ranks in rows:
            stream.write(f'{mask1} {mask2} '+' '.join(map(str, ranks))+'\n')
    print(json.dumps({'segmentations': count, 'output': str(args.output)}))


if __name__ == '__main__': main()
