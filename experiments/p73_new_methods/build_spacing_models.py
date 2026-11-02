"""Independent spacing-convention variants; icekylinx and GPT-6 Astra Pro."""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import numpy as np
import argparse

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--cache', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
OUT = args.output
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('independent_models', ROOT/'experiments/joint_search/tools/build_models.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
provenance = json.load(open(ROOT/'experiments/joint_search/models/provenance.json'))
books = [(source, module.fetch(source, args.cache)) for source in provenance['sources']]
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
lookup = {c:i for i,c in enumerate(alphabet)}
for mode in ['plain', 'word_X']:
    counts = Counter()
    for source, text in books:
        stream = module.streams(text)[0 if mode == 'plain' else 2][0]
        weight, code = source['domain_weight'], 0
        for i, char in enumerate(stream):
            code = (code * 36 + lookup[char]) % (36 ** 4)
            if i >= 3:
                counts[code] += weight
    total = sum(counts.values())
    probability = np.full(36 ** 4, .01 / total, dtype=np.float64)
    for code, count in counts.items():
        probability[code] = count / total
    probability /= probability.sum()
    probability = probability.reshape((36,) * 4)
    marginal = np.empty((37,) * 4, dtype=np.float64)
    for mask in range(16):
        axes = tuple(i for i in range(4) if mask & (1 << i))
        target = tuple(36 if i in axes else slice(0, 36) for i in range(4))
        marginal[target] = probability.sum(axis=axes) if axes else probability
    destination = OUT/f'{mode}_37_quad_marginal.bin'
    np.log10(marginal).astype('<f4').tofile(destination)
    record = {
        'prepared_by': ['icekylinx', 'GPT-6 Astra Pro'], 'convention': mode,
        'sources': provenance['sources'], 'training_includes_challenge_plaintexts': False,
        'training_includes_control_plaintexts': False,
        'weighted_windows': total, 'distinct_quadgrams': len(counts),
        'binary_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
    }
    (OUT/f'{mode}_provenance.json').write_text(json.dumps(record, indent=2) + '\n')
    print(mode, total, len(counts), record['binary_sha256'], flush=True)
