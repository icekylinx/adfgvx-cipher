#!/usr/bin/env python3
"""Verify family-held-out datasets and all recorded loss-search witnesses.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
The witness arithmetic and optional objectives use a separate Python
implementation, not the search engine. No historical plaintext is accepted.
"""
import argparse
import importlib.util
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


witness = load('independent_loss_witness', HERE.parent / 'p198_word_search/verify.py')
builder = load('radio_dataset_builder', HERE / 'build.py')
class_builder = load('radio_class_builder', HERE / 'build_class_model.py')


def verify_numeric_dataset():
    data = json.loads((HERE / 'numeric_dataset.json').read_text())
    assert witness.sha(ROOT / 'data/keys.json') == data['key_catalog_sha256']
    keys = {k['id']: k for k in json.loads((ROOT / 'data/keys.json').read_text())['keys']}
    for i, case in enumerate(data['controls']):
        key = keys[case['key_id']]
        partial = key['square']
        if key['id'] == 'Nov13-15b':
            partial = partial[:17] + 'Y' + partial[18:]
        assert partial == case['partial_square']
        assert key['column_rank_order'] == case['column_rank_order']
        rng = random.Random(202611021715 + i)
        unused = sorted(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') - set(partial))
        rng.shuffle(unused)
        symbols = iter(unused)
        square = ''.join(next(symbols) if c == '?' else c for c in partial)
        truth = (case['complete_authored_text'] + 'XXXXX')[:85]
        assert truth == case['truth'] and square == case['square']
        assert any(c.isdigit() for c in truth)
        assert case['truth_classes'] == ''.join('#' if c.isdigit() else c for c in truth)
        full = witness.encrypt_independent(truth, key['column_rank_order'], square)
        loss = sorted(rng.sample(range(170), 5))
        assert full == case['full_ciphertext'] and loss == case['loss_positions']
        assert ''.join(full[p] for p in loss) == case['fill']
        assert ''.join(c for p, c in enumerate(full) if p not in loss) == case['received_ciphertext']
    return data


def verify(model_directory=None, book_quad=None, lexicon=None):
    assert builder.make_dataset() == json.loads((HERE / 'dataset.json').read_text())
    assert class_builder.prepare() == json.loads((HERE / 'class_dataset.json').read_text())
    verify_numeric_dataset()
    summaries = []
    model_names = {'book': book_quad, 'radio': 'radio_book36_quad.bin',
                   'book_class': 'book_class36_quad.bin',
                   'radio_class': 'radio_book_class36_quad.bin'}
    for stem, dataset_name in [('loss_controls', 'dataset.json'),
                                ('class_loss_controls', 'class_dataset.json'),
                                ('numeric_loss_controls', 'numeric_dataset.json')]:
        data = json.loads((HERE / dataset_name).read_text())
        report = json.loads((HERE / (stem + '.json')).read_text())
        assert report['dataset_sha256'] == witness.sha(HERE / dataset_name)
        assert report['engine_source_sha256'] == witness.sha(HERE / 'quad_loss.cpp')
        assert report['completed_utc'] > report['started_utc']
        assert report['truth_used_as_seed'] is False
        controls = {c['id']: c for c in data['controls']}
        tables = {}
        for name, expected in report['model_sha256'].items():
            relative = model_names[name]
            path = Path(relative) if name == 'book' and relative else (
                model_directory / relative if model_directory and relative else None)
            if path:
                assert witness.sha(path) == expected
                tables[name] = witness.load_quad(path)
        seen = set()
        counts = {}
        proposals = objective_checks = 0
        for row in report['results']:
            key = (row['control_id'], row['model'])
            assert key not in seen
            seen.add(key)
            c = controls[row['control_id']]
            ranks, partial, received = c['column_rank_order'], c['partial_square'], c['received_ciphertext']
            truth = {'plaintext': c['truth'], 'square': c['square'],
                     'loss': c['loss_positions'], 'fill': c['fill']}
            assert witness.check_witness(truth, ranks, partial, received) == c['full_ciphertext']
            best, final = row['best_candidate'], row['final_event']
            witness.check_witness(best, ranks, partial, received)
            witness.check_witness(final, ranks, partial, received)
            assert row['completed_proposals'] == final['proposal'] >= best['proposal']
            assert row['completed_restarts'] == final['restart']
            assert final['seconds'] >= report['seconds_per_job']
            assert abs(best['score'] - final['score']) < 1e-6
            assert row['truth_seeded'] is False and best['word_weight'] == 0
            correct = sum(a == b for a, b in zip(c['truth'], best['plaintext']))
            class_correct = sum(a == b or (a.isdigit() and b.isdigit())
                                for a, b in zip(c['truth'], best['plaintext']))
            assert row['correct_characters'] == correct
            assert row['digit_class_accuracy'] == class_correct
            assert row['exact_plaintext'] == (correct == len(c['truth']))
            assert row['source_coordinates_preserved'] == len(received) == 165
            assert abs(row['best_score_minus_truth'] - best['score'] + row['truth_score']) < 1e-6
            if row['model'] in tables:
                values = tables[row['model']]
                assert abs(witness.quad_score(best['plaintext'], values) - best['score']) < 1e-6
                assert abs(witness.quad_score(c['truth'], values) - row['truth_score']) < 1e-6
                objective_checks += 1
            counts.setdefault(row['model'], {'runs': 0, 'exact': 0, 'correct_characters': 0,
                                              'digit_class_correct': 0, 'digit_class_exact': 0})
            counts[row['model']]['runs'] += 1
            counts[row['model']]['exact'] += row['exact_plaintext']
            counts[row['model']]['correct_characters'] += correct
            counts[row['model']]['digit_class_correct'] += class_correct
            counts[row['model']]['digit_class_exact'] += class_correct == len(c['truth'])
            proposals += row['completed_proposals']
        assert len(seen) == len(controls) * len(report['model_sha256'])
        summaries.append({'batch': stem, 'models': counts,
                          'completed_mutation_proposals': proposals,
                          'objective_pairs_recomputed': objective_checks})
    historical_path = HERE / 'conditional_targets.json'
    historical = 0
    if historical_path.is_file():
        report = json.loads(historical_path.read_text())
        assert report.get('completed_utc')
        assert report['engine_source_sha256'] == witness.sha(HERE / 'quad_loss.cpp')
        jobs = {j['id']: j for j in report['jobs']}
        source = next(m for m in json.loads((ROOT / 'data/messages.json').read_text())['messages']
                      if m['id'] == 'p198')['transcript']['analysis_ciphertext']
        words = witness.WordModel(lexicon) if lexicon else None
        if lexicon:
            assert witness.sha(lexicon) == report['lexicon_sha256']
        for row in report['results']:
            j = jobs[row['id']]
            assert j['received_ciphertext'] == source
            best, final = row['best_candidate'], row['final_event']
            witness.check_witness(best, j['column_rank_order'], j['partial_square'], source)
            witness.check_witness(final, j['column_rank_order'], j['partial_square'], source)
            assert row['completed_proposals'] == final['proposal'] >= best['proposal']
            assert final['seconds'] >= j['seconds']
            assert not row['accepted_historical_reading']
            if j['key_id'] == 'Nov13-15b':
                assert best['square'][17] == 'Y'
            path = (book_quad if j['model'] == 'book_words' else
                    model_directory / ('radio_book_class36_quad.bin' if j['model'] == 'radio_class'
                                       else 'radio_book36_quad.bin') if model_directory else None)
            if path:
                assert witness.sha(path) == j['model_sha256']
                assert abs(witness.quad_score(best['plaintext'], witness.load_quad(path)) - best['quad_sum']) < 1e-6
            if words and j['word_weight']:
                assert abs(words.score(best['plaintext']) - best['word_sum']) < 1e-6
            assert abs(best['score'] - best['quad_sum'] - j['word_weight'] * best['word_sum']) < 1e-6
            historical += 1
        assert historical == len(jobs)
    return {'verified': True, 'matched_control_batches': summaries,
            'completed_conditional_historical_searches': historical,
            'accepted_historical_readings': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models', type=Path)
    parser.add_argument('--book-quad', type=Path)
    parser.add_argument('--lexicon', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.models, args.book_quad, args.lexicon), indent=2))


if __name__ == '__main__':
    main()
