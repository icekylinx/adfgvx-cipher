# A staff officer's assignment to Breslau

The order concerns Major Strzemieczny's assignment to special employment with the VI Army Corps command at Breslau.

**Complete edition by printed page:** [p. 224](../pages/224.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

A two-part personnel order assigns a staff officer to special employment
with a corps command at Breslau, says that he has already been ordered
directly, and requests notification to another corps command. Its name,
rank and formation fields contain raw published-square labels whose
historical interpretation is kept separate from the ordinary-word reading.

The later [Article XII numeral interpretation](../../experiments/nov25_treaty_digits/README.md)
reads the addressee as `AOK11`, using the two received `FX` pairs without
source changes. Together with the earlier `VD=J` letter interpretation,
the opening addresses the 11th Army command and identifies the officer's
rank as Major. A further shared **`AD=Y`** assignment now supports the
surname **Strzemieczny**, also completing the place name **Nagymágocs** in
a different telegram. The previous corps numbers remain unresolved.

## Conditional reading

**Readable German — shared letter and numeral interpretation, with the
same nine observed-coordinate word repairs:**

> AOK 11. Major beauftragt mit Wahrnehmung der Geschaefts des Chef des Generalst. ?? Res. K. Strzemieczny ist unter Versetzung zu den Offizieren V. D. A. dem Generalkdo. 6 A. K. Breslau zu bes. Verwendung zugeteilt, ist unmittelbar beordert. Mitteilung an Generalkdo. ?? AK erbeten. Chef des Generalstabs d. Feldheeres. ???2?.

The order concerns Major Strzemieczny's assignment to special employment
with the VI Army Corps command at Breslau. The reserve-corps and second
command numbers, as well as most of the closing reference, stay unknown.
The [joint surname and place check](../../experiments/nov25_treaty_digits/README.md#the-shared-y-in-strzemieczny-and-nagymagocs)
adds no coordinate repair. It identifies the spelling of the surname,
without establishing the officer's given name or service record.

## Source and earlier edition

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed p224 C, PDF p227. The header reads
`UKS v BSL (00.13 a.m., November 28th)`, followed by the undated origin
time `2230`. A preceding page subheading says November 26. The edition
preserves those printed dates without inferring an original sending date.

All 558 coordinates are valid and the lengths match `RICHI-260` and
`RICHI-298` exactly. The
[literal source edition](../../experiments/breslau_staff_transfer/inputs.json)
includes enlarged crops for ambiguous-looking `G` glyphs. The
[certificate](../../experiments/breslau_staff_transfer/certificates.json)
uses the unchanged published `Nov25-28` square and records every repair
and every numeral or `J/Q/Y` occurrence.

Both bodies had already appeared as unreviewed OCR-derived entries in
[`p73_new_methods/retrieval_inputs.json`](../../experiments/p73_new_methods/retrieval_inputs.json).
The contribution here is their visually checked transcription, exact
source mapping, priced ordinary-word edition and separated historical
context, rather than first computation of those candidates.

## C1: the officer and his previous function

The raw 130-position reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
AOKJJXXMA9ORBEAUFTRAGTMITWAHRNEHMUNG0ERGESCHAEFT9DESCHEFDESGENERALSTX40XRESXKXXSTRZEMIECZNQISTUNTERVERSETZUNGZUDENOFFIZIERENVXDXAX
```

</details>

Three observed-coordinate substitutions repair the ordinary words `0ER`
to `DER` and `GESCHAEFT9` to `GESCHAEFTS`:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
AOKJJXXMA9ORBEAUFTRAGTMITWAHRNEHMUNGDERGESCHAEFTSDESCHEFDESGENERALSTX40XRESXKXXSTRZEMIECZNQISTUNTERVERSETZUNGZUDENOFFIZIERENVXDXAX
```

</details>

The text addresses `AOKJJ` and describes the officer as acting in the
capacity of chief of the general staff of the reserve corps labelled
`40 RES K`. His received surname is `STRZEMIECZNQ`. He is being transferred
to the category of officers designated `V. D. A.`; the destination and
special employment follow in C2.

The token `MA9OR` is consistent with an intended military rank, but the
edition does not select a global interpretation of raw `9`. In particular,
the same unchanged square cell also appears in the garbled `GESCHAEFT9`.
That second occurrence receives its own explicit coordinate repair; a
rank-based relabelling must not conceal its different ordinary-word role.
The surname's final `Q`, the two `J` army labels and the `40` formation
labels are all retained.

## C2: special employment with the Breslau command

The raw 149-position reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DEMGENERALKDOX7XAXKXBRESLAUZUBESXVERWENDUNGZUGETEILTISTUNMITTELBARBEORDERTXMITTEOLUNGANGENREALKDOX40AKEGBETENXXXCHEFDESGENERALSTABSDXFELDHEERES04013X
```

</details>

Six observed-coordinate changes restore `MITTEILUNG`, `GENERAL` in the
second command reference, and `ERBETEN`:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
DEMGENERALKDOX7XAXKXBRESLAUZUBESXVERWENDUNGZUGETEILTISTUNMITTELBARBEORDERTXMITTEILUNGANGENERALKDOX40AKERBETENXXXCHEFDESGENERALSTABSDXFELDHEERES04013X
```

</details>

The officer is assigned to special employment with the command labelled
`7 A K`, Breslau. He has already been ordered directly, and notification
to the command labelled `40 A K` is requested. The signature reads
`CHEF DES GENERALSTABS D. FELDHEERES`, followed by raw `04013`.
The source's `40AK` is not silently changed to match the earlier
`40 RES K` designation.

Immediately after the final three-letter ciphertext group `XDV`, the
page carries a cleartext fragment beginning `VON LP AN CO`. It is outside
this part's 298-coordinate length and is excluded from the ciphertext
transcription and from the count of recovered encrypted records.

## Three untouched fields useful for separate interpretation

| Field | Plaintext index | Pair | Original source indices |
| --- | ---: | --- | --- |
| C1, the `9` of `MA9OR` | 9 | `VD` | 125, 79 |
| C1, final `Q` of `STRZEMIECZNQ` | 90 | `AD` | 86, 210 |
| C2, `7` before `A K BRESLAU` | 14 | `GA` | 247, 1 |

These zero-based source positions are complete observed pairs and are
unchanged by every ordinary-word repair. The certificate lists all other
numeral and `J/Q/Y` positions as well: **16 physical source occurrences**,
with **14** remaining in the ordinary-word candidates. The two removed
occurrences are the separately repaired `0ER` and `GESCHAEFT9`.

<a id="breslaus-vi-army-corps-command-older-primary-context"></a>

### The VI Army Corps command in November 1918

*Der Gebirgsbote*, no. 129, **13 November 1918**, p1, publishes joint
orders of the Breslau soldiers council and the deputy general command
of **VI Army Corps**, dated Breslau, **11 November 1918**. The
[original scan](https://bibliotekacyfrowa.pl/Content/60534/PDF/directory.pdf),
[masthead](../../experiments/nov25_treaty_digits/sources/gebirgsbote_1918_129_title.png)
and [decree crop](../../experiments/nov25_treaty_digits/sources/breslau_vi_corps_nov11.png)
place that command in Breslau during the month of the intercept. The
command signs through Freiherr von Egloffstein; Voigt and Berg sign for
the soldiers council.

Identifying the telegram's Breslau recipient with this command gives
`6XAXKXBRESLAU` from the received pairs. The
[optional `GA=6` layer](../../experiments/nov25_treaty_digits/breslau_certificate.json)
propagates that identification through the same 23-record set without
source changes. It also gives `6?` for the first German-bank mark amount
in the [lei-redemption proposal](../finance/lei_note_exchange.md).

The earlier [July 1917 decree](../../experiments/boots_request/breslau_context/source.json)
provided the initial institutional lead. The November source supplies the
closer dated witness; neither decree identifies the officer named in p224.

<a id="surname-spelling-an-ocr-lead-without-identity-confirmation"></a>

### The surname and the shared Y cell

The original `AD` pair at C1 position 90, source positions **86 and 210**,
gives `STRZEMIECZNQ` under the published labels. The optional assignment
`AD=Y` gives **`STRZEMIECZNY`** without changing either observed coordinate.

The spelling is visible in *Schlesische Zeitung*, 172nd year, no. 337,
morning edition, **17 May 1913**, PDF page 6: an officer-awards notice
names a captain von Strzemieczny of Infantry Regiment 143.
[Institutional scan](https://bibliotekacyfrowa.pl/Content/139045/GSL_P_31292_IV_1913_26511_337.pdf)
· [Masthead](../../experiments/nov25_treaty_digits/sources/schlesische_1913_title.png)
· [Printed name](../../experiments/nov25_treaty_digits/sources/strzemieczny_1913_military.png).
This supplies image evidence beyond the earlier
[*Reichsanzeiger* OCR lead](https://digi.bib.uni-mannheim.de/reichsanzeiger/ocr/film/tesseract-4.0.0-20181201/126-9532/0243.hocr)
recorded in the original
[historical-context file](../../experiments/breslau_staff_transfer/historical_context.json).
The 1913 captain is not identified here with the 1918 major.

The same unchanged pair completes `NAGYMAGOCS` in the
[p220 evening report](../military/nov25_provisions_and_evening_report.md#p220-b).
Across **33 reviewed records**, four native `AD` occurrences include these
two names and the earlier damaged `VORQELEGT` and `EINQIGES`; their separate
word repairs are retained. With the earlier conditional assignments,
the shared Y reduces **362,880 to 40,320** possible complete squares.
The [certificate](../../experiments/nov25_treaty_digits/names_certificate.json)
keeps both supporting pairs, both inconvenient occurrences and all
earlier source costs.

## Scope, credit and reproduction

The published period square fixes all **279 raw-label positions** in the
two parts. The candidates make **nine** observed-coordinate substitutions
and reencrypt exactly. There are no missing-coordinate fills, source
erasure fills, deletions or reordered blocks. These counts are not a claim
that 279 previously unknown key symbols have been solved or that every
raw numerical label has its intended historical value.

Published key provenance is preserved. Lasry and colleagues explicitly
cite the neighboring p224 A message; no explicit discussion of C was
located in the bounded paper/dissertation/comment check. The prior
repository OCR candidates are separately credited, and no universal
historical-priority claim is made.

```bash
python experiments/breslau_staff_transfer/verify.py --verify
python experiments/breslau_staff_transfer/verify.py --verify \
  --pdf /path/to/childs.pdf --historical-pdf /path/to/waldenburg_1917.pdf
```

The verifier reconstructs the column mapping independently, checks every
plaintext position and exact repair, audits the complete label inventory,
and confirms that the three interpretation fields remain untouched.
The PDF options verify both full source hashes and all retained crop pixels.

</details>
<!-- CASE-EDITION:END -->
