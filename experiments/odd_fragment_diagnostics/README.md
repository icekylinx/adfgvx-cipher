# Bounded diagnostics of three unaccepted odd-length fragments

Prepared by **icekylinx and GPT-6 Astra Pro**.

**Result: no accepted complete plaintext.** This package preserves finite
diagnostic work on p159 A, p162 C1 and the unlabelled p163 fragment. It adds
no catalogue record, accepted case, key assignment or first-decipherment
claim. A higher language score is not an accepted reconstruction. Failure
within these finite configurations does not exclude a period key or a broader
damage model.

## Sources and scope

| Source | Literal source slots | Source condition | Evidence |
| --- | ---: | --- | --- |
| p159 A | 271 | `RICHI-272`; includes the four-character group `GDDA` and final `FV` | [Fresh primary-page image](sources/childs_p159_full.png) |
| p162 C1 | 117 | Unknown RICHI length; printed `1 TL` and “missed first part of this message” | [Fresh section crop](sources/childs_p162_C.png) |
| p163 unlabelled | 121 | `J'md`; no surviving length or part label | [Existing withdrawal source crop](../withdrawal_recovery/sources/childs_p163_A15_A16.png) and [unchanged upstream input](../withdrawal_recovery/inputs.json) |

All literal body slots in these three transcriptions are ADFGVX coordinates.
Their odd counts prevent ordinary pair decoding without an additional frame
assumption. The p163 position between parts 15 and 17 suggests a part number
but does not establish one. The p162 annotation does not specify the amount
or position of missing material. None of the explored frames is adopted as
the historical transmission.

[inputs.json](inputs.json) binds the original transcriptions, all retained
runtime scripts/results, the unchanged 25-key register, the original PDF,
new crop pixels and existing p163 dependencies by SHA-256. The original
scripts under `original/` preserve their exact historical bytes, including
workspace paths; use the portable verifier below to replay the package.
The inherited keys retain the historical and research credits recorded in
[data/keys.json](../../data/keys.json), including J. Rives Childs, George
Lasry, and Lasry–Niebel–Kopal–Wacker. No published square or rank list changes.

## Exact finite budgets

Each four-model screen tests insertion or deletion in either the transmitted
coordinate stream or the fractionated stream after inverse column
transposition. An insertion tests every boundary and each of six coordinate
values. A deletion tests every received index. These are separate assumptions:
a change before fractionation pairing is not equated with a change in the
received transposition stream.

| Campaign | Frozen scope | Parameter evaluations | Retained candidates |
| --- | --- | ---: | ---: |
| p159 A: published keys | 25 keys × four single-coordinate models | 95,150 | 500 |
| p162 C1: published keys | 25 keys × four single-coordinate models | 41,250 | 500 |
| p163 fragment: published keys | 25 keys × four single-coordinate models | 42,650 | 500 |
| p159 A: exploratory ranks | Nov7–9 square; unchanged ranks plus every one-pair rank swap among 20 columns, 191 variants; 272 boundaries × 6 values each | 311,712 | 573 |
| p162 C1: prefix/suffix | Nov7–9 only; odd missing lengths 1 through 101, at either end | 102 | All 102 frames |
| p163 fragment: prefix/suffix | Same bounded lengths and key | 102 | All 102 frames |

The first three rows total **179,050** evaluations. With the exploratory
ranks and prefix/suffix diagnostics, the total is **490,966 parameter
evaluations**, not distinct plaintexts, repaired streams or independent
witnesses. The rank campaign's unchanged branch repeats **1,632**
configurations from the earlier p159 single-insertion screen. Other equivalent
insertions/deletions can also produce identical streams; they are not
deduplicated in these counts.

The published-key budgets are independently reconstructed as
`25 × (2 × 6 × (n + 1) + 2 × n)` for each source length `n`.
The p159 files split this total into 40,800 transmitted insertions and
54,350 configurations in the other three models. Each published-key/model
run retains five candidates; each exploratory rank variant retains three.
Global top lists repeat candidates from those run lists and add no evaluations.

## Three different coverage rules

Every reported score is a mean over **fully determined four-gram windows**;
windows containing `?` are excluded. The three actual rules must remain
distinct:

1. Both p159 published-key campaigns and its exploratory rank campaign require
   at least **100** fully known windows.
2. The p162/p163 four-model screens use
   **`floor(0.75 × total four-gram windows)`**. The original result prose says
   “at least 75%”, but the original code uses integer truncation. For p162,
   insertion/deletion minima are 42/41 windows; for p163 they are 43/42.
   This package preserves the actual computation and original files.
3. The two prefix/suffix diagnostics require only **12** fully known windows.
   This substantially weaker coverage rule is not replaced by the 75% rule.

An ineligible configuration is assigned sentinel score `-100`; low-coverage
key branches remain in the run records. The prefix/suffix lists include all
frames, including those below their threshold. The scores are uncalibrated
language diagnostics; averaging only known windows can still favor unevenly
informative candidates.

The initial unknown-rich scoring issue remains material: the frozen marginal
model gives the all-unknown four-gram `????` a score of zero. That value is not
evidence of readable language. An all-unknown square has zero fully known
windows and is ineligible under every retained rule here. No such result is
promoted because a marginal score looks numerically favorable.

The best retained exploratory rank score is approximately **−7.585**, compared
with approximately **−7.681** for the unchanged Nov7–9 transmitted-insertion
branch. Neither candidate is accepted as coherent complete German. This small
score improvement does not justify modifying the published ranks.

## Verification

The default verifier uses the standard library and an independent sorted-column
inverse and square-domain implementation:

```sh
python experiments/odd_fragment_diagnostics/verify.py --verify
```

It checks every bound file, literal source, declared geometry and evaluation
count; replays all **2,073** retained single-change/rank-variant candidates and
all **204** prefix/suffix frames; checks all reported unresolved domains and
known-window counts; and checks that global lists are assembled from the
stored run lists. It preserves the published key and separately reconstructs
each exploratory rank swap.

**Default verification does not recompute language scores or exhaustive
ranking cutoffs.** Checking the ordering of stored scores is not a model-score
validation. For a full finite score/rank-cutoff replay, supply the original
37-symbol float32 model; NumPy is then required:

```sh
python experiments/odd_fragment_diagnostics/verify.py --verify \
  --quad /tmp/adfgvx-models/german_military37_quad_marginal.bin
```

The model SHA-256 is
`2ccbde739f8b5b50ef81970c1c0bb7d1fd40a3a5a6b9914156bd947a90fcef8e`.
The archive-relative equivalent is
`reproduction-assets/book-models/german_military37_quad_marginal.bin`.
The optional run scores all 490,966 parameter configurations, checks each
retained score within absolute tolerance `1e-12`, and independently recomputes
each run's retention cutoff. Equal-score alternatives at a cutoff remain
ties; NumPy's unstable tie order is not historical evidence. No complete
historical array ranking all candidates was retained beyond the recorded
candidate lists; all 191 column-rank variants themselves are preserved.

To also regenerate the two new p159/p162 source images from the pinned PDF,
add `--pdf`; this optional operation requires PyMuPDF:

```sh
python experiments/odd_fragment_diagnostics/verify.py --verify \
  --quad reproduction-assets/book-models/german_military37_quad_marginal.bin \
  --pdf /path/to/adfgvx-childs.pdf \
  --output /tmp/odd-fragment-verification.json
```

The p163 crop and upstream transcription are checked as existing hash-bound
dependencies. This option does not claim a new pixel regeneration of that
older crop. The primary PDF is external to the delivery archive. All checks
are read-only unless an explicit `--output` report path is supplied.
