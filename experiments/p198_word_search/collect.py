#!/usr/bin/env python3
"""Freeze completed pilot runs; an in-progress best is never a completed case.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Original JSONL event hashes remain available for a matching execution log.
The exact final event, rather than the first discovery of the best score,
supplies completed proposal and restart counts.
"""
import argparse
import datetime
import json
from pathlib import Path

from verify import HERE, ROOT, encrypt_independent, sha, verify

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
base = args.scratch
specifications = [('pilot', base / 'pilot_manifest.json'),
                  ('adaptive_weight2', base / 'extended_manifest.json'),
                  ('broad_partial', base / 'broad/manifest.json'),
                  ('unknown_square_controls', base / 'unknown_controls_manifest.json')]
output = {'schema': 'adfgvx-word-loss-completed-v1',
          'authors': 'icekylinx and GPT-6 Astra Pro',
          'collected_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'engine_source_sha256': sha(HERE / 'word_loss.cpp'),
          'engine_binary_sha256': sha(base / 'word_loss'),
          'lexicon_sha256': sha(base / 'lexicon.txt'),
          'quad_model_sha256': json.loads((ROOT / 'experiments/joint_search/models/provenance.json').read_text())['binary_sha256']['german_military36_quad.bin'],
          'declared_cases': [], 'completed': [], 'pending': [], 'batch_lineage': {}}
for batch, manifest_path in specifications:
    manifest = json.loads(manifest_path.read_text())
    output['batch_lineage'][batch] = {key: value for key, value in manifest.items()
                                      if key not in ('jobs', 'hashes')}
    for original in manifest['jobs']:
        label = batch + '/' + original['id']
        output['declared_cases'].append(label)
        job = {key: value for key, value in original.items() if key not in ('input', 'initial')}
        log = Path(original['input']).parent / (original['id'] + '.jsonl')
        result_path = log.with_suffix('.result.json')
        # A result file is written only after the child process exits cleanly.
        if not result_path.is_file():
            output['pending'].append(label)
            continue
        result = json.loads(result_path.read_text())
        events = [json.loads(line) for line in log.read_text().splitlines()]
        assert events and events[-1]['seconds'] >= original['seconds']
        best = max(events, key=lambda event: event['score'])
        final = events[-1]
        row = {'case_id': label, 'input': job, 'best_candidate': best,
               'final_event': final, 'completed_proposals': final['proposal'],
               'completed_restarts': final['restart'], 'elapsed_seconds': result['elapsed_seconds'],
               'original_output_sha256': sha(log), 'accepted_historical_reading': False}
        initial = original.get('initial')
        if initial and initial != '-':
            fields = Path(initial).read_text().split()
            square, losses, fills = fields[0], list(map(int, fields[1:6])), fields[6]
            received = iter(job['source']); inserted = dict(zip(losses, fills))
            full = ''.join(inserted[i] if i in inserted else next(received) for i in range(170))
            # Independent inverse for the seed-state audit only.
            coords = [''] * 170; offset = 0
            for col in sorted(range(len(job['ranks'])), key=job['ranks'].__getitem__):
                for i in range(col, 170, len(job['ranks'])):
                    coords[i] = full[offset]; offset += 1
            alphabet = 'ADFGVX'
            plain = ''.join(square[6 * alphabet.index(coords[i]) + alphabet.index(coords[i + 1])]
                            for i in range(0, 170, 2))
            row['initial_state'] = {'square': square, 'loss': losses, 'fill': fills, 'plaintext': plain,
                                    'origin': 'Earlier four-gram optimum; control truth was not supplied as a seed.'}
        truth = job.get('evaluation_only')
        if truth and truth.get('plaintext'):
            correct = sum(a == b for a, b in zip(truth['plaintext'], best['plaintext']))
            row['control'] = {'correct_characters': correct, 'length': len(truth['plaintext']),
                              'exact_plaintext': correct == len(truth['plaintext'])}
        output['completed'].append(row)
print(json.dumps(verify(output), indent=2))
(HERE / 'records.json').write_text(json.dumps(output, indent=2) + '\n')
