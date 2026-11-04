#!/usr/bin/env python3
"""Audit the p68 A2 procurement continuation without changing its source frame.

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
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(n, ranks):
    wire_order = [i for c in sorted(range(len(ranks)), key=ranks.__getitem__)
                  for i in range(c, n, len(ranks))]
    result = [0]*n
    for j, i in enumerate(wire_order):
        result[i] = j
    assert sorted(result) == list(range(n))
    return result


def inspect(wire, key):
    iv = inverse(len(wire), key['column_rank_order']); positions = []
    for i in range(len(wire)//2):
        ids = iv[2*i:2*i+2]; pair = ''.join(wire[j] for j in ids)
        domain = ''.join(sorted(key['square'][6*r+c]
                               for r in range(6) for c in range(6)
                               if pair[0] in ('?', CO[r]) and pair[1] in ('?', CO[c])))
        positions.append(dict(plaintext_index=i, source_indices=ids, pair=pair, domain=domain))
    raw = ''.join(p['domain'] if len(p['domain']) == 1 else '?' for p in positions)
    assert raw == decrypt(wire, key['column_rank_order'], key['square'])
    return dict(raw=raw, fixed_positions=len(raw)-raw.count('?'), positions=positions)


def apply(source, key, template):
    iv = inverse(len(source), key['column_rank_order']); out = list(source); edits = []
    assert len(template)*2 == len(source)
    for i, label in enumerate(template):
        if label == '?':
            continue
        cell = key['square'].index(label); pair = CO[cell//6]+CO[cell % 6]
        for j, value in zip(iv[2*i:2*i+2], pair):
            if source[j] != value:
                edits.append(dict(plaintext_index=i, label=label, source_index=j,
                                  old=source[j], new=value,
                                  kind='printed_mask_fill' if source[j] == '?' else 'observed_substitution'))
                out[j] = value
    out = ''.join(out); reading = inspect(out, key)
    assert reading['raw'] == template
    full = out.replace('?', 'A'); plain = decrypt(full, key['column_rank_order'], key['square'])
    assert encrypt(plain, key['column_rank_order'], key['square']) == full
    assert all(a == '?' or a == b for a, b in zip(template, plain))
    return dict(ciphertext=out, **reading, edits=edits,
                observed_substitutions=sum(e['kind'] == 'observed_substitution' for e in edits),
                printed_mask_fills=sum(e['kind'] == 'printed_mask_fill' for e in edits),
                remaining_masks=out.count('?'), compatible_complete_plaintexts=str(6**out.count('?')),
                arbitrary_roundtrip_witness=dict(ciphertext=full, plaintext=plain))


def native_donor(spec, keys):
    data = load(ROOT/spec['input_path'])
    rec = next(r for r in data['records'] if r['id'] == spec['record_id'])
    key_id = rec.get('key_id', data.get('key', {}).get('id'))
    key = keys[key_id]
    literal = ''.join(''.join(rec[spec['rows_field']]).split())
    source = ''.join(c if c in CO else '?' for c in literal)
    assert len(source) == rec.get('advertised_length', len(source))
    raw = decrypt(source, key['column_rank_order'], key['square'])
    assert raw == rec['expected_raw']
    a = spec['plaintext_start']; b = a+len(spec['text']); iv = inverse(len(source), key['column_rank_order'])
    assert raw[a:b] == spec['text']
    positions = []
    for i, label in enumerate(spec['text'], a):
        ids = iv[2*i:2*i+2]; pair = ''.join(source[j] for j in ids)
        assert set(pair) <= set(CO)
        assert key['square'][6*CO.index(pair[0])+CO.index(pair[1])] == label
        positions.append(dict(plaintext_index=i, label=label, pair=pair, source_indices=ids))
    return dict(**spec, key_id=key_id, native_source_length=len(source), raw=raw,
                positions=positions, all_word_halves_observed=True, source_frame_changed=False)


def compute():
    inp = load(HERE/'inputs.json')
    for path, digest in inp['dependencies'].items():
        assert sha(ROOT/path) == digest, path
    data = load(ROOT/inp['target']['input_path'])
    certificate = load(ROOT/inp['target']['certificate_path'])
    rec = next(r for r in data['records'] if r['id'] == 'p68_A2')
    prior_cert = next(r for r in certificate['records'] if r['id'] == 'p68_A2')['models'][0]
    keys = {k['id']: k for k in load(ROOT/'data/keys.json')['keys']}
    key = data['key']; assert key == keys['Oct4-6'] and set(key['square']) == set(ALPHABET)
    literal = ''.join(''.join(rec['rows']).split())
    source = literal.replace('-', '?')
    assert literal == rec['literal_source'] and source == rec['analysis_source']
    assert (len(source), source.count('?')) == (186, 41)
    assert rec['layout_models'] == [dict(id='literal', deletions=[], insertions=[],
                                       evidence='Literal slot geometry; parenthesized coordinates retain their recorded values.')]
    base = inspect(source, key)
    assert base['raw'] == prior_cert['raw_plaintext'] == inp['expected_outputs']['raw']
    prior_template = list(base['raw']); prior_template[:21] = 'UNDARTILLERIEMUNITION'
    assert rec['editorial_template'] == 'UNDARTILLERIEMUNITION'+'?'*72
    assert ''.join(prior_template) == inp['expected_outputs']['prior_opening']
    common = list(prior_template)
    for span in inp['new_spans']:
        a = span['start']; common[a:a+len(span['text'])] = span['text']
    assert ''.join(common) == inp['expected_outputs']['common'] and common[45] == '?'
    layers = {name: apply(source, key, template) for name, template in inp['expected_outputs'].items()}
    for name, prices in inp['expected_prices'].items():
        r = layers[name]
        assert [r['fixed_positions'], r['observed_substitutions'], r['printed_mask_fills']] == prices
    old_edits = {(e['source_index'], e['new']) for e in layers['prior_opening']['edits']}
    common_edits = {(e['source_index'], e['new']) for e in layers['common']['edits']}
    assert old_edits <= common_edits
    delta = [e for e in layers['common']['edits'] if (e['source_index'], e['new']) not in old_edits]
    assert sum(e['kind'] == 'observed_substitution' for e in delta) == 1
    assert sum(e['kind'] == 'printed_mask_fill' for e in delta) == 15
    assert [e for e in delta if e['kind'] == 'observed_substitution'] == [
        dict(plaintext_index=50, label='N', source_index=48, old='F', new='A', kind='observed_substitution')]
    assert base['positions'][45]['pair'] == '??'
    variants = [('eingegangen', 'G'), ('eingelangen', 'L')]
    for name, letter in variants:
        q = list(common); q[45] = letter
        assert ''.join(q) == layers[name]['raw']
        assert all(layers[name]['raw'][i] == '?' for i in [22, 23])
    new_positions = [i for i, (a, b) in enumerate(zip(layers['prior_opening']['raw'], layers['common']['raw']))
                     if a == '?' and b != '?']
    assert len(new_positions) == 15
    assert all(base['positions'][i]['pair'].count('?') == 1 for i in new_positions)
    donors = [native_donor(d, keys) for d in inp['donors']]
    discovery = load(HERE/'discovery.json')
    for match in discovery['book_model']['selected_words']:
        observed = mismatches = 0
        for i, letter in enumerate(match['word'], match['start']):
            cell = key['square'].index(letter)
            wanted = CO[cell//6]+CO[cell % 6]
            for old, new in zip(base['positions'][i]['pair'], wanted):
                observed += old != '?'
                mismatches += old != '?' and old != new
        assert observed == match['observed_halves']
        assert mismatches == match['observed_substitutions']
    return dict(schema='adfgvx-p68-procurement-continuation-certificate-v1', authors=inp['authors'],
                input_sha256=sha(HERE/'inputs.json'), literal_source=literal, key_id=key['id'],
                discovery_sha256=sha(HERE/'discovery.json'), context_sha256=sha(HERE/'context.json'),
                baseline=base, native_word_donors=donors, layers=layers, new_common_edits=delta,
                summary=dict(source_slots=186, observed_coordinates=145, printed_masks=41,
                             plaintext_positions=93, raw_fixed_positions=56,
                             prior_opening_asserted_positions=21, prior_opening_model_fixed_positions=61,
                             common_fixed_positions=76, complete_verb_variant_fixed_positions=77,
                             new_common_fixed_positions=15, all_new_common_positions_half_supported=True,
                             new_observed_substitutions=1, new_common_printed_mask_fills=15,
                             optional_wholly_missing_verb_position=45, added_or_excluded_source_slots=0),
                limits=inp['limits'])


def verify_pdf(path, inp):
    import fitz
    from PIL import Image
    data_path = ROOT/inp['target']['input_path']; data = load(data_path)
    assert sha(path) == '157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06'
    spec = next(x for x in data['source']['images'] if x['path'] == 'sources/childs_p68_A.png')
    image_path = data_path.parent/spec['path']; assert sha(image_path) == spec['sha256']
    doc = fitz.open(path)
    rect = spec.get('clip_points', spec.get('crop_pdf_points'))
    scale = spec.get('render_scale', spec.get('scale'))
    page = spec['pdf_page_1based']-1
    pix = doc[page].get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(rect), alpha=False)
    image = Image.open(image_path).convert('RGB')
    assert image.size == (pix.width, pix.height) and image.tobytes() == pix.samples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true'); parser.add_argument('--pdf', type=Path)
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
