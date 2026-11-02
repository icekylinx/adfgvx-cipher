# Crown airlift and an interrupted banknote instruction

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

This source edition covers Childs **p174 A1–A3**, a three-part message of
10 November 1918. The first two parts request the daily dispatch of one
million crowns by ordinary aircraft, alternately to Kronstadt and
Hermannstadt. The interrupted third part supports a request for notes of
the smallest practical denomination. The [case](../../cases/finance/crown_airlift.md)
keeps the literal decryptions and the editorial limits together.

The source prints 146, 146 and 79 coordinates or coordinate-sized glyphs.
The last part is advertised as 98 and explicitly marked **“Did not finish.”**
Its intact `GAVGX` group was omitted in earlier OCR. With 19 missing
coordinates appended after the observed transmission, the third raw
reading is:

```text
INM???LICHS???EINEN???EINEN???DENLX???1A4A1????OP
```

The candidate restores the first 33 letters to
`INMOEGLICHSTKLEINENSCHEINENSENDEN`. This fills **12 absent coordinates**
and changes **no observed coordinate**. Seven absent coordinates remain
unfilled. The observed `L` after `SENDEN`, the raw `1A4A1` field and all
remaining question marks are retained.

## Exact scope and ambiguity

| Quantity | Count |
|---|---:|
| Physical cipher records | 3 |
| Printed source slots | 371 |
| Valid printed ADFGVX coordinates | 370 |
| Modeled coordinates | 390 |
| Plaintext positions | 195 |
| Fixed raw positions under the declared models | 175 |
| Fixed positions in the explicit candidates | 188 |
| Observed-coordinate substitutions | 1 |
| Printed invalid-glyph fills | 1 |
| Missing-tail fills | 12 |

The single substitution repairs `ABWECHSWLND` to `ABWECHSELND` in A2.
The printed `C` at A2 source index 80 is modeled as an erasure; filling it
with `D` produces `FELDKRIEGSKASSE`. Neither repair changes the key.

The interruption annotation motivates the primary trailing-gap model.
It does **not** make the geometry mathematically unique. An exhaustive
screen of all 80 positions for one 19-coordinate gap, using only the
ordinary first 33 letters and masking the entire final 16 positions,
finds three zero-substitution fits: gaps **77, 78 and 79**. All three raw
readings, candidate readings, source maps and fills are retained in
`certificates.json`. Their reference fields differ. The candidate words
are a contextual reconstruction compatible with the source, not uniquely
determined absent text.

## Attribution and interpretation

The unchanged period key is the published Nov10–12 key. Earlier repository
screens already contained A1 and A2 as unreviewed OCR-derived candidates;
their bodies and original screen hashes are frozen in `inputs.json`.
The new contribution is the source transcription, recovery of the omitted
`GAVGX` group, the interrupted-part model and exact repair certificates.
A bounded check found no explicit body discussion in the Lasry et al.
paper, the dissertation chapter or the cached 55-comment thread. This is
not a claim of first historical decipherment.

`EINE MILLION` is transmitted as ordinary words. No amount is inferred
from a raw numerical label. The message requests daily deliveries; it
does not establish that flights took place or that the money arrived.
The unpunctuated `FELDKRIEGSKASSE` at the A2/A3 boundary is preserved
without supplying an unseen office instruction.

## Reproduce

```bash
python experiments/crown_airlift/verify.py --verify
python experiments/crown_airlift/verify.py --verify --pdf /path/to/childs.pdf
```

The first command independently reconstructs the coordinate mappings,
plaintext domains, repairs and all gap alternatives. The optional PDF
argument checks the full source hash and re-renders every crop for an
exact pixel comparison. `catalog_proposal.json` contains three proposed
rows; this package edits no shared catalog or key.
