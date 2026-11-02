#!/usr/bin/env python3
"""Rescore planted and wrong control texts using two held-out German books.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
This is a diagnostic comparison, not a new optimization or historical reading.
Only counts needed to audit the compared texts are retained in the result;
complete source-specific count tables are reproducible from pinned books.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, math, struct, sys
from p73_histogram import source_text, normalized_streams, equivalent

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def float32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def frozen_texts(data):
    texts = {}
    for case in data['cases']:
        planted = case['planted']
        ranks, square = case['column_rank_order'], case['square']
        assert encrypt(planted['plaintext'], ranks, square) == planted['full_ciphertext']
        assert ''.join(ch for i, ch in enumerate(planted['full_ciphertext'])
                       if i not in planted['missing_full_ciphertext_positions_0based']) == case['observed_ciphertext']
        optimum = case['joint_quad_optimum']
        positions = optimum['missing_full_ciphertext_positions']
        assert positions == sorted(set(positions)) and len(positions) == 5
        values = iter(optimum['filled_missing_coordinates'])
        observed = iter(case['observed_ciphertext'])
        full = ''.join(next(values) if i in positions else next(observed) for i in range(170))
        recovered = decrypt(full, ranks, square)
        assert encrypt(recovered, ranks, square) == full
        assert ''.join(ch for i, ch in enumerate(full) if i not in positions) == case['observed_ciphertext']
        texts.setdefault('planted', planted['plaintext'])
        assert texts['planted'] == planted['plaintext']
        texts[case['id'] + '_wrong_joint_optimum'] = recovered
    assert len(texts) == 3 and {len(text) for text in texts.values()} == {85}
    return texts


def table_record(counts, n, texts):
    total = sum(counts.values())
    floor = float32(math.log10(.01 / total))
    relevant = sorted({text[i:i+n] for text in texts.values() for i in range(len(text)-n+1)})
    selected = {gram: counts[gram] for gram in relevant}
    digest = hashlib.sha256()
    for gram, count in sorted(counts.items()):
        digest.update(f'{gram}:{count}\n'.encode('ascii'))
    scores = {}
    for label, text in texts.items():
        values = [float32(math.log10(counts[gram] / total)) if counts[gram] else floor
                  for i in range(len(text)-n+1) for gram in [text[i:i+n]]]
        scores[label] = sum(values) / len(values)
    return dict(order=n, weighted_gram_total=total, distinct_grams=len(counts),
                unseen_probability_numerator=.01, unseen_log10_float32=floor,
                canonical_complete_counts_sha256=digest.hexdigest(),
                relevant_gram_counts=selected, mean_log10_scores=scores,
                wrong_minus_planted={k: v-scores['planted'] for k, v in scores.items() if k != 'planted'})


def build(cache, download):
    inputs = json.loads((HERE / 'joint_control_inputs.json').read_text())
    texts = frozen_texts(inputs)
    sources = json.loads((HERE / 'heldout_sources.json').read_text())['sources']
    training = json.loads((ROOT / inputs['model_provenance']).read_text())['sources']
    assert not {s['id'] for s in sources} & {s['id'] for s in training}
    records = []
    for source in sources:
        streams = dict(normalized_streams(source_text(source, cache, download)))
        models = {4: {}, 6: {}}
        for n in models:
            for name, stream in streams.items():
                models[n][name] = Counter(stream[i:i+n] for i in range(len(stream)-n+1))
            weighted = Counter()
            for name, weight in [('plain', 5), ('sentence_x', 3), ('word_x', 1)]:
                weighted.update({gram: weight*count for gram, count in models[n][name].items()})
            models[n]['weighted_5_3_1'] = weighted
        for convention in ['plain', 'sentence_x', 'word_x', 'weighted_5_3_1']:
            quad, six = [table_record(models[n][convention], n, texts) for n in [4, 6]]
            mixed = {label: .3*quad['mean_log10_scores'][label]+.7*six['mean_log10_scores'][label]
                     for label in texts}
            records.append(dict(book_id=source['id'], convention=convention, quad=quad, six=six,
                                mixed_30_70_scores=mixed,
                                mixed_wrong_minus_planted={k: v-mixed['planted'] for k, v in mixed.items() if k != 'planted'}))
    return dict(project='ADFGVX Cipher', review_credit='icekylinx and GPT-6 Astra Pro',
                inputs_sha256=hashlib.sha256((HERE / 'joint_control_inputs.json').read_bytes()).hexdigest(),
                texts=texts, heldout_sources=sources,
                convention_weights={'plain': 5, 'sentence_x': 3, 'word_x': 1},
                scoring='Each observed n-gram has count/total; an unseen n-gram receives .01/total. Individual base-10 logs are rounded to float32 before their arithmetic mean. Mixed scores use 30% quad and 70% six means.',
                count_hash_format='ASCII records gram:count followed by newline, in lexical gram order; only observed grams are hashed.',
                source_models_built_after_candidates_frozen=True,
                candidates_optimized_against_heldout_books=False,
                results=records,
                limitation='Two controls and two prose books diagnose objective sensitivity; these comparisons are neither independent decipherments nor a calibrated historical acceptance threshold.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--download', action='store_true')
    p.add_argument('--output', type=Path, default=HERE / 'heldout_control_scores.json')
    p.add_argument('--verify', type=Path)
    args = p.parse_args()
    result = build(args.cache, args.download)
    if args.verify:
        assert equivalent(result, json.loads(args.verify.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([dict(book_id=r['book_id'], convention=r['convention'],
                           quad_wrong_minus_planted=r['quad']['wrong_minus_planted'],
                           six_wrong_minus_planted=r['six']['wrong_minus_planted'],
                           mixed_wrong_minus_planted=r['mixed_wrong_minus_planted'])
                      for r in result['results']], indent=2))


if __name__ == '__main__':
    main()
