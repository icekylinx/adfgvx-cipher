#!/usr/bin/env python3
"""Rebuild source maps and exact editorial costs for selected corpus readings.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No language-model score is used to establish a source letter.
"""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

COORDS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direct(cipher, key, original_indices):
    """Independent explicit-column inverse; also preserve every source index."""
    ranks, square = key['column_rank_order'], key['square']
    width, length = len(ranks), len(cipher)
    sizes = [length // width + (c < length % width) for c in range(width)]
    starts = [sum(sizes[d] for d in range(width) if ranks[d] < ranks[c])
              for c in range(width)]
    received = [starts[p % width] + p // width for p in range(length)]
    interim = ''.join(cipher[p] for p in received)
    positions = []
    for p in range(length // 2):
        pair = interim[2*p:2*p+2]
        domain = ''.join(sorted(square[a*6+b]
                               for a in range(6) for b in range(6)
                               if pair[0] in ('?', COORDS[a])
                               and pair[1] in ('?', COORDS[b])))
        positions.append({
            'plaintext_index': p,
            'frame_source_indices': received[2*p:2*p+2],
            'literal_source_indices': [original_indices[i]
                                       for i in received[2*p:2*p+2]],
            'coordinate_pair': pair,
            'domain': domain,
            'raw_plaintext': domain if len(domain) == 1 else '?',
        })
    raw = ''.join(x['raw_plaintext'] for x in positions)
    assert raw == decrypt(cipher, ranks, square, allow_unpaired=bool(length % 2))
    # This direction retains literal erasures. It never guesses their values.
    reconstructed = [''] * length
    for i, value in zip(received, interim):
        assert reconstructed[i] == ''
        reconstructed[i] = value
    assert ''.join(reconstructed) == cipher
    for p in positions:
        if p['raw_plaintext'] != '?':
            at = square.index(p['raw_plaintext'])
            assert COORDS[at//6] + COORDS[at%6] == p['coordinate_pair']
    return {
        'plaintext': raw,
        'plaintext_positions': len(raw),
        'fixed_plaintext_positions': sum(len(p['domain']) == 1 for p in positions),
        'unpaired_coordinate': interim[-1] if length % 2 else None,
        'independent_inverse_agrees_with_project_decoder': True,
        'all_frame_coordinates_roundtrip': True,
        'positions': positions,
    }


def audit_message(message, key, corpus):
    literal = ''.join(''.join(message['source_rows']).split())
    analysis = ''.join(c if c in COORDS else '?' for c in literal)
    invalid = [{'source_index': i, 'literal': c, 'analysis': '?'}
               for i, c in enumerate(literal) if c not in COORDS]
    removed = message.get('geometry_deleted_source_indices', [])
    assert sorted(set(removed)) == removed
    original_indices = [i for i in range(len(literal)) if i not in removed]
    frame = ''.join(analysis[i] for i in original_indices)
    reading = direct(frame, key, original_indices)
    assert reading['plaintext'] == message['expected_raw'], message['id']
    assert len(frame) == message['declared_coordinate_length']
    ocr = ''.join(''.join(corpus[i]['groups']) for i in message['ocr_blocks'])
    opcodes = [
        {'operation': op, 'ocr_span': [a,b], 'source_span': [c,d],
         'ocr': ocr[a:b], 'literal_source': literal[c:d]}
        for op,a,b,c,d in difflib.SequenceMatcher(None, ocr, literal,
                                                autojunk=False).get_opcodes()
        if op != 'equal'
    ]
    report = {
        'id': message['id'],
        'source': {field: message[field] for field in [
            'printed_page', 'pdf_page_1based', 'section', 'heading', 'header',
            'declared_coordinate_length', 'source_rows', 'source_image']},
        'literal_ciphertext': literal,
        'literal_coordinate_slots': len(literal),
        'analysis_ciphertext': analysis,
        'source_erasures_or_invalid_glyphs': invalid,
        'ocr_blocks': message['ocr_blocks'],
        'ocr_comparison': opcodes,
        'key': {f: key[f] for f in ['id', 'column_rank_order', 'square', 'provenance']},
        'geometry': {
            'status': 'unchanged source geometry' if not removed else
                'conditional geometry repair, not the unchanged printed source',
            'deleted_source_indices': removed,
            'deleted_source_glyphs': ''.join(literal[i] for i in removed),
            'frame_ciphertext': frame,
            'frame_coordinates': len(frame),
            'original_source_index_for_frame_index': original_indices,
        },
        'direct_reading_under_stated_geometry': reading,
        'editorial_notes': message['editorial_notes'],
    }
    if removed:
        unmodified = direct(analysis, key, list(range(len(literal))))
        del unmodified['positions']
        report['unmodified_literal_geometry_reading'] = unmodified
    candidate = message.get('editorial_same_length')
    if candidate:
        assert len(candidate) == len(reading['plaintext'])
        encrypted = encrypt(candidate, key['column_rank_order'], key['square'])
        independent = [''] * len(frame)
        letter_edits = []
        for letter, pos in zip(candidate, reading['positions']):
            at = key['square'].index(letter)
            pair = COORDS[at//6] + COORDS[at%6]
            for i, c in zip(pos['frame_source_indices'], pair):
                independent[i] = c
            if pos['raw_plaintext'] != letter:
                letter_edits.append({
                    **pos, 'editorial_plaintext': letter,
                    'editorial_pair': pair,
                    'permitted_by_raw_domain': letter in pos['domain'],
                })
        assert ''.join(independent) == encrypted
        edits, fills = [], []
        for i, (old, new) in enumerate(zip(frame, encrypted)):
            record = {'frame_source_index': i,
                      'literal_source_index': original_indices[i],
                      'literal': literal[original_indices[i]],
                      'analysis': old, 'candidate': new}
            if old == '?':
                fills.append(record)
            elif old != new:
                edits.append(record)
        report['editorial_same_length_candidate'] = {
            'status': 'conditional editorial reading; raw fixed letters and proposed repairs remain separate',
            'plaintext': candidate,
            'reencrypted_ciphertext': encrypted,
            'plaintext_edits_or_fills': letter_edits,
            'known_coordinate_substitutions': edits,
            'erasure_fills': fills,
            'source_coordinate_deletions': len(removed),
            'known_coordinate_substitution_count': len(edits),
            'erasure_fill_count': len(fills),
            'valid_source_coordinates_preserved': len(frame)-len(edits)-len(fills),
            'independent_reencryption_agrees': True,
        }
        if message.get('audit_all_single_deletions'):
            assert len(analysis) == len(encrypted) + 1
            trials = []
            for deleted in range(len(analysis)):
                test = analysis[:deleted] + analysis[deleted+1:]
                trials.append({
                    'deleted_source_index': deleted,
                    'deleted_source_glyph': literal[deleted],
                    'known_coordinate_substitutions': sum(
                        a != '?' and a != b for a, b in zip(test, encrypted)),
                    'erasure_fills': test.count('?'),
                })
            best = min(t['known_coordinate_substitutions'] for t in trials)
            minima = [t['deleted_source_index'] for t in trials
                      if t['known_coordinate_substitutions'] == best]
            report['all_single_deletions_for_stated_candidate'] = {
                'scope': 'Every one-coordinate deletion; the stated plaintext and published key remain fixed. This does not enumerate all German plaintexts.',
                'minimum_known_coordinate_substitutions': best,
                'minimizing_deleted_source_indices': minima,
                'distinct_minimizing_repaired_streams': len({
                    analysis[:i] + analysis[i+1:] for i in minima}),
                'trials': trials,
            }
    elif '?' not in reading['plaintext']:
        assert encrypt(reading['plaintext'], key['column_rank_order'], key['square']) == frame
        report['complete_raw_plaintext_reencrypts_exactly'] = True
    return report


def build(pdf=None):
    sources_path = HERE / 'selected_sources.json'
    sources = json.loads(sources_path.read_text())
    keys_path = ROOT / 'data/keys.json'
    corpus_path = ROOT / 'experiments/p153_corpus/inputs.json'
    keys = {k['id']: k for k in json.loads(keys_path.read_text())['keys']}
    corpus = {b['id']: b for b in json.loads(corpus_path.read_text())['blocks']}
    if pdf:
        assert pdf.stat().st_size == sources['source']['pdf_bytes']
        assert sha(pdf) == sources['source']['pdf_sha256']
    reports = []
    for message in sources['messages']:
        assert keys[message['key_id']]['known_cell_count'] == 36
        reports.append(audit_message(message, keys[message['key_id']], corpus))
    result = {
        'schema': 'adfgvx-corpus-readings-certificate-v1',
        'project': 'ADFGVX Cipher',
        'authors': 'icekylinx and GPT-6 Astra Pro',
        'source': sources['source'],
        'indexing': 'Zero based. Source indices always refer to the literal source transcription, including any separately recorded deleted glyph.',
        'input_hashes': {str(p.relative_to(ROOT)): sha(p)
                         for p in [sources_path, keys_path, corpus_path]},
        'source_crop_hashes': {m['source_image']: sha(ROOT / m['source_image'])
                              for m in sources['messages']},
        'messages': reports,
        'attribution': {
            'period_keys': 'George Lasry and the published historical/research sources enumerated for each key; these keys are not discoveries of the present audit.',
            'present_work': 'Source transcription, complete-message assembly, direct coordinate verification, exact editorial costs, German readings and English explanations: icekylinx and GPT-6 Astra Pro.',
            'priority_limit': 'No first-decipherment priority is claimed for these corpus messages.',
        },
    }
    if sources.get('source_repetitions'):
        by_id = {m['id']: m for m in reports}
        repetitions = []
        for repeat in sources['source_repetitions']:
            literal = ''.join(''.join(repeat['source_rows']).split())
            assert all(c in COORDS for c in literal)
            start, stop = repeat['match_source_span']
            full = by_id[repeat['match_message_id']]['literal_ciphertext']
            assert full[start:stop] == literal
            assert len(literal) == stop - start
            repetitions.append({
                **repeat,
                'literal_ciphertext': literal,
                'matched_coordinate_count': len(literal),
                'exact_transmitted_suffix_match': stop == len(full),
                'scope': 'An exact transmitted substring of the longer witness; not a separately decrypted complete message under a shorter frame.',
            })
            result['source_crop_hashes'][repeat['source_image']] = sha(
                ROOT / repeat['source_image'])
        result['source_repetitions'] = repetitions
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    target = HERE / 'certificates.json'
    if args.verify:
        assert result == json.loads(target.read_text()), 'Certificate differs from fresh computation.'
        print(f'Verified {len(result["messages"])} source-reviewed readings, coordinate maps and editorial costs.')
    else:
        target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        print(f'Wrote {target.relative_to(ROOT)} ({len(result["messages"])} messages).')


if __name__ == '__main__':
    main()
