#!/usr/bin/env python3
"""Verify the optional approval clause in p116 A13 without editing its source.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, transposition_indices

CO = 'ADFGVX'
NEW_SPANS = [(65, 'EINVERSTAENDNIS'), (81, 'ERBETEN')]
ALTERNATIVES = [
    'EINVERSTAENDNIS', 'ERBETEN', 'EINVERSTAENDNIS?ERBETEN',
    'EINVERSTAENDNISSERBETEN', 'EINVERSTAENDNISXERBETEN',
    'EINVERSTAENDNISERBETEN', 'EINVERSTANDEN',
    'EINVERSTANDENERBETEN', 'EINVERSTANDNISERBETEN',
    'EINVERSTAENDNISS', 'EINVERSTAENDNISWIRD',
    'EINVERSTAENDNISWIRDERBETEN', 'ZUSTIMMUNGERBETEN',
    'GENEHMIGUNGERBETEN',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compute():
    data = json.loads((HERE / 'inputs.json').read_text())
    key = data['key_snapshot']
    ranks, square = key['column_rank_order'], key['square']
    source = ''.join(''.join(data['record_snapshot']['source_rows']).split()).replace('-', '?')
    assert len(source) == 160 and source.count('?') == 16
    wire = source + '?' * 62
    raw = decrypt(wire, ranks, square)
    assert raw == data['record_snapshot']['expected_raw']
    permutation = transposition_indices(len(wire), ranks)
    inverse = [permutation.index(i) for i in range(len(wire))]
    domains = plaintext_domains(wire, ranks, square)

    def layer(spans):
        edited = list(wire)
        ledger = []
        selected = {}
        for start, word in spans:
            for j, character in enumerate(word, start):
                if character == '?':
                    continue
                if j in selected:
                    assert selected[j] == character
                selected[j] = character
                pair = CO[square.index(character) // 6] + CO[square.index(character) % 6]
                for half, coordinate in enumerate(pair):
                    model = inverse[2*j+half]
                    observed = wire[model]
                    assert observed == '?' or observed == coordinate, (j, character, model)
                    if observed == '?' and edited[model] == '?':
                        ledger.append(dict(plaintext_index=j, character=character, half=half,
                                           model_index=model, source_index=model if model < 160 else None,
                                           origin='printed_mask' if model < 160 else 'lost_tail',
                                           coordinate=coordinate))
                    edited[model] = coordinate
        edited = ''.join(edited)
        assert all(a == '?' or a == b for a, b in zip(wire, edited))
        text = decrypt(edited, ranks, square)
        assert all(text[j] == c for j, c in selected.items())
        witness = edited.replace('?', 'A')
        plaintext = decrypt(witness, ranks, square)
        assert encrypt(plaintext, ranks, square) == witness
        return dict(plaintext=text, fixed_positions=len(text)-text.count('?'),
                    observed_substitutions=0,
                    printed_mask_fills=sum(x['origin']=='printed_mask' for x in ledger),
                    lost_tail_fills=sum(x['origin']=='lost_tail' for x in ledger),
                    fill_ledger=ledger, edited_ciphertext=edited,
                    arbitrary_roundtrip_witness=dict(ciphertext=witness, plaintext=plaintext,
                        status='Consistency witness only; arbitrary remaining A fills are not a reading.'))

    previous_spans = [(x['start'], x['text']) for x in data['proposal']['new_word_spans']]
    previous = layer(previous_spans)
    assert previous['plaintext'] == data['proposal']['editorial_text']
    assert (previous['fixed_positions'], previous['printed_mask_fills'], previous['lost_tail_fills']) == (75, 5, 32)
    primary = layer(previous_spans + NEW_SPANS)
    doubled = layer(previous_spans + NEW_SPANS + [(80, 'S')])
    assert (primary['fixed_positions'], primary['printed_mask_fills'], primary['lost_tail_fills']) == (90, 11, 43)
    assert (doubled['fixed_positions'], doubled['printed_mask_fills'], doubled['lost_tail_fills']) == (91, 11, 44)
    added = []
    for index, (old, new) in enumerate(zip(previous['plaintext'], primary['plaintext'])):
        if old == '?' and new != '?':
            slots = inverse[2*index:2*index+2]
            observed = [i for i in slots if wire[i] in CO]
            added.append(dict(plaintext_index=index, character=new, model_indices=slots,
                              observed_source_indices=observed, observed_halves=len(observed),
                              original_domain=domains[index]))
        else:
            assert old == new
    assert len(added) == 15
    assert [x['plaintext_index'] for x in added if x['observed_halves']==0] == [68, 87]
    assert sum(x['observed_halves']==1 for x in added) == 13
    assert domains[80] == '3BFKQS' and primary['plaintext'][80] == '?'
    comparisons = []
    for word in ALTERNATIVES:
        placements = []
        for start in range(len(raw)-len(word)+1):
            cost = 0
            for offset, ch in enumerate(word):
                if ch == '?':
                    continue
                pair = CO[square.index(ch)//6] + CO[square.index(ch)%6]
                for half, target in enumerate(pair):
                    observed = wire[inverse[2*(start+offset)+half]]
                    cost += observed in CO and observed != target
            placements.append(cost)
        best = min(placements)
        comparisons.append(dict(word=word, compared_starts=len(placements),
                                minimum_observed_substitutions=best,
                                best_starts=[i for i, cost in enumerate(placements) if cost==best],
                                costs=placements))
    for word, start in [('EINVERSTAENDNIS',65), ('ERBETEN',81),
                        ('EINVERSTAENDNIS?ERBETEN',65), ('EINVERSTAENDNISSERBETEN',65)]:
        row = next(x for x in comparisons if x['word']==word)
        assert row['minimum_observed_substitutions']==0 and row['best_starts']==[start]
    return dict(schema='adfgvx-p116-approval-extension-v1',
        authors='icekylinx and GPT-6 Astra Pro',
        scope='Optional word proposal under the inherited 222-slot tail-loss frame; no new body or changed source observation.',
        dependencies={str(path.relative_to(ROOT)):sha(path) for path in [HERE/'inputs.json', HERE/'certificates.json']},
        key=key, source=source, raw_plaintext=raw,
        prior_fixed_positions=75,
        proposed_spans=[dict(start=s,text=t) for s,t in NEW_SPANS],
        primary=primary, optional_doubled_s=doubled, newly_fixed_positions=added,
        unresolved_position_80=dict(pair=''.join(wire[i] for i in inverse[160:162]),
            domain=domains[80], optional='S', optional_model_fill=194,
            qualification='S is an optional doubled spelling; X is outside the observed half-pair domain.'),
        bounded_word_placement_comparison=comparisons,
        comparison_scope='Target-conditioned words and this fixed frame only; not an exhaustive German-language search.',
        historical_context=dict(
            url='https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf',
            authors='George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker',
            year=2016, doi='10.1080/01611194.2016.1169461',
            location='Table 3, row 13, printed page 20 / PDF page 21',
            short_quote='Approval is requested.',
            qualification='English historical translation guides the lexical hypothesis; it is not an independent German or coordinate witness.'),
        limits=['V at 68 and N at 87 have both coordinates missing and are supplied by the proposed words.',
                'The army label, position 80, and remaining closing fields stay unresolved in the primary layer.',
                'Prior authors retain the historical decipherment credit; this is an additional exact conditional source edition.'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args=parser.parse_args()
    result=compute()
    display=(HERE/'APPROVAL.md').read_text()
    assert re.findall(r'```text\n(.*?)\n```', display, flags=re.S)==[result['primary']['plaintext']]
    quotation=''.join(line[2:] for line in display.splitlines() if line.startswith('> '))
    assert re.sub(r'[^A-Z0-9?]', '', quotation.upper())==result['primary']['plaintext']
    path=HERE/'approval_extension.json'
    if args.write:
        path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    else:
        assert result==json.loads(path.read_text()), 'Approval certificate differs'
    if args.pdf:
        subprocess.run([sys.executable,str(HERE/'verify.py'),'--verify','--pdf',str(args.pdf)],check=True)
    print(json.dumps(dict(passed=True, primary_fixed=90, optional_fixed=91,
        new_primary_positions=15, new_half_observed_positions=13, new_wholly_missing_positions=2,
        observed_substitutions=0, original_pdf_checked=bool(args.pdf))))


if __name__=='__main__':
    main()
