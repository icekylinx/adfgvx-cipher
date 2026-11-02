"""Test a bounded family of digit-after-A..J square-fill conventions.

This is a compatibility check, not a completion rule. Coordinate labels stay
in the usual ADFGVX order; arbitrary row/column relabelings are not covered.
"""
from pathlib import Path
import hashlib
import json
import argparse

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
PAIRS=dict(zip('ABCDEFGHIJ','0123456789'))


def routes():
    for axis in ['rows','columns']:
        for outer_reverse in [False,True]:
            for inner_reverse in [False,True]:
                for snake in [False,True]:
                    path=[]
                    outer=list(range(6))[::(-1 if outer_reverse else 1)]
                    for step,a in enumerate(outer):
                        reverse=inner_reverse ^ (snake and step%2==1)
                        inner=list(range(6))[::(-1 if reverse else 1)]
                        for b in inner:
                            path.append(6*a+b if axis=='rows' else 6*b+a)
                    yield dict(axis=axis,outer_reverse=outer_reverse,inner_reverse=inner_reverse,
                               snake=snake,path=path)


def check(square,path,cyclic):
    successor={path[i]:path[(i+1)%36] for i in range(36 if cyclic else 35)}
    work=list(square);conflicts=[]
    for letter,digit in PAIRS.items():
        if letter not in square:continue
        cell=square.index(letter);target=successor.get(cell)
        if target is None:
            conflicts.append(dict(letter=letter,cell=cell,reason='No following cell in the linear fill route.'))
        elif work[target] not in ['?',digit]:
            conflicts.append(dict(letter=letter,cell=cell,following_cell=target,
                                  required=digit,known=work[target]))
        elif digit in work and work.index(digit)!=target:
            conflicts.append(dict(letter=letter,cell=cell,reason='Required digit is fixed in another cell.'))
        else:work[target]=digit
    if conflicts:return dict(compatible=False,conflicts=conflicts)
    missing=[letter for letter in PAIRS if letter not in work]
    def place(index):
        if index==len(missing):return True
        letter=missing[index];digit=PAIRS[letter]
        for cell in path:
            target=successor.get(cell)
            if target is None or work[cell]!='?' or work[target]!='?':continue
            if digit in work:continue
            work[cell],work[target]=letter,digit
            if place(index+1):return True
            work[cell]=work[target]='?'
        return False
    compatible=place(0)
    return dict(compatible=compatible,conflicts=[],
                necessary_pair_placement_witness=''.join(work) if compatible else None)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',type=Path,default=REPO/'data/certificates/p153.json')
    parser.add_argument('--keys',type=Path,default=REPO/'data/keys.json')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    certificate=json.loads(args.certificate.read_text())
    source=args.keys;keys=json.loads(source.read_text())['keys']
    reported=next(row for row in keys if row['id']=='TRUPPENVERSCHIEBUNG-2026-reported')['reported_full_square']
    results=[]
    for name,square in [('p153_core_19',certificate['core_partial_square']),('reported_p217_positive_control',reported)]:
        cases=[]
        for route in routes():
            for cyclic in [False,True]:
                cases.append(dict(route={key:value for key,value in route.items() if key!='path'},
                                  cyclic=cyclic,**check(square,route['path'],cyclic)))
        results.append(dict(case=name,examined_routes=16,linear_and_cyclic_variants=32,
                            compatible_variants=sum(row['compatible'] for row in cases),cases=cases))
    control=results[1]['cases'][0]
    assert control['compatible']
    record=dict(convention='Each A..J is immediately followed by its matching digit 0..9 in the fill sequence.',
        results=results,source_keys_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        historical_digits_assigned=0,
        scope='Standard coordinate labels; row/column major, either axis direction, optional serpentine reversal, with or without cyclic wrap. '
              'This does not cover arbitrary label permutations, other digit mappings, other generators, or extra source errors.',
        positive_control_scope='Uses the reported p217 full-square convention only to check implementation; it does not re-establish disputed handwriting assignments.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({row['case']:row['compatible_variants'] for row in results}))


if __name__=='__main__':main()
