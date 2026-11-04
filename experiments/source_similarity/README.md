# Direct source retrieval for p73, p170 and p198

**No additional parallel transmission was established.** This experiment compares
the three open ciphertexts directly with all 788 extracted Childs OCR blocks. It
retrieves the known p152, p158 and p109 relationships and three deliberately damaged
controls, but the new targets produce only short local resemblances. The original
page images were checked for each target's highest-scoring candidate. None
supports a plaintext or a change to the case status.

Research and implementation: **icekylinx and GPT-6 Astra Pro**.

## What was compared

The inputs are the unchanged analysis transcriptions in
[`data/messages.json`](../../data/messages.json) and the 788 raw blocks in
[`p153_corpus/inputs.json`](../p153_corpus/inputs.json). Printed five-letter
grouping is removed; existing erasures remain `?`. The targets have 178, 106 and
165 coordinate slots respectively. Each target's own OCR block is excluded from
ranked results and from the corresponding shuffled controls.

Four complementary measurements are calculated:

| Measurement | Exact definition | Intended use |
| --- | --- | --- |
| Longest exact run | Longest common contiguous substring of known coordinates; `?` breaks a run | Detect a preserved stretch without an alignment model |
| Shared multigrams | Multiset intersections of overlapping known 5-, 7- and 9-coordinate substrings | Retrieve similarity independent of printed grouping |
| Affine local alignment | Known match +2, known mismatch −3, erasure comparison 0; each gap run costs 3 for its first slot and 1 for subsequent slots; both ends free | Find a damaged excerpt inside a longer transmission |
| Full-query fitting | Unit-cost insertion, deletion or known substitution; erasure comparison 0; all query coordinates consumed, with free corpus prefix and suffix | Check whether a proposed longer source explains the whole target |

No key, language score, proposed plaintext or coordinate correction enters
retrieval. The alignment is exact for the stated scoring rule. The rules are
heuristics for finding sources, not probabilities of a historical relationship.

There are **26,792 comparisons**: 34 queries against 788 blocks. The 34 queries
comprise seven real input layers, three seeded controls and 24 shuffled controls.
[`results.json`](results.json) records input hashes, ranked hits, exact alignment
traces, seeded damage positions and all control outcomes.

## Calibration on established relationships

The controls use existing source relationships, not newly claimed discoveries.
Their historical interpretation and attribution remain in the linked case files
and certificates.

