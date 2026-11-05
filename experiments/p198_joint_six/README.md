# Exact six-gram calibration of joint decoding

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

## Result

With the supplied true CHI-Nov13 key, both the **pure six-gram** and the
**30% four-gram / 70% six-gram** objectives recover the complete planted
85-letter control text, the exact five deleted-coordinate positions,
and their original values. The earlier exact four-gram objective selected
a wrong text differing at four letters.

```text
DERSTABMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBITTEWEITEREBEFEHLEUEBERMITTELN
```

Both new canonical optima use loss positions `7,44,81,126,158` with fills
`VAXFG`, exactly matching the planted ciphertext. This is a positive
synthetic calibration under a **known true complete key**. It is not a
historical p198 decipherment or evidence that the same model always works.

| Control | Exact four-gram result | Six-gram result | 30/70 mixed result |
| --- | --- | --- | --- |
| CHI-Nov13 | Four wrong letters | Full text, mask and fill recovered by global search | Full text, mask and fill recovered by global search |
| Nov13-15b | Two wrong letters | A feasible wrong competitor already beats truth; truth cannot be globally best | The same feasible competitor already beats truth; truth cannot be globally best |

The second row is a proved limitation of the objective. Another full
Nov13-15b search is unnecessary to establish that its planted truth cannot
be optimal: an independently re-encrypted feasible competitor already
scores higher. Its global six-gram optimum is not computed here.

Each completed CHI-Nov13 search covers all

\[
\binom{170}{5}6^5=8,670,506,592,384
\]

loss-position/fill witnesses, using all 15,504 column allocations and no
beam pruning. These are witnesses, not distinct plaintexts. The report
returns a canonical optimum; it does not enumerate all tied optimal
plaintexts or claim uniqueness.

## Objective sensitivity and the failed control

All models use the same pinned, independent ten-book training corpus,
with no challenge plaintexts included. Four- and six-gram agreement is
therefore **sensitivity evidence**, not statistically independent evidence.
The [model provenance](../joint_search/models/provenance.json) records
the training sources and hashes.

For the CHI-Nov13 control, the six-gram optimum has mean score
**−6.200452799** and the mixed optimum has mean score **−5.607556329**.
Both are the planted text. The previously wrong four-gram winner is
lower than truth by **0.222218680** in six-gram mean and **0.136471359**
in mixed mean.

For Nov13-15b, the wrong feasible four-gram optimum is:

```text
DERSTARMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBETTEWEITEREBEFEHLEUEBERMITTELN
```

It exceeds the planted truth by **0.107354259** in six-gram mean and
**0.110071678** in mixed mean. The exact integer advantages are
144,088,448 six-gram units and 121,143,278,912 mixed units. These are not
rounding effects. This candidate preserves all 165 observed coordinates
after its five explicit inserted coordinates, so it is a valid competing
witness under the supplied true key.

Separate [held-out-book diagnostics](../open_targets/held-out-controls.md)
compare the same frozen candidates under two books absent from the
original training set. Both books reject the CHI-Nov13 wrong candidate
under six-gram and mixed scores, yet both still favor the Nov13-15b wrong
candidate. Every reported normalization convention is retained. No
held-out model was used to optimize these searches. The check shows that
this particular failure persists beyond the original corpus; it does
not establish that every possible language model must fail.

## Exact five-letter-context algorithm

The [joint four-gram decoder](../p198_joint_exact/README.md) already proves
the column-allocation decomposition, source-coordinate preservation,
prefix dominance and canonical loss/fill tie rule. This extension keeps
the last **five concrete plaintext letters**, sufficient to score the
next six-gram, instead of the last three.

The 16-column geometry keeps the recent ten coordinates in distinct
physical columns. For a column allocated `l` losses, a used-loss count
of zero fixes its recent coordinate, while each positive used count
admits at most six coordinate values. The retained value is already
one of those six values. The same bound therefore applies:

\[
\prod_c(1+6l_c)\leq7^5=16,807.
\]

Both full runs attain that state count. Each visits 1,694,119,422 prefix
states and considers 3,324,639,982 transitions. A 100-allocation pilot is
also recorded, explicitly marked as incomplete and excluded from the
global-optimum claim.

A dense array indexed by `36^5` suffixes would waste memory. The new
implementation stores only active states in reusable open-addressed hash
layers. An epoch stamp clears a layer without repeatedly allocating
nodes. The hash table has at least twice the configured state capacity;
inserting a state beyond the cap throws an error before any approximate
answer can be produced. The recorded runs do not reach that cap.

For the supported maximum of six losses, the used-count/suffix code is
below `64 * 36^5 = 3,869,835,264`, within a 32-bit unsigned integer. Each
six-gram code is below `36^6`, also within that range. The model loader
checks the binary format, exact integer scaling and table size.

### Deterministic score arithmetic

The original float32 log values are exactly represented at scale `2^24`.
The pure six-gram integer objective is their sum over 80 windows.
For the mixed objective, with 82 four-gram and 80 six-gram windows, the
integer coefficients are:

\[
240\sum q_4+574\sum q_6,
\]

with display denominator `10 * 82 * 80 * 2^24`. This is exactly 30% of
the four-gram mean plus 70% of the six-gram mean. Integer arithmetic
prevents accumulated floating-point errors from changing rank or ties.
The resulting scores are additive model objectives, not calibrated
probabilities of a historical reading.

## Controls and independent checks

The wrapper explicitly enumerates all **10,188** loss/fill witnesses in
three short controls of widths 4, 6 and 16, then compares their optima
with the dynamic program under **both** objectives. All six canonical
score/mask/fill results agree. The narrower controls need not obey the
16-column state bound; their actual finite state sets are still searched
exactly. Constant-score four- and six-gram tables verify the first tied
mask `[0,1]` with fill `AA` for both objectives.

For each full result, separate Python code reconstructs the filled
ciphertext, decrypts it, rescales every original model entry, re-encrypts
the plaintext and removes the five inserted coordinates to recover the
source. The planted text is used only after optimization for evaluation.

An independent reviewer also loads the sparse six-gram model into a plain
dictionary instead of reusing the engine's hash lookup, repeats the short
exhaustive controls, and verifies the full witnesses. A deliberately
insufficient state cap is checked to abort without an output result.
The complete search and score records are in [results.json](results.json).

## Reproduce

```sh
python3 experiments/p198_joint_six/compute.py \
  --quad /tmp/adfgvx-models/german_military36_quad.bin \
  --six /tmp/adfgvx-models/german_military36_sixgram.bin \
  --work-dir /tmp/adfgvx-six-calibration-reproduce \
  --verify
```

This verifies the pinned models and source inputs, compiles the C++17
engine, reruns all short controls and both full searches, independently
verifies the outputs and compares the committed report. Omit `--verify`
to regenerate it. Models, executables and intermediate files stay in the
chosen temporary directory.

For a fast check without model files or a compiler:

```sh
python3 experiments/p198_joint_six/verify_recorded.py
```

This checks the recorded source witnesses, prior feasible competitors,
key/mask lengths, exact score/display arithmetic and hashes. It does
not rerun the search or validate individual model-table lookups, so it
is not an independent optimality proof.
