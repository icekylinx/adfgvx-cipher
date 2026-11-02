#!/usr/bin/env python3
"""Retrieve possible p215 context in the unverified Childs OCR corpus.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The output is a retrieval queue, not a collection of accepted decryptions.
"""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORPUS = ROOT / 'experiments/p153_corpus'
spec = importlib.util.spec_from_file_location('corpus_screen', CORPUS / 'run_screen.py')
screen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(screen)

TERMS = ['KOSCH', 'KORPS', 'KERTSCH', 'ENTENTE', 'NEUSEEL', 'MILI5',
         'MIDI5', 'MELDG', 'ABSXMI', 'FLOTTE', 'ZWODIVISIONEN', 'NARODA',
         'NACHMELD', 'NAMELD', '24N', '34N']


def main():
    blocks = json.loads((CORPUS / 'inputs.json').read_text())['blocks']
    keys = [key for key in json.loads((ROOT / 'data/keys.json').read_text())['keys']
            if set(key['square']) != {'?'}]
    rows, tested = [], 0
    for block in blocks:
        best, seen = {}, set()
        for ciphertext, edits in itertools.islice(screen.variants(block), 4):
            for tail in range(5):
                candidate = ciphertext + '?' * tail
                if candidate in seen:
                    continue
                seen.add(candidate)
                for key in keys:
                    plain, orphan = screen.decrypt(candidate, key['column_rank_order'], key['square'])
                    plain = plain.upper()
                    tested += 1
                    hits = [term for term in TERMS if term in plain]
                    if not hits:
                        continue
                    score = sum(len(term)**2 for term in hits)
                    row = {'id': block['id'], 'printed_page': block['printed_page'],
                           'pdf_page_1based': block['pdf_page_1based'], 'key': key['id'],
                           'matching_terms': hits, 'retrieval_score': score,
                           'plaintext_hypothesis': plain,
                           'unpaired_intermediate_coordinate': orphan,
                           'group_layout_hypotheses': edits,
                           'trailing_erasure_hypothesis': tail,
                           'ciphertext_hypothesis': candidate,
                           'context_headers_ocr': block['context_headers_ocr']}
                    for term in hits:
                        if term not in best or score > best[term]['retrieval_score']:
                            best[term] = row
        rows.extend(best.values())
    unique = {json.dumps(row, sort_keys=True): row for row in rows}
    rows = sorted(unique.values(), key=lambda row: (-row['retrieval_score'], row['id'], row['key']))
    result = {'project': 'ADFGVX Cipher', 'authors': 'icekylinx and GPT-6 Astra Pro',
              'blocks': len(blocks), 'keys': len(keys), 'models_evaluated': tested,
              'input_hashes': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in [CORPUS / 'inputs.json', CORPUS / 'run_screen.py', ROOT / 'data/keys.json']},
              'terms': TERMS, 'ranked_results': rows,
              'limits': ['OCR, uniform group repairs and trailing erasures are unverified hypotheses.',
                         'Term scores are retrieval aids, not probabilities or historical evidence.',
                         'No key assignment is changed, but all recorded historical keys are tried.',
                         'This bounded search cannot exclude errors or source relationships outside its model.']}
    (HERE / 'retrieval_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'models': tested, 'unique_hits': len(rows),
                      'top': [(r['id'], r['key'], r['matching_terms']) for r in rows[:15]]}))


if __name__ == '__main__':
    main()
