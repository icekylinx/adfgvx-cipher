#!/usr/bin/env python3
"""Reproduce p89 A3's guard-battalion phrase and separate Berlin extension.

icekylinx and GPT-6 Astra Pro. All indices are zero-based.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

CO = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(n, ranks):
    """Original fractionation position -> transmitted position."""
    width = len(ranks)
    heights = [n//width + (j < n % width) for j in range(width)]
    offsets = [sum(heights[k] for k in range(width) if ranks[k] < ranks[j])
               for j in range(width)]
    result = [offsets[i % width] + i//width for i in range(n)]
    assert sorted(result) == list(range(n))
    return result


def inspect(wire, key, mapping):
    iv = inverse(len(wire), key['column_rank_order'])
    rows = []
    for i in range(len(wire)//2):
        ids = iv[2*i:2*i+2]
        pair = ''.join(wire[j] for j in ids)
        domain = ''.join(sorted(key['square'][6*r+c]
                               for r in range(6) for c in range(6)
                               if pair[0] in ('?', CO[r]) and pair[1] in ('?', CO[c])))
        rows.append(dict(plaintext_index=i, pair=pair, model_indices=ids,
                         source_indices=[mapping[j] for j in ids], domain=domain))
    raw = ''.join(p['domain'] if len(p['domain']) == 1 else '?' for p in rows)
    assert raw == decrypt(wire, key['column_rank_order'], key['square'])
    return dict(raw=raw, fixed_positions=len(raw)-raw.count('?'), positions=rows)


def apply(wire, key, mapping, literal, template):
    assert len(wire) == 2*len(template)
    iv = inverse(len(wire), key['column_rank_order'])
    out = list(wire)
    edits = []
    for i, label in enumerate(template):
        if label == '?':
            continue
        cell = key['square'].index(label)
        code = CO[cell//6] + CO[cell % 6]
        for j, value in zip(iv[2*i:2*i+2], code):
            if wire[j] == value:
                continue
            source_j = mapping[j]
            kind = ('lost_coordinate_fill' if source_j is None else
                    'printed_mask_fill' if wire[j] == '?' else 'observed_substitution')
            edits.append(dict(plaintext_index=i, label=label, model_index=j,
                              source_index=source_j, printed=literal[source_j] if source_j is not None else None,
                              old=wire[j], new=value, kind=kind))
            out[j] = value
    out = ''.join(out)
    result = inspect(out, key, mapping)
    assert result['raw'] == template
    # A complete arithmetic witness does not assert the residual A fills.
    witness = out.replace('?', 'A')
    plain = decrypt(witness, key['column_rank_order'], key['square'])
    assert encrypt(plain, key['column_rank_order'], key['square']) == witness
    assert all(a == '?' or a == b for a, b in zip(template, plain))
    return dict(ciphertext=out, **result, edits=edits,
                prices={kind: sum(e['kind'] == kind for e in edits) for kind in
                        ['observed_substitution', 'printed_mask_fill', 'lost_coordinate_fill']},
                unfilled_coordinates=out.count('?'),
                exact_compatible_complete_plaintexts=str(6**out.count('?')),
                arbitrary_witness=dict(ciphertext=witness, plaintext=plain))


def record(data, record_id):
    return next(r for r in data['records'] if r['id'] == record_id)


def compute():
    inp = load(HERE/'inputs.json')
    for path, digest in inp['dependencies'].items():
        assert sha(ROOT/path) == digest, path
    t = inp['target']; d = inp['donor']
    ti = load(ROOT/t['input_path']); tc = load(ROOT/t['certificate_path'])
    di = load(ROOT/d['input_path']); dc = load(ROOT/d['certificate_path'])
    target = record(ti, t['record_id']); donor = record(di, d['record_id'])
    target_cert = record(tc, t['record_id']); donor_cert = record(dc, d['record_id'])
    key = ti['key']
    assert key == di['key']
    assert key == next(k for k in load(ROOT/'data/keys.json')['keys'] if k['id'] == 'Nov1-3')
    assert '?' not in key['square']
    literal = ''.join(''.join(target['source_rows']).split())
    assert len(literal) == 258 and literal.count('-') == 1
    gap = target['explicit_source_loss']
    assert gap['source_offset'] == 200 and gap['missing_coordinates'] == 100
    wire = literal[:200].replace('-', '?') + '?'*100 + literal[200:].replace('-', '?')
    mapping = list(range(200)) + [None]*100 + list(range(200, 258))
    assert wire == target_cert['ciphertext'] and mapping == target_cert['model_to_source_indices']
    raw = inspect(wire, key, mapping)
    assert raw['raw'] == target['expected_raw'] == target_cert['raw']
    prior = target['readable_candidate']
    assert prior == target_cert['readable_candidate']['raw'] == inp['expected_outputs']['prior']
    donor_literal = ''.join(''.join(donor['source_rows']).split())
    assert len(donor_literal) == 149 and set(donor_literal) <= set(CO)
    donor_frames = []
    for boundary in d['all_local_gap_boundaries']:
        dw = donor_literal[:boundary] + '?' + donor_literal[boundary:]
        dm = list(range(boundary)) + [None] + list(range(boundary, 149))
        reading = inspect(dw, key, dm)
        spans = []
        for span in inp['spans']:
            a = span['donor_start']; b = a+len(span['text'])
            positions = reading['positions'][a:b]
            spans.append(dict(id=span['id'], text=reading['raw'][a:b],
                              positions=positions, observed_halves=sum(c != '?' for p in positions for c in p['pair'])))
        assert spans[0]['text'] == inp['spans'][0]['text'] and spans[0]['observed_halves'] == 40
        donor_frames.append(dict(boundary=boundary, raw=reading['raw'], spans=spans))
    primary_donor = next(x for x in donor_frames if x['boundary'] == d['primary_gap_boundary'])
    assert primary_donor['raw'] == donor_cert['raw'] == donor['expected_raw']
    assert primary_donor['spans'][1]['text'] == 'BERLIN'
    assert primary_donor['spans'][1]['observed_halves'] == 12
    assert [x['boundary'] for x in donor_frames if x['spans'][1]['text'] == 'BERLIN'] == [100, 101, 102, 103]
    layers = {'prior': apply(wire, key, mapping, literal, prior)}
    template = list(prior)
    span_evidence = []
    for span in inp['spans']:
        start = span['target_start']; text = span['text']; stop = start+len(text)
        positions = raw['positions'][start:stop]
        assert sum(c != '?' for p in positions for c in p['pair']) == span['observed_target_halves']
        assert all(label in p['domain'] for label, p in zip(text, positions))
        assert [p['plaintext_index'] for p in positions if p['pair'] == '??'] == span['wholly_unobserved_target_positions']
        assert sum(prior[i] == '?' for i in range(start, stop)) == span['new_fixed_positions']
        assert sum(p['pair'].count('?') for p in positions) == span['new_lost_coordinate_fills']
        assert all(mapping[j] is None for p in positions for j in p['model_indices'] if wire[j] == '?')
        span_evidence.append(dict(**span, positions=positions))
        template[start:stop] = text
        name = 'guard_with_prior' if span['id'] == 'guard_battalion' else 'guard_and_berlin_with_prior'
        layers[name] = apply(wire, key, mapping, literal, ''.join(template))
        assert layers[name]['raw'] == inp['expected_outputs'][name]
    expected = {'prior': (151, 1, 1, 69), 'guard_with_prior': (163, 1, 1, 82),
                'guard_and_berlin_with_prior': (166, 1, 1, 85)}
    for name, values in expected.items():
        r = layers[name]; p = r['prices']
        assert (r['fixed_positions'], p['observed_substitution'], p['printed_mask_fill'], p['lost_coordinate_fill']) == values
        assert r['raw'][143] == r['raw'][164] == r['raw'][167] == r['raw'][172] == '?'
    old_edits = {(e['model_index'], e['new']) for e in layers['prior']['edits']}
    assert old_edits <= {(e['model_index'], e['new']) for e in layers['guard_and_berlin_with_prior']['edits']}
    return dict(schema='adfgvx-p89-guard-battalion-extension-certificate-v1', authors=inp['authors'],
                input_sha256=sha(HERE/'inputs.json'), key_id=key['id'], source=literal,
                source_frame=wire, model_to_source_indices=mapping, raw=raw,
                donor_literal=donor_literal, donor_local_frames=donor_frames,
                span_evidence=span_evidence, layers=layers,
                summary=dict(physical_bodies_added=0, raw_fixed_positions=81,
                             prior_fixed_positions=151, guard_fixed_positions=163,
                             guard_and_berlin_fixed_positions=166, plaintext_positions=179,
                             new_observed_substitutions=0, new_printed_mask_fills=0,
                             new_lost_coordinate_fills=16, new_fixed_positions=15,
                             new_positions_with_observed_half=14,
                             wholly_unobserved_new_positions=[150]), limits=inp['limits'])


def verify_pdf(path, inp):
    import fitz
    from PIL import Image
    assert sha(path) == '157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06'
    doc = fitz.open(path)
    for ref in inp['source_images']:
        input_path = ROOT/ref['input_path']; data = load(input_path)
        spec = next(x for x in data['source_images'] if x['path'] == ref['path'])
        image_path = input_path.parent/spec['path']
        assert sha(image_path) == spec['sha256']
        pix = doc[spec['pdf_page_1based']-1].get_pixmap(
            matrix=fitz.Matrix(spec['render_scale'], spec['render_scale']),
            clip=fitz.Rect(spec['crop_pdf_points']), alpha=False)
        image = Image.open(image_path).convert('RGB')
        assert image.size == (pix.width, pix.height) and image.tobytes() == pix.samples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args(); result = compute(); path = HERE/'certificates.json'
    if args.verify:
        assert result == load(path)
    else:
        path.write_text(json.dumps(result, indent=2)+'\n')
    if args.pdf:
        verify_pdf(args.pdf, load(HERE/'inputs.json'))
    print(json.dumps(dict(verified=True, **result['summary'], original_pdf_checked=bool(args.pdf)), indent=2))


if __name__ == '__main__':
    main()
