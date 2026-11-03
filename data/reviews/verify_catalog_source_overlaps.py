#!/usr/bin/env python3
"""Exercise the real p132 relation and reject unregistered source aliases.

Only temporary catalogue/register copies are changed.
Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx import catalog


def main():
    original_data, original_register = catalog.DATA, catalog.SOURCE_OVERLAPS
    data_bytes, register_bytes = original_data.read_bytes(), original_register.read_bytes()
    data, register = json.loads(data_bytes), json.loads(register_bytes)
    rejected = []
    with TemporaryDirectory(prefix='adfgvx-overlap-review-') as directory:
        temporary = Path(directory)
        catalog.DATA = temporary / 'catalogue.json'
        catalog.SOURCE_OVERLAPS = temporary / 'overlaps.json'
        try:
            def install(rows, overlaps):
                catalog.DATA.write_text(json.dumps(rows))
                catalog.SOURCE_OVERLAPS.write_text(json.dumps(overlaps))

            def must_reject(label, expected_message):
                try:
                    catalog.load_catalog()
                except AssertionError as error:
                    assert expected_message in str(error), (label, str(error))
                    rejected.append(label)
                else:
                    raise AssertionError('Accepted an unreviewed overlap: ' + label)

            install(data, register)
            accepted = catalog.load_catalog()
            accounting = catalog.physical_source_accounting(accepted)
            assert accounting['canonical_source_ids']['p132_B'] == 'p132'
            assert accounting['locations']['p132_B'] == accounting['locations']['p132'] == (132, 'B')
            assert accounting['reviewed_entries'] - accounting['unique_physical_sources'] == 1
            later = next(r for r in accepted['other'] if r['id'] == 'p132_B')
            rendered = catalog.table([later], ROOT / 'cases/README.md')
            assert 'later edition of [p132](p132.md)' in rendered
            assert 'Thomas (fragment) and Norbert (body), 2017' in rendered

            absent = deepcopy(register)
            absent['records'] = []
            install(data, absent)
            must_reject('p132 overlap without its registration', 'Unregistered physical-source overlap at p132 B')

            duplicate = deepcopy(data)
            canonical = next(r for r in data['challenge'] if r['id'] == 'p153a')
            source = catalog.source_messages()['p153a']['source']
            duplicate['other'].append({
                'id': 'p153_C5', 'label': 'p153 C5',
                'printed_page': source['printed_page'], 'source_section': source['section'],
                'subject': 'Temporary same-source alias of p153a',
                'status': 'Temporary overlap-rejection fixture',
                'credit': canonical['credit'], 'path': canonical['path'],
                'source_reviewed': True, 'evidence': ['data/messages.json'],
            })
            install(duplicate, register)
            must_reject('proposed p153_C5 alias of p153a', 'Unregistered physical-source overlap at p153 C5')

            wrong_digest = deepcopy(register)
            wrong_digest['records'][0]['literal_source_sha256'] = '0' * 64
            install(data, wrong_digest)
            must_reject('registered relation with a changed literal digest', 'p132_B')
        finally:
            catalog.DATA, catalog.SOURCE_OVERLAPS = original_data, original_register
    assert original_data.read_bytes() == data_bytes
    assert original_register.read_bytes() == register_bytes
    print(json.dumps({
        'verified': True,
        'accepted_same_source_editions': ['p132', 'p132_B'],
        'registered_literal_source_sha256': register['records'][0]['literal_source_sha256'],
        'rejected_temporary_scenarios': rejected,
        'reviewed_entries': accounting['reviewed_entries'],
        'unique_physical_sources': accounting['unique_physical_sources'],
        'additional_physical_sources': accounting['additional_physical_sources'],
        'catalogue_and_register_unchanged': True,
    }, indent=2))


if __name__ == '__main__':
    main()
