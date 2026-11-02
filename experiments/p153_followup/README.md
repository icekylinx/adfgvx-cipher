# Page 153 follow-up: replay, key reuse and completion limits

Authors: **icekylinx and GPT-6 Astra Pro**.

This package records the decisive solver replay and bounded follow-up tests
after the page-153 partial recovery. It leaves the canonical historical
certificate and source transcription unchanged.

## Canonical replay

The component-column solver was freshly compiled from the canonical repository
source. Replaying the archived warm input, with only its model path changed,
reproduces the **entire discovery trace byte for byte**: the same 18-column
ranks, complete search-label square, score and two raw decodes.

`canonical_warm_replay.json` records source, binary, model, input and trace
hashes. `canonical_warm_replay.jsonl` is the reproduced trace. This is a replay
of the decisive warm stage from the preceding unreadable blind fit, not a new
end-to-end search. The arbitrary fitted numeral labels are still not accepted
historical digits.

After building the pinned models and solvers, the same replay template can be
used from the joint-search directory:

```sh
cd ../joint_search
bin/joint_rectangle_warm < ../p153_recovery/warm_replay.in > work/p153_warm_replay.jsonl
```

## New transposition reuse

The recovered page-153 transposition was applied to all 22 canonical transcripts
with the conservative 19-letter square. Odd input was skipped rather than
silently shortened or padded. The direct results are in
`direct_partial_square_screen.json`.

Further fits kept these new ranks but allowed an entirely different bijective
square. The previous page-153 square was only a mutable warm start. Every
surviving half-coordinate was retained by the exact-domain four/six-gram
objective.

| Target | Cases | Restarts per case | Proposals per restart | Requested slots |
| --- | ---: | ---: | ---: | ---: |
| p73 | 1 | 500 | 60,000 | 30,000,000 |
| p170 | 1 | 500 | 60,000 | 30,000,000 |
| p198, conditional five-coordinate gap | 34 | 40 | 60,000 | 81,600,000 |
| Total | 36 | | | 141,600,000 |

The p198 cases insert exactly five erased coordinates at positions
`0, 5, ..., 165`, preserving all 165 received coordinates. The 170-coordinate
result is an explicitly conditional omission model, not an established source
correction or a recovery of the missing symbols.

**No coherent additional historical plaintext emerged.** This is a bounded
negative search, not evidence excluding reuse under another square, geometry,
corruption model or search budget. All 36 final records, their exact seeds,
input strings and best outputs are in `new_rank_cases.json`; the concise result
is `new_rank_summary.json`.

For a single-case replay, using the canonical exact-domain engine and pinned
models:

```sh
python3 replay_rank_fits.py --solver ../joint_search/bin/joint_domain_subsolve6 --quad ../joint_search/models/german_military36_quad.bin --six ../joint_search/models/german_military36_sixgram.bin --case p73 --output work/p73_replay
```

Omit `--case` to replay all 36 cases. The driver checks model hashes and
independently checks each resulting decryption. Overlapping language windows
form a composite objective; a high score is not a plaintext certificate.

## Digit-placement convention

The reported p217 square uses the adjacency convention `A0, B1, ..., J9` in a
filled alphabet sequence. Applying that convention to the new p153 partial
square would be tempting but unsupported.

The compatibility test considers sixteen ordinary row/column routes, varying
both axis directions and serpentine traversal, each with and without cyclic
wrap. **All 32 variants contradict the 19-letter p153 core.** For example,
ordinary row-major traversal has known `M` immediately after `C`, where the
rule would require `2`; ordinary column-major traversal has known `Z` there.
The reported p217 full square passes the intended positive control.

This is only an exclusion of the specified adjacency rule and route family.
It does not cover arbitrary coordinate-label permutations, different digit
mappings, other square generators or extra source errors. No p153 digit is
assigned. The reported p217 values are used as an implementation control, not
as a new resolution of the source's handwriting ambiguity.

```sh
python3 check_digit_convention.py --output work/digit_convention.json
```

The full result is in `digit_convention_check.json`.

## Independent conditional-width review

`even_width_independent_review.json` records a fresh strict compilation and
rerun of the separate even-width validator, all seven archived historical
outputs matched, and the independent substring-exclusion proof reproduced.
The total is 2,853,839 first-message segmentations over widths 14 through 26
in steps of two. This is a post-discovery consistency review conditional on the
sixty-letter crib, not another blind recovery or unrestricted uniqueness proof.

Models, executable binaries, downloaded books and bulk search logs are omitted.
The canonical model builder and solver sources live in the adjacent
`joint_search` package. This package's source metadata and manifest pin the
inputs and small results needed to reproduce the reported experiments.
