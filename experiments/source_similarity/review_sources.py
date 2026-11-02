#!/usr/bin/env python3
"""Reproduce image-reviewed checks of the three leading OCR candidates.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The literal transcriptions below were checked against the Childs page images;
they are supplementary witnesses, not changes to the challenge transcription.
"""
from pathlib import Path
import argparse
import hashlib
import json

from retrieve import ROOT, HERE, build_queries, clean, local_trace, reference_metrics


SOURCE = {
    'title': 'General Solution of the ADFGVX Cipher System, Childs collection',
    'url': 'https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view',
    'pdf_sha256': '157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06',
    'pdf_bytes': 156848258,
    'page_convention': 'Printed page n is PDF page n+3 for these intercept pages.',
}

WITNESSES = [
    {
        'query_id': 'p73', 'block_id': 'p105_ocr_block4',
        'printed_page': 105, 'designation': 'C, part 1',
        'header': 'NKJ v LP (4.55 p.m., November 2nd); FUER UKS 2/11 1300 3 TEILE; 1 TL; RICHI-238',
        'printed_length_field': 238,
        'source_rows': [
            'GVGDG XXVFF FADXD GVFAA XGVGV GDVAF FAVFA GXDXV',
            'DGXVV DFVVA GGGXX XGDXX GFXAG VXXXV DFDVG DGVXF',
            'GVADF DXAGD VGAXG DXDGV AGXXF XDGDX DAFVD GXGXX',
            'DXVAX XDDFD DGADF AGVDG FFDFG AFXVF DVGAV FDXDF',
            'AVXVX VDGAA GVVGA XVFGX GAXXX FFGDD AADFA FXGAG',
            'VGDGD FAVDG GDDFX GXDXD GVDAG VGXVA AFVVX XDX',
        ],
        'source_note': 'All six rows are visible. The OCR block has 199 slots and omits the first 40-coordinate row; its other errors are retained in the separate OCR layer.',
    },
    {
        'query_id': 'p170', 'block_id': 'p110_ocr_block3',
        'printed_page': 110, 'designation': 'C',
        'header': 'NKJ v LP (5.09 p.m., November 3rd); FUER UKS 0520 (3/11); RICHI-398',
        'printed_length_field': 398,
        'source_rows': [
            'VAGDF XVFGG AGFVG DGGXD XXGVG DAAXD GAAFF AGFDG',
            'XXXVV GDXXG FXDXV GGVFG FAVGG DADXV FAGVG DGFVV',
            'DAXDD AVVDV VFDGF DAADV AGXAG ADDFG XVXAX DGDGG',
            'GGDAG GVVGD DVXGG AXGFD GADAX VGDGX GVFAX XGVVF',
            'AXVAF GDVGA VXVDX GVXFF AGDVV GDVXV DAXDX XXVVA',
            'GAGAA VXVXG ADXDV AXVVF DFFXG VGXGX AAXDD AXGGD',
            'DXAVG FDVDA VFDAX FGDDF AGGXG GVDGD XDGDG DGVVD',
            'AGDVF AFGXA VXFGA AVVAD FDVGV AFFVA VFVXG AGGXV',
            'GFADA VGGGD XVFDV GDAXA GXGVF VADVD AAGVG VVVAV',
            'VGDVD AFGVG VXGGD DADFG GAXXD VGDVX XXGAA DGV',
        ],
        'source_note': 'Ten printed rows give 398 coordinates. Image review changes the OCR input length from 399 to 398; the short p170 similarity remains confined to the end of rows 9 and 10.',
    },
    {
        'query_id': 'p198', 'block_id': 'p154_ocr_block1',
        'printed_page': 154, 'designation': 'A, part 2',
        'header': 'UKS v ZON (11.55 p.m., November 7th); 2 TL; RICHI-162',
        'printed_length_field': 162,
        'source_rows': [
            'FXFXF AADVX XDDAV DFGXX DAAXV VDFDVD XXFVA',
            'DAFXA FGVFV AFXFV XXVDV XVAXV DVVVG XXFAD',
            'DVDXF AFXXA FAGFV VFXFF GGVFA XGXVF GAFAA',
            'AFVGX ADGVA VF',
        ],
        'source_note': 'The page itself prints 118 coordinates, including the six-letter group VDFDVD, despite the RICHI-162 field. No padding, deletion or assumed reconstruction is made.',
    },
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, help='Optionally verify the inspected PDF hash.')
    parser.add_argument('--check', action='store_true', help='Check the committed result without rewriting it.')
    args = parser.parse_args()
    if args.pdf:
        assert args.pdf.stat().st_size == SOURCE['pdf_bytes']
        assert hashlib.sha256(args.pdf.read_bytes()).hexdigest() == SOURCE['pdf_sha256']
    corpus_path = ROOT/'experiments/p153_corpus/inputs.json'
    corpus = json.loads(corpus_path.read_text())['blocks']
    blocks = {block['id']: clean(''.join(block['groups'])) for block in corpus}
    queries, _ = build_queries()
    reviews = []
    for witness in WITNESSES:
        image_text = clean(''.join(witness['source_rows']))
        query = queries[witness['query_id']]
        ocr = blocks[witness['block_id']]
        layers = {}
        for name, value in [('raw_corpus_ocr', ocr), ('image_reviewed_transcript', image_text)]:
            score, longest, fit = reference_metrics(query, value)
            trace = local_trace(query, value)
            assert trace['local_score'] == score
            layers[name] = {
                'ciphertext': value, 'slots': len(value),
                'known_coordinates': len(value.replace('?', '')),
                'longest_exact_run': longest, 'full_query_fitting_cost': fit,
                'optimal_local_alignment': trace,
            }
        reviews.append({**witness, 'pdf_page_1based': witness['printed_page']+3,
                        'query': query, 'query_slots': len(query), 'layers': layers,
                        'assessment': 'No parallel transmission established. A short local resemblance does not account for the full target.'})
    result = {
        'schema': 'adfgvx-source-similarity-image-review-v1',
        'project': 'ADFGVX Cipher', 'authors': 'icekylinx and GPT-6 Astra Pro',
        'source': SOURCE,
        'corpus_sha256': hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
        'indexing': 'Zero-based, half-open coordinate spans. Query coordinates use the unchanged catalog analysis transcription.',
        'selection': 'The highest affine-local-score non-self OCR block for each of p73, p170 and p198 in the complete 788-block retrieval.',
        'reviews': reviews,
        'limits': [
            'Only these three leading candidates were newly transcribed from the original page images.',
            'The full corpus remains an unverified OCR retrieval aid, not an edition of all printed ciphertext.',
            'No image-reviewed transcript here is substituted into data/messages.json or used to propose a plaintext.',
        ],
    }
    target = HERE/'source_inspections.json'
    if args.check:
        assert json.loads(target.read_text()) == result, 'Source inspection result differs; rerun without --check.'
    else:
        target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({r['query_id']: {
        name: {'slots': layer['slots'], 'longest': layer['longest_exact_run'],
               'fit': layer['full_query_fitting_cost'],
               'local': layer['optimal_local_alignment']}
        for name, layer in r['layers'].items()} for r in reviews}, indent=2))


if __name__ == '__main__':
    main()
