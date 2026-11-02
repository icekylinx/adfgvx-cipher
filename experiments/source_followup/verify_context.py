#!/usr/bin/env python3
"""Recompute two visually checked contextual source readings.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Uses independent arithmetic in audit_p186.py; no language model is involved.
"""
from pathlib import Path
import argparse
import json
from audit_p186 import ROOT, inspect, encode

RECORDS = [
    {'id': 'p77_B', 'printed_page': 77, 'pdf_page_1based': 80, 'section': 'B',
     'header': 'OSM v LP (6.47 a.m., October 30th); SS BERLIN 29/10 1922; RICHI-350',
     'key_id': 'Oct28-31', 'advertised_length': 350,
     'raw_source_grouped': '''DGXAX XXFAG AGXAX XXFFD XGADG XGAXF AXFVG XVGAV
DFAVD FVDAX GXGAX AXAAA FGFAA XXAXA DAADA FXGGX
AAXAD DXDVX AXFFA FAXFG ADGGV AXADX XFAXV GADDA
XXADA DDAGA XFGAD XXAAA XDDXX DDVVV VXAAV XAAAF
AGXFF VXXAF XVVVV AVAVF ADVGA XXFAF FAXAA VAVXA
AAFFF XXDAA XXVGX AVAGX FVVFD GFXVX XAADF XADXA
AFFGG GGXXF GDAAF GVXFX XAAXA FFDXD FAXAV XXVVV
XAXAX AAXAV FXVXA AXFXG GFADV GFVFG XFGAX GFFVA
DXXFA XXVAA AXDXV DXAAG GAAXD XAGGV''',
     'most_likely_readable_text': 'Nachrichtenchef drahtet mit 4 B 49338: Funkerabtlg. Osmanie. Zu dort 2032: [Funkerabtlg.] Konia erhaelt Rufnamen Nathan Otto Karl. Wellen von dort festlegen. Admiralstab 17830 D 2.',
     'english_meaning': 'The signals chief reports that the radio detachment at Konia receives the call sign spelled Nathan-Otto-Karl; its wavelengths are to be fixed by the recipient. Administrative references and the Admiralty Staff signature remain visible.',
     'relevance': 'An independent source directly contains ERHAELT RUFNAMEN followed by spelling words, supporting the interpretation of the same formula in p146. It also contains a signals-chief reference using 4 B.',
     'limits': 'This is about Konia and an October call-sign instruction. It does not independently establish the Kerch call sign or the date 12 November. No first decipherment claim is made for this wider-corpus message.'},
    {'id': 'p134_B', 'printed_page': 134, 'pdf_page_1based': 137, 'section': 'B',
     'header': 'LP v NKJ (4.02 a.m., November 6th); 0530 (6); RIZI-102',
     'key_id': 'Nov4-6', 'advertised_length': 102,
     'raw_source_grouped': '''GFVVF GFFVD ADAAF FFXXV DXVGG FADGF DAFXF AFDFX
AXVAV AVAGV XFAXA XAGFF XADFA FFDVD GDGVD XAXV?
DDXXX AGDAF FXXAD DADAF AF''',
     'source_glyph_note': 'The last glyph in group 16, source index 79, is overstruck or malformed (R/F/E-like). It is masked, not accepted as a known coordinate. The question mark in this transcription describes that source uncertainty.',
     'most_likely_readable_text': '[Eilvese]. [Telegr.] [der] 4. [Periode] in 5. wiederholen. OSM.',
     'english_meaning': 'A message apparently directed to Eilvese asks for a fourth-period telegram to be repeated in the fifth period.',
     'relevance': 'Independent contextual support for the fourth/fifth-period wording in p132; the repeated vocabulary is present under the same historical period key.',
     'limits': 'The raw place word is EGLV2SSE and other words remain malformed. This is not a source-identical retransmission of p132, and does not independently establish its VORHER wording or the meaning of the periods. No first decipherment claim is made.'},
]


def build():
    keys = {x['id']: x for x in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    results = []
    for source in RECORDS:
        key = keys[source['key_id']]
        arithmetic = inspect(source['raw_source_grouped'], key)
        arithmetic.pop('raw_source_grouped')
        if '?' not in arithmetic['raw_plaintext']:
            encoded = encode(arithmetic['raw_plaintext'], key)
            assert encoded == arithmetic['analysis_ciphertext']
            arithmetic['ordinary_complete_reencryption_exact'] = True
        else:
            arithmetic['ordinary_complete_reencryption_exact'] = False
        assert arithmetic['source_slots'] == source['advertised_length']
        results.append({**source, 'arithmetic': arithmetic})
    return {'format_version': 1, 'project': 'ADFGVX Cipher',
            'authors': ['icekylinx', 'GPT-6 Astra Pro'],
            'source_url': 'https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view',
            'source_status': 'Visually checked against the complete historical scan; all valid received coordinates remain unchanged.',
            'credit': 'Historical corpus and previously published period keys are used. Present source transcription, comparison and independent arithmetic audit: icekylinx and GPT-6 Astra Pro.',
            'records': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('source_context.json'))
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.verify:
        assert result == json.loads(args.output.read_text())
    else:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([{'id': r['id'], 'source_slots': r['arithmetic']['source_slots'],
                       'fixed_plaintext_positions': r['arithmetic']['fixed_plaintext_positions'],
                       'plaintext': r['arithmetic']['raw_plaintext']}
                      for r in result['records']]))
