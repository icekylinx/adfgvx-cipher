#!/usr/bin/env python3
"""Refresh a verified snapshot from completed research or portable result JSONs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from arithmetic import verify_record

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=HERE / 'data/result_snapshot.json')
    parser.add_argument('--interrupted', action='store_true')
    args = parser.parse_args()
    cases = json.loads((HERE / 'data/cases.json').read_text())
    groups = {'historical_records': [], 'control_records': []}
    for path in sorted(args.results.glob('*__*__k*__r*i*.json')):
        record = json.loads(path.read_text())
        checked = verify_record(record, cases['historical'] + cases['controls'])
        assert path.stem == checked['label']
        group = 'control_records' if 'evaluation_only' in record['case'] else 'historical_records'
        groups[group].append({'label': path.stem, 'source_record_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'record': record})
    historical_case_ids = {(row['record']['case']['id'], row['record']['case']['key_id'], row['record']['case']['width'])
                           for row in groups['historical_records']}
    # Snapshot historical records at the advertised budget only; alternate budgets
    # should be reported in a separate snapshot to avoid counting one case twice.
    assert len(historical_case_ids) == len(groups['historical_records'])
    assert all(row['record']['requested_restarts'] == 1000 and row['record']['iterations_per_restart'] == 100000
               for row in groups['historical_records'])
    result = {'snapshot_utc': datetime.now(timezone.utc).isoformat(),
              'planned_historical_cases': 70, 'completed_historical_cases': len(historical_case_ids),
              'historical_search_interrupted_for_p153_followup': args.interrupted,
              'accepted_historical_plaintexts': 0, **groups}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if not k.endswith('_records')}))


if __name__ == '__main__':
    main()
