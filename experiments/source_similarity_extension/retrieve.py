#!/usr/bin/env python3
"""Extend the calibrated source-similarity search to all 22 challenge entries.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
This retrieves OCR candidates; it does not establish source relationships.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / 'experiments/source_similarity'
spec = importlib.util.spec_from_file_location('source_retrieval', BASE / 'retrieve.py')
retrieval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retrieval)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir', type=Path, default=Path('/tmp/adfgvx-source-extension'))
    parser.add_argument('--output', type=Path, default=HERE / 'results.json')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    binary = args.work_dir / 'align'
    subprocess.run(['c++', '-std=c++17', '-O3', str(BASE / 'align.cpp'), '-o', str(binary)], check=True)
    catalog = json.loads((ROOT / 'data/messages.json').read_text())['messages']
    messages = {m['id']: m for m in catalog}
    queries = {m['id']: m['transcript']['analysis_ciphertext'] for m in catalog}
    corpus = json.loads((ROOT / 'experiments/p153_corpus/inputs.json').read_text())['blocks']
    metadata = {b['id']: b for b in corpus}
    blocks = {b['id']: retrieval.clean(''.join(b['groups'])) for b in corpus}
    metrics = retrieval.run_kernel(binary, queries, blocks, args.work_dir)
    rows = {q: [] for q in queries}
    for q, b, local, longest, fitting in metrics:
        rows[q].append({
            'block_id': b,
            'printed_page': metadata[b]['printed_page'],
            'same_printed_page': metadata[b]['printed_page'] == messages[q]['source']['printed_page'],
            'slots': len(blocks[b]),
            'known_coordinates': len(blocks[b].replace('?', '')),
            'affine_local_score': int(local),
            'longest_exact_run': int(longest),
            'full_query_fitting_cost': int(fitting),
        })
    reports = {}
    control_checks = []
    previous = json.loads((BASE / 'results.json').read_text())
    for q in queries:
        key = lambda x: (-x['affine_local_score'], -x['longest_exact_run'], x['block_id'])
        other = sorted([r for r in rows[q] if not r['same_printed_page']], key=key)
        same = sorted([r for r in rows[q] if r['same_printed_page']], key=key)
        exact = sorted([r for r in rows[q] if not r['same_printed_page']],
                       key=lambda x: (-x['longest_exact_run'], -x['affine_local_score'], x['block_id']))
        selected = {r['block_id'] for r in other[:3] + exact[:3]}
        traces = []
        for b in sorted(selected):
            trace = retrieval.local_trace(queries[q], blocks[b])
            row = next(r for r in rows[q] if r['block_id'] == b)
            assert trace['local_score'] == row['affine_local_score']
            traces.append({'block_id': b, 'headers_ocr': metadata[b]['context_headers_ocr'], 'trace': trace})
        reports[q] = {
            'source': messages[q]['source'],
            'query': queries[q],
            'query_slots': len(queries[q]),
            'other_page_local_top5': other[:5],
            'other_page_exact_run_top5': exact[:5],
            'same_page_local_ranking': same,
            'selected_cross_page_alignments': traces,
        }
        if q in previous['reports']:
            for known in previous['reports'][q].get('known_relationship_ranks', []):
                b = known['block_id']
                now = next(r for r in rows[q] if r['block_id'] == b)
                before = known['metrics']
                for metric in ['affine_local_score', 'longest_exact_run', 'full_query_fitting_cost']:
                    assert now[metric] == before[metric]
                control_checks.append({'query': q, 'block_id': b, 'reproduced_metrics': True})
    result = {
        'schema': 'adfgvx-all-target-source-retrieval-v1',
        'project': 'ADFGVX Cipher',
        'authors': 'icekylinx and GPT-6 Astra Pro',
        'input_hashes': {str(p.relative_to(ROOT)): sha(p) for p in [
            ROOT / 'data/messages.json', ROOT / 'experiments/p153_corpus/inputs.json',
            BASE / 'align.cpp', BASE / 'retrieve.py', BASE / 'results.json']},
        'query_count': len(queries),
        'corpus_blocks': len(blocks),
        'pairwise_comparisons': len(metrics),
        'metrics': previous['metrics'],
        'prior_control_metrics_checked': control_checks,
        'reports': reports,
        'limits': [
            'All candidate blocks remain unverified OCR until an explicit image review.',
            'Same-page results include the target itself and are displayed separately, not silently discarded.',
            'Cross-page rank one is a retrieval priority, not evidence that a parallel exists.',
            'Short exact runs and local matches are expected in a six-symbol alphabet.',
            'New search coverage does not fix any plaintext or exclude missing or differently encrypted parallels.',
        ],
    }
    if args.verify:
        assert json.loads(args.output.read_text()) == result
    else:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({
        'queries': len(queries), 'comparisons': len(metrics),
        'previous_relationship_metrics_checked': len(control_checks),
        'best_other_page': {q: r['other_page_local_top5'][:2] for q, r in reports.items()},
    }, indent=2))


if __name__ == '__main__':
    main()
