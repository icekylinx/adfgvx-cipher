# p175 C3: withdrawal from the Danube and Sereth front

**Source analysis and verification: icekylinx and GPT-6 Astra Pro.**

A corrected source frame makes the formerly unread third part of the
10 November six-part message readable. Its candidate reports a withdrawal
from the Danube and Sereth front toward the mountains and a route through
Kronstadt and Hermannstadt. The exact candidate is:

```text
OKMXGEHTHEUTENACHTVONDONAUXUNDSERETHFRONTAUFGEBIRGEZURUECKXWIRDUEBERXKRONSTADTXHERMANNSTADTXRICHTUNGXKLUZENBURG
```

This is a **conditional source edition**. There are multiple equally
cheap source alignments, and the complete wording is an editorial
candidate, not a uniquely established historical plaintext. Read the
[case](../../cases/military/p175_c3_withdrawal_followup.md) for the raw
reading, readable German, source sequence and historical limits.

## What the page actually provides

The [frozen source package](../romanian_ultimatum_companions/inputs.json)
contains **217 literal slots**, including four printed dashes. An enlarged
[header crop](../romanian_ultimatum_companions/sources/p175_C3_heading_detail.png)
unambiguously reads **RICHI-222**. Thus **five unprinted coordinates**
are needed if that header length is accepted. The earlier 232 reading
and fifteen-coordinate estimate were transcription errors and are
excluded from this analysis.

The [local source region](sources/p175_C3_gap_region.png) shows no marked
omission or unusual blank at the accepted positions. A missing whole
five-letter group is a reasonable model to investigate, but its location
is not marked on the page. The original unread record remains frozen in
the earlier package; this follow-up supplies a new, separately qualified
reading of that same physical record.

## Complete enumeration of one contiguous missing block

For a 217-slot source, there are **218** possible positions for inserting
one block of five erased coordinates, including both ends. Every position
is evaluated with the unchanged **Nov10–12** square and ranks. The initial
screen makes no observed-coordinate repairs and supplies no missing value.

Two already frozen models rank these partial readings: the military-book
four-gram model and a half-book, half-radio mixture. Both rank insertion
before source coordinate **96** first. Nearby positions also produce
coherent readings. The models share a component; agreement is not two
statistically independent historical witnesses.

The primary screening objective is the mean marginal log10 probability,
with a uniform-symbol adjustment of `log10(36)` for each unknown position
in each four-gram. It is a heuristic: some cipher-derived domains are
narrower than 36 symbols. Unadjusted marginal and completely known-window
scores are retained as secondary diagnostics. The rule and newly composed
control texts were frozen before viewing the target's ranking.

For the complete candidate above, the exact observed-coordinate repair
minimum over all 218 positions is **four substitutions**. Six positions
tie:

```text
95, 96, 98, 99, 100, 101
```

All six also require the **four printed-dash fills** and **five unprinted
coordinate fills**, separately identified in the certificate. Restricting
the missing block to the **45 existing group boundaries** leaves two
minimum-cost placements, **95 and 100**. That further restriction remains
an assumption about how the material was lost.

The main case uses **95**, the smallest tied source index, as a stable
representative. This is a presentation convention, not evidence that 95
is historically preferable to the other five minima or to the model's
first-ranked 96.

## A broader exact alignment check

Allowing five missing coordinates to occur at arbitrary positions changes
the minimum. For this fixed candidate, a dynamic program examines all
`C(222,5)` possible missing-position sets without enumerating them one
by one. It finds a minimum of **three observed-coordinate substitutions**
and exactly **six** optimal paths. All use a local **1 + 3 + 1** loss
pattern. Their missing positions in the complete 222-coordinate frame are:

| First missing coordinate | Middle missing run | Last missing coordinate |
|---:|---|---:|
| 95 | 98–100 | 102 |
| 95 | 98–100 | 103 |
| 95 | 98–100 | 104 |
| 96 | 98–100 | 102 |
| 96 | 98–100 | 103 |
| 96 | 98–100 | 104 |

The recurrence uses source position `i` and missing-coordinate count `k`.
At complete-cipher position `i+k`, it either consumes the observed source
coordinate, paying one if a known value disagrees with the candidate, or
inserts a missing coordinate at zero observed-substitution cost. Printed
erasures also have zero observed-substitution cost. Counts from tied
minimum branches are added. The certificate includes every state and
enumerates all six optimal paths.

