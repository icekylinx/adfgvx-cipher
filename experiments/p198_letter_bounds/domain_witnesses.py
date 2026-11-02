#!/usr/bin/env python3
"""Construct all single-position symbol witnesses for unrestricted p198 losses.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
This is a feasibility proof, not a language search or a plaintext proposal.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, transposition_indices

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'
EXAMPLES = {(0, 'A'), (42, 'Z'), (84, '0'), (84, '9')}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_line(record):
    return (json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')


def coordinate_preimages(length, ranks):
    """Map each row-major coordinate to its transmitted frame position."""
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    sizes = [length // width + (c < length % width) for c in range(width)]
    starts = [sum(sizes[d] for d in range(width) if ranks[d] < ranks[c])
              for c in range(width)]
    mapping = [starts[p % width] + p // width for p in range(length)]
    assert sorted(mapping) == list(range(length))
    project_order = transposition_indices(length, ranks)
    assert all(project_order[source] == row_major
               for row_major, source in enumerate(mapping))
    return mapping


def construct(case, position, symbol, preimages):
    source, square = case['observed_ciphertext'], case['fixed_complete_square']
    length = len(source) + case['missing_count']
    target = preimages[2*position:2*position+2]
    other_losses = [i for i in range(length) if i not in target][:case['missing_count'] - 2]
    losses = sorted(target + other_losses)
    assert len(losses) == len(set(losses)) == 5
    cell = square.index(symbol)
    pair = COORDINATES[cell // 6] + COORDINATES[cell % 6]
    inserted = {i: 'A' for i in losses}
    inserted.update(zip(target, pair))
    received = iter(source)
    full = ''.join(inserted[i] if i in inserted else next(received)
                   for i in range(length))
    assert next(received, None) is None
    assert ''.join(c for i, c in enumerate(full) if i not in inserted) == source
    interim = ''.join(full[i] for i in preimages)
    plaintext = ''.join(square[6*COORDINATES.index(interim[i])
                               + COORDINATES.index(interim[i+1])]
                        for i in range(0, length, 2))
    assert plaintext[position] == symbol
    assert plaintext == decrypt(full, case['column_rank_order'], square)
    assert encrypt(plaintext, case['column_rank_order'], square) == full
    return {
        'case_id': case['id'],
        'plaintext_position': position,
        'requested_symbol': symbol,
        'target_coordinate_pair': pair,
        'target_ciphertext_indices_in_pair_order': target,
        'other_loss_positions': other_losses,
        'loss_positions': losses,
        'filled_missing_coordinates': ''.join(inserted[i] for i in losses),
        'completed_ciphertext': full,
        'plaintext': plaintext,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true', help='Check the recorded audit without rewriting it.')
    parser.add_argument('--output', type=Path, default=HERE / 'domain_witnesses.json')
    args = parser.parse_args()
    input_path = ROOT / 'experiments/p198_exact_sparse/inputs.json'
    catalog_path = ROOT / 'data/messages.json'
    cases = sorted((c for c in json.loads(input_path.read_text())['cases']
                    if c['kind'] == 'historical'), key=lambda c: c['id'])
    assert [c['id'] for c in cases] == ['p198_CHI-Nov13', 'p198_Nov13-15b']
    catalog = {m['id']: m for m in json.loads(catalog_path.read_text())['messages']}
    catalog_source = catalog['p198']['transcript']['analysis_ciphertext']
    reports, total, combined = [], 0, hashlib.sha256()
    for case in cases:
        source, square = case['observed_ciphertext'], case['fixed_complete_square']
        assert source == catalog_source and len(source) == 165
        assert set(source) <= set(COORDINATES) and case['missing_count'] == 5
        assert len(square) == 36 and set(square) == set(ALPHABET)
        assert all(a == '?' or a == b
                   for a, b in zip(case['partial_historical_square'], square))
        preimages = coordinate_preimages(170, case['column_rank_order'])
        case_digest, examples, count = hashlib.sha256(), [], 0
        domains = [set() for _ in range(85)]
        for position in range(85):
            for symbol in ALPHABET:
                record = construct(case, position, symbol, preimages)
                line = canonical_line(record)
                case_digest.update(line)
                combined.update(line)
                domains[position].add(record['plaintext'][position])
                count += 1
                if (position, symbol) in EXAMPLES:
                    examples.append(record)
        assert count == 85*36 == 3060
        assert all(domain == set(ALPHABET) for domain in domains)
        assert len(examples) == len(EXAMPLES)
        total += count
        reports.append({
            'case_id': case['id'],
            'column_rank_order': case['column_rank_order'],
            'fixed_complete_square': square,
            'fixed_square_status': case['fixed_square_status'],
            'source_ciphertext_sha256': hashlib.sha256(source.encode('ascii')).hexdigest(),
            'plaintext_positions_verified': 85,
            'attainable_domain_at_every_individual_position': ALPHABET,
            'constructive_witnesses_checked': count,
            'received_coordinates_preserved_per_witness': 165,
            'received_coordinates_changed_per_witness': 0,
            'inserted_coordinates_per_witness': 5,
            'target_pair_among_inserted_coordinates_per_witness': 2,
            'other_inserted_coordinates_per_witness': 3,
            'all_witnesses_reencrypt_exactly': True,
            'all_requested_symbols_attained': True,
            'witness_stream_sha256': case_digest.hexdigest(),
            'selected_examples': examples,
        })
    assert total == 6120
    result = {
        'schema': 'adfgvx-p198-single-position-domain-witnesses-v1',
        'project': 'ADFGVX Cipher',
        'authors': 'icekylinx and GPT-6 Astra Pro',
        'input_sha256': {str(p.relative_to(ROOT)): digest(p)
                         for p in [input_path, catalog_path]},
        'indexing': 'All plaintext and completed-ciphertext positions are zero-based. Loss positions refer to the 170-coordinate completed ciphertext, not the 165-coordinate received text.',
        'result': 'Every one of the 85 plaintext positions can contain any of the 36 alphabet symbols in a source-compatible five-loss witness, under each of the two frozen complete-key hypotheses.',
        'quantifiers': 'For each key, for each position, and for each symbol there exists a potentially different witness. This does not say that arbitrary symbols can be chosen independently at all 85 positions in one common witness.',
        'proof': [
            'A fixed columnar transposition is a permutation of the 170 coordinate positions. A chosen plaintext position therefore has two distinct preimages in the transmitted frame.',
            'Choose those two preimages as losses, and choose any three other distinct frame positions as the remaining losses. The construction uses the three smallest available positions.',
            'Place the 165 received coordinates, unchanged and in order, in the remaining 165 frame positions. This is always possible and preserves the entire received source.',
            'A complete bijective square contains every alphabet symbol exactly once. Fill the chosen target pair with the two coordinates of the requested symbol; fill the other three loss positions with A.',
            'Inverse transposition and pair decoding then produce the requested symbol at the chosen position. Re-encryption returns the constructed full frame; deleting its five chosen losses returns the source.',
            'The construction works independently for all 85 positions and all 36 symbols. Therefore no single plaintext position is fixed throughout this unrestricted five-loss family, even though joint restrictions across positions can hold.',
        ],
        'construction_rules': {
            'nominal_coordinates': 170,
            'received_coordinates': 165,
            'losses': 5,
            'target_pair_loss_positions': 'The two ciphertext preimages of the selected plaintext position.',
            'other_loss_positions': 'The three smallest distinct frame positions outside the target pair.',
            'target_pair_fills': 'The requested symbol pair in the fixed complete square.',
            'other_loss_fills': 'AAA',
            'source_order': 'All received coordinates fill the non-loss positions in increasing ciphertext order.',
        },
        'digest_format': 'SHA-256 of canonical JSON records, each encoded as ASCII with sorted keys, separators comma/colon without spaces, and one trailing newline. Record order: case_id lexical order, plaintext position 0 through 84, then symbol order ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789. Selected examples show the exact record fields. No witness is omitted from the digest or verification.',
        'total_constructive_witnesses_checked': total,
        'combined_witness_stream_sha256': combined.hexdigest(),
        'cases': reports,
        'limits': [
            'The complete squares are frozen heuristic hypotheses, not established historical p198 keys. The feasibility argument is conditional on those keys and the stated unrestricted loss model.',
            'The theorem concerns individual-position domains. It does not make every entire plaintext feasible and does not conflict with the separately proved at-least-three-digit joint bound for the Nov13-15b partial-square family.',
            'A restriction to consecutive five-coordinate losses, independently fixed loss positions, or additional source evidence would define a different family and can reduce individual-position domains.',
            'The inserted values and full example plaintexts are proof witnesses, not recovered text or likely historical readings. No language score is computed.',
        ],
        'newly_accepted_historical_plaintext_characters': 0,
    }
    if args.verify:
        assert json.loads(args.output.read_text()) == result
    else:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({
        'complete_key_hypotheses': len(cases),
        'positions_per_key': 85,
        'symbols_per_position': 36,
        'exact_constructive_witnesses_checked': total,
        'source_coordinates_preserved_per_witness': 165,
        'source_coordinate_changes': 0,
        'combined_witness_stream_sha256': combined.hexdigest(),
        'historical_plaintext_characters_accepted': 0,
    }, indent=2))


if __name__ == '__main__':
    main()
