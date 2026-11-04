# Additional corpus readings: shipping, couriers and military administration

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Nine source-checked parts preserve **2,322 coordinate slots** and produce
**1,161 plaintext positions** under the existing published keys. Of these,
**1,155 positions are fixed in the unchanged-source layer**. Six positions
remain unresolved: three source erasures in p210 C and three numeral
occurrences, using two unknown cells, in p203 C. Fixed source garbles remain
visible and are not silently treated as corrected historical text.

## Readable messages

| Message | Source result | Readable edition |
|---|---|---|
| p84 A/B | 223/223 fixed; no coordinate edits or fills | [Oil release and Black Sea shipping safety](../../cases/pages/084.md#edition-cases-naval-p84-ab) |
| p92 A | 214/214 fixed; one explicit substitution gives a clean body | [Dutch courier Vreede: onward passage to Constantinople](../../cases/pages/092.md#edition-cases-people-p92-a) |
| p210 A1–A2 | 208/208 fixed; four substitutions for body words and sender | [Helsinki and return transport for the Ostsee Division](../../cases/pages/210.md#edition-cases-naval-p210-a) |
| p210 B | 158/158 fixed; five body-word substitutions; date/reference strings remain literal | [Consul Burkhardt's oil-company assignment](../../cases/pages/210.md#edition-cases-people-p210-b) |
| p203 C / p210 C | 93/96 and 201/204 fixed; the later body has six substitutions and three erasure fills | [Two inquiries about Richter in Aleppo](../../cases/pages/203.md#edition-cases-people-richter-aleppo) |
| p210 D | 58/58 fixed; one substitution | [Request for the situation in Reval](../../cases/pages/210.md#edition-cases-military-p210-d) |

The editions use **17 explicitly listed valid-coordinate substitutions and
three erasure fills**, with no source-length or key changes. Their arithmetic
consistency is reproducible; their editorial choices remain separately
identified. No earlier researcher is displaced from the published key credit,
and no first-decipherment priority is claimed for these supplementary messages.

## Source and transcription

The two p84 messages need no coordinate repair. Their page heading is 30 October, while their reception headers say 1 November. The repeated IZZETPASCHA and the unexplained 0ROEM1 footer are retained exactly.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
in the [public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [inputs](inputs.json) record literal rows, full headers, PDF page/crop
coordinates and hashes. The eight [source images](sources/) are direct crops
of that hash-pinned scan.

Three OCR corrections restore what the source visibly prints, without
editing the historical ciphertext: p92 A group 15 is `VVVFG`; p210 A1 group
17 is `VFGVV`; p210 D ends `XXDDV V`, not the OCR's extra terminal `V`.
Source p210 C instead contains three invalid glyphs, in `AFEVF`, `CXVVA`
and `EGFDF`. They remain literal in the transcript and become erasures at
the same positions only in the analysis layer. In the middle group, the
leading rounded glyph is recorded as `C` rather than assumed to be `G`.

The unusual `RICHI-428?` label on p92 and `19.42 p.m.` time on p210 A are
retained. The actual p92 body has exactly 428 valid coordinates. Page 203
contains two date headings: section C belongs to **18 November**, not the
16 November heading above section A.

## Related queries and a preserved contradiction

The p203 and p210 inquiries both name an NCO Richter at Aleppo. The later
message adds the first name Kurt and fuller address details. Their postal
fields must nevertheless remain separate:

| Source | Printed-key result | Observed digraphs |
|---|---|---|
| p203 C, positions 92–94 | `???` | `VA VA VV` under Nov16–18 |
| p210 C, positions 84–86 | `227` | `DG DG DA` under Nov19–21 |

Treating the two numbers as identical would require **VA=2** in Nov16–18,
where `2` already occupies **DV**. That violates the unchanged square's
injectivity. The certificate therefore records the discrepancy instead of
using the later number to fill the earlier cells. The related subject alone
does not prove that every address detail or copy is identical. This does not
independently settle any other historical key inference.

Several date-like and reference-like `J` strings under the Nov19–21 key also
remain literal. The present package does not relabel the published square
or silently convert those strings to numerals.

## Verification

```sh
python3 experiments/corpus_recovery/verify.py --verify
python3 experiments/corpus_recovery/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

The second command optionally proves every saved image pixel against the
public source PDF, after checking the PDF's hash and byte length. The
ordinary verifier needs only the repository. It independently constructs
the sorted column layout and plaintext coordinate pairs, compares that
calculation with the project decoder, verifies every domain and source
length, and re-encrypts each complete editorial candidate after applying
exactly its listed edits. It also checks the cross-key postal-number
conflict explicitly.

The [certificate](certificates.json) lists all **1,161** plaintext positions
and their precise source-coordinate pairs. The original period keys retain
the historical and George Lasry / coauthor attribution recorded in
[data/keys.json](../../data/keys.json). Source inspection, related-message
comparison, repair accounting and this edition are by
**icekylinx and GPT-6 Astra Pro**.
