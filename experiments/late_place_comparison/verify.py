#!/usr/bin/env python3
"""Check a Grosswardein word repair and the existing Poestyen interpretation."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
CO = 'ADFGVX'


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(cipher, ranks, square):
    """Construct source positions independently of the project decoder."""
    width = len(ranks)
    heights = [len(cipher) // width + (c < len(cipher) % width) for c in range(width)]
    starts = [sum(heights[j] for j in range(width) if ranks[j] < ranks[c]) for c in range(width)]
    indices = [starts[i % width] + i // width for i in range(len(cipher))]
    assert sorted(indices) == list(range(len(cipher)))
    positions = []
    for i in range(0, len(indices), 2):
        origins = indices[i:i + 2]
        pair = ''.join(cipher[j] for j in origins)
        cells = [6 * a + b for a in range(6) for b in range(6)
                 if pair[0] in ('?', CO[a]) and pair[1] in ('?', CO[b])]
        unused = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') - set(square)
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == '?' else square[cell])
        domain = ''.join(sorted(domain))
        positions.append(dict(plaintext_index=i // 2, source_indices=origins, pair=pair, domain=domain))
    text = ''.join(p['domain'] if len(p['domain']) == 1 else '?' for p in positions)
    assert text == decrypt(cipher, ranks, square)
    return text, positions


def ledger(source, edited):
    changes = [dict(source_index=i, **{'from': a, 'to': b}) for i, (a, b) in enumerate(zip(source, edited)) if a in CO and a != b]
    fills = [dict(source_index=i, literal=a, to=b) for i, (a, b) in enumerate(zip(source, edited)) if a not in CO and b in CO]
    return dict(observed_substitutions=changes, source_mask_fills=fills)


def historical_pdf(path, definition):
    import fitz
    assert sha(path) == definition['pdf_sha256'] and path.stat().st_size == definition['pdf_bytes']
    doc = fitz.open(path)
    for region in definition['regions']:
        pix = doc[region['pdf_page_1based'] - 1].get_pixmap(
            matrix=fitz.Matrix(region['render_scale'], region['render_scale']),
            clip=fitz.Rect(*region['crop_pdf_points']))
        assert (pix.width, pix.height) == (region['width'], region['height'])
        assert hashlib.sha256(pix.samples).hexdigest() == region['rgb_sha256']


def build(check_displays=True):
    data = json.loads((HERE / 'inputs.json').read_text())
    for path, digest in data['dependencies'].items():
        assert sha(ROOT / path) == digest, path
    definition = data['grosswardein']
    original = next(r for r in read('experiments/radio_traffic_transfer_fragment/certificates.json')['records'] if r['id'] == definition['record'])
    key = next(k for k in read('data/keys.json')['keys'] if k['id'] == 'Nov28-Dec1')
    ranks, square = key['column_rank_order'], key['square']
    native = ''.join(c if c in CO else '?' for c in original['literal_source'])
    raw, positions = inspect(native, ranks, square)
    assert raw == original['raw']
    before = original['readable_candidate']['ciphertext']
    old, _ = inspect(before, ranks, square)
    start, end = definition['target_range']
    assert raw[start:end] == definition['target_before'] == 'GROSSW0RDEIN'
    p = positions[definition['plaintext_index']]
    assert p['source_indices'] == definition['source_indices'] == [12, 81] and p['pair'] == definition['native_pair'] == 'VG'
    donor = definition['supporting_A']
    a = positions[donor['plaintext_index']]
    assert a['source_indices'] == donor['source_indices'] == [57, 149]
    assert a['pair'] == donor['pair'] == 'VD' and a['domain'] == 'A'
    assert native[57] == before[57] and native[149] == before[149]
    change = definition['new_change']
    corrected = list(before)
    assert change == {'source_index': 81, 'from': 'G', 'to': 'D'}
    assert corrected[81] == native[81] == 'G'
    corrected[81] = 'D'
    corrected = ''.join(corrected)
    after, new_positions = inspect(corrected, ranks, square)
    assert after[start:end] == definition['target_after'] == 'GROSSWARDEIN'
    assert new_positions[10]['pair'] == 'VD'
    assert [i for i, (x, y) in enumerate(zip(old, after)) if x != y] == [10]
    later_start, later_end = definition['later_range']
    assert after[later_start:later_end] == old[later_start:later_end] == definition['later_spelling'] == 'GROSSVARDEIN'
    assert positions[9]['pair'] == 'XX' and positions[84]['pair'] == 'GV'
    cost = ledger(original['literal_source'], corrected)
    assert len(cost['observed_substitutions']) == 2 and len(cost['source_mask_fills']) == 3
    # Every remaining printed-mask completion re-encrypts; no first-day letter is chosen.
    baseline_witnesses = []
    for coordinate in CO:
        filled = corrected[:23] + coordinate + corrected[24:]
        text = decrypt(filled, ranks, square)
        assert encrypt(text, ranks, square) == filled
        baseline_witnesses.append(dict(source23=coordinate, first_label=text[0]))
    traffic = read('experiments/late_november_calendar_and_units/traffic_certificate.json')
    inherited = next(r for r in traffic['records'] if r['id'] == definition['record'])
    assert inherited['prior_edition_ciphertext'] == before
    dated = list(inherited['conditional_ciphertext'])
    assert dated[81] == 'G'
    dated[81] = 'D'
    dated = ''.join(dated)
    assert all(a == b or i == 81 for i, (a, b) in enumerate(zip(inherited['conditional_ciphertext'], dated)))
    common, _ = inspect(dated, ranks, traffic['conditional_square'])
    branches = []
    for old_witness in inherited['global_witnesses']:
        text, _ = inspect(dated, ranks, old_witness['square'])
        assert encrypt(text, ranks, old_witness['square']) == dated
        assert text[4:16] == 'GROSSWARDEIN' and text[79:91] == 'GROSSVARDEIN'
        branches.append(dict(square=old_witness['square'], plaintext=text, date=text[0], schwere=text[53:55]))
    assert {(b['date'], b['schwere']) for b in branches} == {('4', '15'), ('5', '14')}
    assert old.count('?') == after.count('?') == 1 and len(after) == 93
    assert common.count('?') == 2 and len(common) == 93
    dated_cost = ledger(original['literal_source'], dated)
    assert len(dated_cost['observed_substitutions']) == 2 and len(dated_cost['source_mask_fills']) == 4
    definition2 = data['poestyen']
    record2 = next(r for r in read('experiments/operational_recovery/certificates.json')['records'] if r['id'] == definition2['record'])
    key2 = next(k for k in read('data/keys.json')['keys'] if k['id'] == 'Nov22-24')
    raw2, pp = inspect(record2['source_ciphertext'], key2['column_rank_order'], key2['square'])
    a, b = definition2['word_range']
    assert raw2[a:b] == definition2['baseline_word'] == 'POEST4EN'
    y = pp[57]
    assert y['source_indices'] == definition2['source_indices'] == [139, 222] and y['pair'] == 'DD'
    prior_y = read('experiments/p215_hungarian_y/inputs.json')['new_lexical_Y']
    assert prior_y['baseline_label'] == '4' and prior_y['letter'] == 'Y' and prior_y['pair'] == 'DD'
    assert raw2[a:b].replace('4', 'Y') == definition2['interpreted_word'] == 'POESTYEN'
    if check_displays:
        case = (ROOT / definition['case']).read_text()
        assert '## The repeated place: Grosswardein' in case
        assert '> {4/5}. Dez., Grosswardein. DNZW uebernimmt Verkehr fuer OKM, schwere {15/14}. Rufz.: Natan Adolf Ursula in Grossvardein.' in case
        assert 'source **81 G→D**' in case and '**two observed substitutions and four mask fills**' in case
        case2 = (ROOT / definition2['case']).read_text()
        assert 'POESTYEN' in case2 and '22 November 1918' in case2 and 'already established' in case2
    return dict(schema='adfgvx-late-place-comparison-certificate-v1', authors=data['authors'],
                input_sha256=sha(HERE/'inputs.json'), indexing='Zero-based plaintext and source positions.',
                grosswardein=dict(id=definition['record'], native_plaintext=raw,
                    prior_edition=old, proposed_baseline=after, edited_ciphertext=corrected,
                    new_change=change, native_A_support=donor,
                    native_W=positions[9], retained_V=positions[84],
                    fixed_baseline_before=92, fixed_baseline_after=92, positions=93,
                    baseline_cost=cost, remaining_mask_witnesses=baseline_witnesses,
                    dated_ciphertext=dated, conditional_common=common, conditional_fixed=91,
                    date_branches=branches, dated_cost=dated_cost),
                poestyen=dict(id=definition2['record'], native_plaintext=raw2,
                    baseline_word=raw2[a:b], interpreted_word='POESTYEN', native_Y_pair=y,
                    new_coordinate_changes=0, new_key_assignments=0, new_fixed_positions=0,
                    assignment_dependency='experiments/p215_hungarian_y/inputs.json'),
                historical_sources=data['historical_sources'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--grosswardein-pdf', type=Path)
    parser.add_argument('--poestyen-pdf', type=Path)
    args = parser.parse_args()
    result = build()
    target = HERE / 'certificate.json'
    if args.verify:
        assert json.loads(target.read_text()) == result
    else:
        target.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    if args.pdf:
        from experiments.radio_traffic_transfer_fragment.verify import build as prior_build
        assert prior_build(args.pdf) == read('experiments/radio_traffic_transfer_fragment/certificates.json')
    for name, path in [('grosswardein', args.grosswardein_pdf), ('poestyen', args.poestyen_pdf)]:
        if path:
            historical_pdf(path, result['historical_sources'][name])
    print('Grosswardein: one additional observed-coordinate repair; inherited 4/5 branches retained. Poestyen: existing Y assignment, contemporary context added.')
    checked = [name for name, path in [('grosswardein', args.grosswardein_pdf), ('poestyen', args.poestyen_pdf)] if path]
    print('Historical PDF pixels checked: ' + ', '.join(checked) if checked else 'Historical PDF pixels not checked in this invocation.')


if __name__ == '__main__':
    main()
