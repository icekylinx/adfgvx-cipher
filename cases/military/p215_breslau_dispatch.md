# p215 A — Breslau–Oderberg dispatch fragment

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[All cases](../README.md) · [ADFGVX Cipher](../../README.md)

**Recovery and review: icekylinx and GPT-6 Astra Pro, 4 November 2026.**
A conditional relocation of five printed mask slots reveals a dispatch from
Breslau via Oderberg, mentioning wagonloads and accompanying personnel.
The unchanged published November 22–24 key fixes **176/196 raw positions**.
In that raw layer, all **372 observed coordinates remain unchanged and in their original relative order**.
A separately priced word restoration now identifies horseshoes, hoof nails,
screw nails and the closing **Traindepot Breslau**; its primary layer fixes
**192/196 positions**, including still-uninterpreted numerical labels.

## Most likely reading

**Readable German — excerpt from the conditional raw frame; omitted passages remain outside this quotation and J stays a literal square label:**

> […] Breslau ueber Oderberg in J Waggonladungen und J Begleitern […]

The raw passage identifies the route and transport terms. It does not by itself
authenticate the numerical value of either `J`. The displayed raw stream still contains garbles and unknowns. The word layer
below restores the equipment terms and closing, while leaving numerical
uncertainty explicit. No source-mask fill or observed-coordinate substitution
has been made to obtain the raw output.

## Source and conditional frame

The source header is `A) ZON v BSL (04.50 a.m., November 23rd); WORGAG DORT NR C4A6688;1500(11/22);RICHI-392`.
It means BSL to ZON, received at 04:50 on November 23, with the separate
origin field `1500(11/22)`. The unusual `WORGAG` is preserved as printed.

The literal body contains **390 source slots: 372 valid coordinates and
18 printed dashes**, beneath the advertised `RICHI-392`.
All indices below are zero based and ranges are half open.

1. Insert one unknown coordinate before source157, inside `AFFA`, and one
   before source185, inside `VDGA`. These are two additional unknown slots.
2. Move the five existing printed masks at source[198:203] to boundary270
   of the 387-slot stream remaining after their removal. The final mask block
   occupies model[270:275], between the original `VDGFX` and `FDFFA` groups.

This is an explicit analysis-frame repair, not a changed transcription or an
OCR correction. The source prints the all-dash group at the start of its sixth
body row. Every source slot is retained exactly once. Choosing any contiguous
five masks inside source[195:208] gives the same analysis ciphertext, with nine
different mask-identity maps; none is treated as a new message or an additional
reading. Further frame alternatives remain possible.

**Source transcription — untouched body:**

```text
FFFDA FXFFF GFVGG XFVVA DDAGX GADGG XDVXF XGAAA
FGVGG AVFXA VAAXD FVXGX FFAGG VAXFF FGAGX FDGAV
AVXDG VDGGG VAXGA AVDFF AXDAX FVFVF XVAAF AFFXG
XVVAD ADGXA XGAVX FXFGG XXAFF DVFGD GFFDG AFFA
XVXVD XADGA FAVAA VDXFG VXDXG VDGA AFGGX GX---
----- ----- GVDAX DAVAF GFXAA AFFAF GVDV- XFVFF
XDXFX VFXDV FFAGG FFVXV XVG-A VXXXF VDGFX FDFFA
GAFDD GXXDF GFGXX GFFDD XXDAV GDXAX XGFAG XDVVG
AVXFA VGVDF -FGAG FAFFF --XVX VXVVF GAFGX DDAXV
ADXDV VXVXG VDDGV GVVXV XVADV FXGGF DA
```

## Raw output and evidence

**Raw output — conditional 392-slot frame, unchanged published key, 176/196 fixed positions, no coordinate substitutions or fills:**

```text
D6EABSENDUNGRUERXYYXAR?PEDRI?GXBE??ETIG?ENXJ??11XPAARHU??ISENUND9K??11111XHUF??EGELUNDSC?RAUBNAEGEL?ST??UTEX?BBRESLAUXUEBERODERBERGINXJXWAGGONLADUNGENUNDXJXBEGLEITERNER6OLGTXN?AINDEPO?XBRESLAT5J85
```

The [source and frame certificate](../../experiments/p215_breslau_dispatch/certificates.json)
lists all 196 domains, both coordinate origins for every plaintext position,
and a complete re-encryption witness. Its arbitrary fills serve only to verify
the cipher arithmetic and are not asserted as historical text.

The source crop is bound to the original Childs PDF by its page, pixel rectangle
and SHA-256. Independent arithmetic reproduced the complete 225,250-description
whole-group search and its two tied leaders. Two fresh same-shape group-error
controls recovered every one of their 176 fixed positions. Those tests establish
capability within the declared scope, not unique historical geometry.

## Proposed words and alternative mask positions

**Edited output — primary whole-group frame; 6 observed-coordinate substitutions, 14 printed-mask fills and 2 inserted-slot fills; 192/196 fixed positions:**

