"""Independent book-word model for a source-preserving loss-channel pilot.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
No attacked ciphertext or candidate plaintext is training material.
"""
import argparse
import collections
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cache', type=Path, required=True, help='Hash-pinned Gutenberg book cache')
parser.add_argument('--output', type=Path, required=True, help='Directory for rebuilt lexicon and provenance')
args = parser.parse_args()
OUT = args.output
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('models', ROOT/'experiments/joint_search/tools/build_models.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
provenance = json.loads((ROOT/'experiments/joint_search/models/provenance.json').read_text())
words = collections.Counter()
pairs = collections.Counter()
for source in provenance['sources']:
    text = module.fetch(source, args.cache)
    text = text.translate(str.maketrans({'ä':'ae','ö':'oe','ü':'ue','Ä':'AE','Ö':'OE','Ü':'UE','ß':'ss'})).upper()
    weight = source['domain_weight']
    for sentence in re.split(r'[.!?;:\n]+', text):
        tokens = re.findall('[A-Z]+|[0-9]+',sentence)
        for token in tokens:
            if token.isalpha() and len(token)<=32:
                words[token] += weight
        for a,b in zip(tokens,tokens[1:]):
            if a.isalpha() and b.isalpha() and max(len(a),len(b))<=32:
                pairs[a,b] += weight
total = sum(words.values())
ordered = sorted(words)
ids = {word:i for i,word in enumerate(ordered)}
with (OUT/'lexicon.txt').open('w') as f:
    f.write(f'{len(ordered)} {sum(v>=2 for v in pairs.values())}\n')
    for word in ordered:
        f.write(f'{word} {math.log10(words[word]/total):.9f}\n')
    for (a,b),count in sorted(pairs.items()):
        if count>=2:
            # A positive association bonus; capped and used only as an objective.
            bonus = max(0,min(2,math.log10((count*total)/(words[a]*words[b]))))
            f.write(f'{ids[a]} {ids[b]} {bonus:.9f}\n')
manifest = {'schema':'adfgvx-independent-word-model-pilot-v1','authors':'icekylinx and GPT-6 Astra Pro',
 'sources':provenance['sources'],'total_weighted_words':total,'distinct_words':len(words),
 'minimum_bigram_count':2,'objective_note':'Unigram segmentation with capped observed word-association bonuses; not a calibrated probability.',
 'lexicon_sha256':hashlib.sha256((OUT/'lexicon.txt').read_bytes()).hexdigest()}
(OUT/'lexicon_provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:manifest[k] for k in ['total_weighted_words','distinct_words','lexicon_sha256']}))

assert manifest['lexicon_sha256'] == '6ea36fc166dd884a3a46f99aa7fd9ab03ae237d5a79c1a30f059e983d5f0d9ef', 'Rebuilt model differs from the frozen lexicon'
