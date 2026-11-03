#!/usr/bin/env python3
"""Reproduce the single-glyph p136 source correction and protect the prior edition."""
import argparse,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
C='ADFGVX'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def decode(source,key):
    rank=key['column_rank_order'];w=len(rank);n=len(source)
    height=[n//w+(i<n%w)for i in range(w)]
    columns={};offset=0
    for r in range(1,w+1):
        col=rank.index(r);columns[col]=source[offset:offset+height[col]];offset+=height[col]
    mid=''.join(columns[col][row]for row in range(max(height))for col in range(w)if row<height[col])
    return ''.join(key['square'][6*C.index(a)+C.index(b)]if a in C and b in C else'?'for a,b in zip(mid[::2],mid[1::2]))
def encode(plain,key):
    ranks=key['column_rank_order'];square=key['square'];mid=''.join(C[square.index(x)//6]+C[square.index(x)%6]for x in plain)
    return ''.join(mid[ranks.index(rank)::len(ranks)]for rank in range(1,len(ranks)+1))
def build(pdf=None):
    data=read(HERE/'inputs.json')
    for p in data['prior_artifacts']:assert sha(HERE/p['snapshot'])==p['sha256']
    before=read(HERE/'before/inputs.json');after=read(ROOT/data['original_inputs'])
    bc=read(HERE/'before/certificates.json');ac=read(ROOT/data['original_certificates'])
    assert before['keys']==after['keys']
    assert bc['summary']==ac['summary']
    old,new=before['records'][0],after['records'][0]
    assert old['id']==new['id']==data['record']
    assert before['records'][1]==after['records'][1]
    assert bc['records'][1]==ac['records'][1]
    a=''.join(''.join(old['source_rows']).split());b=''.join(''.join(new['source_rows']).split())
    changes=[(i,x,y)for i,(x,y)in enumerate(zip(a,b))if x!=y]
    assert len(a)==len(b)==244 and changes==[(144,'X','F')]
    assert a[140:145]=='XAFFX'and b[140:145]=='XAFFF'
    key=next(x for x in after['keys']if x['id']==new['key_id'])
    published=next(x for x in read(ROOT/'data/keys.json')['keys']if x['id']==key['id']);assert key==published
    aplain,bplain=decode(a,key),decode(b,key)
    assert aplain==old['expected_raw']==bc['records'][0]['raw']
    assert bplain==new['expected_raw']==ac['records'][0]['raw']
    assert [(i,x,y)for i,(x,y)in enumerate(zip(aplain,bplain))if x!=y]==[(2,'P','D')]
    assert aplain.count('?')==bplain.count('?')==1
    proposed_before=encode(old['readable_candidate'],key);proposed_after=encode(new['readable_candidate'],key)
    assert [(i,x,y)for i,(x,y)in enumerate(zip(proposed_before,proposed_after))if x!=y]==changes
    for old_r,new_r in zip(bc['records'],ac['records']):
        for kind in ['known_coordinate_substitutions','erased_coordinate_fills']:
            assert old_r['readable_candidate'][kind]==new_r['readable_candidate'][kind]
    text=(ROOT/data['case_path']).read_text()
    assert new['expected_raw']in text and new['readable_candidate']in text
    assert '> '+new['readable_german']in text
    fold=lambda x:re.sub('[^A-Z0-9?]','',x.upper()).replace('X','')
    assert fold(new['readable_german'])==fold(new['readable_candidate'])
    assert (ROOT/data['source_crop_path']).exists()and sha(ROOT/data['source_crop_path'])==data['source_crop_sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf)==after['source']['pdf_sha256']and pdf.stat().st_size==after['source']['pdf_bytes']
        imeta=after['source_images'][0];pix=fitz.open(pdf)[imeta['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(imeta['render_scale'],imeta['render_scale']),clip=fitz.Rect(*imeta['crop_pdf_points']))
        im=Image.open(ROOT/data['source_crop_path']).convert('RGB');assert im.size==(pix.width,pix.height)and im.tobytes()==pix.samples
    return {'schema':'adfgvx-one-source-glyph-correction-certificate-v1','authors':data['authors'],'input_sha256':sha(HERE/'inputs.json'),'prior_snapshot_hashes_verified':True,'source_changes':[{'source_index':i,'before':x,'after':y}for i,x,y in changes],'raw_label_changes':[{'plaintext_index':2,'before':'P','after':'D'}],'old_raw':aplain,'corrected_raw':bplain,'old_candidate':old['readable_candidate'],'corrected_candidate':new['readable_candidate'],'unchanged_repair_counts':{'observed_coordinate_substitutions':4,'source_mask_fills':1},'unchanged_companion_record':'p136_A2','physical_sources_added':0,'fixed_raw_positions_added':0,'extra_historical_repair_cost':0,'original_core_files':{p:sha(ROOT/p)for p in ['data/keys.json','data/messages.json']}}
def main():
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args();r=build(a.pdf);f=HERE/'certificates.json'
    if a.verify:assert r==read(f)
    else:f.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,'source_changes':r['source_changes'],'raw_label_changes':r['raw_label_changes'],'physical_sources_added':0,'extra_historical_repair_cost':0},indent=2))
if __name__=='__main__':main()
