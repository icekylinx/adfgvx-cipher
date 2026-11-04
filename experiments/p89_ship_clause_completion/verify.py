#!/usr/bin/env python3
"""Reproduce the conditional p89 A2 ship clause without changing source evidence.

icekylinx and GPT-6 Astra Pro. All indices are zero-based.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, transposition_indices, untranspose
from adfgvx.supplementary import calc as independent_calc

CO = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def by_id(records, name):
    return next(r for r in records if r['id'] == name)


def analyse(wire, key):
    ranks, square = key['column_rank_order'], key['square']
    raw = decrypt(wire, ranks, square)
    alternate = independent_calc(wire, key)
    assert alternate['plaintext'] == raw
    assert alternate['coordinate_roundtrip']
    assert not alternate['fixed_plaintext_reencoding_known_coordinate_conflicts']
    interim = untranspose(wire, ranks)
    source_for_interim = {v: i for i, v in enumerate(transposition_indices(len(wire), ranks))}
    domains = plaintext_domains(wire, ranks, square)
    assert domains == alternate['plaintext_domains']
    assert interim == alternate['intermediate_stream']
    return dict(raw=raw, positions=[dict(plaintext_index=i, label=c, domain=domains[i],
        pair=interim[2*i:2*i+2], source_indices=[source_for_interim[2*i], source_for_interim[2*i+1]])
        for i, c in enumerate(raw)])


def build(inp):
    record = inp['records'][0]
    assert record['id'] == 'p89_A2'
    literal = ''.join(''.join(record['source_rows']).split())
    wire = ''.join(c if c in CO else '?' for c in literal)
    assert len(literal) == record['source_slots'] == record['advertised_length'] == 290
    assert [i for i, c in enumerate(literal) if c == '-'] == record['printed_dash_indices'] == [176, 177]
    assert [i for i, c in enumerate(literal) if c not in CO + '-'] == [70]
    assert literal[70] == '?' and record['uncertain_glyph']['index'] == 70
    base = by_id(load(ROOT / inp['baseline']['input_path'])['messages'], 'p89_A2')
    assert base['source_ciphertext_conservative'] == wire
    assert base['source_glyph_hypotheses'][0] == record['uncertain_glyph']
    key = inp['key']
    assert base['key']['column_rank_order'] == key['column_rank_order']
    assert base['key']['square'] == key['square'] and base['key_id'] == key['id'] == 'Nov1-3'
    raw = analyse(wire, key)
    assert raw['raw'] == record['expected_raw'] == base['source_verification']['plaintext']
    assert len(raw['raw']) == 145 and raw['raw'].count('?') == 3
    expected = [(78, 'W', 176, 'F', 'printed_dash_fill'),
                (85, 'C', 70, 'D', 'uncertain_glyph_fill'),
                (88, 'F', 177, 'A', 'printed_dash_fill')]
    assert [(a['plaintext_index'], a['label'], a['source_index'], a['coordinate'], a['kind'])
            for a in inp['assignments']] == expected
    template = list(raw['raw'])
    ledger = []
    for assignment in inp['assignments']:
        i = assignment['plaintext_index']; position = raw['positions'][i]
        assert position['label'] == '?' and assignment['label'] in position['domain']
        assert assignment['source_index'] in position['source_indices']
        assert position['pair'].count('?') == 1
        template[i] = assignment['label']
        ledger.append(dict(**assignment, source_literal=literal[assignment['source_index']],
                           original_pair=position['pair'], original_domain=position['domain'],
                           source_indices=position['source_indices']))
    template = ''.join(template)
    assert template == record['readable_candidate']
    assert template[78:91] == 'WELCHESCHIFFE'
    candidate_wire = encrypt(template, key['column_rank_order'], key['square'])
    differences = [dict(source_index=i, before=a, after=b) for i, (a, b) in enumerate(zip(wire, candidate_wire)) if a != b]
    assert differences == [dict(source_index=70, before='?', after='D'),
                           dict(source_index=176, before='?', after='F'),
                           dict(source_index=177, before='?', after='A')]
    assert all(a == '?' or a == b for a, b in zip(wire, candidate_wire))
    assert decrypt(candidate_wire, key['column_rank_order'], key['square']) == template
    published_wire = list(wire); published_wire[70] = 'D'; published_wire = ''.join(published_wire)
    published_raw = decrypt(published_wire, key['column_rank_order'], key['square'])
    assert published_raw == record['prior_published_plaintext'] == base['published_plaintext']
    assert published_raw.count('?') == 2
    # Enumerate actual source fills. No independent-domain assumption is needed.
    witnesses = []
    for fills in itertools.product(CO, repeat=3):
        trial = list(wire)
        for i, c in zip([70, 176, 177], fills):
            trial[i] = c
        trial = ''.join(trial)
        decoded = decrypt(trial, key['column_rank_order'], key['square'])
        assert encrypt(decoded, key['column_rank_order'], key['square']) == trial
        assert all(a == '?' or a == b for a, b in zip(raw['raw'], decoded))
        witnesses.append(dict(fill_values=''.join(fills), labels=''.join(decoded[i] for i in [78, 85, 88]),
                              clause=decoded[78:91], selected=decoded == template))
    assert len(witnesses) == len({w['labels'] for w in witnesses}) == 216
    assert sum(w['selected'] for w in witnesses) == 1
    native_witnesses = []
    for spec in inp['native_word_witnesses']:
        data = load(ROOT / spec['input_path']); donor = by_id(data['records'], spec['record_id'])
        donor_key = data.get('key') or by_id(data['keys'], donor['key_id'])
        donor_rows = donor.get('source_rows', donor.get('rows'))
        assert donor_rows == spec['source_rows'] and donor_key['id'] == spec['key_id']
        donor_wire = ''.join(''.join(donor_rows).split())
        assert set(donor_wire) <= set(CO)
        donor_result = analyse(donor_wire, donor_key)
        assert donor_result['raw'] == spec['expected_raw'] == donor.get('expected_raw', donor.get('expected_unmodified_raw'))
        a, word = spec['word_start'], spec['word']; b = a + len(word)
        assert donor_result['raw'][a:b] == word
        positions = donor_result['positions'][a:b]
        assert all('?' not in x['pair'] for x in positions)
        if donor['id'] == 'p98_A2':
            assert donor_key['square'] == key['square'] and donor_key['column_rank_order'] == key['column_rank_order']
        native_witnesses.append(dict(input_path=spec['input_path'], record_id=spec['record_id'],
            key_id=spec['key_id'], word=word, word_start=a, observed_halves=2*len(word), positions=positions))
    images = []
    for image in inp['source_images']:
        assert sha(ROOT / image['path']) == image['sha256']
        images.append(image)
    return dict(schema='adfgvx-p89-ship-clause-completion-certificate-v1', authors=inp['authors'],
        input_sha256=sha(HERE/'inputs.json'), record_id=record['id'],
        summary=dict(source_slots=290, observed_coordinates=287, plaintext_positions=145,
            native_fixed=142, earlier_published_fixed=143, conditional_fixed=145,
            observed_coordinate_substitutions=0, printed_dash_fills=2, uncertain_glyph_fills=1,
            source_mask_fills=3, inserted_or_deleted_coordinates=0, all_observed_coordinates_unchanged=True,
            exact_reencryption=True, cryptographically_compatible_completions=216),
        conservative_source=wire, native=raw, conditional_plaintext=template, conditional_ciphertext=candidate_wire,
        assignments=ledger, source_differences=differences,
        earlier_published_layer=dict(plaintext=published_raw, conditional_source_fill=dict(source_index=70, coordinate='D')),
        native_word_witnesses=native_witnesses, source_images=images,
        complete_compatibility_census=dict(source_fill_order=[70,176,177], plaintext_label_order=[78,85,88],witnesses=witnesses),
        limits=inp['limits'])


def check_pdf(inp, path):
    import fitz
    from PIL import Image
    assert sha(path) == inp['source']['pdf_sha256']
    with fitz.open(path) as doc:
        for spec in inp['source_images']:
            pix = doc[spec['pdf_page_1based']-1].get_pixmap(
                matrix=fitz.Matrix(spec['render_scale'],spec['render_scale']),
                clip=fitz.Rect(spec['crop_pdf_points']), alpha=False)
            image = Image.open(ROOT/spec['path']).convert('RGB')
            assert image.size == (pix.width,pix.height) and image.tobytes() == pix.samples, spec['path']
    return len(inp['source_images'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write',action='store_true')
    p.add_argument('--verify',action='store_true')
    p.add_argument('--pdf',type=Path)
    args=p.parse_args()
    inp=load(HERE/'inputs.json'); result=build(inp)
    if args.write:
        (HERE/'certificates.json').write_text(json.dumps(result,indent=2)+'\n')
    if args.verify:
        assert result == load(HERE/'certificates.json'), 'Certificate differs; inspect before regeneration.'
    if args.pdf:
        result['summary']['original_pdf_crops_verified']=check_pdf(inp,args.pdf)
    print(json.dumps(dict(passed=True,**result['summary']),indent=2))


if __name__=='__main__':
    main()
