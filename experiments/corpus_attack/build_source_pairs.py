#!/usr/bin/env python3
"""Certify three positive, image-checked Nov4–6 source families.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
No language model is needed to reproduce the source geometry or fit costs.
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
from adfgvx.cipher import SYMBOLS, decrypt, encrypt, plaintext_domains, untranspose


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analysis(raw):
    return ''.join(c if c in SYMBOLS else '?' for c in ''.join(raw.split()))


def build():
    inputs = json.loads((HERE/'source_pairs.json').read_text())
    key = json.loads((HERE/'key_snapshot.json').read_text())
    square, ranks = key['square'], key['column_rank_order']
    assert len(set(square)) == 36
    corpus = {r['id']: r for r in json.loads((ROOT/'experiments/p153_corpus/inputs.json').read_text())['blocks']}
    records = {}
    for source in inputs['records']:
        literal = ''.join(source['raw_grouped'].split())
        ct = analysis(literal)
        ocr = ''.join(corpus[source['ocr_block_id']]['groups'])
        changes = [dict(operation=tag, ocr_range=[i,j], source_range=[a,b],
                        ocr_text=ocr[i:j], literal_source_text=literal[a:b])
                   for tag,i,j,a,b in difflib.SequenceMatcher(None,ocr,literal,autojunk=False).get_opcodes() if tag != 'equal']
        record = dict(id=source['id'], raw_literal=literal,
                      analysis_ciphertext=ct, received_slots=len(ct),
                      valid_coordinates=sum(c in SYMBOLS for c in literal),
                      source_erasure_slots=[dict(source_index=i,literal=c) for i,c in enumerate(literal) if c not in SYMBOLS],
                      ocr_block_id=source['ocr_block_id'], ocr_ciphertext=ocr,
                      ocr_to_literal_operations=changes,
                      source_crop=source['source_crop'], source_crop_sha256=sha(HERE/source['source_crop']))
        if len(ct)%2 == 0:
            record['raw_plaintext'] = decrypt(ct,ranks,square)
        else:
            record['raw_plaintext'] = None
            record['raw_odd_length_notice'] = 'The odd received length needs a declared geometry hypothesis; no final coordinate is silently discarded.'
        records[source['id']] = record

    # The sole allowed geometry repair in this family: one missing group of5.
    short = records['p138_A1']['analysis_ciphertext']
    full = records['p148_C1']['analysis_ciphertext']
    trials = []
    for gap in range(len(short)+1):
        aligned = short[:gap]+'?'*5+short[gap:]
        cost = sum(a != '?' and b != '?' and a != b for a,b in zip(aligned,full))
        trials.append(dict(insert_before_source_index=gap,valid_coordinate_disagreements=cost))
    minimum = min(r['valid_coordinate_disagreements'] for r in trials)
    best = [r['insert_before_source_index'] for r in trials if r['valid_coordinate_disagreements']==minimum]
    assert best == [140]
    aligned = short[:140]+'?'*5+short[140:]
    mapping = list(range(140))+[None]*5+list(range(140,len(short)))
    records['p138_A1']['structural_alignment'] = dict(
        hypothesis='One missing consecutive five-coordinate group; all237 received slots retain their identity and order.',
        trials=len(trials), unique_best_gap=140, minimum_valid_coordinate_disagreements=minimum,
        all_gap_costs=trials, aligned_ciphertext=aligned, aligned_to_source_index=mapping,
        aligned_raw_plaintext=decrypt(aligned,ranks,square),
        other_witness_group=full[140:145])

    specifications = [
        dict(id='osthoff_part1', witness_ids=['p138_A1','p148_C1'],
             likely_plaintext='MILITAERMISSIONKONSTANTINOPELXKOMMANDODESHPTMSDERRESOSTHOFFNACHDERTUERKEIUNDSEINEZUTEILUNGZURMILITAERMISSIONISTAUFGEHOBEN',
             hypothesis='Supply the explicit p148 erasure from the parallel witness. In p138, align one missing group at the unique best location and retain the three contrary printed coordinates as source disagreements.'),
        dict(id='osthoff_part2', witness_ids=['p138_A2','p149_A2'],
             likely_plaintext='DERSELBEISTDEM1XERSBATLEISENBAHNREGMTSZUUEBERWEISENAKOFOLGTXAUFALLERHOECHSTENBEFEHLCHEFMILITAERKABINETTSFRHRMARSCHALLX',
             hypothesis='DEM, ERSBATL and REGMTS are editorial emendations of the shared literal readings UEM, ERSBKTL and REGM1S. Three coordinate substitutions in each witness are explicitly charged; two are an adjacent VF/FV exchange. KABINETTS and HOECHSTEN use the clearer p149 witness.'),
        dict(id='glatz_enquiry', witness_ids=['p140_B','p149_C'],
             likely_plaintext='MILITAERXMISSIONKONSTANTINOPELXDRAHTNACHRICHTUEBERVERBLEIBREGXBMSTRXGLATZVOMSTRASSENBAUSONDERKOMMANDO1ERBETETENXMILVERKEHRXROEMX2XAX100166XKOXDURCHADMIRALSTABXKZX95537X',
             hypothesis='Fill the damaged p140 group64 final slot (source319) with X, giving VX=I in KONSTANTINOPEL. The parallel p149 G gives VG=B and does not independently support I. No legible p140 coordinate changes. Preserve the four contrary coordinates in the p149 raw witness.')
    ]
    families=[]
    for spec in specifications:
        target=spec['likely_plaintext']; generated=encrypt(target,ranks,square)
        witness_outputs=[]
        for id in spec['witness_ids']:
            record=records[id]; repair=record.get('structural_alignment')
            ct=repair['aligned_ciphertext'] if repair else record['analysis_ciphertext']
            source_map=repair['aligned_to_source_index'] if repair else list(range(len(ct)))
            assert len(ct)==len(generated)
            edits=[dict(aligned_ciphertext_index=i,source_index=source_map[i],printed=a,required=b)
                   for i,(a,b) in enumerate(zip(ct,generated)) if a!='?' and a!=b]
            fills=[dict(aligned_ciphertext_index=i,source_index=source_map[i],required=b,
                        kind='missing_group_coordinate' if source_map[i] is None else 'source_erasure')
                   for i,(a,b) in enumerate(zip(ct,generated)) if a=='?']
            witness_outputs.append(dict(id=id,aligned_ciphertext=ct,source_map=source_map,
                raw_aligned_plaintext=decrypt(ct,ranks,square),plaintext_domains=plaintext_domains(ct,ranks,square),
                known_coordinate_edits=edits,known_coordinate_edit_count=len(edits),
                supplied_coordinates=fills,retained_known_coordinates=sum(c in SYMBOLS for c in ct)-len(edits),
                exact_round_trip_after_declared_changes=decrypt(generated,ranks,square)==target))
        streams=[untranspose(w['aligned_ciphertext'],ranks)for w in witness_outputs]
        per_position=[]
        for i,ch in enumerate(target):
            observed=[s[2*i:2*i+2]for s in streams]
            allpairs=[SYMBOLS[cell//6]+SYMBOLS[cell%6]for cell in range(36)]
            costs=[sum(a!='?'and a!=b for pair in observed for a,b in zip(pair,p))for p in allpairs]
            low=min(costs);cells=[j for j,cost in enumerate(costs)if cost==low]
            pair=allpairs[square.index(ch)]
            cost=sum(a!='?'and a!=b for p in observed for a,b in zip(p,pair))
            if pair in observed: support='complete_pair_in_a_witness'
            elif all(want in [p[j]for p in observed]for j,want in enumerate(pair)):support='observed_half_pair_composite'
            elif all(want in [p[j]for p in observed] or any(p[j]=='?'for p in observed)for j,want in enumerate(pair)):support='requires_erasure_fill'
            else:support='requires_unattested_coordinate_emendation'
            per_position.append(dict(plaintext_index=i,character=ch,required_pair=pair,observed_pairs=observed,
                minimum_combined_known_coordinate_cost=low,
                minimum_cost_characters=''.join(sorted(square[c]for c in cells)),
                candidate_combined_known_coordinate_cost=cost,support=support))
        families.append(dict(spec,plaintext_length=len(target),candidate_ciphertext=generated,
            witnesses=witness_outputs,per_position=per_position,
            source_fit=dict(combined_known_coordinate_edit_count=sum(w['known_coordinate_edit_count']for w in witness_outputs),
                unconstrained_attainable_minimum=sum(p['minimum_combined_known_coordinate_cost']for p in per_position),
                positions_outside_minimum_cost_domains=[p['plaintext_index']for p in per_position if p['candidate_combined_known_coordinate_cost']>p['minimum_combined_known_coordinate_cost']],
                support_counts={s:sum(p['support']==s for p in per_position)for s in sorted({p['support']for p in per_position})},
                complete_pair_support_is_not_a_claim_of_one_clean_witness=True)))
    return dict(schema='adfgvx-positive-source-family-certificate-v1',credit=inputs['credit'],
        source_inputs_sha256=sha(HERE/'source_pairs.json'),key_snapshot_sha256=sha(HERE/'key_snapshot.json'),
        corpus_inputs_sha256=sha(ROOT/'experiments/p153_corpus/inputs.json'),
        scope='Fixed published Nov4–6 key; image-confirmed source transcriptions. This is a source reconstruction, not a newly recovered key or a claim of historical priority.',
        index_convention='All machine-readable indices are zero-based.',records=list(records.values()),families=families)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    output=HERE/'source_pair_results.json';result=build()
    if args.verify:
        assert json.loads(output.read_text())==result
    else:output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(verified=args.verify,source_records=len(result['records']),
        families=[dict(id=f['id'],plaintext_positions=f['plaintext_length'],
                       known_coordinate_edits=[w['known_coordinate_edit_count']for w in f['witnesses']],
                       minimum=f['source_fit']['unconstrained_attainable_minimum'],
                       support=f['source_fit']['support_counts'])for f in result['families']]),indent=2))


if __name__=='__main__':main()
