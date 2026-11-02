"""Verify fixtures, recorded control certificates, and exact-ranking recall."""
from pathlib import Path
import json
import subprocess

from cipher import cells, decrypt, encrypt, mismatches

ROOT = Path(__file__).resolve().parent.parent


def main():
    cases = json.loads((ROOT/'cases/cases.json').read_text())['cases']
    controls = {row['id']:row for row in cases if 'plaintexts' in row}
    for name, case in controls.items():
        assert [len(text) for text in case['ciphertexts']] == [132,108]
        assert [len(text) for text in case['plaintexts']] == [66,54]
        for text, received in zip(case['plaintexts'], case['ciphertexts']):
            out = encrypt(text, case['ranks'], case['square'])
            assert not mismatches(received, out), name
    for bad in ['ADFGV', 'A']:
        try: cells(bad, [1])
        except ValueError: pass
        else: raise AssertionError('Odd ciphertext silently accepted')
    records = json.loads((ROOT/'results/control_certificates.json').read_text())
    verified = 0
    for record in records:
        case = controls[record['case']]
        square, ranks = record['square'], record['ranks']
        plaintexts = [decrypt(ct, ranks, square) for ct in case['ciphertexts']]
        assert plaintexts == record['plaintexts']
        regenerated = [encrypt(text, ranks, square) for text in case['plaintexts']]
        differences = [mismatches(ct, out) for ct, out in zip(case['ciphertexts'], regenerated)]
        assert differences == record['observed_coordinate_mismatch_positions']
        verified += 1
    ranking = []
    expected = json.loads((ROOT/'results/segmentation16_ranking.json').read_text())
    for name in ['original_control','fresh_control']:
        proc = subprocess.run([str(ROOT/'bin/segmentation_rank'),
                               str(ROOT/'models/military_monograms.txt'),
                               str(ROOT/f'cases/{name}_k16.in'), '1'],
                              capture_output=True, text=True, check=True)
        summary = json.loads(proc.stdout.splitlines()[-1])
        target = next(row for row in expected if row['case'] == name)
        assert summary['enumerated_segmentations'] == 900900
        for field in ['true_unigram_rank_zero_based','true_collision_rank_zero_based']:
            assert summary[field] == target[field], (name, field)
        ranking.append({'case': name, 'iid_rank_zero_based':summary['true_unigram_rank_zero_based'],
                        'collision_rank_zero_based':summary['true_collision_rank_zero_based']})
    print(json.dumps({'verified_control_fixtures':len(controls),
                      'verified_recorded_control_outputs':verified,
                      'known_failures_preserved':sum(any(row['observed_coordinate_mismatch_positions']) for row in records),
                      'exact_segmentation_recall_checks':ranking,
                      'historical_plaintext_claims':0}, indent=2))


if __name__ == '__main__': main()
