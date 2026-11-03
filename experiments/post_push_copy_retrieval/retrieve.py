#!/usr/bin/env python3
"""Frozen literal-coordinate anchor retrieval; no plaintext or key search.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
CO = set('ADFGVX')


def anchors(text, width):
    return [(i, text[i:i+width]) for i in range(len(text)-width+1)
            if set(text[i:i+width]) <= CO]


def covered(starts, width):
    return sorted({p for start in starts for p in range(start, start+width)})


def alignment_at(a, b, offset):
    same, different, unknown, longest, run = [], [], [], 0, 0
    for i in range(max(0, -offset), min(len(a), len(b)-offset)):
        j = i+offset
        if '?' in (a[i], b[j]):
            unknown.append([i,j]);run=0
        elif a[i] == b[j]:
            same.append([i,j]);run+=1;longest=max(longest,run)
        else:
            different.append([i,j]);run=0
    return {'target_minus_reference_offset':offset,'equal_coordinates':len(same),
            'conflicting_coordinates':len(different),'unknown_pairs':len(unknown),
            'longest_exact_run_at_offset':longest,
            'reference_overlap':[max(0,-offset),min(len(a),len(b)-offset)],
            'conflicts':different}


def search(references, targets, method):
    width = method['anchor_length']
    index = defaultdict(list)
    for j, target in enumerate(targets):
        for position, gram in anchors(target['search_string'], width):
            index[gram].append((j,position))
    rows=[];anchored_pairs=0;raw_anchor_matches=0
    for reference in references:
        hits=defaultdict(list)
        for i,gram in anchors(reference['search_string'],width):
            for j,k in index.get(gram,()):
                hits[j].append((i,k));raw_anchor_matches+=1
        anchored_pairs+=len(hits)
        for j,pairs in hits.items():
            target=targets[j]
            rc=covered((a for a,b in pairs),width)
            tc=covered((b for a,b in pairs),width)
            if len(rc)<method['minimum_covered_reference_positions'] or len(tc)<method['minimum_covered_target_positions']:
                continue
            offsets=Counter(b-a for a,b in pairs)
            best_offset=min(offsets,key=lambda off:(-offsets[off],abs(off),off))
            a,b=reference['search_string'],target['search_string']
            rows.append({'reference_id':reference['id'],'reference_page':reference['printed_page'],
                         'target_id':target['id'],'target_page':target['printed_page'],
                         'same_page':reference['printed_page']==target['printed_page'],
                         'reference_length':len(a),'target_length':len(b),
                         'reference_covered_positions':rc,'target_covered_positions':tc,
                         'reference_coverage':len(rc)/len(a),'target_coverage':len(tc)/len(b),
                         'anchor_matches':len(pairs),
                         'anchor_offsets':[[off,n]for off,n in sorted(offsets.items())],
                         'leading_offset_alignment':alignment_at(a,b,best_offset),
                         'all_anchor_pairs':[list(p)for p in sorted(pairs)]})
    rows.sort(key=lambda r:(-min(r['reference_coverage'],r['target_coverage']),
                            -len(r['reference_covered_positions'])-len(r['target_covered_positions']),
                            r['reference_id'],r['target_id']))
    return {'eligible_reference_target_pairs':len(references)*len(targets),
            'pairs_with_at_least_one_exact_anchor':anchored_pairs,
            'raw_anchor_position_matches':raw_anchor_matches,
            'retained_pairs':len(rows),'cross_page_pairs':sum(not r['same_page'] for r in rows),
            'same_page_pairs':sum(r['same_page']for r in rows),'rows':rows}


def build():
    raw=(HERE/'inputs.json').read_bytes();data=json.loads(raw)
    references,targets=data['references'],data['targets']
    assert len(references)==113 and len(targets)==788
    assert len({r['id']for r in references})==len(references)
    assert len({r['id']for r in targets})==len(targets)
    for r in references:
        assert hashlib.sha256(r['literal_source'].encode()).hexdigest()==r['literal_sha256']
        assert ''.join(c if c in CO else '?'for c in r['literal_source'])==r['search_string']
    for t in targets:assert set(t['search_string'])<=CO|{'?'}
    result=search(references,targets,data['method'])
    checks=[]
    for check in data['known_cross_page_checks']:
        matches=[r for r in result['rows'] if r['reference_id']==check['reference_id'] and r['target_page']==check['target_printed_page']]
        assert matches,check
        checks.append({**check,'retrieved_target_ids':[r['target_id']for r in matches]})
    rng=random.Random(data['composition_control']['seed']);controls=[]
    for t in targets:
        chars=list(t['search_string']);rng.shuffle(chars)
        text=''.join(chars);assert Counter(text)==Counter(t['search_string'])
        controls.append({**t,'search_string':text})
    control=search(references,controls,data['method'])
    return {'schema':'adfgvx-post-push-copy-retrieval-result-v1','authors':data['authors'],
            'inputs_sha256':hashlib.sha256(raw).hexdigest(),'method':data['method'],
            'real_corpus':result,'known_cross_page_checks':checks,'composition_control':control,
            'accepted_new_readings':[],
            'limit':'All hits remain retrieval candidates until manual source review and separate source/cipher certificates. The four known relationships are calibration checks, not fresh discoveries.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');a=parser.parse_args()
    result=build();path=HERE/'results.json'
    if a.verify:assert json.loads(path.read_text())==result
    else:path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    brief={k:v for k,v in result['real_corpus'].items() if k!='rows'}
    print(json.dumps({'verified':a.verify,**brief,'composition_control_retained_pairs':result['composition_control']['retained_pairs']},indent=2))


if __name__=='__main__':main()
