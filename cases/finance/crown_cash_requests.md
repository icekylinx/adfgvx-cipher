# Crown-cash requests for Arad and a report of banknote shortage

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

Childs p219 contains a two-part request about an advance for Arad,
following an arrangement with the German military mission at Budapest,
and a separate message reporting partial crown remittances and a severe
shortage of banknotes. This edition preserves all monetary, army and
reference labels exactly under the published square.

The primary source is J. Rives Childs, *General Solution of the ADFGVX
Cipher System*, [printed p219, PDF p222](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The page heading is November 25, 1918. A is headed
`UKS v BSL (09.40 p.m., November 25th)`, with origin field
`1320 (11/25) 2 TLE`; B has receipt `09.16 p.m., November 27th`
and origin `1800 (11/25)`. Both dates of B are retained.

The [literal fixture](../../experiments/crown_cash_requests/inputs.json)
and [certificate](../../experiments/crown_cash_requests/certificates.json)
provide three source crops, every source coordinate, independent
transposition maps, complete raw-label inventories and exact repair
certificates. The three bodies already appeared as unreviewed OCR-derived
entries in the repository's
[`p73_new_methods/retrieval_inputs.json`](../../experiments/p73_new_methods/retrieval_inputs.json).
The contribution here is the visually checked source edition and its
reversible repairs, not first computation of those candidate bodies.

## A1: funds for Arad

All 334 source coordinates are valid. Their raw 167-position reading is:

```text
ETXINTENDXJJFIALAXXNACHVEREINBARUNGMXDERDTXMILXMISSIONBUDAPESTOBLTXKUDELSOLLENAUSSERDENDORTANGEFORDERTEN6MILXKRONENNOCH3YYYYYKRONENFUERMG0ARADZURVERFGXGESTELLTWERDENXX
```

The candidate changes only `MG0` to `MGD`, at one observed coordinate:

```text
ETXINTENDXJJFIALAXXNACHVEREINBARUNGMXDERDTXMILXMISSIONBUDAPESTOBLTXKUDELSOLLENAUSSERDENDORTANGEFORDERTEN6MILXKRONENNOCH3YYYYYKRONENFUERMGDARADZURVERFGXGESTELLTWERDENXX
```

The address contains `ET. INTEND. JJ FIALA`. The message cites an
arrangement with the German military mission at Budapest, followed by
`OBLT. KUDEL`, and requests that an additional amount labelled
`3YYYYY` crowns be made available for `MGD ARAD`, beyond the amount
labelled `6 MIL` already requested there. The received names `FIALA`
and `KUDEL` are not identified with particular historical people.
The army label `JJ` and both amount labels remain unassigned.

The fifth row ends in the complete group `FDDFX`. The final `X`, which
the earlier OCR treated as uncertain, is observed in the source and gives
a complete `KRONEN` reading. It is not a filled ciphertext erasure.

## A2: can an advance be drawn?

All 230 coordinates are valid. The raw 115-position reading is:

```text
ERBITTENDRAHTANTWORTOBVORSCHUSSBISZUDIESERHOEHEAUSDORTXFELDKRIEGSKASSEERFORDERLXZEITPBGEHOBENWEGDENKANNXXMGDXARPDXX
```

Three observed-coordinate changes yield:

```text
ERBITTENDRAHTANTWORTOBVORSCHUSSBISZUDIESERHOEHEAUSDORTXFELDKRIEGSKASSEERFORDERLXZEITABGEHOBENWERDENKANNXXMGDXARADXX
```

A telegraphic reply is requested on whether an advance up to that amount
can be drawn from the local field war cash office at the required time.
The received abbreviated wording `ERFORDERL X ZEIT` is retained without
adding a preposition or lengthening the text.

Two complementary readings within these explicitly numbered parts
support the office/place candidate. A2 contains unchanged `MGD`, while
A1 contains unchanged `ARAD`. They support the separate emendations
`MG0 → MGD` in A1 and `ARPD → ARAD` in A2 if the parts refer to the same
office and place. This is within-message contextual support, not an
independent exact retransmission. The abbreviation `MGD` is not expanded.

| Untouched support | Plaintext indices | Original source indices for each pair |
| --- | --- | --- |
| A2 `MGD` | 105–107 | M: 139,99; G: 199,9; D: 159,179 |
| A1 `ARAD` | 138–141 | A: 303,128; R: 84,200; A: 143,288; D: 12,230 |

The complete source coordinates and the separately priced target changes
are included in the certificate.

## B: partial remittances and a shortage of banknotes

All 354 coordinates are valid. The raw 177-position reading is:

```text
FELDINTENDXAXOXKXJJXXZUJ3Y20AUFDORTIGEKRONENANFORDERUNGDRAHTETKMXXKRONENBETRPEGETEILWEISEUEBERWIESENXRESTFOLGTNACHMOEGLICHK9ITXGROSSERNOTENMANGELXXXGENXINTENDANTXROEM4BJ411XJYJ2
```

Two observed-coordinate repairs restore `BETRAEGE` and `MOEGLICHKEIT`:

```text
FELDINTENDXAXOXKXJJXXZUJ3Y20AUFDORTIGEKRONENANFORDERUNGDRAHTETKMXXKRONENBETRAEGETEILWEISEUEBERWIESENXRESTFOLGTNACHMOEGLICHKEITXGROSSERNOTENMANGELXXXGENXINTENDANTXROEM4BJ411XJYJ2
```

The message addresses `FELDINTEND. A. O. K. JJ`, cites `J3Y20`, and
reports a `KM` telegram that crown amounts have partly been remitted,
with the remainder to follow as possible. It explicitly mentions a
severe shortage of banknotes. The received closing field is
`GEN. INTENDANT. ROEM4BJ411XJYJ2`; the labels and abbreviation are not
expanded into a person, date or departmental number.

A and B concern crown liquidity, but the source does not establish that
B answers this particular A request. The common page and compatible
subject are insufficient to equate their transactions. Nor does a
report of partial remittance establish that the whole requested amount
was ultimately paid.

## All numerical-looking labels remain visible

The amount labels are fully observed and untouched by any candidate repair:

| Field | Plaintext index | Raw label | Pair | Original source indices |
| --- | ---: | --- | --- | --- |
| A1, `6 MIL` | 104 | 6 | DX | 125, 81 |
| A1, first amount character | 119 | 3 | VV | 257, 97 |
| A1, second amount character | 120 | Y | DG | 213, 53 |
| A1, third amount character | 121 | Y | DG | 156, 316 |
| A1, fourth amount character | 122 | Y | DG | 68, 243 |
| A1, fifth amount character | 123 | Y | DG | 330, 25 |
| A1, sixth amount character | 124 | Y | DG | 170, 112 |

These zero-based positions show the received pattern, not the historical
values of its characters. Plausibility of a round amount is not used to
assign `Y`, `3` or `6`.

Every occurrence of `0123456789JQY` in all six raw/candidate views is
listed in the certificate: **27** source occurrences and **25** candidate
occurrences. The two removed source occurrences are raw `0` in `MG0`
and raw `9` in `MOEGLICHK9IT`. Both receive explicit coordinate repairs;
neither is concealed from a later key-label study. All amount, name,
army and reference fields declared unchanged have their full observed
pair witnesses certified.

## Verification and attribution

There are **918 valid observed coordinates**, **459 raw-label plaintext
positions**, and **six** candidate coordinate substitutions: one in A1,
three in A2 and two in B. There are no missing-coordinate fills, source
erasures, insertions, deletions, reordered blocks or key changes. Every
full candidate reencrypts exactly under the published `Nov25-28` key.
These are counts of fixed raw labels and source-edition repairs, not
newly solved numerical values.

The published key is prior work by George Lasry and colleagues; its
provenance is retained. All three earlier automatic retrieval bodies
are explicitly credited. No explicit discussion of these bodies was
located in the bounded paper, ADFGVX dissertation chapter and cached
55-comment checks; this does not establish universal historical priority.

```bash
python experiments/crown_cash_requests/verify.py --verify
python experiments/crown_cash_requests/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier reconstructs the source mapping independently, checks every
raw position and repair, confirms all unchanged fields and complementary
within-message support, and inventories every numerical-looking label.
The optional PDF check verifies the full source hash and every crop pixel.
