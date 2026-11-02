#!/usr/bin/env python3
"""Direct ciphertext retrieval across the 788 unverified Childs OCR blocks.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Exact substrings, multigrams, affine local alignment and full-query fitting.
No decipherment, key search, language score or source correction is performed.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import random
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SYMBOLS = set('ADFGVX?')
SELF = {'p73': 'p73_ocr_block1', 'p170': 'p170_ocr_block1',
        'p198': 'p198_ocr_block4', 'p152': 'p152_ocr_block5',
        'p158': 'p158_ocr_block5', 'p158_typed': 'p158_ocr_block5',
        'p109': 'p109_ocr_block6'}
EXPECTED = {'p152': ['p136_ocr_block3'],
            'p158': ['p159_ocr_block2','p159_ocr_block3','p168_ocr_block3','p168_ocr_block4'],
            'p158_typed': ['p159_ocr_block2','p159_ocr_block3','p168_ocr_block3','p168_ocr_block4'],
            'p109': ['p109_ocr_block3'],
            'seed_full_loss': ['p136_ocr_block3'],
            'seed_fragment_loss': ['p136_ocr_block3'],
            'seed_p109_loss': ['p109_ocr_block3']}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(value):
    result = re.sub(r'\s+', '', value).replace('-', '?')
    assert set(result) <= SYMBOLS
    return result


def grams(text, size):
    return collections.Counter(text[i:i+size] for i in range(len(text)-size+1)
                               if '?' not in text[i:i+size])


def local_trace(a, b):
    """Independent full-matrix reference and one deterministic optimal traceback."""
    n, m, neg = len(a), len(b), -10**9
    H = [[0]*(m+1) for _ in range(n+1)]
    E = [[neg]*(m+1) for _ in range(n+1)]
    F = [[neg]*(m+1) for _ in range(n+1)]
    TH = [[0]*(m+1) for _ in range(n+1)]
    TE = [[0]*(m+1) for _ in range(n+1)]
    TF = [[0]*(m+1) for _ in range(n+1)]
    best, endpoint = 0, (0,0)
    for i in range(1,n+1):
        for j in range(1,m+1):
            ee = [H[i-1][j]-3,E[i-1][j]-1]
            ff = [H[i][j-1]-3,F[i][j-1]-1]
            E[i][j], F[i][j] = max(ee), max(ff)
            TE[i][j], TF[i][j] = ee.index(E[i][j]),ff.index(F[i][j])
            score = 0 if '?' in (a[i-1],b[j-1]) else 2 if a[i-1]==b[j-1] else -3
            options = [0,H[i-1][j-1]+score,E[i][j],F[i][j]]
            H[i][j] = max(options); TH[i][j] = options.index(H[i][j])
            if H[i][j] > best:
                best,endpoint = H[i][j],(i,j)
    i,j = endpoint
    pairs, state = [], 'H'
    while i or j:
        if state == 'H':
            direction = TH[i][j]
            if direction == 0:break
            if direction == 1:
                pairs.append((i-1,j-1));i-=1;j-=1
            else:state='E' if direction==2 else 'F'
        elif state == 'E':
            extension = TE[i][j]
            pairs.append((i-1,None));i-=1
            if not extension:state='H'
        else:
            extension = TF[i][j]
            pairs.append((None,j-1));j-=1
            if not extension:state='H'
    pairs.reverse()
    exact,mismatch,unknown = [],[],[]
    for ai,bi in pairs:
        if ai is None or bi is None:continue
        if '?' in (a[ai],b[bi]):unknown.append([ai,bi])
        elif a[ai] == b[bi]:exact.append([ai,bi])
        else:mismatch.append([ai,bi])
    gap_cost,gap_runs,previous = 0,0,None
    for ai,bi in pairs:
        kind = 'query_gap' if ai is None else 'corpus_gap' if bi is None else None
        if kind:
            gap_cost += 1 if kind == previous else 3
            gap_runs += kind != previous
        previous = kind
    assert 2*len(exact)-3*len(mismatch)-gap_cost == best
    return {'local_score':best, 'query_span':[i,endpoint[0]],'corpus_span':[j,endpoint[1]],
            'known_exact_matches':len(exact),'known_substitutions':len(mismatch),
            'erasure_pairs':len(unknown),'gap_slots':sum(x is None or y is None for x,y in pairs),
            'gap_runs':gap_runs,'aligned_query':''.join('-' if x is None else a[x] for x,y in pairs),
            'aligned_corpus':''.join('-' if y is None else b[y] for x,y in pairs),
            'known_substitution_pairs':mismatch,'erasure_pairs_indices':unknown}


def reference_metrics(a,b):
    longest=0;previous=[0]*(len(b)+1)
    fit=[0]*(len(b)+1)
    for i,ca in enumerate(a,1):
        current=[0]*(len(b)+1);next_fit=[i]+[0]*len(b)
        for j,cb in enumerate(b,1):
            current[j]=previous[j-1]+1 if ca==cb and ca!='?' else 0
            longest=max(longest,current[j])
            next_fit[j]=min(fit[j-1]+(0 if ca==cb or '?' in (ca,cb) else 1),fit[j]+1,next_fit[j-1]+1)
        previous,fit=current,next_fit
    return local_trace(a,b)['local_score'],longest,min(fit)


def run_kernel(executable,queries,blocks,work):
    lines=[str(len(queries))]+[name+' '+seq for name,seq in queries.items()]
    lines += [str(len(blocks))]+[name+' '+seq for name,seq in blocks.items()]
    source='\n'.join(lines)+'\n'
    output=subprocess.check_output([str(executable)],input=source,text=True)
    if work:
        (work/'retrieval_input.txt').write_text(source)
        (work/'retrieval_metrics.tsv').write_text(output)
    return [line.split('\t') for line in output.splitlines()]


def build_queries():
    messages={m['id']:m for m in json.loads((ROOT/'data/messages.json').read_text())['messages']}
    queries={name:messages[name]['transcript']['analysis_ciphertext'] for name in ['p73','p170','p198','p152','p158','p109']}
    queries['p158_typed']=messages['p158']['transcript']['physical_layers']['typed_only']['ciphertext']
    control=json.loads((ROOT/'data/certificates/p152.json').read_text())['source_decryptions'][0]
    parent=clean(control['source_ciphertext'])
    B=json.loads((ROOT/'data/certificates/p109_parallel.json').read_text())['source_B']['ciphertext']
    fixtures=[]
    for name,origin,base,cut,erasures in [
        ('seed_full_loss','p136_B1',parent,155,[19,55,183,254]),
        ('seed_fragment_loss','p136_B1[100:206]',parent[100:206],40,[4,18,85]),
        ('seed_p109_loss','p109_B',B,80,[13,101,177,215])]:
        removed=base[cut:cut+5]
        damaged=base[:cut]+base[cut+5:]
        chars=list(damaged)
        for index in erasures:chars[index]='?'
        queries[name]=''.join(chars)
        fixtures.append({'id':name,'parent':origin,'parent_length':len(base),
                         'deleted_source_span':[cut,cut+5],'deleted_coordinates':removed,
                         'additional_erasure_indices_after_deletion':erasures,
                         'query':queries[name],'expected_ocr_parent':EXPECTED[name]})
    rng=random.Random(19181108)
    for name in ['p73','p170','p198']:
        for index in range(8):
            chars=list(queries[name]);rng.shuffle(chars)
            queries[f'null_{name}_{index:02d}']=''.join(chars)
    return queries,fixtures


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir',type=Path,default=Path('/tmp/adfgvx-source-similarity'))
    parser.add_argument('--output',type=Path,default=HERE/'results.json')
    args=parser.parse_args();args.work_dir.mkdir(parents=True,exist_ok=True)
    binary=args.work_dir/'align'
    subprocess.run(['c++','-std=c++17','-O3',str(HERE/'align.cpp'),'-o',str(binary)],check=True)
    # Independent small cases cover erasures, local endpoints, gaps and fitting.
    short={'q0':'A','q1':'AD','q2':'A?D','q3':'ADFGV','q4':'AAAAD','q5':'XADFGVX'}
    small={'b0':'V','b1':'DAD','b2':'?AD?','b3':'ADVVFGV','b4':'AAAA','b5':'GGADFGVXX'}
    checks=run_kernel(binary,short,small,None)
    for q,b,*values in checks:
        assert tuple(map(int,values))==reference_metrics(short[q],small[b]),(q,b,values)
    corpus=json.loads((ROOT/'experiments/p153_corpus/inputs.json').read_text())['blocks']
    blocks={block['id']:clean(''.join(block['groups'])) for block in corpus}
    metadata={block['id']:block for block in corpus}
    queries,fixtures=build_queries()
    metrics=run_kernel(binary,queries,blocks,args.work_dir)
    rows=collections.defaultdict(list)
    qgrams={name:{k:grams(seq,k) for k in [5,7,9]} for name,seq in queries.items() if not name.startswith('null_')}
    bgrams={name:{k:grams(seq,k) for k in [5,7,9]} for name,seq in blocks.items()}
    for query,block,score,longest,fit in metrics:
        base_query = query.split('_')[1] if query.startswith('null_') else query
        if SELF.get(base_query)==block:continue
        row={'block_id':block,'printed_page':metadata[block]['printed_page'],
             'corpus_slots':len(blocks[block]),'corpus_known_coordinates':len(blocks[block].replace('?','')),
             'affine_local_score':int(score),'longest_exact_run':int(longest),
             'full_query_fitting_cost':int(fit)}
        if not query.startswith('null_'):
            for k in [5,7,9]:row[f'common_{k}gram_occurrences']=sum((qgrams[query][k]&bgrams[block][k]).values())
        rows[query].append(row)
    reports={}
    for name in queries:
        if name.startswith('null_'):continue
        ordered=sorted(rows[name],key=lambda x:(-x['affine_local_score'],-x['longest_exact_run'],x['block_id']))
        exact=sorted(rows[name],key=lambda x:(-x['longest_exact_run'],-x['common_9gram_occurrences'],-x['affine_local_score'],x['block_id']))
        multi=sorted(rows[name],key=lambda x:(-x['common_9gram_occurrences'],-x['common_7gram_occurrences'],-x['affine_local_score'],x['block_id']))
        fitting=sorted(rows[name],key=lambda x:(x['full_query_fitting_cost'],-x['affine_local_score'],x['block_id']))
        ranks={row['block_id']:i+1 for i,row in enumerate(ordered)}
        report={'query':queries[name],'query_slots':len(queries[name]),'excluded_self_block':SELF.get(name),
                'rankings':{'affine_local':ordered[:10],'longest_exact_run':exact[:10],
                            'shared_ninegrams':multi[:10],'full_query_fitting':fitting[:10]}}
        if name in EXPECTED:
            report['known_relationship_ranks']=[{'block_id':b,'affine_local_rank':ranks[b],
                                               'metrics':next(x for x in ordered if x['block_id']==b)} for b in EXPECTED[name]]
        if name in ['p73','p170','p198']:
            candidates={row['block_id'] for ranking in [ordered,exact,multi,fitting] for row in ranking[:6]}
            traces=[]
            for block in sorted(candidates,key=lambda b:ranks[b]):
                trace=local_trace(queries[name],blocks[block])
                assert trace['local_score']==next(x['affine_local_score'] for x in ordered if x['block_id']==block)
                traces.append({'block_id':block,'affine_local_rank':ranks[block],
                               'headers_ocr':metadata[block]['context_headers_ocr'],
                               'trace':trace})
            report['candidate_alignments']=traces
            null=[]
            for i in range(8):
                group=rows[f'null_{name}_{i:02d}']
                top=max(group,key=lambda x:x['affine_local_score'])
                null.append({'replicate':i,'maximum_affine_local_score':top['affine_local_score'],
                             'top_block':top['block_id'],
                             'maximum_exact_run':max(x['longest_exact_run'] for x in group)})
            report['composition_preserving_shuffled_controls']=null
        reports[name]=report
    result={'project':'ADFGVX Cipher','authors':'icekylinx and GPT-6 Astra Pro',
            'status':'Direct source retrieval; OCR candidates are unverified until image inspection.',
            'input_hashes':{str(path.relative_to(ROOT)):digest(path) for path in
                            [ROOT/'data/messages.json',ROOT/'experiments/p153_corpus/inputs.json',
                             ROOT/'data/certificates/p152.json',ROOT/'data/certificates/p109_parallel.json']},
            'corpus_blocks':len(blocks),'queries_including_controls':len(queries),'pairwise_comparisons':len(metrics),
            'metrics':{'affine_local':'Known match +2; known mismatch -3; an erasure pair 0. A gap run costs 3 for its first slot and 1 for every later slot. Both ends are free.',
                       'longest_exact_run':'Longest contiguous identical known-coordinate substring; erasures break runs.',
                       'multigrams':'Multiset intersections of known 5-, 7- and 9-coordinate substrings, independent of printed five-letter grouping.',
                       'full_query_fitting':'Unit insertions/deletions/substitutions; erasure pairs cost zero. Entire query is fitted with free corpus prefix/suffix. This cost alone can favor erased corpus regions.'},
            'small_reference_checks':len(checks),'seeded_fixtures':fixtures,
            'shuffle_control_seed':19181108,'reports':reports,
            'limits':['No language model, plaintext, key hypothesis or coordinate correction enters retrieval.',
                      'Common short substrings occur by chance in a six-symbol alphabet; rankings are not probabilities.',
                      'Eight shuffled queries per target provide descriptive composition controls, not a calibrated significance test.',
                      'Original target blocks are explicitly excluded from ranked retrieval; synthetic parent hits are controls only.',
                      'OCR may omit or severely corrupt a related transmission, and a different encryption changes direct ciphertext similarity.']}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'comparisons':len(metrics),'targets':{n:reports[n]['rankings']['affine_local'][:5] for n in ['p73','p170','p198']},
                      'controls':{n:reports[n]['known_relationship_ranks'] for n in EXPECTED}},indent=2))


if __name__=='__main__':
    main()
