#!/usr/bin/env python3
"""Independently verify the p197/p198 transport source-family certificate.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
Standard-library only. The implementation does not import the builder or any
repository cipher routines. Arithmetic verification does not certify editorial
wording or the historical truth of a proposed geometry.
"""
from pathlib import Path
import argparse
import hashlib
import json

COORDS='ADFGVX'
ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def normalize(raw):
    return ''.join(ch if ch in COORDS else '?' for ch in raw)


def characterize(ct, ranks, square, source_map):
    assert len(ct)%2==0 and len(source_map)==len(ct)
    assert sorted(ranks)==list(range(1,len(ranks)+1))
    assert len(square)==36
    assigned=[ch for ch in square if ch!='?']
    assert len(assigned)==len(set(assigned))
    unused=set(ALPHABET)-set(square)
    assert len(unused)==square.count('?')
    # Write ciphertext columns directly to the row-major intermediate array.
    perm=[pos for column in sorted(range(len(ranks)),key=lambda c:ranks[c])
          for pos in range(column,len(ct),len(ranks))]
    inter=['']*len(ct)
    inverse=[None]*len(ct)
    for cipher_pos, inter_pos in enumerate(perm):
        inter[inter_pos]=ct[cipher_pos]
        inverse[inter_pos]=cipher_pos
    assert ''.join(inter[i] for i in perm)==ct
    rows=[]
    for i in range(0,len(ct),2):
        pair=''.join(inter[i:i+2])
        cells=[];chars=set()
        for row in range(6):
            for col in range(6):
                if pair[0] not in ['?',COORDS[row]] or pair[1] not in ['?',COORDS[col]]:
                    continue
                cell=6*row+col;cells.append(cell)
                chars.update(unused if square[cell]=='?' else square[cell])
        rows.append(dict(plaintext_index=i//2,coordinate_pair=pair,
            source_indices=[source_map[inverse[i]],source_map[inverse[i+1]]],
            corrected_ciphertext_indices=inverse[i:i+2],possible_square_cells=cells,
            possible_characters=''.join(sorted(chars))))
    raw=''.join(row['possible_characters'] if len(row['possible_characters'])==1 else '?' for row in rows)
    return dict(raw_partial_plaintext=raw,domains=rows,
                fixed_plaintext_characters=len(raw)-raw.count('?'),intermediate_stream=''.join(inter))


def diffs(first,second):
    assert len(first)==len(second)
    return [dict(corrected_ciphertext_index=i,first=a,second=b,
                 both_valid_coordinates=a in COORDS and b in COORDS)
            for i,(a,b) in enumerate(zip(first,second)) if a!=b]


