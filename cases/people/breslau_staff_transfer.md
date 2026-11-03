# A staff officer's assignment to Breslau

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

A two-part personnel order assigns a staff officer to special employment
with a corps command at Breslau, says that he has already been ordered
directly, and requests notification to another corps command. Its name,
rank and formation fields contain raw published-square labels whose
historical interpretation is kept separate from the ordinary-word reading.

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

**Raw output:**

```text
AOKJJXXMA9ORBEAUFTRAGTMITWAHRNEHMUNG0ERGESCHAEFT9DESCHEFDESGENERALSTX40XRESXKXXSTRZEMIECZNQISTUNTERVERSETZUNGZUDENOFFIZIERENVXDXAX
```

Three observed-coordinate substitutions repair the ordinary words `0ER`
to `DER` and `GESCHAEFT9` to `GESCHAEFTS`:

**Edited output:**

```text
AOKJJXXMA9ORBEAUFTRAGTMITWAHRNEHMUNGDERGESCHAEFTSDESCHEFDESGENERALSTX40XRESXKXXSTRZEMIECZNQISTUNTERVERSETZUNGZUDENOFFIZIERENVXDXAX
```

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

**Raw output:**

```text
DEMGENERALKDOX7XAXKXBRESLAUZUBESXVERWENDUNGZUGETEILTISTUNMITTELBARBEORDERTXMITTEOLUNGANGENREALKDOX40AKEGBETENXXXCHEFDESGENERALSTABSDXFELDHEERES04013X
```

Six observed-coordinate changes restore `MITTEILUNG`, `GENERAL` in the
second command reference, and `ERBETEN`:

**Edited output:**

```text
DEMGENERALKDOX7XAXKXBRESLAUZUBESXVERWENDUNGZUGETEILTISTUNMITTELBARBEORDERTXMITTEILUNGANGENERALKDOX40AKERBETENXXXCHEFDESGENERALSTABSDXFELDHEERES04013X
```

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

### Breslau's VI Army Corps command: older primary context

The project had already located a decree of the **VI Army Corps deputy
general command**, dated **Breslau, July 6, 1917**, in *Waldenburger
Wochenblatt*, no. 165, **July 18, 1917**, PDF p8. Its title and decree crops
were independently inspected for this edition. The decree is signed by
von Heinemann, Generalleutnant. The
[primary scan](https://jbc.jelenia-gora.pl/Content/51388/52552_waldenburger_wochenblatt_1917-165.pdf)
and [preserved context](../../experiments/boots_request/breslau_context/source.json)
establish a contemporary VI Army Corps deputy-command association with
Breslau.

If the p224 recipient is that institutional command, and its received
pair is correctly copied under the period key, the raw `7` at `GA` would
denote `6`. This remains a conditional location-based inference. The
primary decree is **sixteen months earlier**, not a 1918 decree, and the
p224 abbreviation does not itself include `stellvertretend`. The decree
neither proves continuity to the intercept date nor identifies its officer.
This source edition applies no global key assignment from that evidence.

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
