#!/usr/bin/env python3
"""Bounded retrieval of source companions; no candidate is a decipherment claim.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
This reuses the existing unverified OCR blocks and declared layout generator.
It tries at most the raw plus three uniform group-layout variants, followed by
zero through four explicit trailing erasures. Those are OCR hypotheses only.
Known historical keys are tried without changing any square assignment.
"""
from pathlib import Path
import argparse
import difflib
import hashlib
import importlib.util
import itertools
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORPUS = ROOT / 'experiments/p153_corpus'
spec = importlib.util.spec_from_file_location('corpus_screen', CORPUS / 'run_screen.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

TERMS = {
    'p109': ['SAVA', 'UEBERGANG', 'LETZTER', 'BEENDET', 'ERKANNT',
             'BELGRAD', 'ABENDMEL', 'WEITERE', 'FDLXDIV'],
    'p132': ['EILVESE', 'WIEDERHO', 'TELEGR', 'PERIODE', 'FUENFTER', 'VORHER', '5MIN'],
    'p146': ['KERTSCH', 'RICHARD', 'EMILKARL', 'RUFNAM', 'RUFZEICH',
             'FUNKSTELLE', 'NACHRICHTEN', '12X11'],
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    blocks = json.loads((CORPUS / 'inputs.json').read_text())['blocks']
    messages = {x['id']: x for x in json.loads((ROOT / 'data/messages.json').read_text())['messages']}
    keys = [x for x in json.loads((ROOT / 'data/keys.json').read_text())['keys']
            if set(x['square']) != {'?'}]
    retrieval = {name: [] for name in TERMS}
    direct_similarity = {}
    for name in TERMS:
        source = messages[name]['transcript']['analysis_ciphertext']
        grams = {source[i:i+7] for i in range(len(source)-6)
                 if '?' not in source[i:i+7]}
        rows = []
        for block in blocks:
            text = ''.join(block['groups'])
            shared = sum(text[i:i+7] in grams for i in range(len(text)-6))
            if shared < 2:
                continue
            matches = difflib.SequenceMatcher(None, source, text, autojunk=False).get_matching_blocks()
            rows.append({'id': block['id'], 'printed_page': block['printed_page'],
                         'source_slots': len(text), 'shared_sevengrams': shared,
                         'sequence_matching_characters': sum(x.size for x in matches),
                         'longest_matching_run': max(x.size for x in matches)})
        rows.sort(key=lambda x: (-x['shared_sevengrams'], -x['sequence_matching_characters'], x['id']))
        direct_similarity[name] = rows[:20]
    tested = 0
    for block in blocks:
        best = {}
        layouts = list(itertools.islice(module.variants(block), 4))
        seen = set()
        for ciphertext, edits in layouts:
            for tail in range(5):
                candidate = ciphertext + '?' * tail
                if candidate in seen:
                    continue
                seen.add(candidate)
                for key in keys:
                    plain, orphan = module.decrypt(candidate, key['column_rank_order'], key['square'])
                    plain = plain.upper()
                    tested += 1
                    for name, terms in TERMS.items():
                        hits = [term for term in terms if term in plain]
                        if not hits:
                            continue
                        score = sum(len(term)**2 for term in hits)
                        previous = best.get(name)
                        row = {'id': block['id'], 'printed_page': block['printed_page'],
                               'pdf_page_1based': block['pdf_page_1based'], 'key': key['id'],
                               'matching_terms': hits, 'retrieval_score': score,
                               'plaintext_hypothesis': plain,
                               'unpaired_intermediate_coordinate': orphan,
                               'group_layout_hypotheses': edits,
                               'trailing_erasure_hypothesis': tail,
                               'ciphertext_hypothesis': candidate,
                               'context_headers_ocr': block['context_headers_ocr']}
                        if previous is None or score > previous['retrieval_score']:
                            best[name] = row
        for name, row in best.items():
            retrieval[name].append(row)
    for rows in retrieval.values():
        rows.sort(key=lambda x: (-x['retrieval_score'], x['id']))
    return {'format_version': 1, 'project': 'ADFGVX Cipher',
            'authors': ['icekylinx', 'GPT-6 Astra Pro'],
            'input_hashes': {'ocr_blocks': digest(CORPUS / 'inputs.json'),
                             'layout_code': digest(CORPUS / 'run_screen.py'),
                             'keys': digest(ROOT / 'data/keys.json'),
                             'messages': digest(ROOT / 'data/messages.json')},
            'blocks': len(blocks), 'keys': len(keys), 'models_evaluated': tested,
            'search_terms': TERMS, 'direct_ciphertext_similarity': direct_similarity,
            'ranked_retrieval': {name: rows[:30] for name, rows in retrieval.items()},
            'limits': ['All OCR and layout candidates remain unverified until the source image is checked.',
                       'The score is a deterministic retrieval aid, not a likelihood or confidence.',
                       'The search cannot exclude missing source records, unmodelled errors or different keys.',
                       'Trailing erasures are exploratory OCR hypotheses, not observed source gaps.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=HERE / 'retrieval_results.json')
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'blocks': result['blocks'], 'keys': result['keys'],
                      'models_evaluated': result['models_evaluated'],
                      'top_hits': {k: [(r['id'], r['key'], r['matching_terms']) for r in v[:5]]
                                   for k, v in result['ranked_retrieval'].items()}}))
