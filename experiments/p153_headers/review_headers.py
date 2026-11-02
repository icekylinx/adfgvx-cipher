#!/usr/bin/env python3
"""Reproduce the bounded full-page OCR retrieval for p153 call-sign headers.

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
PAGES = list(range(140, 171))
TARGETS = ['FKR', 'CGH']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ocr_page(args):
    page, pdf, work = args
    import fitz
    image, text = work / f'p{page}.png', work / f'p{page}.txt'
    if not text.exists():
        with fitz.open(pdf) as doc:
            doc[page + 2].get_pixmap(matrix=fitz.Matrix(2, 2)).save(image)
        env = dict(os.environ)
        env['OMP_THREAD_LIMIT'] = '1'
        subprocess.run(['tesseract', str(image), str(text.with_suffix('')),
                        '--psm', '3', '-l', 'eng'], env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
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
        'schema': 'adfgvx-p153-header-followup-v1',
        'project': 'ADFGVX Cipher', 'authors': 'icekylinx and GPT-6 Astra Pro',
        'source': {'title': 'General Solution of the ADFGVX Cipher System, Childs collection',
                   'url': 'https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view',
                   'pdf_sha256': source_digest, 'pdf_bytes': args.pdf.stat().st_size},
        'method': {'printed_pages_inclusive': [140, 170], 'full_pages_ocr': len(pages),
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
            {'printed_page': 152, 'finding': 'Full adjacent page inspected: unrelated UKS/ZON and NKJ/LP records; no CGH/FKR continuation identified.'},
            {'printed_page': 153, 'finding': 'The original confirms FKR v CGH, November 8th, clear field 2250, and only parts 5 TL / CHI-132 and 6 TL / CHI-108.'},
            {'printed_page': 154, 'finding': 'CHH is an analyst-initials annotation at the top of the page. The two traffic headers are UKS v ZON and ZON v UKS; no p153 continuation identified.'},
            {'printed_page': 163, 'finding': 'OCR COH is an artifact inside the spaced RICHI title. The actual page header is --- v UKS, November 9th; this is not a CGH hit.'},
            {'printed_page': 223, 'finding': 'Separately reviewed earlier-corpus near-match: KOW v RVA, November 27th, 1835 (11/27), AN LP v FHR. The source clearly reads FHR, not FKR.'}
        ],
        'control_limit': 'The p153 OCR correctly retrieves FKR and CGH but misreads November 8th as 3th and CHI-132 as CHI-133. Header retrieval therefore does not certify exact transcription.',
        'result': 'No additional CGH/FKR record or parts 1-4 of the p153 message identified in this bounded review.',
        'limits': ['The range contains 31 full pages; it is not a new whole-book absence proof.',
                   'OCR can omit or split call signs or introduce more than one substitution.',
                   'Retransmissions under different call signs or dates need not be retrieved.',
                   'No call-sign-to-unit identification, missing digit, source coordinate or new plaintext letter is inferred.']
    }
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'pages': len(pages), 'candidate_lines': len(hits), '2250_lines': len(time_hits),
                      'output': str(args.output)}))


if __name__ == '__main__':
    main()
