# Redemption of stamped and unstamped lei notes

A three-part telegram requests information needed to redeem stamped lei notes, proposes arrangements with Austrian and Hungarian banks, and reports that negotiations over redemption are still in progress.

**Complete edition by printed page:** [p. 223](../pages/223.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

A three-part telegram requests information needed to redeem stamped lei
notes, proposes arrangements with Austrian and Hungarian banks, and
reports that negotiations over redemption are still in progress. Its
exchange-rate and reference fields are complete received pairs, but their
published-square labels are preserved: this edition establishes no new
numerical key assignments. A later joint interpretation narrows several
of these fields:

| Field | Conditional interpretation |
| --- | --- |
| A2, crown amount | `12?` |
| A2, lei amount | `1??` |
| A3, army-administration reference | `2???X11X1?B?` |
| A3, general war-department reference | `1???X11X1?` |

These values follow from the [Article XII numeral assignments](../../experiments/nov25_treaty_digits/README.md),
without an additional source repair. All three question marks in the
two A2 amounts represent the **same square cell**. The mark amounts
remain unresolved; no complete exchange rate has been identified.

A separate [VI Army Corps identification at Breslau](../people/breslau_staff_transfer.md#the-vi-army-corps-command-in-november-1918)
adds the conditional assignment `GA=6`. Under that additional assumption,
the first German-bank mark amount is `6?`, and the last departmental
reference is `1??6X11X1?`. The units digit and the second mark amount
remain unassigned.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p223 A, PDF p226](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The page heading says **November 27, 1918**; the header reads
`UKS v BSL (02.27 a.m., November 28th)`, followed by
`1.30 (11/27) 3 TLE`. These different date/time fields are retained exactly.
The three advertised lengths are 342, 248 and 410 coordinates.

The [source fixture](../../experiments/lei_note_exchange/inputs.json)
retains every printed group and six source crops. The
[certificate](../../experiments/lei_note_exchange/certificates.json)
contains every plaintext domain, source index, repair and alternative
first-part alignment. All readings use the unchanged published
`Nov25-28` square.

## A1: amounts, denominations and the stamping procedure

With the single missing coordinate placed at source gap 176, the raw
171-position reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional missing coordinate at source gap 176:**

```text
OKMXUMEINLOESUNGABGESPANTELTENLEINOTENVORZUBEREITENXERBITTENDRAHTNCHRXUEBERUNGEFAEHRAUSGEGEBENENGESAOTBETRAGSTUECKELUNGUNDGENAUEEINZELHE?TENWIEABSP?NTELUNGVORGENOMMEWURDEX
```

</details>

The ordinary-word candidate is:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same conditional missing-coordinate frame:**

```text
OKMXUMEINLOESUNGABGESTEMPELTENLEINOTENVORZUBEREITENXERBITTENDRAHTNCHRXUEBERUNGEFAEHRAUSGEGEBENENGESAMTBETRAGSTUECKELUNGUNDGENAUEEINZELHEITENWIEABSTEMPELUNGVORGENOMMEWURDEX
```

</details>

The sender addresses `OKM` and asks for a telegraphic report of the
approximate total issued, the denominations, and precise details of how
the stamping was carried out. The repeated damaged forms of
`ABGESTEMPELTEN` and `ABSTEMPELUNG` receive explicit editorial repairs.
The source spelling `VORGENOMME` is retained; its apparent missing final
`N` is not inserted into the plaintext or ciphertext.

There are **341 printed slots**, including invalid `E` at source index
115, against an advertised length of 342. The fifth row's `DDXF` has
four characters. Two neighboring groups that the earlier automatic
transcription mishandled are visibly complete: `VFAXX` and `VFFXF`.
Only one coordinate is missing.

Every one of the **342 possible insertion boundaries** was scored against
the declared ordinary-word candidate. The unique minimum is gap **176**,
inside `DDXF`, requiring **14** observed-coordinate substitutions. The
geometry score uses no external exchange-rate data or key relabelling.
The five physically local alternatives are all preserved:

| Source gap | Observed-coordinate substitutions for the same candidate |
| ---: | ---: |
| 175 | 15 |
| 176 | 14 |
| 177 | 15 |
| 178 | 16 |
| 179 | 17 |

Every local alternative also has two fills: the printed `E` erasure and
the one missing coordinate. They all produce the same fully specified
candidate ciphertext after their separately priced repairs. The complete
raw alternative texts remain in the certificate, including raw `8` in
the less well-fitting alignments. A unique fit to a declared language
stencil is conditional evidence, not proof that each transmitted word
or received glyph was correct.

## A2: a proposed bank arrangement

The raw 124-position reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
WIRWOLLENOESTERRUNGXBANKENBEAUFTRXNICHTABGESPXLEINOTENVMNDORTXHEERESAZGXZXMKURSEVONJ1YKRONENFUERJYYLEIABZUGSFREIEINZULOESENX
```

</details>

Two observed-coordinate substitutions yield:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
WIRWOLLENOESTERRUNGXBANKENBEAUFTRXNICHTABGESPXLEINOTENVONDORTXHEERESAZGXZUMKURSEVONJ1YKRONENFUERJYYLEIABZUGSFREIEINZULOESENX
```

</details>

The message proposes commissioning Austrian/Hungarian banks to redeem
unstamped lei notes without deductions, at the stated raw-label ratio
`J1Y KRONEN FUER JYY LEI`. The fifth ciphertext group is `FVDXV`, with an
observed `V`; all **248 coordinates** are valid. The candidate repairs
`VMN DORT` to `VON DORT` and `ZXM KURSE` to `ZUM KURSE`.

The abbreviation `HEERESAZG` is left as received. It has not been expanded
into a named army office or silently corrected to a guessed institution.
The source says `BANKEN`, plural; this edition does not replace that with
the name of a particular central bank.

## A3: stamped notes and German-bank rates

The raw 205-position reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ABGESPXABZUGSFRXZUMAUSGEDRUECKTENKRONEOBETRAGXDTXB?NKENWERDENOIT70BZW38MARKEINLYESENX?ERHANDLGXSCHWEBENXNACHIHREMABSCHL?SSSOLGENNAEHXEINZELHXKMXARMEEVERWXDEPX16Y8XJJXJ2B6XXKMXALLGXKRIEGSDE?J447XJJXJ2ANCHXX
```

</details>

Five observed-coordinate substitutions and four printed-erasure fills
produce:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
ABGESPXABZUGSFRXZUMAUSGEDRUECKTENKRONENBETRAGXDTXBANKENWERDENMIT70BZW38MARKEINLOESENXVERHANDLGXSCHWEBENXNACHIHREMABSCHLUSSFOLGENNAEHXEINZELHXKMXARMEEVERWXDEPX16Y8XJJXJ2B6XXKMXALLGXKRIEGSDEPJ447XJJXJ2ANCHXX
```

</details>

Stamped notes are to be redeemed without deductions at the crown amount
expressed on them. The German-bank clause gives raw `70 BZW 38 MARK`.
The sender says negotiations are pending and promises further details
after their conclusion. This describes a proposal and negotiations,
not proof that redemption had already taken place.

The part has **410 printed slots**, with three printed dashes at indices
114, 117 and 123, and invalid `C` at 307. The `AFXGV` group has five
characters; the extra slot suggested by the earlier OCR is absent from
the scan, so this source edition performs **no deletion**. The enlarged
crop preserves the invalid `C` rather than turning it into an observed
ADFGVX coordinate.

## The monetary labels are intact but unassigned

All positions below are zero-based. Each pair is fully observed and
unchanged by the ordinary-word repairs.

| Field | Plaintext index | Raw label | Pair | Original source indices |
| --- | ---: | --- | --- | --- |
| A2, first rate | 83 | J | FX | 211, 7 |
| A2, first rate | 84 | 1 | VG | 168, 190 |
| A2, first rate | 85 | Y | DG | 72, 157 |
| A2, second rate | 96 | J | FX | 191, 73 |
| A2, second rate | 97 | Y | DG | 158, 40 |
| A2, second rate | 98 | Y | DG | 116, 234 |
| A3, first mark amount | 64 | 7 | GA | 379, 76 |
| A3, first mark amount | 65 | 0 | AF | 290, 397 |
| A3, second mark amount | 69 | 3 | VV | 362, 148 |
| A3, second mark amount | 70 | 8 | XX | 95, 237 |

The third part also has unchanged reference fields
`16Y8XJJXJ2B6` and `J447XJJXJ2`. Their full source pairs are certified
alongside the monetary fields. They are not silently converted into dates
or departmental reference numbers.

The selected raw models contain **28** occurrences of
`0123456789JQY`; the ordinary-word candidates contain **27**. The removed
occurrence is the `Y` in raw `EINLYESEN`, which receives its own observed
coordinate repair to `EINLOESEN`. That inconvenient ordinary-word use
remains visible to any later numerical relabelling study. The inventory
also includes every such label in all five local A1 source models and
all their candidate mappings.

No exchange-rate value is inferred merely because it would look
historically plausible. The received ratios offer constraints for a
separate study only when supported by additional evidence. A bounded
search did not locate an independently checked contemporary document
stating these exact redemption terms.

## Counts, credit and reproduction

| Measure | Total |
| --- | ---: |
| Physical encrypted parts | 3 |
| Printed source slots | 999 |
| Valid observed ADFGVX coordinates | 994 |
| Modeled coordinates | 1,000 |
| Plaintext positions | 500 |
| Fixed positions in the selected raw models | 494 |
| Fixed positions in the ordinary-word candidates | 500 |
| Observed-coordinate substitutions | 21 |
| Printed-erasure fills | 5 |
| Missing-coordinate fills | 1 |
| Deleted coordinates | 0 |

The complete candidates reencrypt exactly, but their numerical-looking
characters remain raw labels. These totals do not represent 500 newly
solved key symbols or 500 independently established historical characters.

The published period key is prior work by George Lasry and colleagues;
its provenance is retained in the fixture. The three blocks were already
in the repository's OCR corpus, and A2 was already an unreviewed entry in
[`p73_new_methods/retrieval_inputs.json`](../../experiments/p73_new_methods/retrieval_inputs.json).
This contribution is a source-checked edition and exact repair audit of
those materials. No explicit body discussion was located in the bounded
2016 paper, dissertation chapter and 55-comment snapshot checks; that
negative result is not a universal priority claim.

```bash
python experiments/lei_note_exchange/verify.py --verify
python experiments/lei_note_exchange/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier reconstructs the transposition mapping independently, checks
every raw domain and repair, exhausts all one-loss boundaries, retains
all local alternative maps, verifies every untouched monetary/reference
pair and audits the complete raw-label inventory. The PDF option also
checks the full source hash and every retained crop pixel.

</details>
<!-- CASE-EDITION:END -->
