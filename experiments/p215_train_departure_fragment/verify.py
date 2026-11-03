#!/usr/bin/env python3
"""Verify the conditional p215B1 train-departure fragment and both source glyphs.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt
from adfgvx.source_evidence import verify_source_evidence
from data.reviews.check_reading_presentation import displays,expected_legend
C='ADFGVX'

def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def order(n,ranks):
    rows=[list(range(start,min(n,start+len(ranks))))for start in range(0,n,len(ranks))]
    return [row[c]for c in sorted(range(len(ranks)),key=lambda c:ranks[c])for row in rows if c<len(row)]
def analyze(cipher,key,mapping):
    emitted=order(len(cipher),key['column_rank_order']);inverse=[None]*len(cipher)
    for i,p in enumerate(emitted):inverse[p]=i
    positions=[]
    for p in range(len(cipher)//2):
        indices=inverse[2*p:2*p+2];pair=''.join(cipher[i]for i in indices);domain=set()
        for a in C if pair[0]=='?'else pair[:1]:
            for b in C if pair[1]=='?'else pair[1:]:domain.add(key['square'][C.index(a)*6+C.index(b)])
        domain=''.join(sorted(domain));positions.append({'plaintext_index':p,'model_indices':indices,'source_indices':[mapping[i]for i in indices],'pair':pair,'domain':domain,'raw':domain if len(domain)==1 else'?'})
    raw=''.join(p['raw']for p in positions)
    assert decrypt(cipher,key['column_rank_order'],key['square'])==raw
    return {'raw':raw,'fixed_positions':len(raw)-raw.count('?'),'positions':positions}
def stencil(template,key):
    mid=''.join('??'if c=='?'else C[key['square'].index(c)//6]+C[key['square'].index(c)%6]for c in template)
    return ''.join(mid[p]for p in order(len(mid),key['column_rank_order']))
def layer(template,base,mapping,literal,key):
    wanted=stencil(template,key);corrected=''.join(b if b in C else a for a,b in zip(base,wanted));edits=[];printed=[];added=[]
    for i,(a,b)in enumerate(zip(base,corrected)):
        if a==b:continue
        ev={'model_index':i,'source_index':mapping[i],'printed':literal[mapping[i]]if mapping[i]is not None else None,'from':a,'to':b}
        (edits if a in C else added if mapping[i]is None else printed).append(ev)
    assert not edits
    actual=analyze(corrected,key,mapping);assert actual['raw']==template
    complete=corrected.replace('?','A');plain=decrypt(complete,key['column_rank_order'],key['square']);assert encrypt(plain,key['column_rank_order'],key['square'])==complete
    assert all(a=='?'or a==b for a,b in zip(template,plain))
    return {'template':template,'ciphertext':corrected,**actual,'known_coordinate_substitutions':edits,'printed_mask_fills':printed,'added_slot_fills':added,'full_global_witness':{'square':key['square'],'ciphertext':complete,'plaintext':plain,'roundtrip_verified':True,'historical_value_claim':False}}
def folded(s):return re.sub('[^A-Z0-9?]','',s.upper()).replace('X','')
def build(pdf=None):
    d=load(HERE/'inputs.json');k=d['key'];assert k==next(r for r in load(ROOT/'data/keys.json')['keys']if r['id']=='Nov22-24');assert len(k['square'])==len(set(k['square']))==36
    for path,digest in d['prior_artifacts'].items():assert sha((ROOT if path.startswith('experiments/')else HERE)/path)==digest
    prior=load(HERE/'prior_ocr.json');assert prior==next(r for r in load(ROOT/'experiments/p153_corpus/inputs.json')['blocks']if r['id']=='p215_ocr_block2')
    evidence=verify_source_evidence(pdf,d['source'],d['source_images'],HERE)
    r=d['records'][0];literal=''.join(''.join(r['source_rows']).split());assert len(literal)==145 and sum(c in C for c in literal)==140 and literal.count('-')==5
    assert literal[40:45]=='XVXVG';mapping=list(range(10))+[None]*75+list(range(10,145));assert len(mapping)==220 and sorted(i for i in mapping if i is not None)==list(range(145))
    variants=[]
    for glyph in ['X','A']:
        src=literal[:42]+glyph+literal[43:];base=''.join(src[i]if i is not None and src[i]in C else'?'for i in mapping);raw=analyze(base,k,mapping);assert raw['raw']==r['expected_raw']and raw['fixed_positions']==37
        template=list(raw['raw'])
        for span in r['proposed_spans']:
            for j,c in enumerate(span['text']):
                at=span['start']+j
                if c!='?':assert c in raw['positions'][at]['domain'];template[at]=c
        template=''.join(template);assert template==r['primary_partial_template']
        edited=layer(template,base,mapping,src,k);assert (edited['fixed_positions'],len(edited['printed_mask_fills']),len(edited['added_slot_fills']))==(77,3,39)
        assert template.count('?')==33 and template[70:79]=='ALPEN????'and template[98]=='?'
        variants.append({'source_glyph_at42':glyph,'literal_source':src,'ciphertext':base,'model_to_source_indices':mapping,**raw,'primary_lexical_completion':edited})
    changed=[i for i,(a,b)in enumerate(zip(variants[0]['positions'],variants[1]['positions']))if a['domain']!=b['domain']];assert changed==[77]
    diagnostics=[];diag=d['nearby_length_diagnostic']
    for n in diag['model_lengths']:
        assert n>=145 and n%2==0
        for glyph in ['X','A']:
            src=literal[:42]+glyph+literal[43:];base=(src[:10]+'?'*(n-145)+src[10:]).replace('-','?');template=diag['retrospective_prefix']+'?'*(n//2-len(diag['retrospective_prefix']));wanted=stencil(template,k);cost=sum(a in C and b in C and a!=b for a,b in zip(base,wanted));diagnostics.append({'model_slots':n,'added_unknown_slots':n-145,'source_glyph_at42':glyph,'proposed_prefix_known_coordinate_substitutions':cost})
    text=(ROOT/d['case']).read_text();assert text.count(expected_legend(ROOT/d['case']))==1;fences,quotes=displays(text);assert [f['role_from_caption']for f in fences]==['raw_output','edited_output','source_transcription'];assert [q['role_from_caption']for q in quotes]==['readable_german'];bodies=re.findall(r'```text\n(.*?)\n```',text,re.S);assert bodies[0]==r['expected_raw']and bodies[1]==r['primary_partial_template']and''.join(bodies[2].split())==literal;visible=re.findall(r'^> (.*)$',text,re.M);assert visible==[r['readable_german']]and folded(visible[0])==folded(r['primary_partial_template'])
    summary={'physical_records':1,'printed_source_slots':145,'valid_source_coordinates_per_glyph_variant':140,'printed_mask_slots':5,'added_unknown_slots':75,'modeled_coordinates':220,'plaintext_positions':110,'fixed_raw_positions':37,'primary_fixed_positions':77,'primary_unknown_positions':33,'observed_substitutions':0,'printed_mask_fills':3,'added_slot_fills':39,'source_glyph_variants':2}
    return {'schema':'adfgvx-p215-train-departure-fragment-certificate-v1','authors':d['authors'],'input_sha256':sha(HERE/'inputs.json'),'indexing':d['indexing'],'summary':summary,'records':[{'id':'p215_B1','literal_source':literal,'source_slots':145,'ciphertext':variants[0]['ciphertext'],'model_to_source_indices':mapping,'raw':variants[0]['raw'],'fixed_positions':37,'positions':variants[0]['positions'],'primary_lexical_completion':variants[0]['primary_lexical_completion']}],'source_glyph_variants':variants,'nearby_length_prefix_prices':diagnostics,'diagnostic_limit':diag['limit'],'prior_credit':d['prior_credit'],'limits':d['limits']},evidence
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();c,e=build(a.pdf);out=HERE/'certificates.json'
    if a.verify:assert c==load(out)
    else:out.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'verified':a.verify,**c['summary'],'source_evidence':e['summary']},indent=2))
