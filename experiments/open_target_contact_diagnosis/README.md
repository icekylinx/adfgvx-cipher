# Seven open targets: coordinate contacts and coincidence

**Classical cryptanalysis and source review: icekylinx and GPT-6 Astra Pro.**

In the declared source frames, all six rankable open targets have weaker
coincidence separation than six nearby native controls. The seventh target,
p194 D1, has **no fully observed plaintext pair** in the ten near-period
prefix/suffix models examined. These results help choose the next research
step. **All seven bodies remain open; no key or plaintext is accepted.**

[Inputs](inputs.json) bind every source, header and rank hypothesis.
[Certificates](certificates.json) retain exact integer counts, source-preserving
model scopes, every shuffle maximum, native control outputs and the invariance
proof. The [verifier](verify.py) recomputes the complete analysis in seconds;
it uses no dictionary, language model or plaintext crib.

## What is measured

For a fixed coordinate frame and column rank order, invert the columnar
transposition. Count only plaintext positions whose two coordinates were
actually received and valid. Put their observed pairs in a 6 × 6 table
`n_ab`, with `m` complete pairs. Let `Q_cell` be the sum of `n_ab(n_ab−1)`,
and let `Q_row` and `Q_column` be the corresponding sums over its marginal
row and column counts. The diagnostic is

\[
S=\frac{Q_{cell}}{m(m-1)}-
  \frac{Q_{row}Q_{column}}{[m(m-1)]^2}.
\]

The first term is the pair index of coincidence. The second is its expectation
when the row and column labels are paired independently with those same
marginals. Their difference measures excess repeated contacts. The square's
letter assignments never enter this calculation, so an unknown square does
not obstruct the test. A score is undefined when fewer than two complete pairs
are present; missing halves are never filled to manufacture a statistic.

Every tested rank order is one of **25 recorded vectors**, including the
June CHI example whose whole square is unknown. Their names identify rank
vectors only. A favorable result for a vector labelled `Nov13-15b` does not
establish that period, its square, or its applicability to the target.

## Exact source frequencies

Columnar transposition preserves these one-coordinate counts. They describe
the received material, before any modeled addition:

| Source | A | D | F | G | V | X | Unknown slots | Native slots |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p73 | 16 | 57 | 26 | 28 | 15 | 34 | 2 | 178 |
| p170 | 27 | 7 | 8 | 29 | 22 | 13 | 0 | 106 |
| p198 | 18 | 18 | 35 | 24 | 35 | 35 | 0 | 165 |
| p70_B1 | 35 | 38 | 27 | 28 | 27 | 44 | 7 | 206 |
| p127_B2 | 20 | 11 | 17 | 16 | 14 | 26 | 48 | 152 |
| p145_A | 43 | 22 | 30 | 18 | 31 | 43 | 5 | 192 |
| p194_D1 | 12 | 2 | 6 | 7 | 9 | 9 | 0 | 45 |

p198's five hypothesized missing coordinates and p194 D1's 169 modeled missing
coordinates are **additional unknown slots**, not received masks. No observation
is changed, excluded or silently moved in the source transcription.

## Matched comparisons

For each ranked body, 128 deterministic shuffles preserve its exact observed
coordinate multiset and every printed mask position. Each shuffled body is
optimized over the **same whole rank/geometry family** as the historical body.
This controls for selecting the largest statistic from that declared family.

The literal-frame families contain 25 rank vectors. The p198 family contains
**4,150 models**: 25 rank vectors times all 166 placements of five consecutive
unknown coordinates in a 170-slot frame. The original has 165 coordinates and
prints `CHI-170`; neither contiguity nor the missing location is established.

| Open body | Highest-scoring rank/model label | Complete received pairs | Excess coincidence | Shuffled maxima at least as large |
| --- | --- | ---: | ---: | ---: |
| p73 | `Nov13-15b` | 87 | 0.008738 | 22/128 |
| p170 | `Nov10-12` | 53 | 0.009088 | 73/128 |
| p198 | `Nov1-3, gap 0` | 80 | 0.011580 | 38/128 |
| p70_B1 | `Oct4-6` | 96 | 0.004233 | 61/128 |
| p127_B2 | `Nov19-21` | 33 | 0.014140 | 44/128 |
| p145_A | `CHI-Nov13` | 91 | 0.003654 | 109/128 |

These are **descriptive randomization counts, not probabilities that a key or
reading is correct**. The six target values are exceeded by 22–109 of the 128
matched shuffles. They provide no clear rank identification in these families.
The p70 B1 maximum happens to use the expected October rank order, but 61
shuffled maxima are at least as large; that weak ranking does not validate a
replacement square. Likewise, the p198 maximum at an opening five-slot gap is
only a coincidence preference within one loss family.

The nearby source-reviewed controls use their original ciphertexts and literal
frames. Their known keys are used only to evaluate the ranking:

