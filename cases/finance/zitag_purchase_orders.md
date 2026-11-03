# ZITAG stop-orders and cancellation of procurement contracts

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source:** J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
printed pp102, 103 and 106, PDF pp105, 106 and 109. **Edition:** icekylinx
and GPT-6 Astra Pro. The [experiment](../../experiments/zitag_purchase_orders/README.md)
contains the exact crops, literal coordinates, key provenance and repair
certificates.

Three 180-coordinate messages are almost identical copies of a short
stop-order. A separate two-part message on p103 deals with a request for
rubles, permits loading already paid consignments, orders cancellation
of other contracts and asks again for Westernhagen's prompt return.
The two orders have different scopes and are not merged into one text.

All five records use the unchanged published Nov1–3 square and ranks.
There are no geometry changes or newly assigned key cells.

## p102 A

The source heading is 1 November 1918; the receipt header says November 2
without a time. It addresses the Prussian War Ministry representative
at Constantinople. All **180 coordinates** are observed. The raw reading is:

**Raw output:**

```text
FUERXZITAGVOHNENUMMERNICHTSWEITERKAUFENUNDNICHTSWEITERVERLADENALLESMOEGLICHSTSIVHERNXZITAG
```

The common readable candidate replaces source coordinates **29 G→X**
and **55 G→D**. Both replacements are observed in the other copies.

## p103 D

Header: `OSM v LP (7.08 a.m., November 2nd); 2210 (1/11)`, with the same
War Ministry representative addressee. The source prints the different
forms `VFFAX` and `FDGAG`; neither is silently changed in the transcript.
Its raw **90-character** reading is:

**Raw output:**

```text
FUERXZITAGXOENENUMMERNICHTSWEITERKAUFENUNDNICHTSWEITERVERLADENALLESMOEGLICHSTSICHERNXZITAG
```

Only **source index 162 G→F** is changed for the common candidate,
repairing `OENE` to `OHNE`. Both other copies witness that coordinate.

## p106 B

Header: `NKJ v LP (8.11 p.m., November 2nd); 1/11 2210`, again with the
same addressee. The printed group `XGGGG` has five characters; the earlier
OCR form `XXGGGG` was not an actual extra source coordinate. The raw body is:

**Raw output:**

```text
FUERXZITAGVOHNENUMMERNICHTSWEITERKAUFENUNDNICHTSWEITERVERLADENALLESMOEGLICHSTSICHERNXZITAG
```

The common candidate changes only **source index 29 G→X**, witnessed by
p103 D. The three literal copies differ at exactly three source positions:

| Source index | p102 A | p103 D | p106 B | Candidate |
|---:|---|---|---|---|
| 29 | G | X | G | X |
| 55 | G | D | D | D |
| 162 | F | G | F | F |

The candidate is:

**Edited output:**

```text
FUERXZITAGXOHNENUMMERNICHTSWEITERKAUFENUNDNICHTSWEITERVERLADENALLESMOEGLICHSTSICHERNXZITAG
```

With editorial spacing:

**Readable German:**

> Für Zitag. Ohne Nummer. Nichts weiter kaufen und nichts weiter verladen. Alles möglichst sichern. Zitag.

Every candidate coordinate has an observed witness. This supports a
common original but does not prove which printed version is closest to
the transmission. In particular, the `X` at index 29 is a minority
reading selected for its ordinary wording, not by majority vote.

## p103 B1

This separate message has header `FÜR COS v NKJ (0.43 a.m., November 3rd)`
and `HPTM WESTGRNHAGEN ODER KARL MÜLLER DTSCH WIRTSCHAFTS ABTLG;
1845 (1) 2 TLE`. B1 advertises and prints **274 coordinates**. Its last
group is the observed four-letter `DXGV`; the five-slot OCR version
previously spoiled its frame.

The source-aligned raw reading is:

**Raw output:**

```text
DEUTSCHKAUFDRAHTETNRX5XXBEXTAETIQEN4TEWEGRXINDEDENBESCHAFBUNG6MILLIONENRUBE1ERSUCHGXXERLEDIGTDURCHUNSERTELEGRXNRX3XDASSNUR5EREITSBEZAHLTE
```

The explicit ordinary-word candidate is:

**Edited output:**

```text
DEUTSCHKAUFDRAHTETNRX5XXBESTAETIGENXTELEGRXINDENENBESCHAFFUNG6MILLIONENRUBELERSUCHTXXERLEDIGTDURCHUNSERTELEGRXNRX3XDASSNURBEREITSBEZAHLTE
```

It costs **10 observed-coordinate substitutions** and no fills. Its nine
changed plaintext positions are all listed in the certificate, including
the inconvenient raw digits within damaged words. `TELEGR` remains an
abbreviation. No absent preposition, article or additional word is
inserted to regularize the syntax.

The separate fields `NR X 5`, `6 MILLIONEN` and `NR X 3` are unchanged,
with complete observed pairs. They are retained as raw square labels;
the edition does not infer a new numerical map from a plausible amount.

## p103 B2

The second part advertises and prints **254 slots**. The first group is
`GG-VF`, source group `FCXGD` contains an invalid `C`, and a later group is
`AVG-G`. The raw text is:

**Raw output:**

```text
PARTIENVERLADENWERDENSOL?ENXSTORNIERETSAEMTLXA?DEREKONTRAKTE?EGENALLGEMEINERLAGEXERSUCHENWESTERNHAGENNOCHMALSSOFORTIGERUECKKEHR
```

The candidate fills those three printed erasures and changes no observed
coordinate:

**Edited output:**

```text
PARTIENVERLADENWERDENSOLLENXSTORNIERETSAEMTLXANDEREKONTRAKTEWEGENALLGEMEINERLAGEXERSUCHENWESTERNHAGENNOCHMALSSOFORTIGERUECKKEHR
```

Continuing B1 with editorial spacing:

**Readable German — continuation excerpt; the preceding words are outside this display:**

> … dass nur bereits bezahlte Partien verladen werden sollen. Stornieret sämtl. andere Kontrakte wegen allgemeiner Lage. Ersuchen Westernhagen nochmals sofortige Rückkehr.

The received form `STORNIERET` and the telegraphic wording of the final
request are preserved. `WESTERNHAGEN` is complete in the uncorrected
plaintext. The heading's different `WESTGRNHAGEN` form is kept literally,
and no particular person is identified from the name alone.

The final `SOFORTIGERUECKKEHR` is spaced as **sofortige Rückkehr**. No extra
`R` or connecting preposition is supplied to regularize the telegram's
grammar. The leading ellipsis marks words before this continuation excerpt,
not an unresolved plaintext position.

## Scope and attribution

The short copies and B2 were already present as readable but unreviewed
repository screen candidates. B1 had a degraded candidate under the
wrong OCR length. Their prior bodies are frozen in the inputs file.
The source edition adds precise transcription, frame correction,
cross-copy evidence and reversible edits. A bounded check of the paper,
dissertation chapter and cached 55-comment thread located no explicit
discussion of these bodies; that does not establish first decipherment.

Together the five records contain **1,068 source slots**, **1,065 valid
coordinates** and **534 plaintext positions**. The raw models fix 531
positions; the explicit candidates fix all 534. Total cost is 14 observed
coordinate substitutions plus three printed-erasure fills. These are
edition coverage figures, not a count of newly solved cryptographic
symbols. Neither the stop-order nor the cancellation request proves
that the requested action was carried out.

```bash
python experiments/zitag_purchase_orders/verify.py --verify
python experiments/zitag_purchase_orders/verify.py --verify --pdf /path/to/childs.pdf
```
