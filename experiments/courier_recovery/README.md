# Munich courier message: duplicated first part and direct continuation

ADFGVX Cipher — research and source edition by **icekylinx and GPT-6 Astra Pro**.

This experiment gives a source-audited reading of five Childs intercept
records using the existing **Nov7–9** key. It recovers a direct 67-of-68-position
second part and proposes a separately qualified 134-position first part about
couriers travelling to Munich with radio operating documents. It does not
recover a new transposition key or assign either unresolved numeral cell.

Read the [message edition](../../cases/pages/151.md#edition-cases-radio-courier-munich) first. The
[literal inputs](inputs.json) preserve every printed coordinate. The
[certificate](certificate.json) preserves the source alignments, raw readings,
editorial candidate, all minimum candidate-specific fits, and a second
alignment model that permits one received coordinate to be deleted.

## Source records

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
in the [public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
Each image is a direct crop of that scan; its PDF page, rectangle, render
scale and SHA-256 are recorded in `inputs.json`.

| Record | Printed / PDF page | Source slots | Declared part / length | Source image |
| --- | --- | ---: | --- | --- |
| p153 E1 | 153 / 156 | 259 | First of two / 268 | [D and E](sources/p153_DE.png) |
| p162 A1 | 162 / 165 | 264 | First of two / 268 | [A](sources/p162_A.png) |
| p151 D2 | 151 / 154 | 136 | Second / 136 | [D](sources/p151_D.png) |
| p153 D2 | 153 / 156 | 136 | Second / 136 | [D and E](sources/p153_DE.png) |
| p158 C2 | 158 / 161 | 136 | Second / 136; first missing | [C](sources/p158_C.png) |

Both first-part witnesses visibly contain the six-coordinate group
`VXDVDD`. The literal source retains all six. The longer witness also contains
two consecutive `VXGGX` groups. The fourth glyph of the first is overstruck:
the displayed transcription is `G`, while analysis masks that one source
slot, index 154, as an erasure. No other valid coordinate is silently changed.

The p151 D group following `XVAFD` is **`GXAXV`**, confirmed at enlarged scale.
The `N4 DD` following the last ciphertext coordinate of p158 C is a service
ending, not ciphertext. The lengths above use the literal source, including
the six-letter group, rather than normalized groups of five.

## Direct second part

The best-preserved continuation, p158 C2, deciphers with **zero source edits**:

```text
GRUKONACH?02BENACHRICHTIGENEINTREFFENHIERHERDRAHTENXNACHRCHEF4B49909
```

The two independent repeats differ at one plaintext position each:

```text
p151 D2: GRU1ONACH?02BENACHRICHTIGENEINTREFFENHIERHERDRAHTENXNACHRCHEF4B49909
p153 D2: GRUKONACH?02BENACHWICHTIGENEINTREFFENHIERHERDRAHTENXNACHRCHEF4B49909
```

The certificate keeps these spellings literal. Each record fixes 67 of its
68 plaintext positions. The unresolved position is index 9, coordinate pair
**VF**, whose domain under the unchanged partial square is **{5, 6}**.
The footer `NACHRCHEF4B49909` is directly read; its administrative expansion
is not needed for the decipherment.

## First-part geometry and editorial reading

Inserting one consecutive five-coordinate erasure into the 259-slot witness
allows a direct comparison with the 264-slot witness. Exhausting all **260**
insertion locations gives a minimum of **two** known-coordinate disagreements,
with seven tied gap starts, **151 through 157**. These aliases arise around
the repeated `VXGGX` material. The remaining disagreements are the first two
coordinates of p153 `DFAVX` versus p162 `FGAVX`, at positions 246 and 247 in
the 264-slot comparison frame. This establishes a relative five-slot deficit;
it does **not** locate the other four missing slots required by `RICHI-268`.

The proposed first-part text is:

```text
ANINGENIEURINSPEKTIONMUENCHENXGEFRXGERAUSUNDFELDGRXMAHRERALSKURIERMITFUNKBETRIEBSUNTERLAGENFUERGRUKONACH?02X7UHRABDSNACHDORTABGEFAHREN
```

It is an editorial candidate, informed by recognizable fragments in trials
of the known key and by the direct continuation. The experiment then fixes
that candidate and computes the precise source cost. The German-looking
result is not used to label one insertion geometry as historically certain.

### Model 1: retain every received coordinate

For a source of length `n` and a candidate of length `m`, the builder inserts
exactly `m − n` missing slots and minimizes substitutions of retained known
coordinates. It does not delete or reorder received slots. A printed erasure
costs no substitution, and its proposed value is listed separately.

| Witness | Missing slots inserted | Known coordinates changed | All minimum alignments |
| --- | ---: | ---: | ---: |
| p153 E1 | 9 | 6 | 32 |
| p162 A1 | 4 | 8 | 2 |

The recurrence is exact. For `F[j,l]`, the first `j` candidate coordinates
are matched to the first `j−l` observed coordinates with `l` missing slots:

```text
F[j,l] = min(F[j−1,l−1], F[j−1,l] + known_mismatch)
```

The first branch inserts a missing slot; the second retains the next source
slot. Bounds and source erasures are handled explicitly in `build.py`.
Every minimum path is retained. There is no beam, language-score cutoff or
tie truncation in this certificate.

Across every independently chosen minimum alignment of both witnesses,
**123 of the 134 proposed plaintext positions** have a complete, unchanged
coordinate pair in at least one witness. This is a conditional support
statement about this candidate and model, not a count of 123 positions
proved independently of all geometry choices. The unknown digit is excluded
from that count even where its coordinate pair survives.

### Model 2: allow one received coordinate to be deleted

The source's six-letter group also makes an extra received coordinate a
reasonable alternative. A separate sensitivity check deletes each possible
source coordinate in turn, then fits the remaining source in order. It tests
all **259** and **264** deletion positions; it does not assume that the extra
coordinate lies in the conspicuous group.

| Witness | Received slots deleted | Missing slots inserted | Minimum substitutions | All minimum alignments |
| --- | ---: | ---: | ---: | ---: |
| p153 E1 | 1 | 10 | 4 | 192 |
| p162 A1 | 1 | 5 | 6 | 14 |

For p153, the optimal deletion positions are **42, 44 and 45**, all `D`
coordinates in `VXDVDD`. For p162, the optimal choices are **42, 44, 45 and
247**. All missing-slot masks for these tied choices are recorded. Counts
include distinct source-coordinate choices even where repeated symbols make
the retained stream identical.

This second model has fewer substitutions but assumes an additional source
deletion and missing coordinate. Neither model is selected as historical
fact. Requiring support under **every minimum fit of both models** leaves
**118 of 134 positions** with an unchanged pair in at least one witness.
The direct 67-of-68 continuation is unaffected by either model.

## Digit and part-association limits

At first-part position 104 the candidate uses unassigned cell **VF**, the
same cell directly observed at continuation position 9. If the first-part
candidate instead uses the other unassigned cell **XA**, the source-preserving
fit costs rise from 6/8 to 8/10 substitutions. This supports the matching cell
within that stated candidate model, but cannot distinguish its numerical
value, 5 versus 6.

The key snapshot records the existing provenance distinction. The final
published tables and Childs appendix leave both cells unfilled. Norbert's
2017 completion proposes VF=5 and XA=6; an inconsistent illustrative research
figure prints the opposite. Neither is promoted to an established assignment
here. Unit-number plausibility alone is not an independent cipher constraint.

The first-part/second-part association is supported by the part labels,
same-morning `RVV v N4` headers on p153, the `2120 (SY)` first-part field and
p151 `SY v N4` continuation, and the matching `GRUKONACH?02` reference.
Departure followed by a request to report arrival is coherent. The log does
not explicitly cross-reference these records as one original transmission;
the association remains an interpretation. The second part stands on its own.

## Linked historical consequence: conditionally GRUKONACH602

The separate [9 November operational-report edition](../../cases/pages/166.md#edition-cases-military-nov9-operational-reports-historical-identification-most-likely-the-6th-reserve-division)
records a historical identification of its reserve division as the **6th
Reserve Division**. Its primary support is General Franchet d'Esperey's
telegram 5.956/3 of 19 November, describing the forces on 11 November,
including the 217th and 219th divisions, the Alpenkorps, and the 6th Reserve
Division in the matching area. Full source details and date qualifications
are in [military_context.json](../p170_continuation/military_context.json).
That source had already been reviewed for p176b; the new use is its
consequence for the Nov7–9 square.

**If that historical identification is accepted**, it supplies **VF=6** in
the shared period square. The courier continuation then reads
**GRUKONACH602**, with **zero additional source-coordinate changes**.
The first-part candidate's matching field also becomes 602 without altering
any of its separately documented alignment or edit costs. The link is the
shared cipher cell; no identification between the different military units
is inferred.

The certificate records this as a linked conditional consequence, never an
independent numeral deduction from the courier messages. It preserves the
original `{5,6}` domains, raw variants, and first-part association caveat.
The builder and independent verifier check the external context's exact
base key and assignments and re-encrypt all four displayed conditional
frames. The three second-part sources still retain their own raw spellings.

## Reproduction and attribution

Run from the repository root:

```sh
python3 experiments/courier_recovery/build.py --verify
python3 experiments/courier_recovery/verify.py
```

The builder verifies the source-image hashes and the exact unchanged key
snapshot. The independent verifier uses only the Python standard library:
it imports neither `build.py` nor the project's cipher functions. It checks
the coordinate layout, direct decipherments, all reported candidate edits,
all optimum counts through a separate forward-grid dynamic program, all
deletion trials, pair-support intersections and both unresolved-cell trials.

The period key retains the historical and George Lasry / coauthor attribution
recorded in [the key register](../../data/keys.json). Source transcription,
duplicate recovery, candidate accounting and this edition are by
**icekylinx and GPT-6 Astra Pro**. No first historical decipherment priority
is claimed.
