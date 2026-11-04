# Armistice-departure report: the p151/p157 copy relation

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source comparison and edition: icekylinx and GPT-6 Astra Pro.**

The truncated first part on p157 shares substantial ciphertext with p151 A1.
It supplies a coordinate that changes the latter's opaque `STUR3FSS` ending
to **STURZFSS** under an explicit common-copy model. The complete p157
reading below copies its missing material from p151 and prices every
disagreement. **The p157 source alone fixes 0 of 95 plaintext positions in
this conditional frame.** The copied reading is not an independent native
decryption of the 83 surviving slots.

This supplement leaves the [earlier p151 edition](nov7_fragment_and_acknowledgment.md#p151-a1)
and [p157 parts 2–5](romanian_pacification_consultation.md) unchanged. A
further **STURZ DES** interpretation is priced separately below; two of its
letters have no surviving p157 coordinate support.

## Sources and the copy assumption

The [p151 source](../../experiments/nov7_fragments_and_council/sources/p151_A.png)
has `LP v NKJ (6.42 p.m., November 7th)`, `KR 1215 UKS 5 TLE`, and
`1 TL RICHI-190`. It contains 189 coordinates and the visibly short `AVVG`.
Its earlier conditional edition adds D before that group to read
GEMELDETEN; that lexical assumption remains explicit here.

The [p157 first-part source](../../experiments/romanian_pacification_consultation/sources/p157_A1.png)
has `LP v NKJ (--- November 8th)`, `5 TLE` and blank `RICHI----`, beneath
the [7 November page heading](../../experiments/romanian_pacification_consultation/sources/p157_overview.png).
It preserves **83 slots: 78 coordinates and five printed dashes**. Its
four-symbol groups are `XDDV` and `XXXA`; no advertised length survives.
These headers and date layers are retained.

Two long exact coordinate runs establish the close source relation
without using German word guesses. All indices in this edition are
zero-based, and the endpoints below are inclusive.

| p151 source positions | p157 source positions | Exact length |
| --- | --- | ---: |
| 118–141 | 13–36 | 24 |
| 143–175 | 38–70 | 33 |

The reconstruction assumes the same 190-slot transposition frame as p151:
**105 absent prefix slots plus one absent coordinate in each short group**.
Thus 83 surviving slots plus 107 modeled absent slots give 190. This length
and prefix are copy assumptions, not values printed on p157.

All 25 combinations of the two local insertion boundaries are replayed.
Four share the minimum **six disagreements among 78 observed coordinates**:
`(3, 71)`, `(3, 72)`, `(4, 71)` and `(4, 72)`. Each has 72 observed agreements
with the p151 witness. The primary display uses `(3, 71)`; the other three
remain equally economical local alignments. No unique loss position or
exhaustive optimum over other total lengths is claimed.

## p157 A1

<details>
<summary>Raw decoded text</summary>

**Raw output — p157 coordinates only, with 105 absent prefix slots and two local gaps masked; conditional 190-slot frame, 0/95 fixed positions:**

```text
???????????????????????????????????????????????????????????????????????????????????????????????
```

</details>

Every pair still depends on at least one missing coordinate in this frame.
The certificate retains the individual domains; the question marks do not
mean that all 36 symbols are possible at every position.

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — fill the 112 masked or absent slots from the stated p151 candidate, before changing any observed p157 coordinate:**

```text
OHLXBPHXNACHRICHBVONABREISSDEUTSCHERUAFFENSTILLSTANDSKOMMISSIONHATANSAHEINENDGEMELDETENSTURZFSS
```

</details>

The 112 fills comprise **105 prefix fills, two short-group fills and five
printed-mask fills**. Of these, 111 have actual p151 coordinate counterparts;
one is the earlier conditional D supplying GEMELDETEN. Fixed positions in
this copy-assisted layer are never counted as fixed raw p157 positions.

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same copy-conditioned frame, five observed p157 substitutions plus the 112 separately accounted fills; opaque ending retained:**

```text
OHLXBPXXNACHRICHTVONABREISEDEUTSCHERWAFFENSTILLSTANDSKOMMISSIONHATANSCHEINENDGEMELDETENSTURZFSS
```

</details>

The primary p157 substitutions are **9 X→V, 10 X→V, 11 X→V, 12 V→X,
71 X→F**. The local gap values are V at source boundary 3 and D at boundary
71; the five printed dashes, source positions 73–77, become AXFDX. In the
equally economical second-group boundary 72 alignment, the local value is
F and source position 71 changes X→D instead. Both complete candidates
re-encrypt to the same stated ciphertext after their separately mapped
changes.

**Readable German — copy-conditioned reconstruction; spacing and punctuation only, with STURZFSS retained:**

> OHL. BP. Nachricht von Abreise deutscher Waffenstillstandskommission hat anscheinend gemeldeten STURZFSS

**Meaning:** The shared fragment concerns news of the departure of a German
armistice commission and an apparent effect. Its closing remains opaque in
the primary reading. BP is not expanded, and the missing predicate is not
supplied as an established event.

## The six disagreements and their plaintext effects

The table shows the primary `(3, 71)` alignment. Each pair combines the
listed coordinate with its other coordinate from the stated p151 frame;
these are conditional paired readings, not independently fixed p157 letters.

| p151 source | p157 source | Other p151 coordinate | p151 pair → label | Pair with p157 coordinate → label | Displayed choice and reason |
| --- | --- | --- | --- | --- | --- |
| 114: V | 9: X | 76: V | VV → X | VX → H | p151 separator after BP; the p157 H remains an alternative. |
| 115: V | 10: X | 77: G | GV → T | GX → B | p151 T gives NACHRICHT rather than NACHRICHB. |
| 116: V | 11: X | 78: D | DV → E | DX → S | p151 E gives ABREISE rather than ABREISS. |
| 117: X | 12: V | 79: A | AX → W | AV → U | p151 W gives WAFFEN rather than UAFFEN. |
| 142: A | 37: F | 65: D | DA → 3 | DF → Z | p157 F supplies the Z in STURZFSS; the remaining FSS is retained. |
| 177: F | 71: X | 34: D | FD → C | XD → A | p151 C gives ANSCHEINEND rather than ANSAHEINEND. |

With second-group boundary 72, the last row instead compares p151 source
176 D with the same p157 source 71 X: pair DX → S versus XX → F, in
KOMMISSION/KOMMISFION. The other five rows are unchanged.

The five selected p151 coordinates are editorial choices supported by
ordinary word forms and the p151 witness; p151 is not assumed infallible.
The certificate retains **all 64 combinations** of choosing p151 or p157
at the six primary-frame conflicts. Every combination roundtrips and has
the same combined cost of six observed-coordinate changes across the two
witnesses. Coordinate cost alone does not select the displayed wording.

For p151 itself, the Z proposal costs **one observed substitution, source
142 A→F**, in addition to its already declared missing D. Its other paired
coordinate is printed on p151. The p157 coordinate therefore supports a
specific correction under the copy model; it does not independently decode
the whole closing.

## Conditional interpretation: STURZ DES

The already edited p157 A2 begins `MINISTERIUMSHERBEIGEFUEHRT`. Joining
that continuation to a proposed STURZ DES ending would read “Sturz des
Ministeriums herbeigeführt.” This is a contextual proposal about the fall
of a ministry, with the following additional cost.

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — further contextual STURZ DES proposal; two additional observed p151 substitutions, neither observed on the surviving p157 source:**

```text
OHLXBPXXNACHRICHTVONABREISEDEUTSCHERWAFFENSTILLSTANDSKOMMISSIONHATANSCHEINENDGEMELDETENSTURZDES
```

</details>

Relative to the primary STURZFSS reading, this changes p151 source
**103 X→V** for F→D and **46 X→V** for S→E. Both counterpart positions lie
inside the 105 absent p157 prefix slots. Hence the p151 total becomes
**three observed substitutions plus its one missing-slot fill**. The p157
observed cost stays five only because these two altered values occur in its
copied prefix; they are not free source support. Across both witnesses the
observed-change cost rises from six to eight.

The continuation is itself the explicitly edited p157 A2 reading, not a
literal uncorrected source. The full interpretation does not establish
which ministry fell or that the inferred event happened. In particular,
p151 A2 has a different 186-slot body from p157 A2's 200 slots: the complete
five-part telegrams are not silently equated.

## Accounting, attribution and reproduction

| Quantity for the newly cataloged p157 A1 record | Count |
| --- | ---: |
| Surviving printed slots / valid coordinates | 83 / 78 |
| Conditional modeled coordinates / plaintext positions | 190 / 95 |
| Fixed raw p157 positions / proposed complete positions | 0 / 95 |
| Observed p157 substitutions | 5 |
| Printed-mask fills | 5 |
| Absent-prefix fills / short-group fills | 105 / 2 |
| Observed-coordinate deletions or moves | 0 |

The already cataloged p151 record is a comparison witness and is excluded
from new-record totals. All counts use the primary opaque-ending candidate;
the additional STURZ DES interpretation is separate.

Published period-key recovery retains the credit of George Lasry, Ingo
Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry's 2017 key list.
Earlier repository candidates and both source editions remain frozen.
This supplement supplies explicit source correspondence and bounded
interpretations; it claims no first historical decipherment.

[Inputs](../../experiments/armistice_departure_copy/inputs.json),
[all alignments, conflict choices and position certificates](../../experiments/armistice_departure_copy/certificates.json),
and [reproduction instructions](../../experiments/armistice_departure_copy/README.md)
preserve the exact evidence and counts.

```sh
python experiments/armistice_departure_copy/verify.py --verify
python experiments/armistice_departure_copy/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```
