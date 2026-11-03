# Mecklenburg inquiry and Seeflugstation Ost personnel order

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.**

This package independently edits three native records on Childs **p141**, PDF
p144. The two-part A message asks for answers through Kapitänleutnant Wagner and
the Tiflis consulate about a grand duke's July letter to Herzog Karl Michael and
a possible response. The B message directs any personnel returned from
Seeflugstation Ost, formerly Sewastopol, to the **second** Seefliegerabteilung,
explicitly excluding the **first**. These are statements and requests in the
telegram, not independently verified events or biographical identifications.

All three bodies were already present in earlier repository screens. This
package supplies literal source rows, explicit glyph qualifications, full index
maps, exact editorial costs and readable editions. It uses the unchanged
published **Nov4–6** key and makes no historical first-solution claim.

| Record | Source slots | Valid coordinates | Plaintext positions | Raw fixed | Edited fixed | Observed substitutions | Source fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p141 A1 | 304 | 302 | 152 | 150 | 152 | 3 | 2 |
| p141 A2 | 422 | 416 | 211 | 205 | 211 | 5 | 6 |
| p141 B | 340 | 340 | 170 | 170 | 170 | 3 | 0 |
| Total | 1,066 | 1,058 | 533 | 525 | 533 | 11 | 8 |

The source fills comprise **seven printed dashes and one unreadable visible
glyph**. There is no insertion, deletion, frame change or key change. “Fixed”
counts algebraically single-symbol domains; source errors remain possible even
when a position is fixed. All three complete edited candidates re-encrypt
exactly with the operations in the certificate.

## Source qualifications and wording retained

At **A1 source68**, the fourth mark in `XAX?F` is overstruck or otherwise
indeterminate. The transcription uses `?` as a one-slot placeholder; the source
does not print a question mark. This is separate from A1's actual printed dash
at **109**. Both are filled in the candidate, to F and X respectively.

Two faded but legible source glyphs receive explicit sensitivity variants:

- **A1 source161 G** produces the initial B in `BXMXK`. If that glyph is masked,
  the initial character has domain **8ABGIR**, and the variant leaves it unknown.
- **A2 source279 A** produces the E in the first `ABGESANDT`. If it is masked,
  that character has domain **9EKVXZ**, and the variant leaves it unknown.

These alternatives do not fill the newly masked coordinates by assuming the
desired reading. Each retains all six complete compatibility witnesses. They
are variants of the same records, outside the primary totals. Detail crops show
the exact glyphs. The internal spacing `XAA VF` in A1 remains a five-coordinate
group; it introduces no gap.

A2 literally says **ABGESANDTHANDSCHREIBEN**, without the adjective ending E
normal German would require. It later repeats **ABGESANDT**. Both forms are
retained; the readable case brackets the spelling expansion and explicitly
keeps the repetition. `BXMXK`, `32982XBX2` and `GX4774XROEMX1` remain literal.
No unnamed grand duke, reference date or administrative abbreviation is filled
from outside context.

## Reproduction

```bash
python experiments/mecklenburg_and_seaplane_personnel/verify.py --verify
python experiments/mecklenburg_and_seaplane_personnel/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The default verifier uses the standard library and repository cipher module.
It independently reconstructs the transposition index map, checks it against
the project implementation, regenerates every domain and editing operation,
verifies the complete round trips, and retains all six witnesses for each
faded-glyph variant. The optional PDF mode requires PyMuPDF and Pillow and
checks the source PDF hash, size and all five crop images pixel for pixel.
No temporary screen or external model is needed.

[Inputs](inputs.json), [certificates](certificates.json),
[prior candidates and bounded attribution checks](prior_candidates.json), and
[catalog proposal](catalog_proposal.json) retain the complete evidence.
Readable cases: [Mecklenburg inquiry](../../cases/people/mecklenburg_inquiry.md)
and [seaplane personnel order](../../cases/military/seaplane_personnel_return.md).
The paper/thesis keyword matches for Michael concern unrelated modern
bibliography names. That bounded absence of body discussion is not a priority
claim; the published key and earlier repository readings retain their credit.
