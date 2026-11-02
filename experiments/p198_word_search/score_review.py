#!/usr/bin/env python3
"""Independently score truth and incumbents to distinguish objective failures.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
The truth is evaluation-only. This script does not run the optimizer.
"""
import argparse
import json
from pathlib import Path

from verify import HERE, WordModel, load_quad, quad_score, sha, verify

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--quad', type=Path, required=True)
parser.add_argument('--lexicon', type=Path, required=True)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
path = HERE / 'records.json'
records = json.loads(path.read_text())
verify(records, args.quad, args.lexicon)
quads, words = load_quad(args.quad), WordModel(args.lexicon)
rows = []
for row in records['completed']:
    truth = row['input'].get('evaluation_only')
    if not truth or not truth.get('plaintext'):
        continue
    text = truth['plaintext']
    weight = row['input']['word_weight']
    q, w = quad_score(text, quads), words.score(text)
    score = q + weight * w
    best = row['best_candidate']
    difference = best['score'] - score
    exact = best['plaintext'] == text
    classification = ('exact plaintext' if exact else
                      'wrong incumbent outranks truth' if difference > 1e-6 else
                      'search failed to reach better truth' if difference < -1e-6 else
                      'different text tied with truth')
    rows.append({'case_id': row['case_id'], 'truth_quad_sum': q, 'truth_word_sum': w,
                 'truth_total': score, 'incumbent_minus_truth': difference,
                 'classification': classification,
                 'correct_characters': row['control']['correct_characters'],
                 'letter_or_digit_class_agreement': sum(a == b or (a.isdigit() and b.isdigit())
                                                        for a, b in zip(text, best['plaintext'])),
                 'truth_was_optimizer_seed': False})
report = {'schema': 'adfgvx-word-objective-review-v1',
          'authors': 'icekylinx and GPT-6 Astra Pro',
          'records_sha256': sha(path), 'quad_sha256': sha(args.quad),
          'lexicon_sha256': sha(args.lexicon), 'controls': rows,
          'qualification': 'These are run-level diagnostics. Reused controls are not independent new validation samples, and finite search failures do not exclude historical hypotheses.'}
destination = HERE / 'objective_review.json'
if args.check:
    assert report == json.loads(destination.read_text())
else:
    destination.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'controls_reviewed': len(rows),
                  'classifications': {name: sum(r['classification'] == name for r in rows)
                                      for name in sorted({r['classification'] for r in rows})}}, indent=2))