These broader alignments have the same complete candidate ciphertext,
but imply a different loss pattern. This establishes the candidate's
exact minimum within each stated family; it does not choose the historical
loss process or prove that no other plaintext would also be plausible.

## Exact source costs and what remains conditional

For the representative one-block placement at 95:

| Item | Value |
|---|---:|
| Physical records | 1 |
| Printed source slots | 217 |
| Observed valid coordinates | 213 |
| Working frame | 222 |
| Plaintext positions | 111 |
| Raw fixed labels under this frame | 102 |
| Candidate fixed labels | 111 |
| Observed-coordinate substitutions | 4 |
| Printed-dash fills | 4 |
| Unprinted-coordinate fills | 5 |

The substitutions, in zero-based **source** coordinates, are
**97 G→X, 172 D→A, 174 F→D, and 209 V→F**. The printed-dash fills are
**57→D, 58→D, 59→F, and 119→V**. The inserted block is `VVGXX`.
Every alternative's separate mapping and repair list is retained.

The final raw `0` in `KLUZENBUR0` is changed through the explicit source
209 repair; no numerical key label is reassigned. The spelling
**KLUZENBURG** is retained and is not silently expanded to another
place-name spelling. `OKM`, `SERETH` and the complete connective wording
remain part of the stated editorial candidate.

Before selecting a frame, the common singleton reading across all 218
one-block layouts contains **zero fixed positions**. Consequently, the
102 raw fixed labels above are conditional on the chosen geometry. The
certificate also gives the unrepaired consensus of the six minimum-cost
candidate alignments, which fixes 96 positions. Neither count is evidence
of a geometry-independent complete plaintext.

## Fresh controls and the unfavorable results

Three new, explicitly fictional German message fragments of exactly
111 positions were encrypted with the same published key. For each,
five coordinates were removed at each of four predeclared locations:
**0, 47, 109, 217**. The same four source positions as the historical
printed dashes were masked. This creates **12 truth-known controls**.
Some true frames are tied because adjacent cipher coordinates agree;
the evaluation retains every zero-conflict alignment with the known
truth rather than counting only the originally selected loss position.

| Objective: controls whose first-ranked layout is truth-compatible | Book | Radio/book |
|---|---:|---:|
| Predeclared adjusted marginal objective | 12 / 12 | 12 / 12 |
| Unadjusted marginal diagnostic | 11 / 12 | 9 / 12 |
| Completely known-window mean diagnostic | 10 / 12 | 9 / 12 |

The controls have exact known plaintext and no added observed-coordinate
errors. They demonstrate this bounded screening procedure, not a success
probability for the damaged historical text. All layouts and all
secondary failures remain in [screen_results.json](screen_results.json).
No model was trained or changed for this target.

## Cross-copy and prior-scope checks

A literal ten-coordinate anchor search compares this source with all
**788** frozen OCR corpus blocks. Its own OCR block matches extensively.
The only different-page hit is one ten-coordinate match in a p179 block;
no independent copy is accepted. The full hit list, search rules and
corpus hash are included in the certificate.

[prior_candidates.json](prior_candidates.json) freezes every retained
p175 C3 row from the two earlier candidate caches. Their OCR source had
dropped the full printed `AD---` group. No Nov10–12 reading was retained
for this individual block in those bounded caches. That is a statement
about prior repository screening, not proof of historical priority.
The unchanged published key retains Lasry and colleagues' credit; the
adjacent p176a challenge retains Norbert and Max Baertl's earlier credit.
Other message parts supply context, not independent proof of missing
coordinates in C3.

## Reproduce

From the repository root:

```sh
python experiments/p175_c3_gap_followup/verify.py --verify
python experiments/p175_c3_gap_followup/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
python experiments/p175_c3_gap_followup/verify.py --verify --book-model /path/to/german_military37_quad_marginal.bin --radio-model /path/to/radio_book37_quad_marginal.bin
```

The default standard-library verification recomputes all source frames,
controls, scores, ranks, candidate costs, dynamic-program states and
optimal paths. It uses **11,913** frozen queried model cells per model,
with binary provenance hashes, instead of requiring full model binaries.
The optional model arguments check every queried cell against the exact
hashed binaries. The PDF option additionally checks the original PDF
and all source crop pixels using PyMuPDF and Pillow. No temporary cache
is needed. [edition_inputs.json](edition_inputs.json) binds every frozen
dependency, and [certificates.json](certificates.json) contains the full
source and candidate position ledgers.
