#!/usr/bin/env python3
"""Reproduce full-log page OCR retrieval for p153 call-sign headers.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Requires an externally supplied Childs PDF, PyMuPDF and Tesseract English data.
Full page images and OCR stay in the caller's scratch work directory.
"""
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess

HERE = Path(__file__).resolve().parent
PAGES = list(range(56, 231))
TARGETS = ['FKR', 'CGH']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ocr_page(args):
    page, pdf, work = args
    import fitz
    image, text = work / f'p{page}.png', work / f'p{page}.txt'
    if not text.exists() or text.stat().st_size == 0:
        with fitz.open(pdf) as doc:
            doc[page + 2].get_pixmap(matrix=fitz.Matrix(2, 2)).save(image)
        env = dict(os.environ)
        env['OMP_THREAD_LIMIT'] = '1'
        pending = work / f'p{page}.{os.getpid()}.pending'
        subprocess.run(['tesseract', str(image), str(pending),
                        '--psm', '3', '-l', 'eng'], env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        pending_text = pending.with_suffix('.pending.txt')
        if not pending_text.exists() or not pending_text.stat().st_size:
            raise ValueError(f'Empty OCR output for printed page {page}')
        pending_text.replace(text)
    return page, text.read_text(), digest(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=HERE / 'review.json')
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    source_digest = digest(args.pdf)
    binding = args.work_dir / 'source_sha256.txt'
    if binding.exists():
        assert binding.read_text().strip() == source_digest, 'Work directory belongs to another PDF.'
    else:
        binding.write_text(source_digest + '\n')
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        pages = list(pool.map(ocr_page, [(page, args.pdf, args.work_dir) for page in PAGES]))
    hits, time_hits = [], []
    for page, text, _ in pages:
        for number, line in enumerate(text.splitlines(), 1):
            words = re.findall(r'\b[A-Z0-9]{3}\b', line.upper())
            matched = sorted({word for word in words
                              if min(sum(a != b for a, b in zip(word, target))
                                     for target in TARGETS) <= 1})
            if matched:
                hits.append({'printed_page': page, 'pdf_page_1based': page + 3,
                             'ocr_line_1based': number, 'matched_tokens': matched,
                             'ocr_line': line})
            if re.search(r'\b2250\b', line):
                time_hits.append({'printed_page': page, 'ocr_line_1based': number, 'ocr_line': line})
    result = {
        'schema': 'adfgvx-p153-header-followup-v2',
        'project': 'ADFGVX Cipher', 'authors': 'icekylinx and GPT-6 Astra Pro',
        'source': {'title': 'General Solution of the ADFGVX Cipher System, Childs collection',
                   'url': 'https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view',
                   'pdf_sha256': source_digest, 'pdf_bytes': args.pdf.stat().st_size},
        'method': {'printed_pages_inclusive': [min(PAGES), max(PAGES)], 'full_pages_ocr': len(pages),
                   'render_scale': 2, 'tesseract_page_segmentation_mode': 3,
                   'tesseract_language': 'eng',
                   'tesseract_version': subprocess.check_output(['tesseract', '--version'], text=True).splitlines()[0],
                   'target_tokens': TARGETS,
                   'matching_rule': 'All complete three-character A-Z/0-9 tokens at Hamming distance at most one from either target.',
                   'additional_exact_header_field': '2250',
                   'source_limit': 'OCR covers the entire page, including text omitted from the earlier ciphertext-block extraction.'},
        'page_ocr_hashes': [{'printed_page': page, 'sha256': sha} for page, _, sha in pages],
        'retrieved_token_lines': hits, 'retrieved_time_lines': time_hits,
        'visual_review': [
            {'printed_pages': [56, 122, 163, 225], 'finding': 'CEH, CUH, COH and C7H are OCR artifacts in the spaced RICHI report title. The original title, rather than a traffic call sign, was visually checked on each page.'},
            {'printed_page': 152, 'finding': 'Full adjacent page inspected: unrelated UKS/ZON and NKJ/LP records; no CGH/FKR continuation identified.'},
            {'printed_page': 153, 'finding': 'The original confirms FKR v CGH, November 8th, clear field 2250, and only parts 5 TL / CHI-132 and 6 TL / CHI-108.'},
            {'printed_pages': [154, 174, 179, 180, 181, 182, 184, 185, 186, 187, 188, 190, 192, 198, 200, 208, 210, 212], 'finding': 'All eighteen CHH hits were checked on the original page headers. They are the analyst-initials annotation (chh), not a call sign.'},
            {'printed_page': 209, 'finding': 'OCR FIR is an artifact in the GENERAL HEADQUARTERS, AMERICAN EXPEDITIONARY FORCES heading. No FKR call sign occurs at this retrieved location.'},
            {'printed_page': 223, 'finding': 'KOW v RVA, November 27th, 1835 (11/27), AN LP v FHR. The original clearly reads FHR, not FKR.'}
        ],
        'ordinary_word_hits': {'FUR': sum('FUR' in h['matched_tokens'] for h in hits),
                               'FOR': sum('FOR' in h['matched_tokens'] for h in hits),
                               'finding': 'These retrieved tokens occur as routing/addressee words, not FKR or CGH station labels. They remain in the full retrieval list.'},
        'control_limit': 'The p153 OCR correctly retrieves FKR and CGH but misreads November 8th as 3th and CHI-132 as CHI-133. Header retrieval therefore does not certify exact transcription.',
        'result': 'Only p153 supplies the target call signs or the exact clear field 2250. No additional CGH/FKR record or parts 1-4 were identified in this full-log OCR retrieval and candidate review.',
        'limits': ['The range covers all 175 printed intercept-log pages, 56-230; complete OCR coverage is not proof that an unrecognized or differently headed companion is absent.',
                   'OCR can omit or split call signs or introduce more than one substitution.',
                   'Retransmissions under different call signs or dates need not be retrieved.',
                   'No call-sign-to-unit identification, missing digit, source coordinate or new plaintext letter is inferred.']
    }
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'pages': len(pages), 'candidate_lines': len(hits), '2250_lines': len(time_hits),
                      'output': str(args.output)}))


if __name__ == '__main__':
    main()
