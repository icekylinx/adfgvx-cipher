#!/usr/bin/env python3
"""Rebuild the compact p109 and p146 source-recovery certificates."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.source_recovery import p109_analysis, p146_analysis

B_GROUPS = '''XGGGG GFDFG GAXGF FFVGG VDXDX DAGXF DGXGX AAGDX
DADDD ADXAG GADGV FGGXD FGVVG XXAXA FDVVV XXFXV
DVGXG VDAAD GXDAA XFVAX DGVGG GDAVG F-VGD DVFGF
VDVVX DGFDD VVXDX VDADX XVVX- V--GF GVVVV AGXGG
XGGDA FGADV VDAFG AADAD GDXXV GDXVA AADGV XGGGX
AGGDG VGD-V FAFAX GGVGV FAD-G FAXAD GVFDD DAVGV
FAGAG VGD'''
common = {'authors': ['icekylinx', 'GPT-6 Astra Pro'], 'date': '2026-11-02',
          'project': 'ADFGVX Cipher', 'index_convention': 'Zero based',
          'source_transcriptions_unchanged': True}
p146 = {
    **common, 'schema': 'adfgvx-p146-duplicate-group-v1',
    'status': 'Source-preserving retained-coordinate repair, with explicit five-coordinate completion',
    'source': {'printed_page': 146, 'pdf_page_1based': 149, 'section': 'B',
               'image': 'sources/excerpts/childs_p146_B.png',
               'analysis_reference': 'data/prior_readings.json#p146',
               'header': 'UKS v LP (06.43 a.m., November 7th); UKS AS FUER COS 2100 (6/11); RICHI-244'},
    'attribution': {'earlier_key': 'George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker',
                    'earlier_body_and_gap_hypothesis': 'Norbert, 2017-03-01, comment 19',
                    'new_duplicate-group_repair_and_readable_review': 'icekylinx and GPT-6 Astra Pro'},
    'reading': 'FUNKSTELLE KERTSCH ERHAELT AB 12.[11] RUFNAMEN RICHARD EMIL KARL. FUNKSTELLEN DORTIGEN BEREICHS BENACHRICHTIGEN. NACHRICHTENCHEF 4BG7834',
    'limits': ['A missing group and a duplicated group are the stated damage model, not directly witnessed transmission events.',
               'The source contains two adjacent identical XAAXV groups; their identities cannot be distinguished after deleting one.',
               'The five proposed coordinates AAXAA supply L, 1, N, E, F at the unresolved plaintext positions.',
               'For an ordinary day.month date, the remaining month character in 12.1? is conditionally 1; no date is independently recovered from the absent coordinate.',
               'The suffix 4BG7834 is not expanded. Alternative alignments for the chosen complete reading are retained.'],
    'analysis': p146_analysis(),
}
source_b = ''.join(B_GROUPS.split()).replace('-', '?')
p109 = {
    **common, 'schema': 'adfgvx-p109-source-parallel-v1',
    'status': 'Newly reviewed primary-source near-parallel; conditional editorial reading',
    'source_B': {'printed_page': 109, 'pdf_page_1based': 112, 'section': 'B',
                 'image': 'sources/excerpts/childs_p109_B.png',
                 'header': 'UKS v ZON (11.03 p.m., November 3rd); VEVE 1715 AN LP UD 2130; RICHI-248',
                 'ciphertext_grouped': B_GROUPS, 'ciphertext': source_b,
                 'independent_transcription_review': 'experiments/source_followup/p109_B_review.json'},
    'source_D': {'printed_page': 109, 'pdf_page_1based': 112, 'section': 'D',
                 'image': 'sources/excerpts/childs_p109_D.png',
                 'header': 'UKS v ZON (0.35 a.m., November 3rd); Beginning jammed; RIZI-258',
                 'analysis_reference': 'data/prior_readings.json#p109'},
    'attribution': {'earlier_target_reading': 'Norbert, 2017-03-01, comment 18',
                    'earlier_editorial_alternative': 'Max Baertl, 2017-03-11, comment 39',
                    'parallel_review_and_revised_interpretation': 'icekylinx and GPT-6 Astra Pro'},
    'limits': ['The two printed timestamps and differing endings are retained; an exact retransmission identity is not assumed as an established fact.',
               'The readable 124-character interpretation is not a zero-edit decipherment of either copy.',
               'Under a common-plaintext model it lies four known-coordinate substitutions above the absolute minimum, at three plaintext positions.',
               'A source spelling ABENDMELUNG is retained in the compact proposal; the uncertain closing characters are not interpreted.'],
    'analysis': p109_analysis(source_b),
}
for name, data in [('p146_duplicate_group', p146), ('p109_parallel', p109)]:
    (ROOT / 'data/certificates' / (name + '.json')).write_text(json.dumps(data, indent=2) + '\n')
    print(name, 'written')
