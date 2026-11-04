#!/usr/bin/env python3
"""Recompute the p164 A3 occupation-army word, witnesses and optional layers.

icekylinx and GPT-6 Astra Pro. All machine indices are zero-based.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
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
    wire_order = [i for col in sorted(range(len(ranks)), key=ranks.__getitem__)
                  for i in range(col, n, len(ranks))]
    result = [0] * n
    for position, half in enumerate(wire_order):
        result[half] = position
    assert sorted(result) == list(range(n))
    return result


def complete_squares(square):
    blanks = [i for i, c in enumerate(square) if c == '?']
    missing = sorted(set(ALPHABET) - set(square))
    assert len(blanks) == len(missing)
    result = []
    for values in itertools.permutations(missing):
        out = list(square)
        for cell, value in zip(blanks, values):
            out[cell] = value
        result.append(''.join(out))
    return result


def decode(wire, key):
    iv = inverse(len(wire), key['column_rank_order'])
    squares = complete_squares(key['square'])
    positions = []
    for i in range(len(wire)//2):
        ids = iv[2*i:2*i+2]
        pair = ''.join(wire[j] for j in ids)
        domain = set()
        for square in squares:
            for cell, ch in enumerate(square):
                code = CO[cell//6] + CO[cell%6]
                if all(a == '?' or a == b for a, b in zip(pair, code)):
                    domain.add(ch)
        positions.append(dict(plaintext_index=i, source_indices=ids, pair=pair,
                              domain=''.join(sorted(domain))))
    raw = ''.join(p['domain'] if len(p['domain']) == 1 else '?' for p in positions)
    return dict(raw=raw, fixed_positions=len(raw)-raw.count('?'), positions=positions)


def apply(source, key, proposal):
    assert len(source) == 2*len(proposal)
    iv = inverse(len(source), key['column_rank_order'])
    output = list(source)
    ledger = []
    for i, ch in enumerate(proposal):
        if ch == '?':
            continue
        cell = key['square'].index(ch)
        code = CO[cell//6] + CO[cell%6]
        for p, value in zip(iv[2*i:2*i+2], code):
            if output[p] != value:
                ledger.append(dict(plaintext_index=i, label=ch, source_index=p,
                                   old=source[p], new=value,
                                   kind='printed_mask_fill' if source[p] == '?' else 'observed_substitution'))
                output[p] = value
    wire = ''.join(output)
    reading = decode(wire, key)
    assert all(a == '?' or a == b for a, b in zip(proposal, reading['raw']))
    witnesses = []
    for square in complete_squares(key['square']):
        full = wire.replace('?', 'A')
        text = decrypt(full, key['column_rank_order'], square)
        assert encrypt(text, key['column_rank_order'], square) == full
        witnesses.append(dict(square=square, ciphertext=full, plaintext=text))
    return dict(proposal=proposal, ciphertext=wire, **reading, edits=ledger,
                observed_substitutions=sum(e['kind']=='observed_substitution' for e in ledger),
                printed_mask_fills=sum(e['kind']=='printed_mask_fill' for e in ledger),
                arbitrary_roundtrip_witnesses=witnesses)


def native_donor(item, keys):
    data = load(ROOT/item['input_path'])
    assert sha(ROOT/item['input_path']) == item['input_sha256']
    rec = next(r for r in data['records'] if r['id'] == item['record_id'])
    source = ''.join(''.join(rec[item['rows_field']]).split())
    key = keys[item['key_id']]
    assert set(source) <= set(CO)
    raw = decrypt(source, key['column_rank_order'], key['square'])
    assert raw == rec['expected_raw']
    start, text = item['plaintext_start'], item['text']
    assert raw[start:start+len(text)] == text
    iv = inverse(len(source), key['column_rank_order'])
    positions = []
    for i, label in enumerate(text, start):
        ids = iv[2*i:2*i+2]
        pair = ''.join(source[j] for j in ids)
        assert key['square'][6*CO.index(pair[0])+CO.index(pair[1])] == label
        positions.append(dict(plaintext_index=i, label=label, source_indices=ids, pair=pair))
    return dict(record_id=item['record_id'], key_id=item['key_id'], raw=raw,
                text=text, plaintext_start=start, positions=positions,
                all_halves_are_original_observations=True)


def compute():
    inp = load(HERE/'inputs.json')
    for path, digest in inp['dependencies'].items():
        assert sha(ROOT/path) == digest, path
    for path, digest in inp['search_artifacts'].items():
        assert sha(HERE/path) == digest, path
    source_certificate = load(ROOT/inp['source_certificate'])
    src = next(s for s in source_certificate['sources'] if s['id']=='p164_A3')
    key = source_certificate['key']
    source = src['ciphertext']
    assert len(source)==242 and source.count('?')==84
    keys = {k['id']: k for k in load(ROOT/'data/keys.json')['keys']}
    assert keys[key['id']]['square'] == key['square']
    assert keys[key['id']]['column_rank_order'] == key['column_rank_order']
    baseline = decode(source, key)
    assert baseline['raw'] == next(v for v in source_certificate['variants']
                                  if v['id']=='A3_source_only')['expected_analysis']['raw_partial_plaintext']
    prior = next(v for v in source_certificate['variants']
                 if v['id']=='A3_comment42_full_proposal')['expected_analysis']['raw_partial_plaintext']
    word = inp['word']['text']; start = inp['word']['plaintext_start']
    assert (start, word)==(18,'BESATZUNGSHEER')
    word_text = list(baseline['raw']); word_text[start:start+len(word)] = word
    date_text = list(word_text); date_text[:18] = inp['date_and_place_template']
    combined = list(prior); combined[:18] = inp['date_and_place_template']; combined[18:32] = word
    layers = {name: apply(source,key,''.join(text)) for name,text in
              [('word_only',word_text),('date_and_word',date_text),('combined_with_prior_routes',combined)]}
    expected = {'word_only':(52,0,10),'date_and_word':(60,1,20),
                'combined_with_prior_routes':(104,4,66)}
    for name, values in expected.items():
        layer=layers[name]
        assert (layer['fixed_positions'],layer['observed_substitutions'],layer['printed_mask_fills'])==values
        assert layer['raw']==inp['expected_outputs'][name]
    assert [e['source_index'] for e in layers['date_and_word']['edits']
            if e['kind']=='observed_substitution']==[49]
    word_positions = baseline['positions'][18:32]
    assert sum(sum(c in CO for c in p['pair']) for p in word_positions)==18
    assert sum(len(p['domain'])==1 for p in word_positions)==4
    assert all(sum(c in CO for c in p['pair'])>=1 for p in word_positions)
    assert all(ch in p['domain'] for ch,p in zip(word,word_positions))
    donors = [native_donor(d,keys) for d in inp['donors']]
    assert donors[0]['text']==donors[1]['text']==word
    assert len({key['id'],donors[0]['key_id'],donors[1]['key_id']})==3
    # The date is already Norbert's comment47 proposal. The donor independently
    # witnesses its exact Q/date/place suffix; it does not fill the first3 slots.
    assert donors[2]['text']=='QX9X11XTEMESVARX'
    assert all(layers['date_and_word']['raw'][i]=='?' for i in [0,1,2,32,33])
    if inp.get('source_image'):
        assert sha(HERE/inp['source_image']['path'])==inp['source_image']['png_sha256']
    return dict(schema='adfgvx-p164-occupation-fragment-certificate-v1',authors=inp['authors'],
                input_sha256=sha(HERE/'inputs.json'),key=key,source=source,baseline=baseline,
                native_donors=donors,word_positions=word_positions,layers=layers,
                old_proposal=dict(fixed_positions=101,observed_substitutions=5,printed_mask_fills=63),
                summary=dict(word_length=14,original_observed_word_halves=18,
                             new_half_supported_word_positions=10,word_substitutions=0,
                             combined_fixed_positions=104,combined_observed_substitutions=4,
                             physical_bodies_added=0),limits=inp['limits'])


def verify_pdf(path, inp):
    import fitz
    assert sha(path)==inp['source_pdf']['sha256']
    spec=inp['source_image'];doc=fitz.open(path)
    pix=doc[spec['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(spec['scale'],spec['scale']),
                                               clip=fitz.Rect(spec['crop_pdf_points']),alpha=False)
    assert [pix.width,pix.height]==spec['size']
    assert hashlib.sha256(pix.samples).hexdigest()==spec['rgb_sha256']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true');parser.add_argument('--pdf',type=Path)
    args=parser.parse_args();result=compute();path=HERE/'certificates.json'
    if args.verify:
        assert result==load(path)
    else:
        path.write_text(json.dumps(result,indent=2)+'\n')
    if args.pdf:verify_pdf(args.pdf,load(HERE/'inputs.json'))
    print(json.dumps(dict(verified=True,**result['summary'],original_pdf_checked=bool(args.pdf)),indent=2))


if __name__=='__main__':main()
