# p203 C / p210 C — inquiries about Richter in Aleppo

[ADFGVX Cipher](../../README.md) · [All readings](../README.md) · [Source certificate](../../experiments/corpus_recovery/certificates.json)

**Records:** two related personnel inquiries, on 18 and 20 November 1918,
under different published period keys. **Result:** the earlier message
fixes **93 of 96 raw positions** without any source edit. The later fixes
**201 of 204**, and its readable body requires six coordinate substitutions
and three source-erasure fills. Their postal-number fields differ; they
are not forced into one recovered number.

## The earlier inquiry, p203 C

> K.M., Abt. Nachrichtenmittel, erbittet Nachricht Verbleib Untffz.
> Richter, Funkerpark Aleppo, Feldpost ???.

**Meaning:** The War Ministry's communications-equipment section asks
for news of the whereabouts of an NCO named Richter at the radio park
in Aleppo. Its field-post number remains unresolved.

The source abbreviation **UNTFFZ** is retained. Its interpretation as an
NCO is supported by the later message's directly read **UNTEROFFZ**.
The earlier message itself does not supply the first name Kurt.

```text
KMXABTXNACHRICHTENMITTELXERBITTETNACHRICHTVERBLEIBUNTFFZXRICHTERXFUNKERPARKXALEPPOXFELDPOSTX???X
```

All **192** coordinates in [p203 C](../../experiments/corpus_recovery/sources/p203_C.png)
are valid and unchanged. The three question marks are unknown square-cell
values, not damaged source glyphs. The source section belongs to the
**18 November** heading, below an earlier 16 November section:

```text
XYZ v LP (03.51 p.m., November 18th)
IWE KOW AS FUER XYZ 14.50 (18/11)
RICHI-192
```

## The later inquiry, p210 C

The same-length editorial reconstruction reads:

> Ist ueber den Unteroffz. Kurt Richter, Aleppo, Armeenachrichtenpark
> J527, Deutsche Feldpost 227, Auskunft ueber jetzigen Standort oder
> Verbleib zu erfahren? [Raw following character: J.]
> Nr. Q90 strich JJ, J4, A. Nch. Kriegsminist., Allgem.
> Kriegsdepartement.

**Meaning:** The later message asks whether information can be obtained
about the current location or whereabouts of NCO Kurt Richter in Aleppo,
giving an Army Signals Park designation and field-post number. The name
**KURT RICHTER**, Aleppo, and **FELDPOST227** are directly read.
The designation **J527**, references **Q90 / JJ / J4**, and the isolated
`J` following `ERFAHREN` remain literal. They are not silently converted to
numerals or a reconstructed reference.

The [p210 C source](../../experiments/corpus_recovery/sources/p210_C.png)
has **408** coordinate slots and this header:

```text
XYZ v LP (02.55 p.m., November 20th)
17.40 (20/11)
RICHI-408
```

Its raw decipherment under the unchanged Nov19–21 key is:

```text
IS0XEBERDENUNTEROFFZXKURTXRICHTERXALEPPOXARMEENACHRICHTENPARKXJ527XDEUTSCLEFELDPOSTX227XAUSKUNFTUEBER3ETZIGENSTANDORTOWERVERBLEIBZUERFAHRENJXNRXQ90STRICHJJXJ4XAXNCHX?RIEGSMINISTXALLGEMXK?I?GSDEPARTEMENTXX
```

The invalid source glyphs in **AFEVF**, **CXVVA** and **EGFDF** retain
their positions in the literal transcript. For analysis, they are masked
as erasures at source indices **302, 365 and 385**. The candidate fills
those slots with **F, G and F**, respectively. The remaining body repairs
change six valid coordinates:

| Source index, zero-based | Source | Proposed |
|---:|:---:|:---:|
| 50 | G | X |
| 61 | G | F |
| 230 | A | X |
| 265 | A | X |
| 316 | G | F |
| 378 | X | V |

These give the readable opening `IST UEBER`, `DEUTSCHE`, `JETZIGEN`,
`ODER` and the War Ministry closing. The candidate preserves **399 valid
source coordinates** and re-encrypts exactly after the six changes and
three fills. It adds no plaintext letters and does not change the key.
The question mark in the spaced German is editorial punctuation; the
following literal `J` is explicitly acknowledged above.

## Why the postal number is not transferred across keys

The shared surname, rank and Aleppo location support reading these as
related inquiries. They do not establish that the address fields were
identical or copied without error.

| Message and positions | Printed-key result | Observed pairs |
|---|---|---|
| p203 C, 92–94 | `???` | `VA VA VV` under Nov16–18 |
| p210 C, 84–86 | `227` | `DG DG DA` under Nov19–21 |

The earlier first two digits are one shared unknown, and the last digit
must be different under an injective square. The base domain for each
cell is `{0,3,4,5,6,7,8,9}`. The later **227** cannot simply be copied back:
that would put `2` at **VA**, while the unchanged Nov16–18 square already
puts `2` at **DV**. The coordinate certificate checks this conflict.

The separate [p201/p206 order-date inference](p201_p206_orders.md)
conditionally assigns **VA=5**. If accepted, it would make this earlier
field `55?`; it would not settle the mismatch with `227`. This edition
preserves the evidence without selecting a changed address, a copying
error, or a different digit labelling as the explanation.

## Source, reproduction and credit

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed pp. 203 and 210 / PDF pp. 206 and 213 in the
[public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [source package](../../experiments/corpus_recovery/README.md) preserves
literal rows, source images, complete published key snapshots and every
plaintext-to-coordinate map. The existing keys retain their external
attribution in [data/keys.json](../../data/keys.json).

Source inspection, related-message comparison and this edition:
**icekylinx and GPT-6 Astra Pro**. No first historical decipherment priority
is claimed.

```sh
python3 experiments/corpus_recovery/verify.py --verify
```
