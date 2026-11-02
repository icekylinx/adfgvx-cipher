#!/usr/bin/env python3
"""Independent word-score, log-counter, dataset and radio-model audit.

Read-only except for the requested report and a temporary compiled harness.
Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from __future__ import annotations

import argparse
import ast
import collections
import functools
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import struct
import subprocess
import tempfile

import numpy as np

HERE = Path(__file__).resolve().parent
RADIO = HERE.parent
ROOT = RADIO.parents[1]
WORD = ROOT / 'experiments/p198_word_search'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def float32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


class BackwardWordObjective:
    """Substring lookups and a backwards recurrence; no trie or forward DP."""

    def __init__(self, path):
        self.words, self.pairs = {}, {}
        with path.open() as source:
            self.word_count, self.pair_count = map(int, source.readline().split())
            for word_id in range(self.word_count):
                word, weight = source.readline().split()
                assert word not in self.words
                self.words[word] = (word_id, float32(float(weight)))
            for _ in range(self.pair_count):
                first, second, weight = source.readline().split()
                key = int(first), int(second)
                assert key not in self.pairs
                self.pairs[key] = float32(float(weight))
            assert not source.read().strip()
        assert len(self.pairs) == self.pair_count
        assert all(0 <= value <= 2 for value in self.pairs.values())

    def score(self, text):
        assert set(text) <= set(ALPHABET)
        matches = []
        for start, char in enumerate(text):
            choices = [(start + 1, -1, -.25 if char == 'X' else -3.)]
            for end in range(start + 1, min(len(text), start + 32) + 1):
                word = text[start:end]
                if word in self.words:
                    word_id, value = self.words[word]
                    choices.append((end, word_id, value))
            if char in '0123456789':
                for end in range(start + 1, min(len(text), start + 10) + 1):
                    if text[end - 1] not in '0123456789':
                        break
                    choices.append((end, -2, -1. - (end - start)))
            matches.append(choices)

        @functools.lru_cache(None)
        def suffix(start, previous_word):
            if start == len(text):
                return 0.
            return max(value +
                       (.65 * self.pairs.get((previous_word, current_word), 0.)
                        if previous_word >= 0 and current_word >= 0 else 0.) +
                       suffix(end, current_word)
                       for end, current_word, value in matches[start])

        return suffix(0, -1)


def word_tests(records, lexicon, compiler):
    objective = BackwardWordObjective(lexicon)
    texts = ['', 'X', 'X' * 90, '0', '0123456789',
             '012345678901234567890123456789', 'BITTE', 'BETTE',
             'ANXDENKOMMANDANTEN', 'QUITTUNGXERBETEN', 'M1', '5X5X5', 'M' * 12]
    for row in records['completed']:
        texts.append(row['best_candidate']['plaintext'])
        truth = (row['input'].get('evaluation_only') or {}).get('plaintext')
        if truth:
            texts.append(truth)
        if row.get('initial_state'):
            texts.append(row['initial_state']['plaintext'])
    rng = random.Random(202611021710)
    for _ in range(40):
        texts.append(''.join(rng.choice(ALPHABET) for _ in range(rng.randrange(1, 95))))
    texts = list(dict.fromkeys(texts))
    with tempfile.TemporaryDirectory(prefix='adfgvx-independent-word-') as directory:
        executable = Path(directory) / 'score'
        subprocess.run([compiler, '-O2', '-std=c++17', str(HERE / 'word_score_harness.cpp'),
                        '-o', str(executable)], check=True)
        run = subprocess.run([str(executable), str(lexicon.resolve())],
                             input='\n'.join(texts) + '\n', text=True,
                             capture_output=True, check=True)
    compiled = list(map(float, run.stdout.splitlines()))
    assert len(compiled) == len(texts)
    backwards = [objective.score(text) for text in texts]
    errors = [abs(a - b) for a, b in zip(compiled, backwards)]
    assert max(errors) < 1e-9
    specification = importlib.util.spec_from_file_location('reviewed_word_verifier', WORD / 'verify.py')
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    forward = module.WordModel(lexicon)
    forward_errors = [abs(forward.score(text) - value) for text, value in zip(texts, backwards)]
    assert max(forward_errors) < 1e-9
    return {'texts': len(texts), 'cpp_vs_backward_reference_max_abs_error': max(errors),
            'forward_python_vs_backward_reference_max_abs_error': max(forward_errors),
            'lexicon_sha256': sha(lexicon), 'word_count': objective.word_count,
            'pair_count': objective.pair_count}


def original_logs(records, base):
    if base is None:
        return {'checked': False, 'reason': '--original-log-root was not provided',
                'archived_completed_cases': len(records['completed']),
                'pending_cases_not_counted': len(records['pending'])}
    specifications = {'pilot': base / 'pilot_manifest.json',
                      'adaptive_weight2': base / 'extended_manifest.json',
                      'broad_partial': base / 'broad/manifest.json',
                      'unknown_square_controls': base / 'unknown_controls_manifest.json'}
    jobs = {}
    for batch, path in specifications.items():
        for job in read(path)['jobs']:
            jobs[batch + '/' + job['id']] = (path.parent, job)
    completed = proposals = 0
    exact_truth_seeds = []
    for row in records['completed']:
        folder, job = jobs[row['case_id']]
        # The four archived manifests place each input/log alongside its manifest.
        # Resolve the basename so a copied original-log directory is portable.
        input_path = folder / Path(job['input']).name
        log = folder / (job['id'] + '.jsonl')
        assert log.with_suffix('.result.json').is_file()
        events = [json.loads(line) for line in log.read_text().splitlines()]
        assert sha(log) == row['original_output_sha256']
        assert events[-1] == row['final_event']
        assert max(events, key=lambda event: event['score']) == row['best_candidate']
        assert all(a['proposal'] <= b['proposal'] and a['restart'] <= b['restart']
                   and a['score'] <= b['score'] for a, b in zip(events, events[1:]))
        assert events[-1]['proposal'] == row['completed_proposals']
        assert events[-1]['seconds'] >= job['seconds']
        fields = input_path.read_text().split()
        width, missing = int(fields[0]), int(fields[1])
        assert missing == 5 and fields[2] == job['partial_square']
        assert list(map(int, fields[3:3 + width])) == job['ranks']
        assert fields[3 + width] == job['source'] and len(fields) == width + 4
        truth = (job.get('evaluation_only') or {}).get('plaintext')
        initial = (row.get('initial_state') or {}).get('plaintext')
        if truth and initial == truth:
            exact_truth_seeds.append(row['case_id'])
        completed += 1
        proposals += events[-1]['proposal']
    assert len(set(records['declared_cases'])) == len(records['completed']) + len(records['pending'])
    return {'checked': True, 'completed_logs': completed, 'completed_proposals': proposals,
            'exact_truth_seed_states': exact_truth_seeds, 'all_inputs_match_manifest': True,
            'pending_cases_not_counted': len(records['pending']),
            'engine_binary_matches_archive': sha(base / 'word_loss') == records['engine_binary_sha256']}


def radio_counts(rows):
    counts = collections.Counter()
    grams = 0
    for row in rows:
        for span in row['plaintext_layer'].split('?'):
            values = [ALPHABET.index(c) if c in ALPHABET[:26] else 26 for c in span]
            for a, b, c, d in zip(values, values[1:], values[2:], values[3:]):
                counts[((a * 27 + b) * 27 + c) * 27 + d] += 1
                grams += 1
    probabilities = np.full(27 ** 4, .01, dtype=np.float64)
    for index, count in counts.items():
        probabilities[index] += count
    return probabilities / probabilities.sum(), grams


def marginals(probabilities, alphabet_size):
    base = probabilities.reshape((alphabet_size,) * 4)
    table = np.empty((alphabet_size + 1,) * 4, dtype=np.float64)
    for mask in range(16):
        axes = tuple(i for i in range(4) if mask >> i & 1)
        target = tuple(alphabet_size if mask >> i & 1 else slice(alphabet_size) for i in range(4))
        table[target] = base.sum(axis=axes) if axes else base
    return table


def reconstruct_models(book_path, model_directory):
    base_data, class_data = read(RADIO / 'dataset.json'), read(RADIO / 'class_dataset.json')
    base_provenance = read(RADIO / 'model_provenance.json')
    class_provenance = read(RADIO / 'class_model_provenance.json')
    assert sha(book_path) == base_provenance['book_quad_sha256'] == class_provenance['book_quad_sha256']
    assert sha(RADIO / 'dataset.json') == base_provenance['source_dataset_sha256']
    assert sha(RADIO / 'class_dataset.json') == class_provenance['dataset_sha256']
    # Extract radix-36 digits from a flat index, independently of np.indices.
    working = np.arange(36 ** 4, dtype=np.int64)
    coordinates = []
    for _ in range(4):
        coordinates.append(working % 36)
        working //= 36
    coordinates.reverse()
    folded = np.zeros(36 ** 4, dtype=np.int64)
    digit_count = np.zeros(36 ** 4, dtype=np.int8)
    for values in coordinates:
        folded = folded * 27 + np.minimum(values, 26)
        digit_count += values >= 26
    book = np.power(10., np.fromfile(book_path, dtype='<f4').astype(np.float64))
    book /= book.sum()
    radio, grams = radio_counts(base_data['training_records'])
    assert grams == base_provenance['training_quadgrams']
    expanded = radio[folded] / (10. ** digit_count)
    assert abs(expanded.sum() - 1) < 1e-10
    mixture = .5 * (book + expanded)
    results = {}

    def compare(name, probabilities):
        encoded = np.log10(probabilities).astype('<f4').tobytes()
        assert encoded == (model_directory / name).read_bytes(), name
        results[name] = {'sha256': hashlib.sha256(encoded).hexdigest(), 'bytes': len(encoded)}

    compare('radio_book36_quad.bin', mixture)
    compare('radio_book37_quad_marginal.bin', marginals(mixture, 36))
    book27 = np.bincount(folded, weights=book, minlength=27 ** 4)
    class_radio, class_grams = radio_counts(class_data['training_records'])
    assert class_grams == class_provenance['training_quadgrams']
    for prefix, probabilities in [('book_class', book27),
                                   ('radio_book_class', .5 * (book27 + class_radio))]:
        compare(prefix + '36_quad.bin', probabilities[folded])
        marginal = marginals(probabilities, 27)
        lookup = np.array(list(range(26)) + [26] * 10 + [27])
        compare(prefix + '37_quad_marginal.bin', marginal[np.ix_(lookup, lookup, lookup, lookup)])
    checks = []
    for name, data, held_field, validation_field in [
            ('base', base_data, 'held_out_families', 'held_out_records'),
            ('class', class_data, 'further_held_out_families', 'validation_records')]:
        training = data['training_records']
        held = set(data[held_field])
        assert not ({row['family'] for row in training} & held)
        held_substrings = {span[i:i + 32] for row in data[validation_field]
                           for span in row['plaintext_layer'].split('?')
                           for i in range(len(span) - 31)}
        overlaps = [row['id'] for row in training
                    if any(span[i:i + 32] in held_substrings
                           for span in row['plaintext_layer'].split('?')
                           for i in range(len(span) - 31))]
        assert not overlaps
        assert len({row['plaintext_layer'] for row in training}) == len(training)
        checks.append({'dataset': name, 'training_rows': len(training),
                       'held_families': len(held),
                       'training_heldout_32gram_overlaps': len(overlaps)})
    return results, checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quad', type=Path, required=True)
    parser.add_argument('--lexicon', type=Path, required=True)
    parser.add_argument('--models', type=Path, required=True)
    parser.add_argument('--original-log-root', type=Path)
    parser.add_argument('--records', type=Path, default=WORD / 'records.json')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--compiler', default='c++')
    args = parser.parse_args()
    records = read(args.records)
    assert records['engine_source_sha256'] == sha(WORD / 'word_loss.cpp')
    assert records['lexicon_sha256'] == sha(args.lexicon)
    assert records['quad_model_sha256'] == sha(args.quad)
    words = word_tests(records, args.lexicon, args.compiler)
    logs = original_logs(records, args.original_log_root)
    models, splits = reconstruct_models(args.quad, args.models)
    exclusions = None
    for node in ast.parse((RADIO / 'build.py').read_text()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'EXCLUDED_LATE_KEYS'
                                               for t in node.targets):
            exclusions = ast.literal_eval(node.value)
    assert exclusions and 'Nov25-28' in exclusions and 'Nov25-27' not in exclusions
    report = {'prepared_by': ['icekylinx', 'GPT-6 Astra Pro'],
              'snapshot_records_sha256': sha(args.records),
              'snapshot_completed_cases': len(records['completed']),
              'snapshot_pending_cases': len(records['pending']),
              'audit_source_sha256': sha(Path(__file__)),
              'word_harness_sha256': sha(HERE / 'word_score_harness.cpp'),
              'word_score_check': words, 'original_log_audit': logs,
              'independent_model_reconstruction': models, 'split_checks': splits,
              'issues': [{'severity': 'latent selector typo', 'status': 'resolved',
                          'location': 'radio_domain_model/build.py EXCLUDED_LATE_KEYS',
                          'detail': 'Nov25-27 was corrected to catalog key Nov25-28. '
                                    'No frozen training row used that period; the dataset and all model bytes are unchanged.',
                          'frozen_dataset_sha256': sha(RADIO / 'dataset.json')}],
              'scope': 'Current completed archive only; pending jobs are not counted. '
                       'Explicit source-family and exact-overlap separation do not establish statistical independence. '
                       'No repository file is modified by this audit except an explicitly requested report path.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
