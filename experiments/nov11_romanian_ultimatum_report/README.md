# Evening report on the Romanian evacuation ultimatum

**Recovery and edition: icekylinx and GPT-6 Astra Pro.**

A source-frame correction restores the p180 D1 report to OHL. Its 98-position
reading describes an unanswered Romanian ultimatum and retains the literal
phrase `24 STUNDEN VOR DER WAFFENSTRECKUNG`. The new body needs two changes
to observed coordinates; the other additions fill explicitly recorded
source masks and missing coordinates.

[Read the report](../../cases/military/nov11_romanian_ultimatum_report.md)
· [Reviewed inputs](inputs.json)
· [Complete certificate](certificates.json)
· [Independent check](independent.py)
· [Original PDF, p183](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)

## Source and frame

The original has **197 printed slots**, against advertised `RICHI-196`:
187 observed coordinates, nine dashes and one invalid `O`-like glyph.
A second inspection independently confirmed every glyph, the receipt time
**03.49 p.m.**, the genuinely repeated `XGVXD` groups, and the two final As.
The page heading is partly handwritten; its receipt header says November 11,
while the separate originating-time field is simply `22.20`.

The conditional frame excludes one repeated five-group and one final A,
then inserts five missing coordinates. The complete search compares every
insertion boundary in the retained 191-coordinate stream:

| Check | Scope and result |
|---|---|
| One-coordinate exclusion alone | All 197 exclusions; minimum 17 observed changes for the fixed candidate |
| Duplicate group, final A and five losses | 2 × 2 × 192 = 768 source maps; minimum two observed changes |
| All minimum maps | Eight: four identical-group/end-A origins, with each of two gap boundaries |
| Primary gap | Before original source 150; retained boundary 145; 85/98 raw labels fixed |
| Alternative gap | Before original source 151; retained boundary 146; 84/98 raw labels fixed |
| Complete candidate | Identical 196-coordinate ciphertext and 98-position text in all eight maps |

The primary inserted group is `DXXDD`; the alternative supplies `XXDDD`.
They exchange the origin of a neighboring D. Both geometries are retained.
The finite minimum is conditional on the stated lexical candidate and frame
family; the source model and all repair prices accompany the reading.

## Exact repair prices

- **Six observed source slots excluded:** one `XGVXD` occurrence and one final A.
- **Five inserted coordinates filled**, separate from the printed masks.
- **Ten source-mask fills:** nine dashes and the literal invalid O-like glyph.
- **Two observed substitutions:** source 40 `V→X` and source 121 `X→D`.

The two substitutions produce the E in `FORDERTE` and the O in
`BEANTWORTET`. The second costs a real observed-coordinate change even
though its prior pair pointed to an unknown square cell. The published
Nov10–12 key, the literal `24`, and the negative `NICHT` remain unchanged.
`Rumaen.` retains the encoded abbreviation instead of adding an expansion.

The separate [p175 ultimatum report](../romanian_ultimatum_companions/README.md)
is related context. No plaintext or coordinate is copied from it.
The earlier unreviewed p180 OCR fragment is preserved in `prior_ocr.json`.

## Reproduce

```sh
python experiments/nov11_romanian_ultimatum_report/verify.py --verify
python experiments/nov11_romanian_ultimatum_report/independent.py --verify
python experiments/nov11_romanian_ultimatum_report/verify.py --verify --pdf /path/to/childs.pdf
```

`independent.py` implements the ragged-column cipher directly and imports no
project cipher, transposition or geometry helper. Both implementations compare
all 768 maps and agree on all eight minima, raw streams, original-coordinate
maps, mask and insertion counts. The main verifier also checks the actual
Markdown source, raw, edited and German displays and full re-encryption.
The PDF option reproduces the crop dimensions and RGB hash from the original
scan; new image bytes are not required for the default proof.

The period key and prior digital source retain their individual credits.
The present source review, frame restoration and evening-report reading
are by **icekylinx and GPT-6 Astra Pro**.
