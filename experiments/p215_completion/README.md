# p215: exact model-ranked completions under the earlier geometry

**This experiment recovers no new historical letters.** It finds the exact best
ten completions under each of three specified language objectives while keeping
all 237 valid received coordinates unchanged. It remains conditional on
Norbert's previously published insertion of two missing five-coordinate groups
at original source offsets 30 and 215. The printed header itself says 248
coordinates; the reconstructed rectangle has 258.

The purpose is to separate a source-compatible completion from fluent editing.
The earlier p215 constraint review showed that the known square and this
geometry fix 109 of 129 plaintext characters. Twenty plaintext positions remain
uncertain: nineteen have six choices, and one has 36. Their Cartesian product
contains **6²¹ = 21,936,950,640,377,856** compatible strings. This search does not
reduce that cryptographic ambiguity count.

## Exact optimization and its limits

The dynamic program retains the ten best prefixes for each suffix of length
three or five. Future additive four-/six-gram scores depend only on that suffix
and the current position. Discarding a lower-ranked prefix from the same state
therefore cannot remove one of the global top ten completions. The largest
active state sets have only 36 suffixes for four-grams and 216 for the mixed
model, so this exact calculation is small despite the large completion count.

All comparisons use integers derived exactly from the stored float32 log-table
entries, with scale 2²⁴. The mixed objective is 30% mean four-gram log frequency
and 70% mean six-gram log frequency. Its averaging denominators are cleared
before optimization. Equal objectives are ordered lexicographically. Small
independent exhaustive controls verify both recurrences and the tie rule.

The three models are the independent general German quadgram model, the
independent military German quadgram model, and the military four-/six-gram
mixture. Their sources and exact rebuild recipes are in the adjacent
`fixed_search` package. No p215 candidate or challenge plaintext was used in
their training. These additive objectives are language rankings, not posterior
probabilities, confidence levels or evidence that a proposed erased symbol
was actually transmitted. Scores from different objectives are not directly
comparable.

## What changes between models

The best completions disagree at two plaintext positions:

| Zero-based plaintext position | Source-supported domain | General four-gram | Military four-gram | Military 30/70 mixture |
|---:|---|---|---|---|
| 25 | `2 7 N Q X Z` | `N` | `2` | `2` |
| 63 | All 36 letters and digits | `L` | `L` | `D` |

At position 63, the six-gram mixture favors the recognizable `ZWODIVISIONEN`
where both four-gram models prefer `ZWOLIVISIONEN`. This is a model effect, not
a newly observed coordinate. Agreement elsewhere is also only model agreement.
All three retain the source-constrained forms `NA6M`, `FLHTTE`, `FRATZ`,
`KOR1S` and `3Y52`; the calculation does not silently normalize those strings.

The best mixed-model completion, reproduced literally, is:

```text
ABSXMILI5XNA6MELDXXS4NXS42XNORFDAKERTSCHXBRINGTENTENDEFLHTTEZWODIVISIONENXNEUSRELAENDERXENGLXUXFRATZGXMITXNOBOHLXKOR1STGOSCHX3Y52
```

This is an explicitly conditional proposal. It should not replace the raw
109-character constraint reading in the main p215 case. Several alternate
completions score almost as well, and no scoring threshold establishes the
historical wording.

## Coordinate certificates and the earlier editorial reading

Every retained completion contains a full plaintext, its exact reencrypted
258-coordinate ciphertext, and all 21 proposed coordinate fills. Eleven fills
correspond to erasures in the received source; ten occupy the two inserted
groups. Each record identifies both its augmented index and its original source
index when one exists. **No known source coordinate changes.**

The earlier Baertl text has 130 letters and is outside this 129-position domain
model. As established in the parent p215 certificate, even its best one-letter
deletion contradicts 27 known coordinates at 20 plaintext positions. The present
completions avoid those contradictions by retaining the source constraints;
they do not prove Norbert's geometry or make Baertl's historical interpretation
correct or incorrect independently of that geometry.

## Reproduce and verify

The code needs only Python's standard library on a little-endian machine.
Reuse the binary models rebuilt by `fixed_search`; do not duplicate its books
or model files in this directory.

```sh
python compute_completions.py \
  --general-quad /path/to/shared-models/german36_quad.bin \
  --military-quad /path/to/shared-models/german_military36_quad.bin \
  --military-six /path/to/shared-models/german_military36_sixgram.bin

python verify_completions.py --output verification.json
```

The standalone verifier independently reconstructs the geometry, the domains,
the unchanged count 6²¹, every proposed fill and all source-preserving
reencryptions. It does not need the language models and does not check ranking.
The computation script reproduces the exact rankings and includes its own
exhaustive small-case controls. `conditional_completions.json` contains all
thirty candidates, with ten for each objective. `input.json` records the
source certificate and the earlier readings for attribution.
