#!/usr/bin/env python3
"""Reproduce the bounded language-guided geometry screen for p159 A.

This is exploratory ranking, not authentication. The fixed-target verifier
separately prices the explicitly stated partial reading and retains all ties.
Research and editorial work: icekylinx and GPT-6 Astra Pro.
"""
import argparse
import heapq
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from experiments.romanian_pacification_consultation.verify import permutation
C='ADFGVX'
WORDS='VERPFLEGUNG VERPFLEG REGIERUNG STAERKE TRANSPORT DEUTSCHE VERFUEGUNG BERLIN SOFORT BEREITS ERBITTEN ANTWORT LIEFERUNG VORRAETE REICHT FUENF ZEHN TAGE NOCH UNGARN UNGAR MANN TIERE NACH DURCH WEGEN WIRD WERDEN WURDE WURDEN SOLLEN ERWIRKEN GENACH ARAD DER DIE DAS UND EIN ZUR ZUM VON MIT AUF AUS BEI FUER SICH NICHT IST SIND DEN DEM DES VOR UEBER UNTER ARMEE OKM OHL AOK'.split()
WEIGHTS={w:len(w)**2 for w in WORDS}
PATTERN=re.compile('|'.join(sorted(WORDS,key=len,reverse=True)))
def score(text):return sum(WEIGHTS[m[0]]for m in PATTERN.finditer(text))-text.count('?')
def build():
    d=json.loads((HERE/'inputs.json').read_text());s=''.join(''.join(d['record']['source_rows']).split());key=d['key'];order=permutation(272,key['column_rank_order']);pairs=list(zip(order[::2],order[1::2]));square={C[i//6]+C[i%6]:ch for i,ch in enumerate(key['square'])}
    excluded=set(range(25,30))|set(range(80,85));orig=[(ch,i)for i,ch in enumerate(s)if i not in excluded]
    heap=[];count=0
    for single in range(115,120):
        q=next(i for i,(_,idx)in enumerate(orig)if idx>=single);base=''.join(ch for ch,i in orig[:q])+'?'+''.join(ch for ch,i in orig[q:]);assert len(base)==262
        for a in range(len(base)+1):
            for b in range(a,len(base)+1):
                text=base[:a]+'?'*5+base[a:b]+'?'*5+base[b:]
                raw=''.join(square.get(text[i]+text[j],'?')for i,j in pairs);count+=1
                item=(score(raw),single,a,b,raw)
                if len(heap)<300:heapq.heappush(heap,item)
                elif item>heap[0]:heapq.heapreplace(heap,item)
    rows=[{'score':sc,'single_gap_source_boundary':single,'first_five_gap_stage_boundary':a,'second_five_gap_stage_boundary':b,'raw':raw}for sc,single,a,b,raw in sorted(heap,reverse=True)]
    assert count==173580
    return {'schema':'adfgvx-bounded-exploration-v1','authors':d['authors'],'scope':'Language-guided exploration of the declared source family, using one retained-instance representative of each duplicate pair. It supplies no independent source witness and is not a probability or proof of decipherment. Words were chosen to inspect a provisions/strength lead; this is not a blind held-out evaluation.','evaluations':count,'duplicate_exclusion_starts':[25,80],'one_coordinate_source_boundaries':list(range(115,120)),'word_weights':WEIGHTS,'score_description':'Sum squared word lengths for nonoverlapping regex matches, longer alternatives first, minus one per question-mark position. Keep the300 greatest(score,single,a,b,raw) tuples.','top_results':rows}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');a=p.parse_args();out=build();path=HERE/'exploration.json'
    if a.verify:assert out==json.loads(path.read_text())
    else:path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,'evaluations':out['evaluations'],'top_score':out['top_results'][0]['score'],'retained_rows':len(out['top_results'])}))
if __name__=='__main__':main()
