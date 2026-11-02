"""Small independent arithmetic checks for the anchored-square experiment."""
import hashlib
import math

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COORDINATES = 'ADFGVX'


def case_label(case, restarts, iterations):
    return f"{case['id']}__{case['key_id']}__k{case['width']:02d}__r{restarts}i{iterations}"


def seed_for(label):
    return int(hashlib.sha256(label.encode()).hexdigest()[:15], 16)


def validate_case(case):
    width = case['width']
    square = case['partial_square']
    ciphertext = case['ciphertext']
    assert isinstance(width, int) and 2 <= width <= 40
    assert len(square) == 36 and set(square) <= set(ALPHABET + '?')
    supplied = square.replace('?', '')
    assert len(set(supplied)) == len(supplied)
    assert len(ciphertext) >= 8 and len(ciphertext) % 2 == 0
    assert set(ciphertext) <= set(COORDINATES + '?')
    assert len(ciphertext) < 4095


def untranspose(ciphertext, ranks):
    width = len(ranks)
    assert sorted(ranks) == list(range(1, width + 1))
    n = len(ciphertext)
    streams = [''] * width
    offset = 0
    for col in sorted(range(width), key=lambda j: ranks[j]):
        length = n // width + (col < n % width)
        streams[col] = ciphertext[offset:offset + length]
        offset += length
    assert offset == n
    return ''.join(streams[i % width][i // width] for i in range(n))


def domains(ciphertext, ranks, square):
    assert len(square) == 36 and set(square) == set(ALPHABET)
    stream = untranspose(ciphertext, ranks)
    assert len(stream) % 2 == 0
    result = []
    for first, second in zip(stream[::2], stream[1::2]):
        rows = range(6) if first == '?' else [COORDINATES.index(first)]
        cols = range(6) if second == '?' else [COORDINATES.index(second)]
        result.append(''.join(sorted(square[r * 6 + c] for r in rows for c in cols)))
    return result


def encrypt(plaintext, ranks, square):
    assert len(square) == 36 and set(square) == set(ALPHABET)
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    stream = ''.join(COORDINATES[square.index(c) // 6] + COORDINATES[square.index(c) % 6] for c in plaintext)
    return ''.join(stream[col::len(ranks)] for col in sorted(range(len(ranks)), key=lambda j: ranks[j]))


def control_evaluation(case, best, letter_domains):
    truth = case['evaluation_only']['plaintext']
    plaintext = best['plaintexts'][0]
    predicted = encrypt(truth, best['ranks'], best['square'])
    observed = case['ciphertext']
    return {
        'fully_observed_plaintext_positions': sum(c != '?' for c in plaintext),
        'correct_fully_observed_positions': sum(c != '?' and c == t for c, t in zip(plaintext, truth)),
        'observed_coordinates': sum(c != '?' for c in observed),
        'compatible_observed_coordinates': sum(c != '?' and c == p for c, p in zip(observed, predicted)),
        'true_plaintext_in_every_domain': all(t in d for t, d in zip(truth, letter_domains)),
        'truth_was_not_supplied_to_search': True,
    }


def verify_record(record, known_cases):
    case, best = record['case'], record['best']
    validate_case(case)
    assert case in known_cases, 'Record does not use one of the frozen cases'
    restarts, iterations = record['requested_restarts'], record['iterations_per_restart']
    assert isinstance(restarts, int) and restarts > 0
    assert isinstance(iterations, int) and iterations > 0
    assert record['seed'] == seed_for(case_label(case, restarts, iterations))
    assert math.isfinite(best['score'])
    assert 0 <= best['restart'] < restarts
    assert len(best['ranks']) == case['width']
    assert len(best['plaintexts']) == 1
    assert best['known_square_cells'] == sum(c != '?' for c in case['partial_square'])
    assert all(a == '?' or a == b for a, b in zip(case['partial_square'], best['square']))
    actual = domains(case['ciphertext'], best['ranks'], best['square'])
    assert record['domains'] == actual
    assert best['plaintexts'][0] == ''.join(d if len(d) == 1 else '?' for d in actual)
    witness = ''.join(d[0] for d in actual)
    encoded = encrypt(witness, best['ranks'], best['square'])
    assert all(c == '?' or c == p for c, p in zip(case['ciphertext'], encoded))
    assert record['accepted_historical_plaintext'] is False
    if 'evaluation_only' in case:
        truth = case['evaluation_only']
        assert encrypt(truth['plaintext'], truth['ranks'], truth['square']) == truth['full_ciphertext']
        assert all(c == '?' or c == p for c, p in zip(case['ciphertext'], truth['full_ciphertext']))
        assert record['control_evaluation'] == control_evaluation(case, best, actual)
    return {'label': case_label(case, restarts, iterations),
            'observed_coordinates_preserved_by_domain_witness': sum(c != '?' for c in case['ciphertext']),
            'known_square_cells_preserved': sum(c != '?' for c in case['partial_square']),
            'requested_proposal_slots': restarts * iterations,
            'control_evaluation': record.get('control_evaluation')}
