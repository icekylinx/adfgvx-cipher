#!/usr/bin/env python3
"""Verify frozen anchored-search arithmetic without an engine or language model."""
import argparse
import json
from pathlib import Path
from arithmetic import verify_record

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, default=HERE / 'data/result_snapshot.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    cases = json.loads((HERE / 'data/cases.json').read_text())
    snapshot = json.loads(args.snapshot.read_text())
    controls = snapshot['control_records']
    historical = snapshot['historical_records']
    assert snapshot['planned_historical_cases'] == len(cases['historical']) == 70
    assert snapshot['completed_historical_cases'] == len(historical)
    assert snapshot['accepted_historical_plaintexts'] == 0
    labels = [row['label'] for row in controls + historical]
    assert len(labels) == len(set(labels))
    report = []
    for row in controls + historical:
        result = verify_record(row['record'], cases['historical'] + cases['controls'])
        assert result['label'] == row['label']
        report.append(result)
    output = {'verified': True, 'historical_completed': len(historical),
              'historical_planned': 70, 'control_records': len(controls),
              'accepted_historical_plaintexts': 0, 'checks': report,
              'scope': 'Arithmetic, frozen inputs and budgets only; language scores are not recomputed.'}
    text = json.dumps(output, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
