#!/usr/bin/env python3
"""Exact coupled domain/column-order/deletion feasibility, bounded by node cap.

Scratch research. A capped result is not an exclusion. Domains are independent
plaintext alternatives, while one injective square is shared by the full body.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time

A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
C = 'ADFGVX'


class Capped(Exception):
    pass


class Search:
    def __init__(self, case, cap):
        self.case, self.cap = case, cap
        self.width = case['width']
        self.domains = case['domains']
        self.target = case['target'].replace('-', '?')
        self.length = 2*len(self.domains)
        self.deleted = self.length-len(self.target)
        assert self.width % 2 == 0 and self.deleted >= 0
        self.square = case['square']
        assert len(self.square) == 36
        self.cells = [i for i, c in enumerate(self.square) if c == '?']
        self.unused = sorted(set(A)-set(self.square))
        assert len(self.unused) == len(self.cells)
        assert len(self.unused) <= 8
        self.permutations = list(itertools.permutations(self.unused))
        self.allkeys = (1 << len(self.permutations))-1
        size = (len(self.permutations)+7)//8
        data = [[bytearray(size) for _ in self.unused] for _ in self.cells]
        label_index = {c: i for i, c in enumerate(self.unused)}
        for i, assignment in enumerate(self.permutations):
            for j, label in enumerate(assignment):
                data[j][label_index[label]][i//8] |= 1 << (i % 8)
        maps = [{c: int.from_bytes(data[j][i], 'little') for i, c in enumerate(self.unused)}
                for j in range(len(self.cells))]
        cell_map = dict(zip(self.cells, maps))
        self.masks = {}
        for domain in set(self.domains):
            cell_masks = []
            for i, label in enumerate(self.square):
                if label != '?':
                    cell_masks.append(self.allkeys if label in domain else 0)
                else:
                    mask = 0
                    for c in domain:
                        mask |= cell_map[i].get(c, 0)
                    cell_masks.append(mask)
            patterns = []
            for row in range(7):
                for col in range(7):
                    value = 0
                    for i, bitset in enumerate(cell_masks):
                        if (row == 6 or row == i//6) and (col == 6 or col == i % 6):
                            value |= bitset
                    patterns.append(value)
            self.masks[domain] = patterns
        self.by_position = [self.masks[d] for d in self.domains]
        self.columns = [list(range(c, self.length, self.width)) for c in range(self.width)]
        self.values = [C.index(c) if c in C else 6 for c in self.target]
        self.pairs = [[6, 6] for _ in self.domains]
        self.nodes = self.global_nodes = self.local_nodes = 0
        self.cache = set()
        self.history = []
        self.found = None
        self.hint = case.get('column_order_hint', list(range(self.width)))
        self.depth_profile = {}

    def tick(self, local=False):
        self.nodes += 1
        self.local_nodes += int(local)
        self.global_nodes += int(not local)
        if self.nodes > self.cap:
            raise Capped

    def memo_key(self, used, offset, keys):
        # Exact key sets, never a hash-only exclusion. Most late states have a
        # small key set; represent those by indices instead of sparse 5KB ints.
        if keys.bit_count() <= 12:
            indices = []
            while keys:
                low = keys & -keys
                indices.append(low.bit_length()-1)
                keys -= low
            keyset = tuple(indices)
        else:
            keyset = keys
        context = 0
        for group in range(self.width//2):
            first, second = 2*group, 2*group+1
            if bool(used & (1 << first)) == bool(used & (1 << second)):
                continue
            for row_index in range(group, len(self.domains), self.width//2):
                row, col = self.pairs[row_index]
                context = (context << 3) | row
                context = (context << 3) | col
        return used, offset, context, keyset

    def visit(self, used, offset, losses, keys):
        self.tick()
        if used == (1 << self.width)-1:
            assert offset == len(self.target) and losses == self.deleted
            self.found = (keys, list(self.history))
            return True
        depth = used.bit_count()
        profile = self.depth_profile.setdefault(depth, {'visits': 0, 'minimum_global_keys': len(self.permutations)})
        profile['visits'] += 1
        profile['minimum_global_keys'] = min(profile['minimum_global_keys'], keys.bit_count())
        memo = self.memo_key(used, offset, keys) if depth >= self.width-4 else None
        if memo is not None and memo in self.cache:
            return False
        for loss in range(self.deleted-losses+1):
            for column in self.hint:
                if used & (1 << column):
                    continue
                positions = self.columns[column]
                if loss > len(positions) or offset+len(positions)-loss > len(self.target):
                    continue
                alignment = []
                if self.align(column, positions, 0, offset, loss, keys, used, losses, alignment):
                    return True
        if memo is not None and len(self.cache) < 200000:
            self.cache.add(memo)
        return False

    def align(self, column, positions, i, offset, remaining_loss, keys, used, losses, alignment):
        self.tick(True)
        if remaining_loss > len(positions)-i:
            return False
        if i == len(positions):
            assert remaining_loss == 0
            self.history.append((column, tuple(alignment)))
            found = self.visit(used | (1 << column), offset, losses+alignment.count(None), keys)
            self.history.pop()
            return found
        pos = positions[i]
        pt, side = divmod(pos, 2)
        if offset < len(self.target) and len(positions)-i > remaining_loss:
            value = self.values[offset]
            old = self.pairs[pt][side]
            assert old == 6
            self.pairs[pt][side] = value
            row, col = self.pairs[pt]
            narrowed = keys & self.by_position[pt][7*row+col]
            if narrowed:
                alignment.append(offset)
                if self.align(column, positions, i+1, offset+1, remaining_loss,
                              narrowed, used, losses, alignment):
                    self.pairs[pt][side] = old
                    return True
                alignment.pop()
            self.pairs[pt][side] = old
        if remaining_loss:
            alignment.append(None)
            if self.align(column, positions, i+1, offset, remaining_loss-1,
                          keys, used, losses, alignment):
                return True
            alignment.pop()
        return False

    def witness(self):
        keys, history = self.found
        index = (keys & -keys).bit_length()-1
        square = list(self.square)
        for cell, label in zip(self.cells, self.permutations[index]):
            square[cell] = label
        square = ''.join(square)
        observed = ['?']*self.length
        order, target_to_interim = [], [None]*len(self.target)
        for column, alignment in history:
            order.append(column)
            for pos, source_index in zip(self.columns[column], alignment):
                if source_index is not None:
                    observed[pos] = self.target[source_index]
                    target_to_interim[source_index] = pos
        plaintext, interim = '', ''
        for i, domain in enumerate(self.domains):
            choices = []
            for c in domain:
                cell = square.index(c)
                pair = C[cell//6]+C[cell % 6]
                if all(a == '?' or a == b for a, b in zip(observed[2*i:2*i+2], pair)):
                    choices.append((c, pair))
            assert choices
            c, pair = choices[0]
            plaintext += c
            interim += pair
        full = ''.join(interim[pos] for col in order for pos in self.columns[col])
        kept, deleted = [], []
        cursor = 0
        for col, alignment in history:
            for source_index in alignment:
                if source_index is None:
                    deleted.append(cursor)
                else:
                    assert source_index == len(kept)
                    kept.append(cursor)
                cursor += 1
        assert len(deleted) == self.deleted
        assert all(c == '?' or c == full[i] for c, i in zip(self.target, kept))
        assert all(c in d for c, d in zip(plaintext, self.domains))
        return dict(square=square, plaintext=plaintext, column_order=order,
                    full_ciphertext=full, retained_transmitted_indices=kept,
                    deleted_transmitted_indices=deleted, target_to_interim=target_to_interim,
                    remaining_global_keys=keys.bit_count())

    def run(self):
        start = time.monotonic()
        try:
            feasible = self.visit(0, 0, 0, self.allkeys)
            status = 'feasible' if feasible else 'excluded'
        except Capped:
            status = 'capped'
        return dict(id=self.case['id'], status=status, seconds=time.monotonic()-start,
                    nodes=self.nodes, local_nodes=self.local_nodes, global_nodes=self.global_nodes,
                    exact_memo_states=len(self.cache), square_completions=len(self.permutations),
                    depth_profile=self.depth_profile,
                    witness=self.witness() if self.found else None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--cap', type=int, default=1000000)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    cases = data if isinstance(data, list) else data.get('cases', [data])
    results = []
    for case in cases:
        print('Starting', case['id'], flush=True)
        result = Search(case, args.cap).run()
        results.append(result)
        print(json.dumps({k: v for k, v in result.items() if k != 'witness'}), flush=True)
        if args.output:
            args.output.write_text(json.dumps(results, indent=2)+'\n')
    if not args.output:
        print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
