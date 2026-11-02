"""Independent finite membership and field-domain review; no shared writes.

Prepared by icekylinx and GPT-6 Astra Pro. Uses only standard-library code,
not the package verifier or project cipher implementation.
"""
from collections import Counter
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--verify',action='store_true')
args=parser.parse_args()
C='ADFGVX'
A='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
report=json.load(open(ROOT/'experiments/contextual_key_constraints/certificate.json'))
parent=json.load(open(ROOT/'experiments/p198_category_frontier/results.json'))
case=next(c for c in json.load(open(ROOT/'experiments/p198_exact_sparse/inputs.json'))['cases']if c['id']=='p198_Nov13-15b')
key=report['p198_conditional_frontier']

def decode(cipher,ranks,square):
    stream=['']*len(cipher)
    source=iter(cipher)
    for col in sorted(range(len(ranks)),key=lambda c:ranks[c]):
        for p in range(col,len(cipher),len(ranks)):
            stream[p]=next(source)
    pairs=[''.join(stream[i:i+2])for i in range(0,len(stream),2)]
    cells=[6*C.index(pair[0])+C.index(pair[1])for pair in pairs]
    return ''.join(square[c]for c in cells),cells

def encode(plaintext,ranks,square):
    stream=''.join(C[square.index(c)//6]+C[square.index(c)%6]for c in plaintext)
    return ''.join(stream[col::len(ranks)]for col in sorted(range(len(ranks)),key=lambda c:ranks[c]))

partial=parent['partial_square']
unknown=[i for i,c in enumerate(partial)if c=='?']
symbols=sorted(set(A)-set(partial))
assert symbols==list('234789QY') and unknown==[1,2,16,17,18,19,27,35]
classes=Counter()
weak_classes=Counter()
all_completions=0
for values in itertools.permutations(symbols):
    square=list(partial)
    for cell,symbol in zip(unknown,values):square[cell]=symbol
    all_completions+=1
    membership=tuple(i for i,c in enumerate(square)if c in 'QY')
    if square[17]in'QY':weak_classes[membership]+=1
    if square[17]=='Y':classes[membership]+=1
assert all_completions==40320 and len(classes)==7 and sum(classes.values())==5040
assert set(classes.values())=={720}
assert len(weak_classes)==7 and set(weak_classes.values())=={1440}
assert sum(weak_classes.values())==10080
assert set(classes)=={tuple(m['QY_cell_indices'])for m in key['membership_results']}
witnesses=0
swapped_members=0
for member in key['membership_results']:
    old=next(m for m in parent['membership_results']if m['QY_cell_indices']==member['QY_cell_indices'])
    swapped=old['representative_square'][17]=='Q'
    swapped_members+=swapped
    for row in member['witnesses']:
        assert row['QY_label_swap_applied']==swapped
        square=row['representative_square']
        assert square[17]=='Y' and set(square)==set(A)
        assert all(c=='?'or c==square[i]for i,c in enumerate(partial))
        losses=row['loss_positions']
        assert losses==sorted(set(losses)) and len(losses)==5
        source=iter(case['observed_ciphertext'])
        fill=iter(row['fill'])
        full=''.join(next(fill)if i in losses else next(source)for i in range(170))
        assert full==row['filled_ciphertext']
        plaintext,cells=decode(full,case['column_rank_order'],square)
        assert plaintext==row['plaintext_witness']
        assert encode(plaintext,case['column_rank_order'],square)==full
        assert sum(c.isdigit()for c in plaintext)==row['digits']
        assert sum(c in'QY'for c in plaintext)==row['Q_or_Y']
        assert ''.join(c for i,c in enumerate(full)if i not in losses)==case['observed_ciphertext']
        witnesses+=1
points={(w['digits'],w['Q_or_Y'])for m in key['membership_results']for w in m['witnesses']}
frontier=sorted(p for p in points if not any(q!=p and q[0]<=p[0]and q[1]<=p[1]for q in points))
assert frontier==[(4,6),(5,5),(6,4),(7,3),(8,2),(10,1),(13,0)]

keys={k['id']:k for k in json.load(open(ROOT/'data/keys.json'))['keys']}
old_square=keys['Nov13-15a']['square']
assert old_square[9]=='?'and'Y'not in old_square
new_square=old_square[:9]+'Y'+old_square[10:]
field_reports=[]
for entry in report['reviewed_frame_inventory']['effects']:
    if entry['id']!='p187_D'or'editorial'not in entry['variant']:continue
    raw,cells=decode(entry['ciphertext'],keys['Nov13-15a']['column_rank_order'],new_square)
    positions=[i for i,c in enumerate(raw)if c=='?']
    fields=sorted({cells[i]for i in positions})
    available=sorted(set(A)-set(new_square))
    assert len(positions)==12 and len(fields)==5 and 9 not in fields
    assert ''.join(available)=='0123456789Q'
    templates=set()
    for assigned in itertools.permutations(available,5):
        square=list(new_square)
        for cell,symbol in zip(fields,assigned):square[cell]=symbol
        rest_cells=[i for i,c in enumerate(square)if c=='?']
        rest_symbols=sorted(set(A)-set(square))
        assert len(rest_cells)==len(rest_symbols)==6
        for cell,symbol in zip(rest_cells,rest_symbols):square[cell]=symbol
        assert len(set(square))==36
        assert all(c=='?'or c==square[i]for i,c in enumerate(new_square))
        templates.add(''.join(square[cells[i]]for i in positions))
    assert len(templates)==55440==math.perm(11,5)
    assert 55440*math.factorial(6)==math.factorial(11)
    field_reports.append({'variant':entry['variant'],'positions':positions,'cells':fields,
        'cell_occurrences':{str(cell):count for cell,count in Counter(cells[i]for i in positions).items()},
        'assignments_before':math.perm(12,5),'assignments_after':len(templates),
        'complete_extension_witness_checked_for_each_assignment':True})
assert len(field_reports)==2
result={'prepared_by':['icekylinx','GPT-6 Astra Pro'],'status':'No substantive mathematical issue found',
    'all_square_completions_enumerated':all_completions,'FX_Y_completions':sum(classes.values()),
    'FX_Q_or_Y_completions':sum(weak_classes.values()),'retained_memberships':len(classes),
    'QY_swapped_memberships':swapped_members,'converted_witnesses_checked':witnesses,
    'conditional_frontier':[list(p)for p in frontier],'p187_D_fields':field_reports,
    'scope':'Audits the finite restriction and witness/domain arithmetic. It does not independently authenticate the historical name assumptions or rerun the parent 28 exact frontier calculations.'}
result['dependency_sha256']={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [HERE/'certificate.json', ROOT/'experiments/p198_category_frontier/results.json', ROOT/'experiments/p198_exact_sparse/inputs.json', ROOT/'data/keys.json']}
output=HERE/'independent_review.json'
if args.verify:
    assert result==json.loads(output.read_text())
else:
    output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verified':True,'square_completions_enumerated':all_completions,'converted_witnesses':witnesses,'field_assignments_per_alias':55440},indent=2))