```text
DIEABSENDUNGFUERXYYXARMEEDRINGXBENOETIGTENXJ??11XPAARHUFEISENUND9K??11111XHUFNAEGELUNDSCHRAUBNAEGELISTHEUTEXABBRESLAUXUEBERODERBERGINXJXWAGGONLADUNGENUNDXJXBEGLEITERNERFOLGTXTRAINDEPOTXBRESLAU5J85
```

**Readable German — the same primary edited stream with spacing and separator punctuation; numerical labels and unresolved quantity positions remain literal:**

> Die Absendung fuer YY Armee dring. benoetigten J??11 Paar Hufeisen und 9K??11111 Hufnaegel und Schraubnaegel ist heute ab Breslau ueber Oderberg in J Waggonladungen und J Begleitern erfolgt. Traindepot Breslau 5J85.

**Meaning:** A dispatch of urgently needed horseshoes, hoof nails and screw
nails has left Breslau via Oderberg, with wagonloads and accompanying personnel.
The closing is read as Traindepot Breslau. The number of the army, shipment
quantities, wagon and escort counts, and closing identifier are not authenticated
by the baseline numeral labels. `DRING` is retained as an abbreviation; no missing
article is silently inserted into the telegraphic wording.

The primary word proposal changes six clear source coordinates. These are
editorial repairs, not improved OCR:

| Source index | Printed | Proposed |
|---:|:---:|:---:|
| 269 | D | G |
| 270 | G | D |
| 271 | F | G |
| 272 | X | F |
| 316 | V | F |
| 334 | A | V |

Each of its 16 newly filled word positions already has one observed half-coordinate.
There are no wholly unobserved word positions in that gain. The complete ledger
keeps printed-mask fills separate from the two fills in inserted slots.

Moving the same five masks to a coordinate-level boundary inside `VDGFX`
produces two serious alternatives. The selected primary keeps the original
whole-group discovery for continuity; it is neither the highest-scoring nor
the least-edited candidate. The same ordinary-word proposal is tested separately
in each frame:

| Mask destination in shortened frame | Selection basis | Raw fixed | Word fixed | Observed substitutions | Printed-mask fills | Inserted-slot fills |
|---:|---|---:|---:|---:|---:|---:|
| 270, primary | Whole-group discovery; blind rank 23 | 176/196 | 192/196 | 6 | 14 | 2 |
| 268 | Highest blind joint-language score | 176/196 | 193/196 | 4 | 15 | 2 |
| 266 | Fewest substitutions for the proposed words; blind rank 34 | 176/196 | 194/196 | 3 | 16 | 2 |

The 268 model inserts the masks between original source 270 and 271; the 266
model inserts them between original source 268 and 269. The comparison covers
9,700 frames: 25 possible short-group placements and 388 mask destinations.
The word-cost result is conditional on the proposed words, not an independent
plaintext discovery. A language-score optimum is not historical proof.

The three word streams agree at **192/196 positions**. Their differing quantity
fields are deliberately not pooled:

| Destination | Before `PAARHUFEISEN` | Between `UND` and `HUFNAEGEL` |
|---:|---|---|
| 270 | `J??11` | `9K??11111` |
| 268 | `J??11` | `9K?Y11111` |
| 266 | `J?J11` | `9K?Y11111` |

Thus positions 44,45,66,67 remain unresolved in the shared reading; even the
remaining fixed digit labels do not acquire historical values. No registered
square, shared numerical assignment or footer number is changed here.

After the word fills, `AFFFA` permits insertion before source 156,157 or158,
and `VVDGA` permits insertion before 184 or185. Together with nine mask-identity
choices, each word model has 54 equivalent ownership descriptions and one
identical corrected ciphertext. These are explanations of the same evidence,
not 54 independent confirmations. The primary unfilled gap positions 157/185
are a specified analysis choice, not a unique historical inference.

A contemporary institution witness independently supports the closing vocabulary:
[Lublinitzer Kreisblatt, 19 April 1918, printed p. 193, notice 274](https://sbc.org.pl/Content/735084/PDF/iii350718-1918-16-0001.pdf)
mentions the Traindepot of the VI Army Corps in Breslau. Its vehicle-sale notice
is not a copy of this November telegram and proves no shipment, quantity or
sender identity. The [context record](../../experiments/p215_breslau_dispatch/historical_context.json)
preserves the source URL, PDF hash and crop recipes without adding large images.

## Credit and reproduction

Childs supplied the historical source; George Lasry and colleagues supplied the
published period key. This source-frame discovery and edition are by
**icekylinx and GPT-6 Astra Pro**. Earlier sources and key credits remain in the
[registered key](../../data/keys.json) and the [recovery package](../../experiments/p215_breslau_dispatch/README.md).

```sh
python experiments/p215_breslau_dispatch/verify.py --verify
python experiments/p215_breslau_dispatch/verify.py --verify --pdf /path/to/childs.pdf
```
