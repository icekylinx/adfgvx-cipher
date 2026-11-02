"""Exact insertion-only alignment audit of Baertl's earlier p215 completion.

Every received source position is retained; '?' is an observed erasure slot.
Target gaps may occur anywhere. Count only contradictions at known coordinates.
"""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parent
REPOSITORY=ROOT.parent.parent
sys.path.insert(0,str(REPOSITORY))
from adfgvx.cipher import encrypt


def minimum_substitutions(source,target):
    """Return minimum known-coordinate substitutions and exact injection count."""
    n,m=len(source),len(target)
    if n>m:raise ValueError('The target is shorter than the preserved source')
    infinity=n+1
    previous=[0]*(m+1);previous_count=[1]*(m+1)
    for i,a in enumerate(source,1):
        row=[infinity]*(m+1);count=[0]*(m+1)
        for j in range(i,m+1):
            pair=previous[j-1]+int(a!='?' and a!=target[j-1])
            skip=row[j-1];best=min(pair,skip)
            row[j]=best
            count[j]=(previous_count[j-1] if pair==best else 0)+(count[j-1] if skip==best else 0)
        previous,previous_count=row,count
    return previous[m],previous_count[m]


def controls():
    cases=[('A?D','AXDDV'),('AAA','AAAAA'),('?D','AADV'),('AD','VF'),('','ADX')]
    for source,target in cases:
        costs=[sum(a!='?' and a!=target[j] for a,j in zip(source,indices))
               for indices in combinations(range(len(target)),len(source))]
        expected=(min(costs),costs.count(min(costs)))
        assert minimum_substitutions(source,target)==expected
    return len(cases)


def compute():
    path=REPOSITORY/'data/prior_readings.json'
    records=json.loads(path.read_text())['messages']
    record=next(r for r in records if r['id']=='p215')
    published=next(r for r in record['published_readings'] if r['id']=='baertl_comment39')
    text=published['compact_plaintext'];source=record['analysis_ciphertext'];key=record['key']
    rows=[]
    for removed in [None]+list(range(len(text))):
        candidate=text if removed is None else text[:removed]+text[removed+1:]
        target=encrypt(candidate,key['column_rank_order'],key['square'])
        cost,count=minimum_substitutions(source,target)
        rows.append({'removed_plaintext_index':removed,'plaintext_length':len(candidate),
                     'required_insertions':len(target)-len(source),
                     'minimum_known_coordinate_substitutions':cost,
                     'optimal_source_preserving_injections':count})
    return {'schema':'p215-editorial-arbitrary-insertion-audit-v1',
            'attribution':published['source'],'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
            'editorial_plaintext_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'scope':'Fixed attested key; unchanged order of every received source position; arbitrary inserted coordinates, plus counted substitutions. No received-coordinate deletions or rearrangements. All 130 one-letter deletions of the editorial plaintext are compared as a generous additional test.',
            'full_editorial_result':rows[0],
            'best_one_letter_deletion_substitutions':min(r['minimum_known_coordinate_substitutions'] for r in rows[1:]),
            'records':rows,'independent_exhaustive_small_controls':controls(),
            'accepted_new_historical_letters':0}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    args=p.parse_args();result=compute()
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    else:assert result==json.loads((ROOT/'editorial_alignment.json').read_text())
    best=[r for r in result['records'][1:] if r['minimum_known_coordinate_substitutions']==27]
    assert len(best)==1 and best[0]['removed_plaintext_index']==8
    assert best[0]['optimal_source_preserving_injections']==6355
    assert result['full_editorial_result']['minimum_known_coordinate_substitutions']==166
    print(json.dumps({'passed':True,'full_130_letter_text_minimum_substitutions':166,
                      'best_one_letter_deletion_minimum_substitutions':27,
                      'best_deletion_original_plaintext_index':8,'optimal_injections':6355,
                      'new_historical_letters':0}))


if __name__=='__main__':main()
