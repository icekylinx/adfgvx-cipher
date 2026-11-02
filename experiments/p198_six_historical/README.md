# Exact six-gram follow-up on a conditional p198 key

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

## Result

The exact pure six-gram search improves its stated objective under the
one frozen CHI-Nov13 square completion, but the resulting p198 text is
still unreadable. **No historical plaintext is accepted.** Its canonical
model optimum is preserved in full so that the result can be assessed
without selecting isolated readable fragments:

```text
O9Y29MLBC16TIU4N0KZ7166SUC002WZPHEEINEMUSIKEHK6SAPMZSO4VJZRJY4SXNBG3C5B19C21UEYEGE39F
```

The chosen losses are at zero-based ciphertext positions
`16,26,37,78,122`, with inserted coordinates `FDGVV`. All **165 observed
coordinates** remain unchanged and in their original relative order.
The exact optimum covers every five-loss geometry and every filling of
the missing coordinates under this fixed complete key:

\[
\binom{170}{5}6^5=8,670,506,592,384
\]

loss/fill witnesses. Every one of the 15,504 column allocations completed;
the search reached at most 16,807 active states and used no beam pruning.

## Why this is still a conditional experiment

The preceding [six-gram calibration](../p198_joint_six/README.md) recovered
the entire CHI-Nov13 synthetic control using its supplied **true complete
square**. That result motivated this one historical follow-up.

The historical run instead supplies a frozen **heuristic completion** of
the recorded partial square. Fourteen square labels are still hypotheses
in that supplied key. The search also assumes that the 165-coordinate
source lost exactly five coordinates from a 170-coordinate frame. Neither
the completed key nor the damage model is established by a language score.

At the newly selected geometry, 81 plaintext positions are singleton
domains under the supplied complete square before the five gap values
are filled. Only **48** are singleton under the recorded **partial** square.
Even those 48 are conditional on the selected geometry. These counts
therefore do not represent newly recovered source letters.

The exactness claim covers this fixed completion and transposition only.
It does not bound other completions of the partial square, other keys,
or substitutions, insertions and other transmission damage. Success on
one synthetic key does not supply the missing historical evidence.

## Comparison with the earlier four-gram optimum

The new six-gram optimum has integer score **−12,562,934,248**, or mean
**−9.360115415**. The earlier [exact joint four-gram optimum](../p198_joint_exact/README.md),
rescored with the same six-gram table, has mean **−9.574241561**. The new
geometry improves the six-gram total by **287,395,248** integer units,
equivalently **0.214126146** in mean score.

| Feasible candidate | Four-gram mean | Six-gram mean | 30/70 mixed mean |
| --- | ---: | ---: | ---: |
| Earlier exact four-gram optimum | −7.703862272 | −9.574241561 | −9.013127774 |
| New exact six-gram optimum | −9.031523626 | −9.360115415 | −9.261537878 |

This table compares two feasible texts; no full historical mixed-objective
search is reported. The differing preferences show why a single score
must not be confused with a historical reading.

A separate Python finite-domain dynamic program optimizes the six-gram
fill values while holding the earlier four-gram loss mask fixed. Its best
score is still **−9.574241561**, so the reported improvement genuinely
requires changing the geometry within this fixed key. Some alternative
fills tie at that old-mask score; the exact records retain the independently
chosen lexical completion as well as the original four-gram candidate.

## Verification and reproduction

[results.json](results.json) records the completed and padded ciphertexts,
full conditional plaintext, all partial-square letter domains, exact
score components, earlier-mask comparison, and provenance hashes. Each
winner is independently decrypted, rescored and re-encrypted; removing
the five inserted coordinates recovers the original received source.

The experiment reuses the independently reviewed
[five-letter-context engine](../p198_joint_six/exact_joint_six.cpp).
It verifies the frozen calibration result and source inputs before running.
The original model tables are hash-pinned; their four- and six-gram scores
come from the same independent training corpus. The record reports a
canonical optimum without claiming that every tied optimal plaintext
has been enumerated.

To repeat the complete search with Python, a C++17 compiler and the pinned
models available:

```sh
python3 experiments/p198_six_historical/compute.py \
  --quad /tmp/adfgvx-models/german_military36_quad.bin \
  --six /tmp/adfgvx-models/german_military36_sixgram.bin \
  --work-dir /tmp/adfgvx-six-historical-reproduce \
  --verify
```

Omit `--verify` to regenerate the report. The output scope remains the
same fixed key and five-deletion hypothesis.

A fast check without model files or a compiler is also available:

```sh
python3 experiments/p198_six_historical/verify_recorded.py
```

It verifies the recorded source witness, conditional key-domain counts,
prior feasible candidate, score/display arithmetic and file hashes. It
does not rerun optimization or verify individual model-table lookups,
so it does not independently prove global optimality.
