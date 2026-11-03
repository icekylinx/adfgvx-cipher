#!/usr/bin/env python3
"""Independent source, cost, insertion and coupled-key audit for p162 B1/C2/D1.

Prepared by icekylinx and GPT-6 Astra Pro. Standard library only. Source glyph
observations are manual; the script independently replays arithmetic and full
re-encryption. It imports neither adfgvx.cipher nor the package verifier.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CO = 'ADFGVX'
KEY = {'id': 'Nov7-9', 'square': 'PRMYUW3LZGES8C71QOV29ITB40?KXH?AJNDF',
       'column_rank_order': [6, 12, 7, 15, 1, 11, 16, 5, 8, 14, 3, 18, 9, 13, 2, 17, 20, 10, 19, 4]}
ROWS = {
'p162_B1': '''DGDD AFGXA DXDXG VGGGA DAGXV FDDVF XVGGA ADGVG
AGAAD DVXAX GDGXV GDGDX DAGFD DAXVV VFXDX GXDAV
FDVXV Z-VXD VVVXV VDFXV XVDVG VFXVV VFGGD DDDVD
VDVDG DDVVG XXFVV DGDXD XXXXD GDDGG -DVDD ADDVX
DDGAA GDFGF FDDGD VGDDG FD''',
'p162_C1': '''GGDFX VVVDV VVDVD VDXDG VVXXG GDDVV XXVGD VVGXD
XGVXD DDAXD GVGDF AGVDD VGXXV AVDGD GDGAX FDGGD
DDVXX VDVGD FFVDF AXAXD XGFFV VXAVA AFAXD AG''',
'p162_C2': '''ADDXV DDDVD AAXVA DXGGA DDDFG GVDAX GGADF D-XDF
FVXXF VVDXF DVVGX VXVDD XVVDX XVDVF GGVVD XDADF
DGVGV AFGVD AXDXV DVAFA''',
'p162_D1': '''AFXAX DVFDA FXGDG XGVXV VXCGV XGDDA DDGVG DXCGD
VGXAA XXADF VDDVX VVXDD XVGDV XDVVX VXVVG GVXXC
VGXXF DXGVV FXDVV GFAFA'''
}
TARGETS = {
'p162_B1': 'STELLVERTRXGENERALSTABBERLINXZUSENDUNGVONJE?0BLAETTERNKARTE1ZU7?000XB1B2B3C1C2C3D1D2D3E2E3X',
'p162_C2': 'TIRASPOLERHIELTMXGXFEUERANDERGRENZEXAKONACH17ROEM4',
'p162_D1': 'DEUTSCHEBOTSCHAFTKONSTANTINOPELXUNTERSCHRIFTSTUMMX'
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def order(n):
    ranks = KEY['column_rank_order']
    return sorted(range(n), key=lambda i: (ranks[i % len(ranks)], i // len(ranks)))


def decode(source, square=None):
    square = square or KEY['square']
    mid, origins = [''] * len(source), [None] * len(source)
    for j, i in enumerate(order(len(source))):
        mid[i], origins[i] = source[j], j
    details = []
    for i in range(0, len(mid) - 1, 2):
        pair = ''.join(mid[i:i + 2])
        cells = [a * 6 + b for a in range(6) for b in range(6)
                 if (pair[0] not in CO or pair[0] == CO[a])
                 and (pair[1] not in CO or pair[1] == CO[b])]
        domain = set()
        for cell in cells:
            domain.update(square[cell] if square[cell] != '?' else '56')
        domain = ''.join(sorted(domain))
        details.append({'plaintext_index': i // 2, 'pair': pair, 'working_source_indices': origins[i:i + 2],
                        'square_cells': cells, 'domain': domain,
                        'label': domain if len(domain) == 1 else '?'})
    return ''.join(d['label'] for d in details), details


def encrypt(text, square=None, unknown_pairs=None):
    square = square or KEY['square']
    unknown_pairs = unknown_pairs or {}
    mid = ''
    for i, c in enumerate(text):
        if c == '?':
            mid += unknown_pairs[i]
        else:
            j = square.index(c)
            mid += CO[j // 6] + CO[j % 6]
    return ''.join(mid[i] for i in order(len(mid)))


def frame(source, gap=None):
    if gap is None:
        return source, list(range(len(source)))
    return source[:gap] + '?' + source[gap:], list(range(gap)) + [None] + list(range(gap, len(source)))


def cost(actual, wanted, origins):
    assert len(actual) == len(wanted) == len(origins)
    subs, fills, additions = [], [], []
    for i, (a, b) in enumerate(zip(actual, wanted)):
        if a == b:
            continue
        item = {'working_index': i, 'source_index': origins[i], 'before': a, 'after': b}
        if origins[i] is None:
            additions.append(item)
        elif a in CO:
            subs.append(item)
        else:
            fills.append(item)
    return {'observed_substitutions': subs, 'source_mask_fills': fills, 'missing_coordinate_fills': additions}


def counts(ledger):
    return {k: len(v) for k, v in ledger.items()}


def build(source_dir=None, inputs=None, certificate=None):
    source = {k: ''.join(v.split()) for k, v in ROWS.items()}
    assert [len(source[k]) for k in ROWS] == [181, 117, 100, 100]
    image_bindings = []
    if source_dir:
        for name in ['B.png', 'B_faint.png', 'B_group4.png', 'B_group8.png', 'C.png', 'D.png']:
            p = source_dir / name
            image_bindings.append({'path_at_manual_review': str(p), 'sha256': sha(p)})
        import ast
        rows_ast = ast.parse((source_dir / 'rows.py').read_text())
        assignment = next(n for n in rows_ast.body if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == 'ROWS' for t in n.targets))
        owner_rows = ast.literal_eval(assignment.value)
        assert {k: ''.join(v.split()) for k, v in owner_rows.items()} == source
    formal = None
    if inputs:
        inp = json.loads(inputs.read_text())
        key = inp['key']
        assert key['id'] == KEY['id'] and key['square'] == KEY['square']
        assert key['column_rank_order'] == KEY['column_rank_order']
        formal = {'inputs_sha256': sha(inputs)}
        if certificate:
            formal['certificates_sha256'] = sha(certificate)
        # Input field normalization is deliberately explicit and bounded.
        for r in inp['records']:
            assert r['id'] in TARGETS
            rows = r.get('rows', r.get('source_rows'))
            assert rows is not None
            assert ''.join(''.join(rows).split()) == source[r['id']]
    records = []
    expected_ledgers = {
      'p162_B1': {'observed_substitutions': [(110, 'F', 'D'), (150, 'D', 'V')],
                 'source_mask_fills': [(84, 'Z', 'A'), (85, '-', 'V'), (149, '-', 'D')],
                 'missing_coordinate_fills': [(None, '?', 'D')]},
      'p162_C2': {'observed_substitutions': [], 'source_mask_fills': [(36, '-', 'G')],
                 'missing_coordinate_fills': []},
      'p162_D1': {'observed_substitutions': [], 'source_mask_fills': [(22, 'C', 'G'), (37, 'C', 'G'), (79, 'C', 'G')],
                 'missing_coordinate_fills': []}}
    for ident, target in TARGETS.items():
        gap = 1 if ident == 'p162_B1' else None
        actual, origins = frame(source[ident], gap)
        raw, raw_details = decode(actual)
        pairs = {43: 'XA', 63: 'XA'} if ident == 'p162_B1' else {}
        wanted = encrypt(target, unknown_pairs=pairs)
        edited, edited_details = decode(wanted)
        assert edited == target
        ledger = cost(actual, wanted, origins)
        for kind, entries in ledger.items():
            assert [(e['source_index'], e['before'], e['after']) for e in entries] == expected_ledgers[ident][kind]
        records.append({'id': ident, 'source_slots': len(source[ident]),
                        'valid_source_coordinates': sum(c in CO for c in source[ident]),
                        'working_frame_slots': len(actual), 'plaintext_positions': len(raw),
                        'raw_plaintext': raw, 'raw_fixed_positions': len(raw) - raw.count('?'),
                        'edited_plaintext': edited, 'edited_fixed_positions': len(edited) - edited.count('?'),
                        'raw_domains': [d for d in raw_details if d['label'] == '?'],
                        'edited_domains': [d for d in edited_details if d['label'] == '?'],
                        'primary_missing_coordinate_index': gap, 'ledger': ledger,
                        'repaired_working_ciphertext': wanted})
    b = records[0]
    fixed_wanted = b['repaired_working_ciphertext']
    scans = []
    for glyph in ['F', 'E']:
        variant = source['p162_B1'][:110] + glyph + source['p162_B1'][111:]
        evaluations = []
        for gap in range(182):
            actual, origins = frame(variant, gap)
            ledger = cost(actual, fixed_wanted, origins)
            evaluations.append({'insert_before_source_index': gap, **counts(ledger)})
        minimum = min(r['observed_substitutions'] for r in evaluations)
        best = [r['insert_before_source_index'] for r in evaluations if r['observed_substitutions'] == minimum]
        assert best == [0, 1] and minimum == (2 if glyph == 'F' else 1)
        primary, origins = frame(variant, 1)
        scans.append({'source110_glyph_model': glyph, 'actual_evaluated_insertion_boundaries': len(evaluations),
                      'scope': 'Fixed 91-position target with the two unresolved numerical positions both bound to square cell XA; all 182 transmitted-frame one-coordinate insertion boundaries. Source masks are retained. This is a retrospective source-consistency comparison, not an unrestricted plaintext search.',
                      'minimum_observed_substitutions': minimum, 'minimizing_boundaries': best,
                      'first_five_observed_substitution_costs': [r['observed_substitutions'] for r in evaluations[:5]],
                      'observed_substitution_histogram': {str(k): v for k, v in sorted(Counter(r['observed_substitutions'] for r in evaluations).items())},
                      'all_evaluations': evaluations, 'selected_boundary1_ledger': cost(primary, fixed_wanted, origins),
                      'selected_boundary1_raw': decode(primary)[0]})
    # Two global full-key completions; each is shared by all positions and records.
    witnesses = []
    for vf, xa in [('5', '6'), ('6', '5')]:
        square = list(KEY['square']);square[26] = vf;square[30] = xa;square = ''.join(square)
        assert len(set(square)) == 36
        completions = []
        for r in records:
            text, details = decode(r['repaired_working_ciphertext'], square)
            assert '?' not in text and encrypt(text, square) == r['repaired_working_ciphertext']
            assert all(a == '?' or a == z for a, z in zip(r['edited_plaintext'], text))
            completions.append({'id': r['id'], 'plaintext': text,
                                'reencoded_ciphertext': encrypt(text, square)})
        btext = completions[0]['plaintext']
        assert btext[43] == xa == btext[63]
        witnesses.append({'square': square, 'assignments': {'VF': vf, 'XA': xa},
                          'quantity_field': btext[43:45], 'scale_denominator_field': btext[62:67],
                          'records': completions})
    assert [(x['quantity_field'], x['scale_denominator_field']) for x in witnesses] == [('60', '76000'), ('50', '75000')]
    summary = {'accepted_physical_records': len(records),
               'source_slots': sum(r['source_slots'] for r in records),
               'valid_source_coordinates': sum(r['valid_source_coordinates'] for r in records),
               'working_frame_slots': sum(r['working_frame_slots'] for r in records),
               'plaintext_positions': sum(r['plaintext_positions'] for r in records),
               'raw_fixed_positions': sum(r['raw_fixed_positions'] for r in records),
               'edited_fixed_positions': sum(r['edited_fixed_positions'] for r in records),
               'observed_substitutions': sum(len(r['ledger']['observed_substitutions']) for r in records),
               'source_mask_fills': sum(len(r['ledger']['source_mask_fills']) for r in records),
               'missing_coordinate_fills': sum(len(r['ledger']['missing_coordinate_fills']) for r in records),
               'observed_coordinate_exclusions': 0,
               'primary_complete_insertion_scan_evaluations': 182,
               'alternate_E_glyph_insertion_scan_evaluations': 182,
               'global_key_completions': len(witnesses),
               'unread_C1_source_slots_not_counted_as_accepted': 117}
    assert summary['source_slots'] == 381 and summary['valid_source_coordinates'] == 374
    assert summary['raw_fixed_positions'] == 181 and summary['edited_fixed_positions'] == 189
    assert (summary['observed_substitutions'], summary['source_mask_fills'], summary['missing_coordinate_fills']) == (2, 7, 1)
    return {'schema': 'adfgvx-p162-independent-audit-v1', 'authors': ['icekylinx', 'GPT-6 Astra Pro'],
            'formal_package_binding': formal, 'source_images_manually_reviewed': image_bindings,
            'manual_source_observations': [
                'B1 opening DGDD has four characters. The printed label is RICHI-182?; the question mark is literal. The complete transcribed frame has 181 slots.',
                'The high-resolution fourth and eighth groups support VGGGA and ADGVG, respectively.',
                'Faded groups XVGGA and VFXDX are retained. VFGGD is the main reading, with explicit F/E sensitivity at source 110. No plaintext was used to resolve that ambiguity.',
                'B1 Z at 84 and dashes at 85/149 are source masks; source 110 remains an observed F in the primary cost ledger.',
                'C1 has 117 observed coordinates and remains unread. It is excluded from accepted-record and plaintext totals.',
                'C2 has 100 slots with one dash at 36. The footer NKJ UM is outside the cipher frame.',
                'D1 has 100 slots with three visible C glyphs at 22,37,79. The header reads 1330 (8/13), a literal odd date which is not normalized.'],
            'records': records, 'summary': summary, 'insertion_scans': scans,
            'global_full_key_witnesses': witnesses,
            'coupled_numeral_finding': {'plaintext_positions_zero_based': [43, 63], 'shared_square_cell': 'XA',
                                       'supported_quantity_and_scale_pairs': [['50', '1:75000'], ['60', '1:76000']],
                                       'unsupported_mixed_pairs': [['50', '1:76000'], ['60', '1:75000']],
                                       'basis': 'Both positions use the same fixed pair XA. The two missing labels 5/6 are assigned globally bijectively to VF/XA, never independently per occurrence.'},
            'limits': ['The all-boundary scans test the stated fixed text and XA pair constraints only; their minima do not establish historical uniqueness.',
                       'Insertion boundaries 0 and 1 remain equally priced and yield the same repaired stream after a missing D is supplied, with different source-origin assignments.',
                       'A historically familiar map scale does not establish a new key assignment.',
                       'The F/E source sensitivity changes one observed substitution into one source-mask fill; it cannot silently reduce the main cost.',
                       'Source counts and glyph observations were manually reviewed from the hashed images; the executable checks independently reproduce the stated model arithmetic.']}



def package_result(pdf=None):
    inp = json.loads((HERE / 'inputs.json').read_text())
    assert sha(HERE / 'prior_evidence.json') == inp['prior_evidence_sha256']
    prior = json.loads((HERE / 'prior_evidence.json').read_text())
    assert {r['id'] for r in inp['records']} == set(TARGETS)
    ctx = inp['unread_context']
    assert ''.join(''.join(ctx['rows']).split()) == ''.join(ROWS['p162_C1'].split()) == ctx['literal_source']
    assert ctx['source_slots'] == 117 and ctx['id'] not in TARGETS
    doc = None
    if pdf:
        import fitz
        assert sha(pdf) == inp['source']['pdf_sha256']
        doc = fitz.open(pdf)
    for im in inp['source']['images']:
        assert sha(HERE / im['path']) == im['sha256']
        if doc is not None:
            fitz.TOOLS.store_shrink(100)
            pix = doc[im['pdf_page_1based'] - 1].get_pixmap(
                matrix=fitz.Matrix(im['scale'], im['scale']), clip=fitz.Rect(im['clip_points']))
            assert (pix.width, pix.height) == (im['width'], im['height'])
            assert hashlib.sha256(pix.samples).hexdigest() == im['pixel_sha256']
    result = build(inputs=HERE / 'inputs.json')
    result['schema'] = 'adfgvx-nov8-map-and-boundary-certificates-v1'
    result['source_images_manually_reviewed'] = [{'path': im['path'], 'sha256': im['sha256']}
                                                for im in inp['source']['images']]
    displays = []
    for r in inp['records']:
        got = next(x for x in result['records'] if x['id'] == r['id'])
        assert got['raw_plaintext'] == r['expected_raw']
        assert got['edited_plaintext'] == r['editorial_text'] == TARGETS[r['id']]
        assert got['ledger'] == r['expected_ledger']
        assert got['primary_missing_coordinate_index'] == r['model_insert_before_source_index']
        assert ''.join(''.join(r['rows']).split()) == r['literal_source']
        assert r['unknown_target_pairs'] == ({'43': 'XA', '63': 'XA'} if r['id'] == 'p162_B1' else {})
        display = r['readable_german']
        normalized = display
        for a, b in [('ä', 'AE'), ('ö', 'OE'), ('ü', 'UE'), ('Ä', 'AE'), ('Ö', 'OE'), ('Ü', 'UE')]:
            normalized = normalized.replace(a, b)
        normalized = ''.join(re.findall('[A-Z0-9?]', normalized.upper()))
        labels = [(i, c) for i, c in enumerate(got['edited_plaintext']) if c != 'X']
        assert normalized == ''.join(c for _, c in labels)
        case = ROOT / r['readable_case_path']
        assert ('> ' + display) in case.read_text()
        mapping = [{'readable_normalized_index': j, 'edited_plaintext_index': i, 'label': c}
                   for j, (i, c) in enumerate(labels)]
        displays.append({'id': r['id'], 'case_path': r['readable_case_path'],
                         'exact_quote': display, 'normalized_non_x_labels': normalized,
                         'mapping': mapping, 'positional_unknown_count': normalized.count('?')})
        # Every numerical label is carried literally except the separately priced 2 in KAR2E.
        got['raw_numeral_positions'] = [{'plaintext_index': i, 'raw_label': c,
                                        'edited_label': got['edited_plaintext'][i],
                                        'unchanged': c == got['edited_plaintext'][i]}
                                       for i, c in enumerate(got['raw_plaintext']) if c.isdigit()]
        for kind in got['ledger']:
            for e in got['ledger'][kind]:
                pi = order(got['working_frame_slots'])[e['working_index']] // 2
                e['plaintext_index'] = pi
                e['raw_label'] = got['raw_plaintext'][pi]
                e['edited_label'] = got['edited_plaintext'][pi]
    # The retained native odd frame is a diagnostic only, outside accepted plaintext totals.
    literal = ''.join(ROWS['p162_B1'].split())
    mid = [''] * len(literal)
    origins = [None] * len(literal)
    for j, i in enumerate(order(len(literal))):
        mid[i], origins[i] = literal[j], j
    result['native_B1_181_slot_diagnostic'] = {'paired_prefix': decode(literal)[0],
                                            'unpaired_coordinate': mid[-1],
                                            'unpaired_source_index': origins[-1],
                                            'status': 'Unrepaired native-frame diagnostic only; the accepted conditional model is 182 slots.'}
    first_five = []
    wanted = result['records'][0]['repaired_working_ciphertext']
    for gap in range(5):
        actual, source_origins = frame(literal, gap)
        first_five.append({'insert_before_source_index': gap, 'raw_plaintext': decode(actual)[0],
                           'working_source_indices': source_origins,
                           'fixed_target_ledger': cost(actual, wanted, source_origins)})
    result['B1_first_five_source_group_placements'] = first_five
    assert [len(x['fixed_target_ledger']['observed_substitutions']) for x in first_five] == [2, 2, 3, 4, 4]
    result['readable_mappings'] = displays
    result['summary']['readable_non_x_labels'] = sum(len(x['mapping']) for x in displays)
    result['summary']['readable_positional_unknowns'] = sum(x['positional_unknown_count'] for x in displays)
    comparisons = []
    for old in prior['selected_rows']:
        old_decoded = decode(old['ciphertext'])[0]
        assert old_decoded == old['best']['plaintext']
        comparisons.append({'block_id': old['block_id'], 'source_slots': old['source_slots'],
                            'old_plaintext': old_decoded,
                            'old_unpaired_coordinate': old['best']['unpaired_coordinate'],
                            'scope': 'Prior OCR evidence; no first historical body recovery claim.'})
    result['prior_ocr_checks'] = comparisons
    result['source_glyph_sensitivity'] = inp['source_glyph_sensitivity']
    result['limits'] = inp['limits']
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--pdf', type=Path)
    args = p.parse_args()
    result = package_result(args.pdf)
    if args.verify:
        assert result == json.loads((HERE / 'certificates.json').read_text())
    else:
        (HERE / 'certificates.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': args.verify, 'source_pixels_checked': bool(args.pdf), **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