def verify(record):
    key=record['key'];ranks,square=key['column_rank_order'],key['square']
    assert key['id']=='Nov13-15b'
    assert square=='H??BMUF15PX0DJLR????S6VONKZ?AWITEGC?'
    assert ranks==[4,11,5,14,9,7,16,1,12,15,6,10,3,13,8,2]
    records={row['id']:row for row in record['records']}
    assert set(records)=={'p197_C','p198_B','p197_D','p198_E'}
    expected_counts={'p197_C':(185,178),'p198_B':(190,190),'p197_D':(142,141),'p198_E':(147,146)}
    for row in records.values():
        raw=''.join(row['raw_grouped'].split())
        ct=normalize(raw)
        assert raw==row['raw_literal'] and ct==row['analysis_ciphertext']
        assert row['received_slot_count']==len(raw)
        assert row['valid_coordinate_count']==sum(ch in COORDS for ch in raw)
        assert (len(raw),row['valid_coordinate_count'])==expected_counts[row['id']]
        assert row['invalid_source_slots']==[dict(source_index=i,printed=ch,analysis='?') for i,ch in enumerate(raw) if ch not in COORDS]
        if len(raw)%2==0:
            assert row['literal_analysis']==characterize(ct,ranks,square,list(range(len(raw))))
    def check_analysis(row):
        assert row['analysis']==characterize(row['corrected_ciphertext'],ranks,square,row['corrected_to_source_index'])
    e=records['p198_E']['analysis_ciphertext'];rep=record['duplicate_group_repair']
    assert len(rep['candidates'])==2
    for start,row in zip([15,20],rep['candidates']):
        assert row['deleted_source_indices']==list(range(start,start+5))
        assert row['deleted_literal']==e[start:start+5]=='XAXVV'
        assert row['corrected_ciphertext']==e[:start]+e[start+5:]
        assert row['corrected_to_source_index']==list(range(start))+list(range(start+5,len(e)))
        assert row['known_source_substitutions']==[]
        check_analysis(row)
    eref=rep['candidates'][0]['corrected_ciphertext']
    assert eref==rep['candidates'][1]['corrected_ciphertext']
    assert len(eref)==rep['corrected_length']==142
    assert sum(ch in COORDS for ch in eref)==rep['retained_valid_coordinate_count']==141
    assert rep['corrected_ciphertext_identical_for_both_choices'] is True
    assert rep['candidates'][0]['analysis']['raw_partial_plaintext']=='ESKOMMTEIN?TONNENAMTOXNURBEST5NANH?GNGERB?LADENXBENEINPUMPEBEREITHALTEN'

    d=records['p197_D']['analysis_ciphertext'];rel=record['erasure_relocation']
    assert [i for i,ch in enumerate(d) if ch=='?']==[89]
    valid=d[:89]+d[90:];mapping=list(range(89))+list(range(90,142))
    distances=[]
    for gap in range(142):
        ct=valid[:gap]+'?'+valid[gap:]
        distance=sum(x['both_valid_coordinates'] for x in diffs(ct,eref))
        distances.append(dict(insert_erasure_before_surviving_source_index=gap,valid_coordinate_disagreements=distance))
    assert distances==rel['all_trial_distances'] and rel['tested_placements']==142
    assert min(x['valid_coordinate_disagreements'] for x in distances)==rel['minimum_valid_coordinate_disagreements']==8
    best=[x['insert_erasure_before_surviving_source_index'] for x in distances if x['valid_coordinate_disagreements']==8]
    assert best==[74,75]
    assert [x['insert_erasure_before_surviving_source_index'] for x in rel['best_alignments']]==best
    for gap,row in zip(best,rel['best_alignments']):
        assert row['corrected_ciphertext']==valid[:gap]+'?'+valid[gap:]
        assert row['corrected_to_source_index']==mapping[:gap]+[89]+mapping[gap:]
        assert ''.join(ch for ch in row['corrected_ciphertext'] if ch in COORDS)==valid
        assert sorted(row['corrected_to_source_index'])==list(range(142))
        assert row['differences_from_duplicate_repaired_p198_E']==diffs(row['corrected_ciphertext'],eref)
        check_analysis(row)

    c,b=(records[i]['analysis_ciphertext'] for i in ['p197_C','p198_B'])
    mis=record['missing_group_alignment'];distances=[]
    for gap in range(186):
        ct=c[:gap]+'?'*5+c[gap:]
        distance=sum(x['both_valid_coordinates'] for x in diffs(ct,b))
        distances.append(dict(insert_five_erasures_before_source_index=gap,valid_coordinate_disagreements=distance))
    assert distances==mis['all_trial_distances'] and mis['tested_placements']==186
    assert min(x['valid_coordinate_disagreements'] for x in distances)==mis['minimum_valid_coordinate_disagreements']==18
    best=[x['insert_five_erasures_before_source_index'] for x in distances if x['valid_coordinate_disagreements']==18]
    assert best==[64,65]
    assert [x['insert_five_erasures_before_source_index'] for x in mis['best_alignments']]==best
    for gap,row in zip(best,mis['best_alignments']):
        assert row['corrected_ciphertext']==c[:gap]+'?'*5+c[gap:]
        assert row['corrected_to_source_index']==list(range(gap))+[None]*5+list(range(gap,185))
        assert ''.join(ch for ch in row['corrected_ciphertext'] if ch in COORDS)==''.join(ch for ch in c if ch in COORDS)
        assert row['differences_from_p198_B']==diffs(row['corrected_ciphertext'],b)
        check_analysis(row)
    assert mis['best_alignments'][0]['corrected_ciphertext']==mis['best_alignments'][1]['corrected_ciphertext']
    assert mis['corrected_ciphertexts_identical'] is True

    paired=[('lorry_and_petrol_pump',rel['best_alignments'][-1]['analysis'],rep['candidates'][0]['analysis']),
            ('equipment_for_darmstadt',mis['best_alignments'][-1]['analysis'],records['p198_B']['literal_analysis'])]
    summaries={}
    for label,first,second in paired:
        editorial=record['editorial_readings'][label];target=editorial['normalized_editorial_target']
        assert len(target)==len(first['domains'])==len(second['domains'])
        rows=[]
        for i,ch in enumerate(target):
            if ch=='?':continue
            cell=square.index(ch);expected=COORDS[cell//6]+COORDS[cell%6]
            a,b=first['domains'][i]['coordinate_pair'],second['domains'][i]['coordinate_pair']
            if expected==a or expected==b:kind='complete_pair_in_at_least_one_witness'
            elif all(expected[k] in [a[k],b[k]] for k in range(2)):kind='observed_coordinate_composite'
            elif all(expected[k] in [a[k],b[k]] or '?' in [a[k],b[k]] for k in range(2)):kind='requires_erasure_fill'
            else:kind='requires_unattested_coordinate_emendation'
            rows.append(dict(plaintext_index=i,editorial_character=ch,required_pair=expected,
                             first_observed_pair=a,second_observed_pair=b,support=kind))
        assert rows==editorial['per_letter_support']
        counts={kind:sum(r['support']==kind for r in rows) for kind in sorted({r['support'] for r in rows})}
        assert counts==editorial['support_counts']
        audit=editorial['combined_coordinate_cost']
        positions=[]
        unused=set(ALPHABET)-set(square)
        for i,ch in enumerate(target):
            a,b=first['domains'][i]['coordinate_pair'],second['domains'][i]['coordinate_pair']
            costs=[]
            for cell in range(36):
                pair=COORDS[cell//6]+COORDS[cell%6]
                costs.append(sum(observed[k]!='?' and observed[k]!=pair[k] for observed in [a,b] for k in range(2)))
            minimum=min(costs);cells=[cell for cell in range(36) if costs[cell]==minimum]
            letters=set()
            for cell in cells:letters.update(unused if square[cell]=='?' else square[cell])
            required=None if ch=='?' else COORDS[square.index(ch)//6]+COORDS[square.index(ch)%6]
            per_witness=None if required is None else [sum(pair[k]!='?' and pair[k]!=required[k] for k in range(2)) for pair in [a,b]]
            positions.append(dict(plaintext_index=i,first_observed_pair=a,second_observed_pair=b,
                minimum_known_coordinate_cost=minimum,minimum_cost_cells=cells,minimum_cost_characters=''.join(sorted(letters)),
                editorial_character=ch,editorial_required_pair=required,editorial_cost_by_witness=per_witness,
                editorial_combined_cost=None if per_witness is None else sum(per_witness)))
        assert positions==audit['per_position']
        minimum=sum(p['minimum_known_coordinate_cost'] for p in positions)
        specified=sum(p['editorial_combined_cost'] or 0 for p in positions)
        unresolved=sum(p['minimum_known_coordinate_cost'] for p in positions if p['editorial_character']=='?')
        assert minimum==audit['unconstrained_attainable_minimum']
        assert specified==audit['editorial_cost_at_specified_positions']
        assert unresolved==audit['minimum_cost_at_unresolved_positions']
        assert specified+unresolved==audit['attainable_minimum_with_specified_editorial_letters']
        assert audit['editorial_cost_by_witness_at_specified_positions']==[sum(p['editorial_cost_by_witness'][j] for p in positions if p['editorial_cost_by_witness'] is not None) for j in range(2)]
        assert audit['positions_outside_minimum_cost_domains']==[p['plaintext_index'] for p in positions if p['editorial_combined_cost'] is not None and p['editorial_combined_cost']>p['minimum_known_coordinate_cost']]
        assert audit['complete_pair_support_is_one_globally_clean_witness'] is False
        for field,expected_cost,use_editorial in [('minimum_cost_attainment_witness',minimum,False),('editorial_cost_attainment_witness',specified+unresolved,True)]:
            witness=audit[field];ct=witness['ciphertext']
            actual=characterize(ct,ranks,square,list(range(len(ct))))
            stream=actual['intermediate_stream']
            assert stream==witness['intermediate_coordinate_stream']
            for i,p in enumerate(positions):
                cell=COORDS.index(stream[2*i])*6+COORDS.index(stream[2*i+1])
                if use_editorial and p['editorial_character']!='?':assert square[cell]==p['editorial_character']
                else:assert cell in p['minimum_cost_cells']
            costs=[sum(a!='?' and a!=b for a,b in zip(w['intermediate_stream'],stream)) for w in [first,second]]
            assert costs==witness['cost_by_witness']
            assert sum(costs)==witness['combined_cost']==expected_cost
        summaries[label]=dict(support_counts=counts,minimum_combined_coordinate_cost=minimum,
                              editorial_minimum_combined_coordinate_cost=specified+unresolved,
                              specified_cost_by_witness=audit['editorial_cost_by_witness_at_specified_positions'],
                              positions_outside_minimum_cost_domains=audit['positions_outside_minimum_cost_domains'])
    assert summaries['lorry_and_petrol_pump']['support_counts']=={'complete_pair_in_at_least_one_witness':66,'observed_coordinate_composite':1,'requires_unattested_coordinate_emendation':3}
    assert summaries['equipment_for_darmstadt']['support_counts']=={'complete_pair_in_at_least_one_witness':91,'requires_erasure_fill':1}
    return dict(verified=True,source_records=4,all_coordinate_domain_sets_verified=True,
                source_coordinates_preserved_under_explicit_geometries=True,
                exact_duplicate_deletion_alternatives=2,d_erasure_positions=[74,75],
                c_five_slot_gap_positions=[64,65],c_geometry_ciphertexts_identical=True,
                editorial_support=summaries,
                separate_p198_D_target_solved=False,
                original_historical_plaintexts_proved=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',nargs='?',type=Path,default=ROOT/'data/certificates/p197_p198_transport.json')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=verify(json.loads(args.certificate.read_text()))
    result['certificate_sha256']=hashlib.sha256(args.certificate.read_bytes()).hexdigest()
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
