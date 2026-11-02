"""Independent domain adaptation from public-domain German wartime books.

The six earlier general German books have weight one. Four separately sourced
wartime books have weight two. Stream conventions remain 5:3:1 (joined text,
sentence X, word X). No challenge message, candidate, or decrypted source
parallel is used in training. Both four- and six-gram tables are emitted.
"""
from collections import Counter
from pathlib import Path
import array
import hashlib
import json
import math
import re
import struct

from build_models import fetch, streams, IDS, ALPHABET

ROOT=Path(__file__).resolve().parent.parent


def main():
    sources=[];texts=[]
    for book_id in IDS:
        meta,text=fetch(book_id)
        if meta['language'].lower()!='german':continue
        meta={**meta,'domain_weight':1,'group':'general_German'}
        sources.append(meta);texts.append((meta,text))
    folder=ROOT/'data/military_corpus'
    for record in json.loads((folder/'source.json').read_text()):
        path=folder/f"pg{record['id']}.txt";data=path.read_bytes()
        assert hashlib.sha256(data).hexdigest()==record['sha256']
        text=data.decode('utf-8-sig')
        language=re.search(r'^Language:\s*(.+)$',text,re.M).group(1).strip()
        assert language=='German'
        title=re.search(r'^Title:\s*(.+)$',text,re.M).group(1).strip()
        author=re.search(r'^Author:\s*(.+)$',text,re.M).group(1).strip()
        start=re.search(r'\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*',text,re.S)
        end=re.search(r'\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK',text)
        assert start and end
        text=text[start.end():end.start()]
        meta={**record,'title':title,'author':author,'language':language,
              'domain_weight':2,'group':'wartime_German'}
        sources.append(meta);texts.append((meta,text))
    q4=Counter();q6=Counter();mono=Counter();indices={c:i for i,c in enumerate(ALPHABET)}
    for meta,text in texts:
        for stream,stream_weight in streams(text):
            weight=stream_weight*meta['domain_weight'];z=0
            for i,ch in enumerate(stream):
                v=indices[ch];z=(z*36+v)%(36**6);mono[ch]+=weight
                if i>=3:q4[z%(36**4)]+=weight
                if i>=5:q6[z]+=weight
        print(json.dumps({'book_id':meta['id'],'quad_types':len(q4),'six_types':len(q6)}),flush=True)
    output=ROOT/'data/military_models';output.mkdir(exist_ok=True)
    total4=sum(q4.values());floor4=math.log10(.01/total4)
    a=array.array('f',[floor4])*(36**4)
    for z,count in q4.items():a[z]=math.log10(count/total4)
    p4=output/'german_military36_quad.bin'
    with p4.open('wb') as f:a.tofile(f)
    total6=sum(q6.values());floor6=math.log10(.01/total6);size=1
    while size<2*len(q6):size*=2
    keys=array.array('I',[0])*size;values=array.array('f',[floor6])*size
    for z,count in q6.items():
        key=z+1;h=key;h=((h^(h>>16))*0x7feb352d)&0xffffffff
        h=((h^(h>>15))*0x846ca68b)&0xffffffff;h^=h>>16;slot=h&(size-1)
        while keys[slot]:slot=(slot+1)&(size-1)
        keys[slot]=key;values[slot]=math.log10(count/total6)
    p6=output/'german_military36_sixgram.bin'
    with p6.open('wb') as f:
        f.write(struct.pack('<8sIIf',b'G6HASH2\0',size,len(q6),floor6));keys.tofile(f);values.tofile(f)
    info={'sources':sources,'training_includes_challenge_plaintexts':False,
          'stream_weights':{'plain':5,'sentence_X':3,'word_X':1},
          'domain_weights':{'general_German':1,'wartime_German':2},
          'monograms':dict(mono),
          'quad':{'weighted_windows':total4,'distinct':len(q4),'floor':floor4,'sha256':hashlib.sha256(p4.read_bytes()).hexdigest()},
          'six':{'weighted_windows':total6,'distinct':len(q6),'floor':floor6,'hash_size':size,'sha256':hashlib.sha256(p6.read_bytes()).hexdigest()},
          'scope':'Domain adaptation motivated by short military-text controls; no historical target candidate is used as training data.'}
    (output/'provenance.json').write_text(json.dumps(info,indent=2))
    print(json.dumps({k:v for k,v in info.items() if k not in ['sources','monograms']}),flush=True)


if __name__=='__main__':main()
