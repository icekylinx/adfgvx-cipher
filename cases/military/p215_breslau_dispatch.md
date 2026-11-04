# p215 A — Breslau–Oderberg dispatch fragment

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[All cases](../README.md) · [ADFGVX Cipher](../../README.md)

**Recovery and review: icekylinx and GPT-6 Astra Pro, 4 November 2026.**
A conditional relocation of five printed mask slots reveals a dispatch from
Breslau via Oderberg, mentioning wagonloads and accompanying personnel.
The unchanged published November 22–24 key fixes **176/196 raw positions**.
All **372 observed coordinates remain unchanged and in their original relative order**.

## Most likely reading

**Readable German — excerpt from the conditional raw frame; omitted passages remain outside this quotation and J stays a literal square label:**

> […] Breslau ueber Oderberg in J Waggonladungen und J Begleitern […]

The raw passage identifies the route and transport terms. It does not by itself
authenticate the numerical value of either `J`. The opening, equipment words,
quantities and closing still contain garbles or unresolved positions in this
initial edition. No source-mask fill or observed-coordinate substitution has
been made to obtain the raw output.

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

## Credit and reproduction

Childs supplied the historical source; George Lasry and colleagues supplied the
published period key. This source-frame discovery and edition are by
**icekylinx and GPT-6 Astra Pro**. Earlier sources and key credits remain in the
[registered key](../../data/keys.json) and the [recovery package](../../experiments/p215_breslau_dispatch/README.md).

```sh
python experiments/p215_breslau_dispatch/verify.py --verify
python experiments/p215_breslau_dispatch/verify.py --verify --pdf /path/to/childs.pdf
```
