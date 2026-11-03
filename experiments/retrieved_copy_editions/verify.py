#!/usr/bin/env python3
"""Independently price the three source-reviewed cross-page copy editions.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from adfgvx.cipher import decrypt,encrypt,plaintext_domains,untranspose
CO='ADFGVX';ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def order(n,ranks):
    w=len(ranks);heights=[n//w+(i<n%w)for i in range(w)]
    starts=[sum(heights[j]for j in range(w)if ranks[j]<ranks[i])for i in range(w)]
    result=[starts[i%w]+i//w for i in range(n)]
    assert sorted(result)==list(range(n));return result


def inspect(cipher,key):
    indices=order(len(cipher),key['column_rank_order'])
    middle=''.join(cipher[i]for i in indices)
    assert middle==untranspose(cipher,key['column_rank_order'])
    square=key['square'];unused=set(ALPHABET)-set(square);positions=[]
    for i in range(len(cipher)//2):
        pair=middle[2*i:2*i+2];domain=set()
        for r in range(6):
            for c in range(6):
                if pair[0]in('?',CO[r])and pair[1]in('?',CO[c]):
                    v=square[6*r+c];domain.update(unused if v=='?'else v)
        domain=''.join(sorted(domain))
        positions.append({'plaintext_position':i,'pair':pair,'coordinate_indices':indices[2*i:2*i+2],
                          'domain':domain,'raw':domain if len(domain)==1 else'?'})
    raw=''.join(p['raw']for p in positions)
    assert raw==decrypt(cipher,key['column_rank_order'],square)
    assert [p['domain']for p in positions]==plaintext_domains(cipher,key['column_rank_order'],square)
    values=iter(sorted(unused));witness_square=''.join(next(values)if c=='?'else c for c in square)
    witness_cipher=cipher.replace('?','A');witness_text=decrypt(witness_cipher,key['column_rank_order'],witness_square)
    assert encrypt(witness_text,key['column_rank_order'],witness_square)==witness_cipher
    return {'raw':raw,'positions':positions,'fixed_positions':len(raw)-raw.count('?'),
            'arbitrary_full_roundtrip_witness':{'square':witness_square,'ciphertext':witness_cipher,
                                               'plaintext':witness_text,'historical_claim':False}}


def edition(cipher,template,key):
    assert '?'not in template
    target=encrypt(template,key['column_rank_order'],key['square'])
    assert len(target)==len(cipher)
    changes=[{'source_index':i,'from':a,'to':b}for i,(a,b)in enumerate(zip(cipher,target))if a!=b]
    assert all(e['from']in CO for e in changes)
    rebuilt=list(cipher)
    for e in changes:rebuilt[e['source_index']]=e['to']
    assert ''.join(rebuilt)==target
    result=inspect(target,key);assert result['raw']==template
    return {'ciphertext':target,'known_coordinate_substitutions':changes,**result}


def build(pdf=None):
    inp=json.loads((HERE/'inputs.json').read_text())
    for rel,digest in inp['dependencies'].items():assert sha(ROOT/rel)==digest
    assert sha(ROOT/'experiments/post_push_copy_retrieval/inputs.json')==inp['retrieval']['inputs_sha256']
    published={k['id']:k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']}
    for id,key in inp['keys'].items():assert all(published[id][f]==v for f,v in key.items())
    for image in inp['source_images']:assert sha(HERE/image['path'])==image['sha256']
    if pdf:
        import fitz
        from PIL import Image
        assert sha(pdf)==inp['source']['pdf_sha256'];doc=fitz.open(pdf)
        for item in inp['source_images']:
            if item.get('fresh_render_cache'):fitz.TOOLS.store_shrink(100)
            pix=doc[item['pdf_page_1based']-1].get_pixmap(matrix=fitz.Matrix(item['render_scale'],item['render_scale']),clip=fitz.Rect(*item['crop_pdf_points']))
            im=Image.open(HERE/item['path']).convert('RGB')
            assert im.size==(pix.width,pix.height)and im.tobytes()==pix.samples
    records=[]
    for r in inp['records']:
        source=''.join(''.join(r['source_rows']).split());assert set(source)<=set(CO)
        assert len(source)==r['advertised_length'];key=inp['keys'][r['key_id']]
        raw=inspect(source,key);assert raw['raw']==r['expected_raw']
        ed=edition(source,r['editorial_plaintext'],key)
        records.append({'id':r['id'],'literal_source':source,'source_slots':len(source),'raw':raw,'edition':ed,
                        'key_changed':False,'source_deletions':0,'source_insertions':0})
    by_id={r['id']:r for r in records};contexts={r['id']:r for r in inp['contextual_existing_records']}
    old4=contexts['p125_A4']['literal_source'];new4=by_id['p137_B4']['literal_source']
    differences4=[{'source_index':i,'earlier':a,'new_witness':b}for i,(a,b)in enumerate(zip(old4,new4))if a!=b]
    assert differences4==[{'source_index':30,'earlier':'2','new_witness':'X'}]
    assert not by_id['p137_B4']['edition']['known_coordinate_substitutions']
    oldc=contexts['p126_B']['literal_source'];newc=by_id['p137_C']['literal_source']
    assert oldc==newc and len(newc)==134
    assert by_id['p137_C']['edition']['known_coordinate_substitutions']==[
        {'source_index':27,'from':'G','to':'F'},{'source_index':56,'from':'G','to':'F'}]
    prior=contexts['p174_A3'];old=prior['literal_source'];new=by_id['p195_A2']['literal_source']
    assert len(old)==79 and len(new)==98 and prior['advertised_length']==98
    prefix_differences=[{'source_index':i,'earlier':a,'full_witness':new[i]}for i,a in enumerate(old)if a!=new[i]]
    assert prefix_differences==[{'source_index':65,'earlier':'A','full_witness':'X'}]
    bank_key=inp['keys']['Nov10-12'];raw_prefix=inspect(old+'?'*19,bank_key)
    copied=old+new[79:];copied_layer=inspect(copied,bank_key)
    final=by_id['p195_A2']['edition'];assert final['known_coordinate_substitutions']==[{'source_index':95,'from':'X','to':'D'}]
    cell=by_id['p195_A2']['raw']['positions'][27];assert cell['domain']=='56789'and'S'not in cell['domain']
    old_certificate=json.loads((ROOT/'experiments/crown_airlift/certificates.json').read_text())
    old_record=next(r for r in old_certificate['records']if r['id']=='p174_A3')
    assert old_record['raw']==raw_prefix['raw']
    old_fills=old_record['readable_candidate']['erased_coordinate_fills']
    fill_support=[]
    for e in old_fills:
        i=e['model_index']
        fill_support.append({'model_index':i,'earlier_conjectural_fill':e['to'],'full_source_value':new[i],
                             'agrees':e['to']==new[i]})
    assert len(fill_support)==12 and sum(x['agrees']for x in fill_support)==11
    gap_costs=[]
    for g in range(80):
        f=old[:g]+'?'*19+old[g:]
        gap_costs.append({'gap_before_source_index':g,'observed_disagreements_against_literal_witness':sum(a!='?'and a!=b for a,b in zip(f,new))})
    minimum=min(r['observed_disagreements_against_literal_witness']for r in gap_costs)
    minimizers=[r['gap_before_source_index']for r in gap_costs if r['observed_disagreements_against_literal_witness']==minimum]
    supported_coordinates=[{'coordinate_index':i,'value':new[i],'full_witness_source_index':i}for i in range(79,98)]
    summary={'physical_records':3,'earlier_records_not_counted':3,'printed_source_slots':444,
             'valid_source_coordinates':444,'modeled_coordinates':444,'plaintext_positions':222,
             'baseline_fixed_positions':sum(r['raw']['fixed_positions']for r in records),
             'candidate_fixed_positions':sum(r['edition']['fixed_positions']for r in records),
             'known_coordinate_substitutions':sum(len(r['edition']['known_coordinate_substitutions'])for r in records),
             'new_source_mask_fills':0,'new_source_length_changes':0,'previously_missing_banknote_coordinates_witnessed':19,
             'earlier_banknote_fill_choices_corroborated':11,'earlier_banknote_fill_choices_contradicted':1,
             'baseline_keys_changed':False}
    assert summary['baseline_fixed_positions']==221 and summary['candidate_fixed_positions']==222
    assert summary['known_coordinate_substitutions']==3
    return {'schema':'adfgvx-retrieved-copy-source-certificate-v1','authors':inp['authors'],
            'inputs_sha256':sha(HERE/'inputs.json'),'summary':summary,'records':records,
            'armistice_clause_witness':{'earlier_record':'p125_A4','new_record':'p137_B4','differences':differences4,
                                      'supports_earlier_mask_fill':True,'earlier_paper_glyph_preserved':True},
            'receipt_witness':{'earlier_record':'p126_B','new_record':'p137_C','all134_coordinates_identical':True,
                               'both_word_repairs_shared_and_not_independently_confirmed':True},
            'banknote_witness':{'earlier_record':'p174_A3','new_record':'p195_A2','prefix_observed_coordinates':79,
                               'prefix_equal_coordinates':78,'prefix_differences':prefix_differences,
                               'previous_missing_tail':new[79:],'tail_coordinate_origins':supported_coordinates,
                               'earlier_mask_only_reading':raw_prefix,'literal_copy_with_original_prefix':copied_layer,
                               'earlier_fill_support':fill_support,'complete_one_gap_costs':gap_costs,
                               'minimum_observed_disagreements':minimum,'all_minimizing_gaps':minimizers,
                               'word_repair_uses_observed_source_change_not_new_square_letter':cell,
                               'header_and_part_number_conflicts_retained':True}}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--pdf',type=Path);a=p.parse_args()
    result=build(a.pdf);target=HERE/'certificates.json'
    if a.verify:assert json.loads(target.read_text())==result
    else:target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'verified':a.verify,'source_pixels_checked':a.pdf is not None,**result['summary']},indent=2))


if __name__=='__main__':main()
