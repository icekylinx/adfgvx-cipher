#!/usr/bin/env python3
"""Verify the full p168 C witness and its source-linked KDO comparison.

icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt
from adfgvx.source_evidence import verify_source_evidence
from experiments.romanian_pacification_consultation.verify import inspect
from data.reviews.check_reading_presentation import displays, expected_legend
C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame(source, excluded, inserted):
    assert len(source) == 280 and 80 <= excluded < 86 and 195 <= inserted <= 199
    origins = [i for i in range(280) if i != excluded]
    origins.insert(inserted, None)
    cipher = ''.join('?' if i is None else source[i] for i in origins)
    assert [i for i in origins if i is not None] == [i for i in range(280) if i != excluded]
    return cipher, origins


def reference(data):
    old = load(ROOT / 'data/certificates/p158.json')['components']['readings'][0]
    source = old['raw_ciphertext']
    values, origins = list(source), list(range(len(source)))
    for edit in sorted(old['edits'], key=lambda x: x['start'], reverse=True):
        a, b = edit['start'], edit['end']
        assert ''.join(values[a:b]) == edit['before']
        replacement = list(edit['after'])
        owners = origins[a:b] if b-a == len(replacement) else [None] * len(replacement)
        values[a:b], origins[a:b] = replacement, owners
    cipher = ''.join(values)
    assert cipher == old['corrected_ciphertext'] and len(cipher) == 280
    # The alignment score uses only genuine observations in the original p159
    # source, not cells already restored using p168 or the p158 composite.
    observed = ''.join(source[i] if i is not None and source[i] in C else '?' for i in origins)
    return dict(literal_source=source, reconstructed_ciphertext=cipher,
                original_observations=observed, model_to_source_indices=origins,
                prior_raw=old['raw_plaintext'])


def completed_witnesses(cipher, key):
    witnesses = []
    for digits in itertools.permutations('56'):
        it = iter(digits)
        square = ''.join(next(it) if ch == '?' else ch for ch in key['square'])
        full = cipher.replace('?', 'A')
        plain = decrypt(full, key['column_rank_order'], square)
        assert encrypt(plain, key['column_rank_order'], square) == full
        witnesses.append(dict(unassigned_digit_order=''.join(digits), square=square,
                              ciphertext=full, plaintext=plain))
    return dict(arbitrary_remaining_coordinate='A', historical_fill_claim=False, witnesses=witnesses)


def scan(source, target):
    rows = []
    for excluded in range(80, 86):
        for inserted in range(195, 200):
            cipher, origins = frame(source, excluded, inserted)
            differences = [i for i,(a,b) in enumerate(zip(cipher, target)) if a in C and b in C and a != b]
            rows.append(dict(excluded_source_index=excluded, inserted_model_index=inserted,
                             observed_disagreements=len(differences), disagreement_model_indices=differences))
    return rows


def controls(key):
    texts = [
        'DIEVERBINDUNGMITDERSTATIONISTWIEDERHERGESTELLTXDIEABFAHRTDERZUEGEERFOLGTHEUTENACHMITTAGXALLEEMPFAENGERSOLLENDENBEFEHLSOFORTBESTAETIGENX',
        'DERTRANSPORTISTHEUTEINMUENCHENEINGETROFFENXDIEWEITERFAHRTWIRDMORGENFRUEHERFOLGENXDASPERSONALUNDALLEWAGENSTEHENBEREITXEMPFANGBESTAETIGENX']
    out = []
    for number, text in enumerate(texts):
        plain = (text + 'X'*140)[:140]
        full = encrypt(plain, key['column_rank_order'], key['square'])
        removed = 195 + number * 3
        values = list(full)
        del values[removed]
        values.insert(83, full[82])
        source = ''.join(values)
        rows = scan(source, full)
        best = min(r['observed_disagreements'] for r in rows)
        assert best == 0
        winners = [r for r in rows if r['observed_disagreements'] == best]
        for row in winners:
            cipher, _ = frame(source, row['excluded_source_index'], row['inserted_model_index'])
            at = row['inserted_model_index']
            completed = cipher[:at] + full[at] + cipher[at+1:]
            assert completed == full and decrypt(completed, key['column_rank_order'], key['square']) == plain
        out.append(dict(plaintext=plain, source=source, missing_original_model_index=removed,
                        duplicated_source_index=83, models_checked=30, best_disagreements=best,
                        best_ownerships=len(winners), all_best_completed_streams_equal_truth=True))
    return out


def build(pdf=None):
    data = load(HERE / 'inputs.json')
    for name, digest in data['dependencies'].items():
        assert sha(ROOT/name) == digest, name
    key = data['key']
    assert key == next(k for k in load(ROOT/'data/keys.json')['keys'] if k['id']=='Nov7-9')
    record = data['records'][0]
    source = ''.join(''.join(record['source_rows']).split())
    assert len(source) == 280 and all(ch in C for ch in source)
    assert hashlib.sha256(source.encode()).hexdigest() == record['literal_sha256']
    assert [len(''.join(row.split())) for row in record['source_rows']] == [40,40,41,40,39,40,40]
    assert source[80:86]=='VDADDD' and source[196:200]=='VVVG'
    evidence = verify_source_evidence(pdf, data['source'], data['source_images'], HERE)
    donor = reference(data)
    candidates = scan(source, donor['original_observations'])
    best = min(r['observed_disagreements'] for r in candidates)
    winners = [r for r in candidates if r['observed_disagreements']==best]
    assert best == 6 and len(winners) == 12
    assert {(r['excluded_source_index'],r['inserted_model_index'])for r in winners} == set(itertools.product([83,84,85],[195,196,197,198]))
    aliases, completions, raw_streams = [], [], []
    for row in winners:
        a,b = row['excluded_source_index'],row['inserted_model_index']
        cipher, origins = frame(source,a,b)
        result = inspect(cipher,key,origins)
        assert result['fixed_positions']==139
        donor_origin = donor['model_to_source_indices'][b]
        assert donor['literal_source'][donor_origin] == 'V'
        completed = cipher[:b]+'V'+cipher[b+1:]
        completions.append(completed);raw_streams.append(result['raw'])
        aliases.append(dict(**row, raw=result['raw'], unknown_plaintext_indices=[i for i,c in enumerate(result['raw'])if c=='?'],
                            mapping_sha256=hashlib.sha256(json.dumps(origins,separators=(',',':')).encode()).hexdigest(),
                            donor_source_index=donor_origin, donor_observed_glyph='V'))
    assert len(set(completions))==1 and len(set(raw_streams))==4
    primary_frame = record['primary_frame']
    cipher, origins = frame(source,primary_frame['exclude_source_index'],primary_frame['insert_unknown_at_shortened_boundary'])
    raw = inspect(cipher,key,origins)
    completed = completions[0]
    restored = inspect(completed,key,origins)
    assert restored['fixed_positions']==140 and '?' not in restored['raw']
    assert encrypt(restored['raw'],key['column_rank_order'],key['square'])==completed
    common = ''.join(chars[0] if len(set(chars))==1 else '?' for chars in zip(*raw_streams))
    assert len(common)-common.count('?')==136
    # One genuinely observed p168 coordinate supports KDO in the associated
    # p159 component. The p159 observation is X, so this remains a priced repair.
    position = raw['positions'][16]
    assert position['raw']=='K' and position['pair']=='VG'
    assert position['model_indices']==[113,169] and position['source_indices']==[114,170]
    assert source[170]=='G' and donor['literal_source'][169]=='X'
    base = donor['reconstructed_ciphertext']
    assert base[169]=='X'
    joint = base[:169]+'G'+base[170:]
    joint_raw = decrypt(joint,key['column_rank_order'],key['square'])
    assert [(i,a,b)for i,(a,b)in enumerate(zip(donor['prior_raw'],joint_raw))if a!=b]==[(16,'H','K')]
    assert encrypt(joint_raw,key['column_rank_order'],key['square'])==joint
    # Reconcile the two editions using only printed donor coordinates. At
    # model7 p159 prints invalid R: its V alternative comes from p158, not p159.
    prior = load(ROOT/'data/certificates/p158.json')
    p158 = prior['source_layers']['layers']['typed_only']['ciphertext']
    assert p158[7] == 'V'
    reconciled = []
    for label, target in [('two_witness', joint[:7]+'F'+joint[8:]), ('three_witness', joint)]:
        substitutions = []
        for index,(before,after) in enumerate(zip(completed,target)):
            if before == after:
                continue
            original = origins[index]
            assert original is not None and source[original] == before
            donor_origin = donor['model_to_source_indices'][index]
            if donor_origin is not None and donor['literal_source'][donor_origin] in C:
                donor_id = 'p159_B'
                assert donor['literal_source'][donor_origin] == after
            else:
                assert label == 'three_witness' and index == 7 and after == 'V'
                donor_id,donor_origin = 'p158_D',7
                assert p158[donor_origin] == after
            substitutions.append(dict(model_index=index,source_index=original,before=before,after=after,
                                      donor_id=donor_id,donor_source_index=donor_origin,donor_observation=after))
        assert len(substitutions) == (5 if label == 'two_witness' else 6)
        plain = decrypt(target,key['column_rank_order'],key['square'])
        assert encrypt(plain,key['column_rank_order'],key['square']) == target
        reconciled.append(dict(id=label,ciphertext=target,raw=plain,fixed_positions=140,
            p168_observed_coordinate_substitutions=substitutions,
            p168_inserted_slot_fills=[dict(model_index=195,glyph='V',donor_id='p159_B',donor_source_index=195)],
            p159_observed_substitution=dict(source_index=169,before='X',after='G',donor_id='p168_C',donor_source_index=170),
            p159_inherited_component_variant='p159B_supported_F' if label=='two_witness' else 'p159B_supported_V',
            changed_plaintext_positions=[dict(index=i,before=a,after=b) for i,(a,b) in enumerate(zip(restored['raw'],plain)) if a!=b],
            full_roundtrip_witness=completed_witnesses(target,key)))
    assert reconciled[1]['ciphertext']==joint
    case = ROOT/data['case']; text=case.read_text()
    assert text.count(expected_legend(case))==1
    f,q=displays(text); assert all(x['role_from_caption'] is not None for x in f+q)
    bodies=re.findall(r'```text\n(.*?)\n```',text,re.S)
    for required in ['\n'.join(record['source_rows']),raw['raw'],restored['raw'],joint_raw]:
        assert required in bodies
    primary=dict(id='p168_C',literal_source=source,ciphertext=cipher,model_to_source_indices=origins,**raw,
                 full_roundtrip_witness=completed_witnesses(cipher,key),
                 parallel_supplied_layer=dict(ciphertext=completed,raw=restored['raw'],fixed_positions=140,
                     supplied_coordinate=dict(model_index=195,source_index=None,glyph='V',donor_id='p159_B',donor_source_index=195),
                     observed_coordinate_substitutions=[],full_roundtrip_witness=completed_witnesses(completed,key)))
    return dict(schema='adfgvx-p168-munich-witness-certificate-v1',authors=data['authors'],input_sha256=sha(HERE/'inputs.json'),
                indexing='Zero based; ranges half open.',summary=dict(physical_sources=1,literal_source_slots=280,
                    observed_source_coordinates=280,frame_slots=280,plaintext_positions=140,excluded_observed_coordinates=1,
                    inserted_unknown_slots=1,raw_observed_substitutions=0,primary_raw_fixed_positions=139,
                    common_unfilled_fixed_positions=136,parallel_supplied_fixed_positions=140,ownership_aliases=12,
                    pair_joint_p168_observed_substitutions=5,three_witness_p168_observed_substitutions=6,
                    joint_p159_additional_observed_substitutions=1),
                records=[primary],source_directed_frame_comparison=candidates,optimal_frame_aliases=aliases,
                common_unfilled_raw=common,matched_controls=controls(key),
                joint_reconciliations=reconciled,
                p159_component_kdo_repair=dict(baseline_variant='p159B_supported_V',prior_raw=donor['prior_raw'],
                    ciphertext=joint,raw=joint_raw,source_substitution=dict(source_index=169,before='X',after='G',
                    donor_source='p168_C',donor_source_index=170,donor_observation='G'),changed_plaintext_index=16,
                    changed_plaintext_letter='H to K',no_other_plaintext_changes=True,
                    full_roundtrip_witness=completed_witnesses(joint,key))),evidence


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--verify',action='store_true');ap.add_argument('--pdf',type=Path);args=ap.parse_args()
    result,evidence=build(args.pdf);target=HERE/'certificates.json'
    if args.verify:assert result==load(target),'Certificate differs; inspect before regeneration'
    else:target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(verified=True,**result['summary'],source_evidence=evidence['summary']),indent=2))

if __name__=='__main__':main()
