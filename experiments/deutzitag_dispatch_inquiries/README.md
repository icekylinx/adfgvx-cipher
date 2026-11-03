# DEUTZITAG dispatch inquiries and an adjacent Tiflis order

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

Childs p80 A and p81 A/C preserve three versions of a commercial inquiry asking whether purchases had already been dispatched, when and where future dispatches would occur, and how onward transport was planned. The two short versions are **identical across all 274 source coordinates**. The longer version has a 32-character addressee before the same 137-character inquiry, with one local source error explicitly repaired by the two other witnesses.

The adjacent p81 B is a **separate military order** permitting a pioneer detachment to remain in Tiflis. It is included because the same source page and published key allow a complete, reversible reading. It is not joined to the commercial traffic.

Read the [commercial edition](../../cases/finance/deutzitag_dispatch_inquiries.md) and [pioneer-detachment edition](../../cases/caucasus/tiflis_pioneer_detachment.md). The exact source inputs are [inputs.json](inputs.json), the [crops](sources/), and [certificates.json](certificates.json).

## Literal source and comparison

All four advertised lengths match the source: 274, 338, 132 and 274 coordinates, respectively. Every coordinate is observed. Earlier OCR question marks are corrected from the scan; they are not treated as erasures in the historical ciphertext.

The p81 A group `AXGXD` contains an overprinted second glyph, read as X; a ten-times-scale source crop retains its appearance. Its received addressee reads `FUERXSAULXWEINREICHXDOPPELPUNKTX`. No personal identity is inferred from that name alone.

Only one ordinary-word repair is used: p81 A source index 248 `G → F` changes `DRAHTETJB` to `DRAHTETOB`. The 137-character suffix then agrees with both short versions at every plaintext position and every underlying coordinate pair. All three position mappings are frozen, including the original J. This changes a local coordinate, not the published square or the global meaning of J.

The p81 B source decrypts directly without any repair. Both `4452` and `BX103830XO9` remain exactly as received. In particular, the final `O9` is not silently changed to `OP`.

The printed page headings are 30 October 1918; the three commercial receipt headers are on 31 October and their origin headers say 30 October. The pioneer receipt is on 30 October. These source dates are all retained.

## Counts, attribution and limits

There are four physical records, 1,018 observed coordinates and 509 fixed plaintext positions. There is one observed-coordinate substitution, no erasure fill, no insertion/deletion, and no key or rank change. The 137-character inquiry is represented in three physical records and is not counted as three independent unique texts.

All four bodies were recognizable in earlier unreviewed repository screens. Those candidate strings and hashes are frozen. A bounded check of the Lasry–Niebel–Kopal–Wacker paper, Lasry dissertation and cached 2017 discussion located no explicit body discussion under the recorded search terms; this is not proof of priority. The contribution is source verification and a precise repeated-witness certificate, not first historical decipherment.

The inquiry requests information, so it does not establish that a particular purchase was shipped. The pioneer permission does not independently establish whether the detachment actually stayed.

## Reproduce

Run from the repository root with Python 3.10 or later:

```sh
python experiments/deutzitag_dispatch_inquiries/verify.py --verify
python experiments/deutzitag_dispatch_inquiries/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary check uses the standard library and repository cipher module. It independently rebuilds the inverse column mapping, every plaintext domain, all three shared-body coordinate witnesses, and the single repair, then compares the frozen certificate. The PDF option additionally needs PyMuPDF and Pillow and reproduces the source crops pixel for pixel after checking the PDF hash.
