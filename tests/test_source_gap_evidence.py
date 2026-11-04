"""Conflicting source inputs must not pass as supplemental evidence."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'source_gap_audit', ROOT / 'data/reviews/verify_source_gap_audit.py')
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class SupplementalSourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        data = json.loads((ROOT / 'data/reviews/source_gap_audit_20261103.json').read_text())
        self.source = next(r for r in data['records'] if r['id'] == 'p84_C')
        self.matches = []
        for name in ('p84_field_post_fragment', 'p84_mother_illness_fragment'):
            path = f'experiments/{name}/inputs.json'
            data = json.loads((ROOT / path).read_text())
            records = data['records'] if 'records' in data else [data['record']]
            self.matches.append((path, next(r for r in records if r['id'] == 'p84_C')))

    def test_identical_supplements_are_all_verified(self):
        result = AUDIT.verify_matching_inputs(self.source, self.matches)
        self.assertEqual(result['native_records_verified'], 2)
        self.assertEqual(result['evidence_paths'], [p for p, _ in self.matches])

    def test_each_native_identity_conflict_is_rejected(self):
        changes = {
            'id': 'p84_D', 'printed_page': 85, 'pdf_page_1based': 88,
            'source_section': 'D', 'source_slots': 120, 'advertised_length': 246,
            'observed_coordinates': 112, 'printed_masks': 8,
            'literal_sha256': '0' * 64, 'header_transcription': 'Different reception',
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                matches = copy.deepcopy(self.matches)
                matches[1][1][field] = value
                with self.assertRaises(AssertionError):
                    AUDIT.verify_matching_inputs(self.source, matches)

    def test_conflicting_coordinate_and_grouping_are_rejected(self):
        for regroup in (False, True):
            with self.subTest(regroup=regroup):
                matches = copy.deepcopy(self.matches)
                record = matches[1][1]
                if regroup:
                    record['source_rows'] = [AUDIT.literal(record)]
                else:
                    record['source_rows'][0] = 'D' + record['source_rows'][0][1:]
                with self.assertRaises(AssertionError):
                    AUDIT.verify_matching_inputs(self.source, matches)

    def test_missing_or_repeated_single_file_evidence_is_rejected(self):
        for matches in ([], [self.matches[0], self.matches[0]]):
            with self.subTest(matches=len(matches)):
                with self.assertRaises(AssertionError):
                    AUDIT.verify_matching_inputs(self.source, matches)


if __name__ == '__main__':
    unittest.main()