| Native body | Previously established rank vector | Rank within the 25-vector comparison | Shuffled maxima at least as large |
| --- | --- | ---: | ---: |
| p127_B1 | `Nov4-6` | 1/25 | 0/128 |
| p145_B1 | `Nov4-6` | 1/25 | 0/128 |
| p145_B3 | `Nov4-6` | 1/25 | 2/128 |
| p72_A3 | `Oct4-6` | 1/25 | 0/128 |
| p194_C | `Nov13-15b` | 1/25 | 0/128 |
| p194_E | `Nov13-15b` | 1/25 | 0/128 |

All six native controls rank their established vector first, and only 0–2
matched shuffle maxima reach their scores. These are six physical bodies
from five message families, including two parts of the same message; repeated
period keys and adjacent parts are not independent statistical trials.
They demonstrate a useful diagnostic on these bodies, not a general recovery
rate. Their mask patterns and vocabularies also differ from the open fragments.
The certificate preserves all native raw garbles and unresolved square labels;
no edited reading is substituted into the statistic.

## Why coincidence cannot determine the whole key

The p70 B1 frame gives an exact example. At length 206 and width 22, four
adjacent column pairs have height 10 and seven have height 9. Permuting whole
pairs within each height class changes the plaintext order but leaves the
observed cell-contact table unchanged. Swapping the two columns in every pair
transposes the table and swaps its marginals, preserving the same statistic.

Consequently **2 × 4! × 7! = 241,920 distinct rank vectors** share this statistic
with the published October vector. This is a proved invariance family, not a
number of tested independent keys. The verifier checks 64 deterministic source
examples, including the global half swap, and preserves all native masks.
Higher coincidence can therefore help diagnose pairings or choose a bounded
next test, while word order still needs independent constraints.

An additional small exhaustive oracle checks all **4,374** combinations of
six-slot strings over `A`, `D`, `?` and all three-column rank permutations.
It reconstructs column chunks and row order independently, then compares the
exact table counts and rational statistic with the vectorized implementation.

## Source geometry and the next useful questions

| Target | Source qualification and consequence |
| --- | --- |
| p73 | 26 October page/origin markers conflict with the 8 November reception. The literal 178-slot comparison supplies no rank identification. The separate [square-count diagnostic](../open_targets/P73_HISTOGRAM.md) and [primary-source review](../p73_primary_followup/README.md) remain relevant; neither selects a date or key. |
| p170 A | All 106 received symbols are clear, but 106 is handwritten beside RICHI. A complete 106-slot message is only one hypothesis. Source-supported length or an overlapping reception remains more useful than the largest literal-frame score. |
| p198 D | The 165/170 shortfall is real. This comparison covers a single consecutive five-loss model; arbitrary scattered losses, another length, different ranks and other damage remain open. The [exact loss/count constraints](../p198_letter_bounds/README.md) retain their own broader and narrower boundaries. |
| p70 B1 | The source labels 206 slots and records jamming before the body and after its first 30 slots. Its top October-vector score is weak under matched controls. Additional reception evidence or a better supported corruption model is needed. |
| p127 B2 | The source preserves 152 slots with 48 masks. Part B1 under the same clear header is independently readable with the Nov4–6 key; B2's literal layout does not show comparable rank separation. The repeated `XFFGG` groups are real source observations, not permission to delete a group. |
| p145 A | The source says “missed first part” and supplies no total length. Only the five-dash run aligns with the ciphertext; the nine-dash label placeholder remains outside it. The 192-slot literal model is a diagnostic endpoint. A longer clipped original remains possible. |
| p194 D1 | `RICHI-214` accompanies only 45 coordinates. Prefix and suffix placement are separate hypotheses; the source does not establish either. Printed p195 A has a different sender/origin header and is not silently appended. |

For p194 D1, under each of the `Nov13-15a`, `Nov13-15b`, `CHI-Nov13`,
`Nov16-18` and `CHI-Nov8-2026-recovery` vectors, **both** the prefix and suffix
model have exactly **0 complete pairs, 45 half-observed positions and 62 wholly
unobserved positions**. No coincidence score is reported for these models.
An observed half still constrains a letter domain, but it does not fix a label.
The certificate also retains the other twenty rank hypotheses: across all
50 prefix/suffix models, the maximum is only five fully observed pairs.

## Reproduce and inspect the original source

```sh
python -m pip install -r REQUIREMENTS.txt
python experiments/open_target_contact_diagnosis/verify.py --verify
```

This recomputes all target/control tables, all 1,536 shuffled source families,
the exact p198 model family, the p194 ownership counts, the pair-order witnesses
and the tiny independent oracle. NumPy is used for batching; integer fractions
bind the retained statistics and comparisons.

```sh
python experiments/open_target_contact_diagnosis/verify.py --verify --pdf /path/to/childs.pdf
```

The optional command verifies the original PDF byte count and SHA-256 and all
eight recorded source-pixel recipes, including the p194/p195 boundary review.
Without the PDF, the report explicitly marks source-pixel comparison as
unperformed. The recipes are references, not embedded PNG assets. The source
is J. Rives Childs, *General Solution of the ADFGVX Cipher System*; its original
hosted URL and the published period-key provenance remain in the bound inputs
and the repository key catalogue. Earlier source readings retain their credited
authors. This new classical diagnostic is by **icekylinx and GPT-6 Astra Pro**.