| Query | Expected source | Rank by local score | Local score | Longest exact run |
| --- | --- | ---: | ---: | ---: |
| [p152](../../cases/pages/152.md#edition-cases-p152) | p136 B, part 1 | 1 | 167 | 34 |
| [p158](../../cases/pages/158.md#edition-cases-p158), augmented layer | p168 C; p159 B; p168 D; p159 C | 1, 2, 3, 4 | 213, 213, 184, 177 | 41, 37, 50, 46 |
| p158, typed-only layer | The same four components | 1, 2, 3, 4 | 213, 213, 184, 180 | 41, 37, 50, 46 |
| [p109](../../cases/pages/109.md#edition-cases-p109), raw D | p109 B | 1 | 303 | 23 |
| p136 B1 with a five-coordinate deletion and four erasures | p136 B, part 1 | 1 | 601 | 100 |
| A 106-coordinate p136 B1 excerpt, then a five-coordinate deletion and three erasures | p136 B, part 1 | 1 | 189 | 45 |
| p109 B with a five-coordinate deletion and four additional erasures | p109 B | 1 | 455 | 66 |

The source sequences for the synthetic controls come from the
[p152 certificate](../../data/certificates/p152.json) and the
[p109 parallel certificate](../../data/certificates/p109_parallel.json). Their
parent hits are calibration only and are excluded from any claim of a new
relationship. In particular, the short excerpt control demonstrates retrieval
after a missing five-coordinate group without requiring the query to be a
complete message. These examples do not establish exhaustive recall for other
forms of damage.

## Results for the open cases

| Target | Highest-scoring non-self OCR candidate | Local score | Query span used | Known matches / substitutions / gap slots | Maximum exact run anywhere in the corpus |
| --- | --- | ---: | --- | --- | ---: |
| [p73](../../cases/pages/073.md#edition-cases-p73) | p105 C, part 1 | 23 | `[50:83)` | 26 / 2 / 11 | 9 |
| [p170](../../cases/pages/170.md#edition-cases-p170) | p110 C | 27 | `[35:55)` | 18 / 1 / 2 | 8 |
| [p198](../../cases/pages/198.md#edition-cases-p198) | p154 A, part 2 | 21 | `[110:133)` | 20 / 2 / 5 | 9 |

Spans are zero-based, half-open coordinate offsets in the unchanged query. Gap
slots are counted on either side of the local alignment, so a local span is not
an uninterrupted exact match. The maximum exact-run column is a separate
whole-corpus measurement and need not refer to the highest local-score hit.

Eight composition-preserving shuffles per target give maximum local scores of
19–24 for p73, 19–22 for p170 and 18–23 for p198. The p170 hit is stronger than
these eight shuffled examples, but uses only 20 of its 106 query coordinates.
After image review, fitting the entire p170 query to p110 C still costs 58
unit edits. This does not establish a common transmission. Eight shuffles are
descriptive controls, not a calibrated significance test or a completeness
claim.

The best full-query fitting score for all three targets is instead an
erasure-heavy block, p127 OCR block 3, with 50 unknown coordinates. Its costs
are 80, 41 and 74 respectively. Because matching an erasure costs zero, this
ranking illustrates why fitting cost alone cannot certify a source match.

## Inspection of the original pages

The highest local-score candidate for each target was independently transcribed
from the [Childs scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The PDF hash, exact headers, literal printed rows, OCR and reviewed layers, and
recomputed alignments are in
[`source_inspections.json`](source_inspections.json). The printed pages are 105,
110 and 154; their PDF pages are 108, 113 and 157.

| Candidate | What image review establishes | Effect on the candidate match |
| --- | --- | --- |
| p105 C1 | The page prints 238 coordinates. OCR omitted the first 40-coordinate row and inserted an erasure later, leaving 199 slots. | Local score remains 23 and whole-query fitting cost remains 98. Restoring the missing row does not extend the resemblance to p73. |
| p110 C | The page prints 398 coordinates. OCR gives 399 slots, including an extra `V` and two erasures where source letters are readable. | Local score remains 27 and fitting cost remains 58. The 20-coordinate p170 resemblance survives image review, without extending to the full query. |
| p154 A2 | The page itself prints 118 coordinates, including the six-letter group `VDFDVD`, although the header says `RICHI-162`. | Local score remains 21. Reading the OCR erasure as the printed `D` changes full-query fitting cost from 93 to 94. No length repair or padding is imposed. |

These are supplementary source transcriptions. They do not replace the challenge
transcriptions, establish an unknown key, or supply a candidate plaintext. Only
these three leading candidates received new image transcription in this
experiment; the 788-block corpus remains an unverified retrieval aid.

## Reproduce

From the repository root, with Python 3 and a C++17 compiler:

```sh
python experiments/source_similarity/retrieve.py
python experiments/source_similarity/review_sources.py --check
```

To bind the visual inspection record to a local copy of the source PDF:

```sh
python experiments/source_similarity/review_sources.py --check --pdf /path/to/childs.pdf
```

[`align.cpp`](align.cpp) implements the three sequence-alignment measurements
with two-row dynamic programming. [`retrieve.py`](retrieve.py) also calculates
multigram intersections and checks the compiled results against independent
full-matrix Python calculations on 36 short pairs covering erasures, endpoints,
insertions and deletions. Every retained target alignment has a checked
traceback. [`review_sources.py`](review_sources.py) contains the literal
image-reviewed transcriptions and independently recomputes their results.

The negative result is bounded by this corpus, these transcriptions and these
direct comparisons. A badly omitted OCR passage, an absent source page, or a
re-encrypted/retransposed copy can evade direct ciphertext similarity. The
experiment does not prove that a parallel source does not exist.
