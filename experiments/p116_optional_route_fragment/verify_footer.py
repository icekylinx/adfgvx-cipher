#!/usr/bin/env python3
"""Verify the optional p116 A13 footer against original donor fields and source halves."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(n, ranks):
    order = [p for col in sorted(range(len(ranks)), key=lambda col: ranks[col])
             for p in range(col, n, len(ranks))]
    result = [0] * n
    for cipher_index, half in enumerate(order):
        result[half] = cipher_index
    return result


def donor(folder, identifier, start, text, target_start):
    path = ROOT / 'experiments' / folder / 'inputs.json'
    data = load(path)
    record = next(r for r in data['records'] if r['id'] == identifier)
    source = ''.join(''.join(record['source_rows']).split())
    key = data['key']
    ranks, square = key['column_rank_order'], key['square']
    raw = decrypt(source, ranks, square)
    assert raw == record['expected_raw'] and raw[start:start+len(text)] == text
    iv = inverse(len(source), ranks)
    positions = []
    for i, label in enumerate(text, start):
        ids = iv[2*i:2*i+2]
        pair = ''.join(source[j] for j in ids)
        assert all(c in C for c in pair)
        assert square[6*C.index(pair[0])+C.index(pair[1])] == label
        positions.append(dict(donor_plaintext_index=i, label=label, source_indices=ids, pair=pair,
                              target_plaintext_index=target_start+i-start))
    completions = [square]
    if '?' in square:
        completions = []
        for symbols in ['56', '65']:
            values = iter(symbols)
            completions.append(''.join(next(values) if c == '?' else c for c in square))
    assert all(encrypt(raw, ranks, s) == source for s in completions)
    return dict(id=identifier, input_path=str(path.relative_to(ROOT)), input_sha256=sha(path),
                key_id=key['id'], ranks=ranks, square=square, literal_source=source,
                raw=raw, span=[start, start+len(text)], text=text, target_start=target_start,
                positions=positions, completed_square_witnesses=completions,
                all_donor_halves_original_observations=True)


def compute():
    spec = importlib.util.spec_from_file_location('approval', HERE/'verify_approval.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = module.compute()
    assert base == load(HERE/'approval_extension.json')
    key = base['key']
    square, ranks = key['square'], key['column_rank_order']
    wire = base['source'] + '?'*62
    iv = inverse(len(wire), ranks)
    domains = plaintext_domains(wire, ranks, square)
    donors = [donor('p164_acknowledgment', 'p164_D', 41, 'XKXMXRMX1', 91),
              donor('nov2_acknowledgments_and_personnel', 'p105_C1', 77, 'XRMX1XA', 95)]
    closing_donor = donor('nov2_acknowledgments_and_personnel', 'p105_C1', 61, 'OPX', 108)
    assert donors[1]['square'] == square and donors[1]['ranks'] == ranks
    claims = {}
    for d in donors:
        for p in d['positions']:
            at, label = p['target_plaintext_index'], p['label']
            assert at not in claims or claims[at] == label
            claims[at] = label
    assert ''.join(claims[i] for i in range(91,102)) == 'XKXMXRMX1XA'

    def extend(previous, spans):
        current = list(previous['edited_ciphertext'])
        ledger = []
        for start, text in spans:
            for i, ch in enumerate(text, start):
                if ch == '?':
                    continue
                assert ch in domains[i]
                assert previous['plaintext'][i] in ('?', ch)
                pair = C[square.index(ch)//6] + C[square.index(ch)%6]
                models = iv[2*i:2*i+2]
                if previous['plaintext'][i] == '?':
                    assert sum(wire[j] in C for j in models) == 1
                for half, (model, value) in enumerate(zip(models, pair)):
                    assert current[model] in ('?', value)
                    if current[model] == '?':
                        ledger.append(dict(plaintext_index=i, character=ch, half=half, model_index=model,
                                           source_index=model if model<160 else None,
                                           origin='printed_mask' if model<160 else 'lost_tail', coordinate=value,
                                           original_pair=''.join(wire[j] for j in models),
                                           original_domain=domains[i]))
                        current[model] = value
        current = ''.join(current)
        assert all(a == '?' or a == b for a,b in zip(wire,current))
        text = decrypt(current,ranks,square)
        witness = current.replace('?','A')
        witness_text = decrypt(witness,ranks,square)
        assert encrypt(witness_text,ranks,square) == witness
        return dict(plaintext=text, edited_ciphertext=current, fixed_positions=len(text)-text.count('?'),
                    observed_substitutions=0,
                    printed_mask_fills=previous['printed_mask_fills']+sum(x['origin']=='printed_mask' for x in ledger),
                    lost_tail_fills=previous['lost_tail_fills']+sum(x['origin']=='lost_tail' for x in ledger),
                    additional_fills=ledger, unresolved_positions=[i for i,c in enumerate(text) if c=='?'],
                    arbitrary_roundtrip_witness=dict(ciphertext=witness,plaintext=witness_text,
                        status='Residual A fills are arithmetic witnesses only, not historical text.'))

    primary = extend(base['primary'], [(91,'XKXMXRMX1XA')])
    assert (primary['fixed_positions'],primary['printed_mask_fills'],primary['lost_tail_fills']) == (97,12,49)
    assert [x['plaintext_index'] for x in primary['additional_fills']] == [93,94,95,96,98,99,100]
    closing = extend(primary, [(104,'GR?XOPX')])
    assert (closing['fixed_positions'],closing['printed_mask_fills'],closing['lost_tail_fills']) == (101,12,53)
    assert [x['plaintext_index'] for x in closing['additional_fills']] == [105,107,108,109]
    assert all(closing['plaintext'][i]=='?' for i in [90,102,106])
    assert 'X' not in domains[102]
    displays = re.findall(r'```text\n(.*?)\n```', (HERE/'FOOTER.md').read_text(), re.S)
    assert displays == [primary['plaintext'],closing['plaintext']]
    return dict(schema='adfgvx-p116-optional-footer-v1', authors=['icekylinx','GPT-6 Astra Pro'],
                dependencies={str(p.relative_to(ROOT)):sha(p) for p in
                              [HERE/'inputs.json',HERE/'approval_extension.json']},
                key=key, original_analysis_frame=wire, original_observed_coordinates=144,
                prior_word_fixed_positions=90, donors=donors,
                proposed_span=dict(start=91,stop=102,text='XKXMXRMX1XA'),
                optional_footer=primary, separately_optional_closing=closing,
                original_same_period_closing_template=closing_donor,
                historical_context=dict(url='https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf',
                    authors=['George Lasry','Ingo Niebel','Nils Kopal','Arno Wacker'],year=2016,
                    doi='10.1080/01611194.2016.1169461',location='Table 3, row 13; printed p20 / PDF p21',
                    short_quote='(Signed) K.M. I A GR-OP',
                    qualification='Published English reconstruction, partly based on Childs; not an independent German coordinate witness.'),
                search_scope=dict(initial_json_raw_donors=331,additional_unique_case_raw_displays=314,
                    target_frames=['p215_B1','p154_A2','p71_A2','p212_A4','p116_A13'],
                    initial_minimum_phrase_length=12,initial_new_hits=0,
                    exploratory_minimum_phrase_length=8,exploratory_minimum_observed_support=8,
                    discovery='The lower-length scan found a p164 field with12 observed target coordinates. Its trailing XRMX1 overlaps the same-key p105 field; the joined11-position proposal has15 observed target coordinates.',
                    limit='The joined template and historical closing are contextual proposals, not a blind single-donor hit or calibrated statistical identification.'),
                limits=['No copied-transmission relationship is asserted. Donor letters suggest a shared field format; recipient fills are re-encoded under its own key.',
                        'The literal1 is also witnessed in the same-period p105 field. No digit substitution, historical numeral value or Roman-numeral interpretation is inferred.',
                        'Position90 is wholly missing; no O is supplied. Position102 cannot be X; position106 remains unknown.',
                        'The seven footer fills and four separate closing fills each retain one original observed half-coordinate.',
                        'The90-position approval layer and optional doubled-S spelling remain unchanged; no first historical decipherment is claimed.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    args = parser.parse_args()
    result = compute()
    target = HERE/'footer_extension.json'
    if args.verify:
        assert load(target) == result, 'Footer certificate differs; inspect before regeneration'
    else:
        target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(verified=True,optional_footer_fixed=97,optional_closing_fixed=101,
                         observed_substitutions=0,new_footer_half_fills=7,new_closing_half_fills=4)))


if __name__ == '__main__':
    main()
