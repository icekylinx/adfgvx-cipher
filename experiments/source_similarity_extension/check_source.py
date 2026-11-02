#!/usr/bin/env python3
"""Check the source-reviewed p189 C hit and its unchanged-key reading.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The supplementary message is contextual evidence, not a p132 retransmission.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

spec = importlib.util.spec_from_file_location(
    'source_retrieval', ROOT / 'experiments/source_similarity/retrieve.py')
retrieval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retrieval)

COORDS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
SOURCE = {
    'title': 'General Solution of the ADFGVX Cipher System, Childs collection',
    'url': 'https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view',
    'pdf_sha256': '157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06',
    'pdf_bytes': 156848258,
    'printed_page': 189,
    'pdf_page_1based': 192,
    'section': 'C',
    'printed_heading': '15th NOVEMBER, 1918.',
    'header': 'NKJ v LP (9.14 a.m., November 15th); 1000 (15); RIZI-124',
    'printed_length_field': 124,
    'source_rows': [
        'XXVFV FFDVG VGFFV AGVAA XDAVF XXGXX VXAAF GDFGV',
        'XXFVV AFAFA FFAGV DVAXV DFAXF GXDFF DFFFA AVXGG',
        'VFFAA XVAVA XFAGF AVXDV AFXAG FAGFA AFAFG XGAXX',
        'XFXX',
    ],
    'inspection': 'The full page and a fourfold-resolution crop were visually inspected. All 124 coordinate glyphs are legible; the last row XFXX is present in the source but absent from the 120-slot corpus OCR block.',
    'crop_pdf_points': [35, 330, 543.16, 435],
}
EXPECTED_RAW = 'UNLOESBA?EHUNKSPRUECHENACHDEZEMBERSCHLUESSELENTZIFFERNXXIRRTUM'
EDITORIAL = 'UNLOESBAREFUNKSPRUECHENACHDEZEMBERSCHLUESSELENTZIFFERNXXIRRTUM'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direct_decode(ciphertext, key):
    """Use explicit column offsets, independently of the project decoder."""
    ranks, square = key['column_rank_order'], key['square']
    width, length = len(ranks), len(ciphertext)
    sizes = [length // width + (c < length % width) for c in range(width)]
    starts = [sum(sizes[d] for d in range(width) if ranks[d] < ranks[c])
              for c in range(width)]
    source_index = [starts[p % width] + p // width for p in range(length)]
    interim = ''.join(ciphertext[p] for p in source_index)
    unused = ''.join(sorted(set(ALPHABET) - set(square)))
    positions = []
    for p in range(length // 2):
        pair = interim[2*p:2*p+2]
        cell = 6 * COORDS.index(pair[0]) + COORDS.index(pair[1])
        char = square[cell]
        positions.append({
            'plaintext_index': p,
            'source_indices': source_index[2*p:2*p+2],
            'coordinate_pair': pair,
            'square_cell_index': cell,
            'raw_plaintext': char,
            'domain_under_conservative_square': unused if char == '?' else char,
        })
    raw = ''.join(p['raw_plaintext'] for p in positions)
    assert raw == decrypt(ciphertext, ranks, square)
    # Reconstruct the transmitted stream from each independently mapped pair.
    reconstructed = [''] * length
    for p in positions:
        for at, value in zip(p['source_indices'], p['coordinate_pair']):
            assert not reconstructed[at]
            reconstructed[at] = value
    assert ''.join(reconstructed) == ciphertext
    # Every known plaintext letter has a unique pair and reproduces its two
    # observed coordinates. The unknown cell is retained by pair, not filled.
    for p in positions:
        if p['raw_plaintext'] != '?':
            cell = square.index(p['raw_plaintext'])
            assert COORDS[cell // 6] + COORDS[cell % 6] == p['coordinate_pair']
    return {
        'key_id': key['id'],
        'column_rank_order': ranks,
        'square': square,
        'raw_plaintext': raw,
        'plaintext_slots': len(raw),
        'fixed_plaintext_positions': len(raw.replace('?', '')),
        'source_coordinates_preserved': length,
        'independent_column_map_agrees_with_project_decoder': True,
        'per_position': positions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, help='Optionally verify the inspected PDF hash.')
    parser.add_argument('--verify', action='store_true', help='Check the committed result without rewriting it.')
    args = parser.parse_args()
    if args.pdf:
        assert args.pdf.stat().st_size == SOURCE['pdf_bytes']
        assert sha(args.pdf) == SOURCE['pdf_sha256']
    inputs = [ROOT / 'data/messages.json', ROOT / 'data/keys.json',
              ROOT / 'experiments/p153_corpus/inputs.json',
              ROOT / 'experiments/source_similarity/retrieve.py',
              HERE / 'results.json']
    messages = {m['id']: m for m in json.loads(inputs[0].read_text())['messages']}
    keys = {k['id']: k for k in json.loads(inputs[1].read_text())['keys']}
    corpus = {b['id']: b for b in json.loads(inputs[2].read_text())['blocks']}
    query = messages['p132']['transcript']['analysis_ciphertext']
    source = retrieval.clean(''.join(SOURCE['source_rows']))
    ocr_block = corpus['p189_ocr_block3']
    ocr = retrieval.clean(''.join(ocr_block['groups']))
    assert len(source) == SOURCE['printed_length_field'] == 124
    assert len(ocr) == 120 and ocr == source[:120] and source[120:] == 'XFXX'
    layers = {}
    for name, sequence in [('raw_corpus_ocr', ocr), ('image_reviewed_transcript', source)]:
        score, longest, fitting = retrieval.reference_metrics(query, sequence)
        trace = retrieval.local_trace(query, sequence)
        assert trace['local_score'] == score
        layers[name] = {
            'ciphertext': sequence,
            'slots': len(sequence),
            'known_coordinates': len(sequence.replace('?', '')),
            'affine_local_score': score,
            'longest_exact_run': longest,
            'full_query_fitting_cost': fitting,
            'optimal_local_alignment': trace,
        }
    recorded = json.loads(inputs[4].read_text())['reports']['p132']
    prior_trace = next(x['trace'] for x in recorded['selected_cross_page_alignments']
                       if x['block_id'] == 'p189_ocr_block3')
    assert prior_trace == layers['raw_corpus_ocr']['optimal_local_alignment']
    decodes = [direct_decode(source, keys[k])
               for k in ['Nov13-15a', 'Nov13-15b', 'CHI-Nov13']]
    reading = next(d for d in decodes if d['key_id'] == 'Nov13-15b')
    assert reading['raw_plaintext'] == EXPECTED_RAW
    assert len(EDITORIAL) == len(EXPECTED_RAW) == 62
    assert reading['fixed_plaintext_positions'] == 61
    key = keys['Nov13-15b']
    candidate_cipher = encrypt(EDITORIAL, key['column_rank_order'], key['square'])
    candidate_from_map = [''] * len(source)
    for candidate, position in zip(EDITORIAL, reading['per_position']):
        cell = key['square'].index(candidate)
        pair = COORDS[cell // 6] + COORDS[cell % 6]
        for at, value in zip(position['source_indices'], pair):
            assert not candidate_from_map[at]
            candidate_from_map[at] = value
    assert ''.join(candidate_from_map) == candidate_cipher
    coordinate_edits = [
        {'source_index': i, 'observed': a, 'editorial_candidate': b}
        for i, (a, b) in enumerate(zip(source, candidate_cipher)) if a != b]
    assert coordinate_edits == [
        {'source_index': 23, 'observed': 'V', 'editorial_candidate': 'F'},
        {'source_index': 62, 'observed': 'A', 'editorial_candidate': 'D'},
    ]
    letter_edits = []
    for p, (raw, candidate) in enumerate(zip(EXPECTED_RAW, EDITORIAL)):
        if raw == candidate:
            continue
        original = reading['per_position'][p]
        cell = key['square'].index(candidate)
        pair = COORDS[cell // 6] + COORDS[cell % 6]
        letter_edits.append({
            **original, 'editorial_plaintext': candidate,
            'editorial_coordinate_pair': pair,
            'changed_source_indices': [i for i, a, b in zip(
                original['source_indices'], original['coordinate_pair'], pair) if a != b],
            'compatible_without_known_coordinate_change':
                candidate in original['domain_under_conservative_square'],
        })
    assert [p['plaintext_index'] for p in letter_edits] == [8, 10]
    # No source erasures exist: both editorial changes replace observed glyphs.
    assert '?' not in source and len(coordinate_edits) == 2
    for d in decodes:
        if d['key_id'] != 'Nov13-15b':
            del d['per_position']
    result = {
        'schema': 'adfgvx-p189-C-source-inspection-v1',
        'project': 'ADFGVX Cipher',
        'authors': 'icekylinx and GPT-6 Astra Pro',
        'source': SOURCE,
        'input_hashes': {str(p.relative_to(ROOT)): sha(p) for p in inputs},
        'indexing': 'Zero-based indices and half-open spans. Source coordinates refer to the complete image-reviewed 124-coordinate p189 C transcript.',
        'selection': 'The highest unreviewed cross-page affine-local hit in the 22-target extension: p132 against p189_ocr_block3. Its source date motivated the three unchanged published Nov13 key checks.',
        'query_id': 'p132',
        'query_ciphertext': query,
        'query_slots': len(query),
        'ocr_block_id': 'p189_ocr_block3',
        'ocr_header': ocr_block['context_headers_ocr'],
        'ocr_corrections': [
            {'kind': 'omitted_final_row', 'source_span': [120, 124],
             'visible_text': 'XFXX', 'change_to_observed_source': False},
            {'kind': 'header_year_misrecognition', 'ocr': '1915', 'source': '1918'},
        ],
        'layers': layers,
        'unchanged_key_decodes': decodes,
        'editorial_reading': {
            'status': 'Plausible normalization requiring two known-coordinate substitutions; not a verbatim decryption.',
            'plaintext': EDITORIAL,
            'display': 'Unloesba[r]e [F]unksprueche nach Dezemberschluessel entziffern. Irrtum.',
            'meaning': 'Decipher undecipherable radio messages using the December key. Error.',
            'punctuation': 'Word spacing, capitalization and punctuation are editorial. XX precedes IRRTUM in the raw text.',
            'plaintext_edits': letter_edits,
            'reencrypted_candidate': candidate_cipher,
            'coordinate_substitutions': coordinate_edits,
            'source_coordinate_substitutions': 2,
            'source_erasures_filled': 0,
            'source_coordinates_unchanged': 122,
            'unknown_square_explanation': 'Raw position 8 uses VG, an unfilled square cell with domain 234789QY. R is already fixed at FG, so inserting R in VG would violate the injective square. UNLOESBARE instead requires observed source index 23 V to change to F.',
            'chronology_note': 'DEZEMBER and IRRTUM are directly decoded with fixed published square cells. The printed heading is 15 November 1918. No explanation, date correction, cancellation convention or substitution of NOVEMBER is inferred.',
        },
        'comparison_with_p132': {
            'p132_published_reading': 'FFEREILVESEXWIEDERHOLETTELEGRXVONVIERTERPERIODEINFUTNFTERXGEBETSORHER5MINXVVV',
            'p132_key': 'Nov4-6',
            'p189_C_key': 'Nov13-15b',
            'assessment': 'The messages both discuss handling difficult radio traffic, but their decoded instructions and published keys differ. The short ciphertext match does not identify a common plaintext segment or a repeated transmission.',
            'p132_reference': 'cases/p132.md',
            'p132_prior_credit': 'Thomas, comment 27 (2017-03-02), and Norbert, comments 37 and 40 (2017-03-11 and 2017-03-12); prior readings remain credited in the case page.',
        },
        'attribution': {
            'period_key': 'George Lasry, 2017-02-27, comment 11; published period key provenance retained in data/keys.json.',
            'key_url': 'https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1',
            'present_work': 'Source transcription, recovery of an omitted OCR row, direct unchanged-key verification, exact editorial costs and contextual comparison: icekylinx and GPT-6 Astra Pro.',
            'priority_limit': 'No first decipherment priority is claimed for this supplementary corpus message.',
        },
        'limits': [
            'The 788-block OCR corpus remains a retrieval aid. Only this additional leading hit was newly image-reviewed here.',
            'Adding the visible final XFXX repairs the OCR layer, not the historical ciphertext.',
            'No unknown square cell was assigned, no key was optimized, and no source coordinate was changed in the raw reading.',
            'The editorial reading is separately re-encrypted and its two observed-coordinate disagreements are explicit.',
            'This supplementary instruction adds no fixed plaintext letters to the p132 challenge and does not independently validate its VORHER clause.',
        ],
    }
    target = HERE / 'source_inspection.json'
    if args.verify:
        assert json.loads(target.read_text()) == result
    else:
        target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({
        'source_slots': len(source), 'ocr_slots': len(ocr),
        'source_metrics': {k: v for k, v in layers['image_reviewed_transcript'].items()
                           if k not in ['ciphertext', 'optimal_local_alignment']},
        'raw_plaintext': EXPECTED_RAW,
        'editorial_plaintext': EDITORIAL,
        'editorial_coordinate_edits': coordinate_edits,
        'unknown_square_cell_fills': 0,
        'p132_parallel_established': False,
    }, indent=2))


if __name__ == '__main__':
    main()
