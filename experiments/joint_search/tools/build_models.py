"""Rebuild independent German models from source-hash-verified public books.

Requires NumPy only for the37^4 wildcard table. No challenge plaintext,
control plaintext, candidate or recovered historical text enters training.
"""
from pathlib import Path
from collections import Counter
import argparse
import array
import hashlib
import json
import math
import random
import re
import struct
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(source, cache):
    path = cache / f'pg{source["id"]}.txt'
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        data = urllib.request.urlopen(source['url'], timeout=60).read()
        if hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ValueError(f'Source bytes changed for book{source["id"]}; provide the recorded version in the cache')
        path.write_bytes(data)
    if digest(path) != source['sha256']:
        raise ValueError(f'Cached source hash mismatch: {path}')
    text = path.read_bytes().decode('utf-8-sig', 'replace')
    language = re.search(r'^Language:\s*(.+)$', text, re.M)
    if not language or language.group(1).strip().lower() != 'german':
        raise ValueError('Only the documented German books may enter this model')
    start = re.search(r'\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*', text, re.S)
    end = re.search(r'\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK', text)
    if not start or not end: raise ValueError('Gutenberg body markers are absent')
    return text[start.end():end.start()]


def streams(text):
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
    text = text.replace('Ä', 'AE').replace('Ö', 'OE').replace('Ü', 'UE').replace('ß', 'ss').upper()
    plain = re.sub(r'[^A-Z0-9]', '', text)
    sentence = re.sub(r'[.!?;:\n]+', 'X', text)
    sentence = re.sub('XX+', 'X', re.sub(r'[^A-Z0-9]', '', sentence))
    word = 'X'.join(re.findall(r'[A-Z0-9]+', text))
    return [(plain, 5), (sentence, 3), (word, 1)]


def write_array(stream, values):
    if sys.byteorder == 'big':
        values = array.array(values.typecode, values); values.byteswap()
    values.tofile(stream)


def features(texts):
    counts = Counter(''.join(texts).replace('?', ''))
    n = sum(counts.values())
    ordered = sorted(counts.values(), reverse=True)+[0]*(36-len(counts))
    pairs = Counter(text[i:i+2] for text in texts for i in range(len(text)-1)
                    if '?' not in text[i:i+2])
    m = sum(pairs.values())
    return [value/n for value in ordered]+[sum(value*(value-1) for value in pairs.values())/(m*(m-1))]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', type=Path, default=ROOT/'work/corpus')
    parser.add_argument('--output', type=Path, default=ROOT/'models')
    parser.add_argument('--download-only', action='store_true')
    parser.add_argument('--verify-existing', action='store_true')
    args = parser.parse_args()
    specification = json.loads((ROOT/'models/provenance.json').read_text())
    if args.verify_existing:
        for filename, expected in specification['binary_sha256'].items():
            actual = digest(args.output/filename)
            if actual != expected: raise ValueError(f'Model hash mismatch: {filename}')
        print(json.dumps({'verified_binary_models': len(specification['binary_sha256'])})); return
    texts = [(source, fetch(source, args.cache)) for source in specification['sources']]
    if args.download_only:
        print(json.dumps({'verified_source_books': len(texts)})); return
    args.output.mkdir(parents=True, exist_ok=True)
    q4, q6, mono = Counter(), Counter(), Counter()
    profile_samples = []; rng = random.Random(2026110242)
    mapping = {ch:i for i,ch in enumerate(ALPHABET)}
    for source, text in texts:
        for stream, stream_weight in streams(text):
            weight = stream_weight*source['domain_weight']; code = 0
            for i, ch in enumerate(stream):
                code = (code*36+mapping[ch]) % (36**6); mono[ch] += weight
                if i >= 3: q4[code % (36**4)] += weight
                if i >= 5: q6[code] += weight
            if source['group'] == 'general_German':
                for _ in range(200*stream_weight):
                    start = rng.randrange(len(stream)-120)
                    sample = stream[start:start+120]
                    second = list(sample[66:])
                    for position in rng.sample(range(54), rng.randrange(8,16)): second[position] = '?'
                    profile_samples.append(features([sample[:66], ''.join(second)]))
        print(json.dumps({'book_id': source['id'], 'distinct_quadgrams': len(q4), 'distinct_sixgrams': len(q6)}), flush=True)
    total4, total6 = sum(q4.values()), sum(q6.values())
    floor4, floor6 = math.log10(.01/total4), math.log10(.01/total6)
    quads = array.array('f', [floor4])*(36**4)
    for code, count in q4.items(): quads[code] = math.log10(count/total4)
    with (args.output/'german_military36_quad.bin').open('wb') as stream: write_array(stream, quads)
    size = 1
    while size < 2*len(q6): size *= 2
    keys, values = array.array('I', [0])*size, array.array('f', [floor6])*size
    for code, count in q6.items():
        key = code+1
        h = ((key^(key>>16))*0x7feb352d)&0xffffffff
        h = ((h^(h>>15))*0x846ca68b)&0xffffffff; h ^= h>>16
        slot = h&(size-1)
        while keys[slot]: slot = (slot+1)&(size-1)
        keys[slot], values[slot] = key, math.log10(count/total6)
    with (args.output/'german_military36_sixgram.bin').open('wb') as stream:
        stream.write(struct.pack('<8sIIf', b'G6HASH2\0', size, len(q6), floor6))
        write_array(stream, keys); write_array(stream, values)
    import numpy as np
    source = np.fromfile(args.output/'german_military36_quad.bin', dtype='<f4').astype(np.float64).reshape((36,)*4)
    probability = np.power(10, source); probability /= probability.sum()
    marginal = np.empty((37,)*4, dtype=np.float64)
    for mask in range(16):
        axes = tuple(i for i in range(4) if mask&(1<<i))
        target = tuple(36 if i in axes else slice(0,36) for i in range(4))
        marginal[target] = probability.sum(axis=axes) if axes else probability
    np.log10(marginal).astype('<f4').tofile(args.output/'german_military37_quad_marginal.bin')
    means = [sum(row[i] for row in profile_samples)/len(profile_samples) for i in range(37)]
    variances = [sum((row[i]-means[i])**2 for row in profile_samples)/(len(profile_samples)-1) for i in range(37)]
    profile_text = '\n'.join(f'{mean:.12g} {variance:.12g}' for mean,variance in zip(means,variances))+'\n'
    (args.output/'profile.txt').write_text(profile_text)
    total_mono = sum(mono.values())
    (args.output/'military_monograms.txt').write_text('\n'.join(format(mono[ch]/total_mono, '.18g') for ch in ALPHABET)+'\n')
    generated = {name:digest(args.output/name) for name in specification['binary_sha256']}
    for name, expected in specification['binary_sha256'].items():
        if generated[name] != expected: raise ValueError(f'Rebuilt model hash differs: {name}')
    expected_profile = specification['profile_text_sha256']
    if digest(args.output/'profile.txt') != expected_profile: raise ValueError('Rebuilt short-text profile differs')
    record = dict(source_books=len(texts), profile_samples=len(profile_samples),
                  weighted_quadgrams=total4, weighted_sixgrams=total6,
                  verified_binary_hashes=generated, numpy_version=np.__version__,
                  training_includes_challenge_plaintexts=False)
    (args.output/'build_record.json').write_text(json.dumps(record, indent=2))
    print(json.dumps(record, indent=2))


if __name__ == '__main__': main()
