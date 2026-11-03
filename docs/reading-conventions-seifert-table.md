# Live Seifert reading-table review

Prepared by **icekylinx and GPT-6 Astra Pro**, 3 November 2026 UTC.

The [Seifert case](../cases/radio/seifert.md#read-the-messages) presents seven
readable passages in a Markdown table. The general presentation inventory
classifies fenced blocks and blockquotes; those selectors do not cover
these table cells. The separate
[table manifest](../data/reviews/seifert_readable_table_20261103.json) and
[portable checker](../data/reviews/verify_seifert_readable_table.py) close
that specific gap without changing the table or its source evidence.

## What the check establishes

The current seven German cells map to **329 ordered nonseparator labels**
in the unchanged [source/cipher record](../experiments/p170_continuation/seifert_records.json).
The mapping preserves every digit and the one displayed unresolved
position. Word spacing, case, punctuation and conventional umlaut rendering
are display transformations. Each removed X is explicitly treated as a
separator for these seven passages; no global X-removal rule is asserted.

| Table row | Evidence used | Bracket treatment |
|---|---|---|
| p168 A, with the p169 A repeat separately qualified | Unedited p168 A raw output | `[d]` and `[ion und]` are display-only spelling/abbreviation expansions; they add no recovered positions. |
| p168 B | The existing two-substitution candidate | No bracketed expansion or new source change. |
| p172 A | The existing one-mask-fill candidate | `[s]` belongs to the costed source-mask completion; `[önlicher]` expands `PERS` only in the display. |
| p174 B | The existing one-mask-fill candidate | `[n]` belongs to the costed source-mask completion; `[icht]` expands `NACHR` only in the display. |
| p174 C | Unedited raw output | The question mark after Seifert is explicitly registered as sentence punctuation. |
| p172 B / p174 D | The identical raw outputs | The literal `?00` remains unresolved; its question mark is a cipher unknown. |
| p174 E | The existing two-substitution name proposal | No new spelling or coordinate change. |

The brackets therefore contain **19 display-only letters** and **two
source-mask completion letters**. Those are different categories. Counting
the former as recovered plaintext would misrepresent abbreviation
expansions; discarding the latter before comparison would hide the actual
proposed fills. These display counts do not increase the source corpus.

The first row maps to the clean p168 A reading. It does not promote the
errored p169 A copy to the same direct reading: the table's qualification,
the repeat's conditional deletion frame, and its raw output remain intact.

## One displayed unknown, shared by two copies

The listening instruction has the literal field `?00`. The p172 B and p174 D
records have identical native ciphertext, column ranks, partial squares and
raw domains. Their hundreds label is the same unassigned cell, so one
global key completion must supply the same value in both copies. The
manifest retains the domain **{5, 6, 7, 8, 9}** at plaintext position 10,
using zero-based indexing. A duplicate source does not select one member.

The existing [cipher verifier](../experiments/p170_continuation/verify_seifert.py)
constructs consistent full-square witnesses for the possible digits. The
new table check protects that evidence link and the live literal display;
it does not independently authenticate the scan or establish the digits'
historical values.

## Reproduce

From the repository root:

```sh
python data/reviews/verify_seifert_readable_table.py
```

The script uses only the standard library and can also run by absolute path
from another directory. It rejects a missing, added or reordered table row,
changed source label or local qualification, unreviewed bracket material,
changed ordered labels, a lost `?00`, or a changed evidence-file digest.
No case file, source record or certificate is written by the checker.

The original publication credit for the p168 A/B interpretations remains
with **J. Rives Childs** and **George Lasry, Ingo Niebel, Nils Kopal and Arno
Wacker**, as recorded in the case. This addition supplies live presentation
coverage only.
