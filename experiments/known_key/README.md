# Portable ranking reproduction

These scripts reproduce two bounded experiments by **icekylinx and GPT-6 Astra Pro**. Their language scores rank hypotheses; they do not certify a historical plaintext. The arithmetic certificates and their standard-library verifiers remain the authority for source preservation and plaintext constraints.

## Model provenance

The base table is the published `data/quad.bin` from [0wwafa/adfgvx-1918 at commit 0839217](https://github.com/0wwafa/adfgvx-1918/tree/083921732d7c18e52424336ab4160fada5c61b4b). It contains 456,976 little-endian float32 log10 quadgram values, totaling 1,827,904 bytes. Its SHA-256 is:

```text
a39714514cd2884605b1b04a2f65565fcf33aec1f7162bcd1b472c7108601009
```

[model_provenance.json](model_provenance.json) provides the pinned binary URL, build-script and vocabulary hashes, documented Gutenberg text IDs, and the upstream license. The upstream script describes its training procedure, but does not pin the downloaded corpus bytes and skips failed requests. Rebuilding from live corpus URLs therefore need not reproduce the distributed binary. These scripts require the stated binary hash.

The upstream vocabulary contains previously solved messages, including the p171 body used for the two synthetic p170 controls. Those controls are implementation and ranking-sensitivity checks, not out-of-sample accuracy estimates. The model is never used as evidence that an arbitrary proposed plaintext is correct.

Download the small upstream table separately; no 23 MB coordinate model is committed here:

```sh
curl -L --fail \
  https://raw.githubusercontent.com/0wwafa/adfgvx-1918/083921732d7c18e52424336ab4160fada5c61b4b/data/quad.bin \
  -o quad26.bin
```

The scripts check its hash automatically. They require NumPy; the p170 search additionally requires a C compiler. `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` keep model construction within one numerical worker.

## p185 D: all 194 gap positions

Run from this directory and substitute the path of the published p185 D certificate:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
python rank_p185_gap.py \
  --certificate ../../data/certificates/p185_D_transport.json \
  --quad26 quad26.bin \
  --output p185_ranking.json
```

The script constructs its coordinate arrays in memory. It independently retransposes each masked candidate, computes both ranking scores, and checks all 194 scores and both full orderings against the certificate. An optional `--quad49 FILE --single49 FILE` pair accepts precomputed arrays, subject to the certificate's exact hashes.

The portable implementation reproduced every stored score with **zero numerical discrepancy** in the recorded environment. The composite ranking favors gap 55; the conventional quadgram ranking favors gap 57. That disagreement is retained. [p185_ranking_reproduction.json](p185_ranking_reproduction.json) records the check. It does not establish a unique gap position or a full decryption.

## p170: every stated contiguous placement

First check the stored scope, candidate arithmetic and synthetic control roundtrips without NumPy or a language model:

```sh
python verify_p170.py p170_experiment.json
```

Then reproduce all 21 key scans and both controls:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
python run_p170.py \
  --experiment p170_experiment.json \
  --quad26 quad26.bin \
  --output-dir p170_output
```

The runner compiles `p170_scan.c`, builds each temporary coordinate model, and writes the top 100 candidates in each of four pools. It compares the SHA-256 of every output to the original archived run. All **23 outputs reproduced byte for byte** in the recorded environment; see [p170_reproduction_report.json](p170_reproduction_report.json). Floating-point libraries or tie ordering on a different platform may change exact output hashes without changing the substantive result; inspect the numerical differences if that occurs.

Use `--key Nov7-9 --no-controls` for one target key, or `--controls-only` for the two controls. The detailed scope and its limits are in [p170-truncation.md](p170-truncation.md). The result remains negative: no newly accepted p170 plaintext, and no exclusion of the truncation hypothesis.

## Scoring distinction

Both experiments sum one quarter of overlapping four-pattern log correlation ratios. For p185 D, the single-pattern term is the log ratio of joint row/column probability to independent coordinate probabilities. For p170, which changes which observed coordinates pair and which are rows or columns, it is the log marginal probability of the observed coordinate pattern. [marginal_model.py](marginal_model.py) builds both terms explicitly.

Unassigned square cells are averaged over the unused alphabet only for scoring. This ignores dependencies between repeated occurrences of one unassigned cell. The certificate domains retain those cells as unassigned. The 3% total digit mass is a modeling choice, not an estimated historical digit frequency.
