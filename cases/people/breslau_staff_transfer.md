# A staff officer's assignment to Breslau

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
rank as Major. His surname and corps numbers remain unresolved.

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

### Surname spelling: an OCR lead without identity confirmation

The digitized [*Deutscher Reichsanzeiger*, no. 94, April 21, 1913,
p4](https://digi.bib.uni-mannheim.de/reichsanzeiger/ocr/film/tesseract-4.0.0-20181201/126-9532/0243.hocr)
has an OCR entry `v. Strzemieczny` in its official army personnel changes.
It lists a captain of that name on the staff of Infantry Regiment 143
among appointments as company commanders.

The underlying scan image was unavailable during the check, so this is
an **OCR-only spelling lead**. No independent link to the officer in the
1918 message was established. The received `STRZEMIECZNQ` is therefore
retained, and no `Q→Y` assignment or individual identification is made.
These two different types of context are documented in
[`historical_context.json`](../../experiments/breslau_staff_transfer/historical_context.json).

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
