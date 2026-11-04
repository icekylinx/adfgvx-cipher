# Delegation travel and Danube field reports, 10–11 November

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

This package supplies four source-exact physical records from two different
messages: **p175 A1/A2**, concerning delegates travelling through Spa toward
Berlin, and **p176 B2/B3**, the final two parts of a field report. Both use
the unchanged published **Nov10–12** key. They are not a shared-plaintext
family. The 2016 paper already discusses the p175 travel message; the
earlier repository screen also contained candidate readings of all four
parts. The present contribution is a reversible source edition and an
explicit uncertainty and attribution record.

Read the cases for [delegation travel](../../cases/pages/175.md#edition-cases-people-spa-berlin-delegates)
and the [Danube field report](../../cases/pages/176.md#edition-cases-military-nov10-danube-field-report).

## Source and arithmetic

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed pp175–176, PDF pages 178–179. The complete PDF identity,
literal rows, source headers, crop rectangles and image hashes are in
[inputs.json](inputs.json). All four literal streams have the length
advertised by their own part headers.

| Part | Source coordinates | Plaintext positions | Raw fixed labels | Candidate fixed labels | Observed-coordinate substitutions |
| --- | ---: | ---: | ---: | ---: | ---: |
| p175 A1 | 192 | 96 | 96 | 96 | 4 |
| p175 A2 | 104 | 52 | 51 | 51 | 1 |
| p176 B2 | 252 | 126 | 125 | 126 | 1 |
| p176 B3 | 272 | 136 | 136 | 136 | 4 |
| **Total** | **820** | **410** | **408** | **409** | **10** |

There are **no source erasure fills, modeled gaps, deletions, source
reordering or published-key changes**. The fixed-position counts refer
to labels under the published square; they are not 409 independently
proved historical characters or 409 newly discovered characters.
Coordinate substitutions are editorial repairs, even when the resulting
word looks ordinary. The certificate preserves every pre-repair label.

An enlarged [p176 B3 group crop](sources/p176_B3_group.png) reads `VDVAV`.
A temporary manual transcription had accidentally doubled its `D`.
That scratch error is rejected: there is no 273-coordinate historical
source or source-deletion hypothesis in the edition.

## Exact repairs

Indices are zero-based in each native literal ciphertext.

| Part | Observed-coordinate changes | Plaintext effect |
| --- | --- | --- |
| p175 A1 | 14 V→F; 69 V→F; 121 D→G; 145 X→V | `MANNITAED1→MANNSTAEDT`, `NAMUT→NAMUR`, `ODET→ODER` |
| p175 A2 | 70 D→F | `NACWM→NACHM` |
| p176 B2 | 108 F→G | `ENGLAEN?ERN→ENGLAENDERN` |
| p176 B3 | 52 X→V; 216 X→D; 217 X→D; 226 V→A | `BELEG1→BELEGT`, `RUS2UK→RUSTUK`, `SNE→SIE`, `NOERDLNCH→NOERDLICH` |

The B2 question mark is an unknown **square-cell label** at pair `FD`,
not an erased coordinate. Reading `D` requires the stated observed
coordinate replacement; it does not assign an unknown key cell.
[certificates.json](certificates.json) gives the original and repaired
pair, both source indices and the complete domain at every plaintext
position. Its independent column-offset inversion is checked against
the repository cipher implementation. Complete candidates re-encrypt
exactly; the one partial candidate receives the finite completion audit
below.

## The time is still unknown

p175 A2 retains `AM11X11X?X03XNACHMXOHLRM4BX`. The unknown at plaintext
position **33** is pair `FD`, from observed coordinates **42 and 69**.
Its unchanged published-square domain is **56789**. The following
`03`, the date-like `11X11` and reference `OHLRM4B` are retained literally.

The verifier enumerates all **120** injective completions of the five
unassigned square cells. Every completion preserves the exact repaired
ciphertext. There are **five** distinct literal candidate plaintexts,
with **24** completions for each of the five possible time digits.
One full-square witness for each digit is frozen in the certificate.
These completions demonstrate compatibility; none is asserted to be
the historical square.

Lasry et al., §6.4, author PDF page 24, discuss this p175 A message together
with p172 C and give a Berlin arrival time of 15:00. This source edition
does not import that narrative time into the distinct literal `?X03`
field or silently reinterpret onward travel as arrival. It also does
not establish the paper's personnel or regimental identifications from
these four source parts alone.

## Relations and attribution

The p175 source labels A1/A2 as two parts of one message. Its time is
22:57 on 10 November. Existing p171 C / p172 E contain a related Namur
and Weiher instruction, but are not exact copies of this text. In
particular, their `HPTMANNSTAEDT` string can be segmented differently
from this message's `HPTMXMANNSTAEDT`; this package asserts neither a
new personal identification nor a correction of the earlier edition's
2,048 minimum-cost alternatives. `EXIX2` is not normalized to its
`INSP1IN` field.

p176 B's header says `2305 (10) 3 TLE`, received at 03:38 on 11 November.
Its first part is already cataloged as **p176b**, with earlier credit to
**Prinz and GPT-6 Astra, 19 September 2026**. That part, its reconstructed
20-coordinate shortage and its unknown unit digits are excluded from
the new-record counts. These two companion parts do not recover the
missing block or assign those unit digits. Shared geographical names
with the Nov9 and Nov3 reports do not establish retransmissions.

The prior checks and explicit references are recorded in `inputs.json`.
[prior_candidates.json](prior_candidates.json) freezes the four earlier
unreviewed readings with their source-cache hashes. Absence of a
particular body from the bounded paper/comment check is not proof that
no earlier researcher read it. There is no first-decipherment claim.

## Reproduce

From the repository root:

```sh
python experiments/nov10_delegates_and_field_report/verify.py --verify
python experiments/nov10_delegates_and_field_report/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command uses the Python standard library and repository code.
The optional PDF check needs PyMuPDF and Pillow and compares the supplied
PDF's size and SHA-256, then every crop's decoded RGB pixels. The verifier
does not read the temporary candidate caches: their selected records
are frozen inside this package. The catalog proposal contains only the
four new physical records.
