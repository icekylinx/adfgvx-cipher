# Independent counts for the continuation source batch

Prepared by **icekylinx and GPT-6 Astra Pro** on 3 November 2026.

The [count manifest](../data/reviews/continuation_source_count_audit_20261103.json)
records a bounded checkpoint of **16 packages and 34 primary physical
records**. It lists the packages explicitly and retains each record's
literal length, source masks, frame mapping costs, native orphan, raw and
edited counts, and exact substitution/fill ledgers. Optional p144 B and
p158 E1 proposals, p156 A1's alternative source transcription and older
comparison witnesses are excluded from the totals. Later continuation
packages require a separate reviewed addition to this scope.

## Independent reconstruction

The [portable checker](../data/reviews/verify_continuation_source_counts.py)
counts the literal input rows and rebuilds the primary insertion/exclusion
maps from their declared operations. A separate implementation using
explicit ragged rows reconstructs every raw pair, domain and source origin,
then encodes each candidate's fixed labels and prices the resulting
coordinate changes. It imports no repository cipher or experiment-verifier
functions. Only after those calculations does it compare the per-record
certificates and the generators' count summaries.

| Quantity | Reviewed primary total |
| --- | ---: |
| Literal source slots | 5,865 |
| Valid observed coordinates | 5,810 |
| Literal source masks | 55 |
| Excluded source slots | 37: 33 observed coordinates and 4 masks |
| Added slots | 22: 21 initially unknown slots and 1 source-linked A |
| Analysis-frame slots | 5,850 |
| Plaintext positions in those frames | 2,925 |
| Fixed raw positions with every added slot unassigned | 2,837 |
| Fixed positions in the displayed raw frames | 2,838 |
| Fixed positions in the primary candidates | 2,900 |
| Observed-coordinate substitutions | 73 |
| Retained source-mask fills | 38 |
| Inserted-slot fills | 20 |
| Separately supplied source-linked coordinates | 1 |

Frame accounting is **5,865 − 37 + 22 = 5,850**. Of the 55 literal source
masks, four are excluded, 38 are filled and 13 remain unfilled. The 25
unresolved positions in the primary candidates also include unassigned
square cells; an unresolved plaintext position and a source-mask slot are
different counting units. One of p159 A's newly added slots also remains
unfilled; 20 of the 21 initially unknown added slots are filled in the
primary candidates.

### The two raw totals

The p158 E1 edition supplies one A from the independently printed p170 B1
witness before presenting its source-linked raw frame. That raises this
record from **116 to 117 fixed positions out of 118**, accounting for the
difference between the aggregate 2,837 and 2,838. At the initial 14-package
checkpoint the corresponding totals were 2,329 and 2,330. The other declared raw
models leave newly added slots unassigned. Neither aggregate is a count
of fixed positions in the unmodified native frames.

The A is counted once as a source-linked addition. The separate
`source_or_model_erasure_fills` summaries total **58**: 38 retained-source
fills plus 20 inserted-slot fills. Adding that A to the fill count would
mix two declared stages. The manifest preserves original summary field
names and identifies which count fields were independently checked.

### Native odd lengths stay separate

Seven native records have odd lengths. Pairing each individual message gives
**2,929 complete native pairs plus seven orphan coordinates**. Residual
coordinates from different messages cannot be paired together. The initial
14-package checkpoint already had six such orphans despite its even
4,816-slot aggregate; adding p159 A supplies 135 complete pairs and one
further orphan. The five native pp. 152–153 records add 389 complete pairs
and no orphan. An orphan placeholder in a diagnostic output is
not an additional complete plaintext position. Every declared analysis
frame in this checkpoint is even.

| Record | Native slots | Complete native pairs | Orphan source index | Literal glyph |
| --- | ---: | ---: | ---: | --- |
| p146 C2 | 191 | 95 | 157 | `F` |
| p124 B | 183 | 91 | 161 | `F` |
| p197 A1 | 193 | 96 | 48 | `X` |
| p223 C | 235 | 117 | 102 | `D` |
| p185 B | 279 | 139 | 55 | `A` |
| p158 E1 | 235 | 117 | 23 | `D` |
| p159 A | 271 | 135 | 40 | `V` |

Native untransposition locates each orphan; the indices above refer to
zero-based positions in its literal source. The complete per-record domains and event ledgers remain
in the manifest and the individual experiment certificates.

## Verify or extend the bounded scope

From the repository root:

```sh
python data/reviews/verify_continuation_source_counts.py --verify
```

`--verify` reads the frozen manifest and live evidence without writing any
file. `--manifest /path/to/review.json` selects another explicitly reviewed
scope. `--emit` prints newly computed ledgers for examination and never
updates expected values automatically. A new package must have its frame
family and source/repair classification reviewed before its identifier and
expected ledger are added; an unrecognized frame family fails explicitly.
The p159 A extension was independently checked by direct enumeration of all
173,580 canonical frames before its primary ledger was admitted. Its 64
source maps and 12 complete witnesses remain alternatives within one record.

The pp. 152–153 extension was checked from all five native input rows,
their identity source maps and every substitution/fill event. It adds
778 source slots, 384 raw fixed positions, 388 candidate fixed positions,
14 observed substitutions and four source-mask fills, with no frame
addition or exclusion. Both source crops were inspected. The dash-only
`RICHI----` header on p152 C remains an unknown advertised length; 108 is
the independently counted body length. The surviving p152 B2 `EB?Q` has
the six certified completions, and no one of them is selected by this count
audit. The p153 A3/B1 headers and reception times remain distinct.

This check establishes count and source/model consistency. Source-image
readability, historical numeral assignments, header ambiguities, unique
historical wording and the choice of a historical error mechanism retain
the separate limits of each source edition. The
[live readable mappings](../data/reviews/live_readable_mappings.json)
checks the corresponding current quotations independently of these totals.
