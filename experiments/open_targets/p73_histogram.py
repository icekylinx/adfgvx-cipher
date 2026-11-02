#!/usr/bin/env python3
"""Calibrate the p73 coordinate-count invariant against held-out war prose.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
The references were not used in any repository quadgram/sixgram model. This
empirical distance comparison supplies search priority, never a key exclusion
or a normal-theory significance claim. NumPy is required.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,itertools,json,math,re,urllib.request
import numpy as np
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';COORDS='ADFGVX'


def source_text(source,cache,download):
    path=cache/f'pg{source["id"]}.txt'
    if not path.exists():
        if not download:raise FileNotFoundError(f'{path}: supply the pinned source or use --download')
        cache.mkdir(parents=True,exist_ok=True);path.write_bytes(urllib.request.urlopen(source['url'],timeout=60).read())
    raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==source['sha256']
    text=raw.decode('utf-8-sig','replace')
    language=re.search(r'^Language:\s*(.+)$',text,re.M);assert language and language.group(1).strip()=='German'
    start=re.search(r'\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*',text,re.S)
    end=re.search(r'\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK',text)
    assert start and end
    return text[start.end():end.start()]


def normalized_streams(text):
    for original,expanded in [('ä','ae'),('ö','oe'),('ü','ue'),('Ä','AE'),('Ö','OE'),('Ü','UE'),('ß','ss')]:text=text.replace(original,expanded)
    text=text.upper();plain=re.sub('[^A-Z0-9]','',text)
    sentence=re.sub(r'[.!?;:\n]+','X',text)
    sentence=re.sub('XX+','X',re.sub('[^A-Z0-9]','',sentence))
    words='X'.join(re.findall('[A-Z0-9]+',text))
    return [('plain',plain),('sentence_x',sentence),('word_x',words)]


def run(cache,download):
    sources=json.loads((HERE/'heldout_sources.json').read_text())['sources']
    training=json.loads((ROOT/'experiments/joint_search/models/provenance.json').read_text())['sources']
    assert not {r['id']for r in sources}&{r['id']for r in training}
    key=next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']if k['id']=='Nov7-9')
    partial=key['square'];unused=sorted(set(ALPHABET)-set(partial));assert unused==['5','6']
    target=next(m for m in json.loads((ROOT/'data/messages.json').read_text())['messages']if m['id']=='p73')
    companion=json.loads((ROOT/'data/certificates/p155.json').read_text())['sections'][0]
    inputs=[dict(id='p73',role='open target',literal=target['transcript']['raw_source_compact']),dict(id='p155_A1',role='independent readable historical control under Nov7-9',literal=companion['raw_literal'])]
    for row in inputs:
        ct=row['literal'];row['plaintext_length']=len(ct)//2;assert len(ct)%2==0
        row['known_coordinate_counts']=[ct.count(ch)for ch in COORDS]
        row['unknown_slots']=len(ct)-sum(row['known_coordinate_counts'])
    results=[];stream_metadata=[]
    for source in sources:
        text=source_text(source,cache,download)
        for convention,stream in normalized_streams(text):
            stream_metadata.append(dict(book_id=source['id'],convention=convention,normalized_characters=len(stream),normalized_sha256=hashlib.sha256(stream.encode()).hexdigest()))
            codes=np.fromiter((ALPHABET.index(ch)for ch in stream),dtype=np.int16)
            for item in inputs:
                length=item['plaintext_length'];count=len(stream)//length
                blocks=codes[:count*length].reshape(count,length)
                letter_counts=np.stack([(blocks==i).sum(axis=1)for i in range(36)],axis=1)
                additions=[]
                for choice in itertools.combinations_with_replacement(range(6),item['unknown_slots']):additions.append(np.bincount(choice,minlength=6))
                added=np.array(additions);observed=added+np.array(item['known_coordinate_counts'])
                for fill in itertools.permutations(unused):
                    it=iter(fill);square=''.join(next(it)if ch=='?'else ch for ch in partial)
                    matrix=np.zeros((36,6),dtype=np.int64)
                    for cell,ch in enumerate(square):matrix[ALPHABET.index(ch),cell//6]+=1;matrix[ALPHABET.index(ch),cell%6]+=1
                    counts=letter_counts@matrix
                    assert np.all(counts.sum(axis=1)==2*length)
                    # Total count is fixed. Five coordinates contain all six-
                    # coordinate information without a singular covariance.
                    values=counts[:,:5];mean=values.mean(axis=0);covariance=np.cov(values,rowvar=False)
                    inverse=np.linalg.inv(covariance);difference=values-mean
                    distances=np.einsum('ij,jk,ik->i',difference,inverse,difference)
                    difference=observed[:,:5]-mean
                    target_distances=np.einsum('ij,jk,ik->i',difference,inverse,difference)
                    best=float(target_distances.min());at_least=int(np.count_nonzero(distances>=best-1e-12))
                    rows=[i for i,d in enumerate(target_distances)if abs(d-best)<1e-10]
                    results.append(dict(target_id=item['id'],book_id=source['id'],convention=convention,square_completion_for_reference_encoding_only=square,
                        unknown_digit_order=''.join(fill),reference_windows=count,window_stride=length,
                        most_favorable_completed_histograms=[observed[i].tolist()for i in rows],most_favorable_erasure_additions=[added[i].tolist()for i in rows],
                        squared_mahalanobis_distance=round(best,12),reference_windows_at_least_as_distant=at_least,
                        empirical_reference_fraction=at_least/count,mean_counts_first_five=[round(float(x),12)for x in mean],
                        covariance_first_five=[[round(float(x),12)for x in row]for row in covariance],
                        reference_distance_quantiles={str(q):round(float(np.quantile(distances,q)),12)for q in [.5,.9,.95,.99,1.0]},
                        count_matrix_sha256=hashlib.sha256(counts.astype('<i4').tobytes()).hexdigest()))
    ordinary=sorted({ch for cell,ch in enumerate(partial)if ch.isalpha()and ch!='?'and(cell//6==2 or cell%6==2)})
    assert ordinary==list('CJMOQZ')
    v_weights={ch:int(cell//6==4)+int(cell%6==4)for cell,ch in enumerate(partial)
               if ch in ALPHABET[:26]and(cell//6==4 or cell%6==4)}
    assert set(v_weights)==set('DEHKQTUX') and v_weights['X']==2
    assert all(weight==1 for ch,weight in v_weights.items()if ch!='X')
    p73=next(row for row in inputs if row['id']=='p73')
    v_max=p73['known_coordinate_counts'][4]+p73['unknown_slots']
    assert v_max==17
    return dict(project='ADFGVX Cipher',review_credit='icekylinx and GPT-6 Astra Pro',key_id=key['id'],partial_square=partial,
        coordinate_order=COORDS,inputs=inputs,heldout_sources=sources,normalized_streams=stream_metadata,
        method=dict(metric='Squared Mahalanobis distance in the first five coordinate counts; the sixth is determined by total length.',
                    reference='All consecutive non-overlapping fixed-length blocks from each normalized source stream, starting at offset 0. No windows cross book boundaries.',
                    erasures='Minimize target distance over every completion of its unknown coordinate counts; no source position is filled in a ciphertext.',
                    square='Evaluate both 5/6 completions separately. These are only reference encodings, not new historical digit assignments.',
                    convention_comparisons='Reported separately; repeated transformed text is not pooled or treated as independent evidence.',
                    calibration='The mean and covariance are fitted only to the reference book windows. Reference fractions are descriptive empirical ranks, not p-values.'),
        exact_F_invariant=dict(observed_F_count=26,ordinary_letters_whose_pairs_contain_F='CJMOQZ',
            maximum_F_coordinates_per_character=2,unique_double_F_character='7',
            minimum_characters_from_CJMOQZ_or_digits=13,
            minimum_CJMOQZ_characters_if_digit_free=26,
            minimum_CJMOQZ_with_at_most_d_digits='max(0, 26 - 2*d)',
            proof='Every observed F must belong to a C/J/M/O/Q/Z or digit pair; only 7=FF contributes two. Transposition preserves coordinate totals.'),
        exact_V_invariant=dict(observed_V_count=15,unknown_coordinate_slots=2,
            maximum_completed_V_count=v_max,
            ordinary_letter_V_coefficients=dict(sorted(v_weights.items())),
            inequality='n_D + n_E + n_H + n_K + n_Q + n_T + n_U + 2*n_X <= 17',
            maximum_encoded_X_characters=v_max//2,
            maximum_DEHKQTU_characters_if_five_X= v_max-2*5,
            conditional_bound='With r encoded X characters, n_D+n_E+n_H+n_K+n_Q+n_T+n_U <= 17-2*r; r must be between 0 and 8.',
            proof='The two source erasures can add at most two V coordinates. The seven listed non-X letters use one V each, X=VV uses two, and all other V-bearing cells are digits. Digits consume the same budget and cannot relax the inequality.',
            limitation='Conditional on Nov7-9 and preservation of all 176 observed coordinates. X need not be a separator, no X count is assigned, and this does not exclude an atypical historical body.'),
        results=results,
        interpretation='Nov7-9 is a low-priority p73 square under the tested ordinary-German prose assumptions. This does not identify a different key, prove the October 26 origin, recover plaintext, or exclude atypical names, digits, code groups, another language, or other source damage.',
        control_limit='The word-X convention also puts the readable p155 A1 control beyond every reference window; it is therefore a visibly unsuitable convention for that body and must not be used as independent exclusion evidence.')


def equivalent(a,b):
    if isinstance(a,float):return isinstance(b,(float,int))and abs(a-b)<=1e-8*max(1,abs(a))
    if isinstance(a,dict):return set(a)==set(b)and all(equivalent(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(equivalent(x,y)for x,y in zip(a,b))
    return a==b


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache',type=Path,required=True);p.add_argument('--download',action='store_true');p.add_argument('--output',type=Path,default=HERE/'p73_histogram_result.json');p.add_argument('--verify',type=Path)
    args=p.parse_args();result=run(args.cache,args.download)
    if args.verify:assert equivalent(result,json.loads(args.verify.read_text()))
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    summaries=[]
    for target in ['p73','p155_A1']:
        for book in result['heldout_sources']:
            for convention in ['plain','sentence_x','word_x']:
                rows=[r for r in result['results']if r['target_id']==target and r['book_id']==book['id']and r['convention']==convention]
                summaries.append(dict(target=target,book_id=book['id'],convention=convention,reference_windows=rows[0]['reference_windows'],largest_reference_fraction_over_digit_completions=max(r['empirical_reference_fraction']for r in rows)))
    print(json.dumps(dict(verified_replay=bool(args.verify),results=summaries),indent=2))

if __name__=='__main__':main()
