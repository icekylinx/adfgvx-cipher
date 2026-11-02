#!/usr/bin/env python3
"""Record three transparent, same-length reading proposals; never edit a source."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.editorial import audit

DISCUSSION = 'https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1'
records = [
    {
        'message_id': 'p109',
        'baseline_variant': 'norbert18',
        'status': 'Conditional editorial reading supported by a separately transcribed near-parallel',
        'compact_plaintext': 'OXKXMXABENDMELUNGXSAVAXUEBERGANGLETZTERTEILEBEENDETX1WEITEREFDLXDIVXIMMARSCHAUFBELGRADERKANNTXSONSTKEINEEREIGNISSEXXASOXK511',
        'interpretation': 'The last elements have completed the Sava crossing; one further enemy division was observed marching on Belgrade; no other events. ABENDMELUNG and the uncertain closing string are retained.',
        'attribution': {'underlying_reading': 'Norbert, comment 18, 2017-03-01',
                        'source': DISCUSSION + '#comment-852658',
                        'editorial_and_source_review': 'icekylinx and GPT-6 Astra Pro'},
        'limits': ['Same-length wording, conditional on the earlier ten-coordinate deletion/reconstruction.',
                   'The neighboring p109 B witness supports the interpretation but retains its own errors and different ending.',
                   'The final digits are copied from the earlier raw reading, not historically interpreted.'],
    },
    {
        'message_id': 'p132',
        'baseline_variant': 'norbert37_displayed_rectangle',
        'status': 'Coordinate audit of an earlier editorial interpretation',
        'compact_plaintext': 'FUEREILVESEXWIEDERHOLETTELEGRXVONVIERTERPERIODEINFUENFTERXGEBETVORHER5MINXVVV',
        'interpretation': 'For Eilvese: repeat the telegram from the fourth period in the fifth; send VVV for five minutes beforehand.',
        'attribution': {'underlying_reading': 'Thomas and Norbert, 2017; displayed rectangle in Norbert comment 37',
                        'VORHER_interpretation': 'Norbert, comment 40, 2017-03-12',
                        'source': DISCUSSION + '#comment-858211',
                        'other_readable_normalizations': 'Compare Max Baertl, comment 39, 2017-03-11',
                        'coordinate_review': 'icekylinx and GPT-6 Astra Pro'},
        'limits': ['Retains the earlier sender-error hypothesis: remove one duplicated V after inverse transposition.',
                   'The displayed rectangle already contains two erasure fills and one known-coordinate change.',
                   'VORHER is an attributed 2017 interpretation, not a new decipherment by this project.'],
    },
    {
        'message_id': 'p146',
        'baseline_variant': 'norbert19',
        'status': 'Conditional same-length editorial reading',
        'compact_plaintext': 'FUNKSTELLEKERTSCHERHAELTAB12X11XRUFNAMENRICHARDEMILKARLXFUNKSTELLENDORTIGENBEREICHSBENACHRICHTIGENXNACHRICHTENCHEF4BG7834X',
        'interpretation': 'The Kerch radio station receives the call sign Richard Emil Karl from 12 November; notify radio stations in the area.',
        'attribution': {'underlying_reading': 'Norbert, comment 19, 2017-03-01',
                        'source': DISCUSSION + '#comment-852664',
                        'editorial_review': 'icekylinx and GPT-6 Astra Pro'},
        'limits': ['The date 12 November is an editorial reading, not a newly observed source date.',
                   'Earlier inserted/reduced groups remain part of the baseline repair.',
                   'The closing 4BG7834 is retained without expanding it.'],
    },
]
entries = {m['id']: m for m in json.loads((ROOT / 'data/prior_readings.json').read_text())['messages']}
for record in records:
    record['audit'] = audit(entries[record['message_id']], record)
document = {'schema': 'adfgvx-explicit-editorial-readings-v1',
            'title': 'ADFGVX Cipher: explicit editorial reading audit',
            'authors': ['icekylinx', 'GPT-6 Astra Pro'],
            'date': '2026-11-02',
            'source_transcriptions_unchanged': True,
            'index_convention': 'Zero based; changes are additional to the individually named earlier repair.',
            'readings': records}
path = ROOT / 'data/certificates/editorial_readings.json'
path.write_text(json.dumps(document, indent=2) + '\n')
for record in records:
    a = record['audit']
    print(record['message_id'], len(a['plaintext_changes']), 'plaintext substitutions;',
          a['extra_coordinate_change_count'], 'additional coordinate changes')
