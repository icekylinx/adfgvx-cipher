#!/usr/bin/env python3
"""Independently decrypt and re-encrypt the six positive source witnesses.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
This implementation imports neither adfgvx.cipher nor the certificate builder.
It checks arithmetic and provenance, not an independent visual source review.
"""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
AXES='ADFGVX'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def undo(ct,ranks):
    q,extra=divmod(len(ct),len(ranks));columns={};start=0
    for rank in range(1,len(ranks)+1):
        col=ranks.index(rank);size=q+(col<extra);columns[col]=ct[start:start+size];start+=size
    assert start==len(ct)
    return ''.join(columns[col][row]for row in range(q+1)for col in range(len(ranks))if row<len(columns[col]))


def forward(stream,ranks):
    return ''.join(stream[col::len(ranks)]for rank in range(1,len(ranks)+1)for col in [ranks.index(rank)])


def main():
    source=json.loads((HERE/'source_pairs.json').read_text())
    key=json.loads((HERE/'key_snapshot.json').read_text())
    cert=json.loads((HERE/'source_pair_results.json').read_text())
    assert cert['source_inputs_sha256']==sha(HERE/'source_pairs.json')
    assert cert['key_snapshot_sha256']==sha(HERE/'key_snapshot.json')
    assert cert['corpus_inputs_sha256']==sha(ROOT/'experiments/p153_corpus/inputs.json')
    ranks=key['column_rank_order'];square=key['square'];assert sorted(ranks)==list(range(1,len(ranks)+1))and len(set(square))==36
    pairs={square[6*r+c]:AXES[r]+AXES[c]for r in range(6)for c in range(6)}
    def decrypt(ct):
        interim=undo(ct,ranks);assert len(interim)%2==0
        return ''.join(square[AXES.index(a)*6+AXES.index(b)]if a in AXES and b in AXES else '?'for a,b in zip(interim[::2],interim[1::2]))
    records={r['id']:r for r in cert['records']}
    for raw in source['records']:
        record=records[raw['id']];literal=''.join(raw['raw_grouped'].split())
        ct=''.join(c if c in AXES else '?'for c in literal)
        assert record['raw_literal']==literal and record['analysis_ciphertext']==ct
        assert record['received_slots']==len(ct)
        assert record['valid_coordinates']==sum(c in AXES for c in literal)
        assert record['source_crop_sha256']==sha(HERE/raw['source_crop'])
        if len(ct)%2==0:assert decrypt(ct)==record['raw_plaintext']
        else:assert record['raw_plaintext']is None
    a=records['p138_A1']['analysis_ciphertext'];b=records['p148_C1']['analysis_ciphertext']
    outcomes=[]
    for gap in range(len(a)+1):
        trial=a[:gap]+'?????'+a[gap:]
        outcomes.append(sum(x in AXES and y in AXES and x!=y for x,y in zip(trial,b)))
    assert min(outcomes)==3 and [i for i,c in enumerate(outcomes)if c==3]==[140]
    alignment=records['p138_A1']['structural_alignment']
    assert alignment['all_gap_costs']==[dict(insert_before_source_index=i,valid_coordinate_disagreements=c)for i,c in enumerate(outcomes)]
    summaries=[]
    for family in cert['families']:
        target=family['likely_plaintext'];stream=''.join(pairs[c]for c in target);ct=forward(stream,ranks)
        assert ct==family['candidate_ciphertext']and decrypt(ct)==target
        interim=[];source_cost=0
        for witness in family['witnesses']:
            record=records[witness['id']];original=record['analysis_ciphertext']
            if witness['id']=='p138_A1':
                assert witness['aligned_ciphertext']==original[:140]+'?????'+original[140:]
                expected_map=list(range(140))+[None]*5+list(range(140,len(original)))
            else:
                assert witness['aligned_ciphertext']==original;expected_map=list(range(len(original)))
            assert witness['source_map']==expected_map
            observed=witness['aligned_ciphertext'];dec=decrypt(observed)
            assert dec==witness['raw_aligned_plaintext']
            expected_edits=[dict(aligned_ciphertext_index=i,source_index=expected_map[i],printed=x,required=y)for i,(x,y)in enumerate(zip(observed,ct))if x in AXES and x!=y]
            assert expected_edits==witness['known_coordinate_edits']and len(expected_edits)==witness['known_coordinate_edit_count']
            assert witness['retained_known_coordinates']==sum(x in AXES for x in observed)-len(expected_edits)
            expected_fills=[dict(aligned_ciphertext_index=i,source_index=expected_map[i],required=y,kind='missing_group_coordinate'if expected_map[i]is None else 'source_erasure')for i,(x,y)in enumerate(zip(observed,ct))if x=='?']
            assert expected_fills==witness['supplied_coordinates']
            interim.append(undo(observed,ranks));source_cost+=len(expected_edits)
        minimum=0;support_counts={};outside=[]
        for position,row in enumerate(family['per_position']):
            observations=[s[2*position:2*position+2]for s in interim]
            costs={ch:sum(a in AXES and a!=b for observed in observations for a,b in zip(observed,pair))for ch,pair in pairs.items()}
            low=min(costs.values());minimum+=low;chosen=target[position];pair=pairs[chosen]
            assert row['observed_pairs']==observations and row['required_pair']==pair
            assert row['minimum_combined_known_coordinate_cost']==low
            assert row['minimum_cost_characters']==''.join(sorted(ch for ch,cost in costs.items()if cost==low))
            assert row['candidate_combined_known_coordinate_cost']==costs[chosen]
            if costs[chosen]>low:outside.append(position)
            if pair in observations:support='complete_pair_in_a_witness'
            elif all(pair[j]in [p[j]for p in observations]for j in [0,1]):support='observed_half_pair_composite'
            elif all(pair[j]in [p[j]for p in observations]or '?'in [p[j]for p in observations]for j in [0,1]):support='requires_erasure_fill'
            else:support='requires_unattested_coordinate_emendation'
            assert row['support']==support;support_counts[support]=support_counts.get(support,0)+1
        fit=family['source_fit']
        assert fit['combined_known_coordinate_edit_count']==source_cost
        assert fit['unconstrained_attainable_minimum']==minimum
        assert fit['positions_outside_minimum_cost_domains']==outside
        assert fit['support_counts']==support_counts
        summaries.append(dict(id=family['id'],positions=len(target),combined_coordinate_cost=source_cost,attainable_minimum=minimum,support=support_counts))
    print(json.dumps(dict(status='pass',source_records=len(records),candidate_plaintext_positions=sum(r['positions']for r in summaries),
        geometry_locations_exhausted=len(outcomes),families=summaries,
        implementation_scope='Independent standard-library arithmetic; no language model and no cipher/build imports. Source images still require human reading.',
        certificate_sha256=sha(HERE/'source_pair_results.json')),indent=2))


if __name__=='__main__':main()
