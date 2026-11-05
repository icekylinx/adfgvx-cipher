# October routing, weather and personnel requests

Prepared by **icekylinx and GPT-6 Astra Pro**. This package preserves four
additional records from Childs pp62, 63 and 65 under the previously published
**Oct4–6 key**. Earlier key credit remains with **J. Rives Childs, George Lasry,
and Lasry–Niebel–Kopal–Wacker**. The [case note](../../pages/062.md#edition-cases-caucasus-october-requests)
gives the readings and their source limits.

| Record | Literal slots | Plaintext positions after stated layout | Raw fixed positions | Proposed positions | Known-coordinate substitutions | Erasure fills | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| p62 A | 124 | 62 | 62 | 62 | 0 | 0 | Exact source-frame reading |
| p62 B | 188 | 93 | 91 | 92 | 2 | 1 | Conditional on two unmarked deletions |
| p63 A | 270 | 135 | 133 | 114 | 12 | 2 | Partial editorial reading; 21 positions unassigned |
| p65 A | 260 | 130 | 130 | 130 | 5 | 0 | Five explicit word repairs |

The four source records contain **842 literal slots**. After the declared
p62 B layout, there are 420 plaintext positions, of which 416 are fixed by
the raw inverse. The edition asserts 398 positions; 378 need no coordinate
repair or erasure fill. Raw fixed positions include garbled characters and
must not be reported as a count of correct intended plaintext.

## Files and verification

- [inputs.json](inputs.json) preserves every source row, literal invalid
  glyph, header, key, layout and editorial template.
- [certificates.json](certificates.json) retains raw domains, coordinate
  origins, all edits and fills, the two equivalent p62 B layouts, and
  complete arithmetic witnesses. Its unaccepted p63 normalization is kept
  outside the accepted partial template.
- [sources](sources) contains four scan crops with PDF coordinates, scales,
  byte hashes and rendered-pixel hashes recorded in the inputs.
- [verify.py](verify.py) uses an independent column-height inverse and
  compares it with the repository cipher implementation. It preserves
  actual printed group positions, including the six-character `FGAFRG`
  group on p62 B.

From the repository root:

```sh
python experiments/october_requests/verify.py --verify
python experiments/october_requests/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

The second command also checks the complete source PDF hash and independently
rerenders each crop to its recorded pixel hash. Both commands exhaust all
**17,578 two-deletion layouts** for p62 B against the partial editorial template
and published key. The minimum is two known-coordinate substitutions, attained
only by deletion indices `[79, 187]` and `[80, 187]`. Those two choices remove
one of the same adjacent `FF` pair and produce identical 186-slot streams.
This is a conditional template-fit result; the scan does not mark the deletions.

Review of p62 B corrects our second-group transcription from `FVEFF` to `FVFEF`. The `L` in `WERTLOS` is observed; the actual mask supplies the first character of `FEWEWA?10`. Its domain is `018MRV`, with `0`, `1` and `8` surviving a decimal-only restriction. The earlier `110` is one compatible completion. The primary edition leaves that field unresolved.

The literal `E` and `R` on p62 B are retained as erasures. Deleting them simply
because they are outside the coordinate alphabet produces a different and
garbled result. The final `X` deletion is also explicit. No source glyph is
quietly removed or changed.

For p63 A, the source field is **`RICHI-54`**, while the body has **54 groups
of five slots**. The edition preserves that distinction. Its raw middle span
is `VASCHIWNENMECH8ISCHEN`. Fully replacing the technical expression with
`MASCHINENMECHANISCHEN` would raise the total from 12 to **28** known-coordinate
substitutions. That full reading is not accepted. The partial template leaves
all 21 positions unassigned; complete witness characters at those positions
are arithmetic fillers or retained raw values, not recovered text.

## Provenance limits

The Westernhagen surname has a separate later source witness in p70 A1, and
the clear p69 B1/B2 header names `HPTM GEMOLL`. These witnesses support the
name readings without proving every surrounding editorial repair. The
source spelling `FEZDEIRENBAHNCHEF`, the p65 `0` after the addressee, and the
references `4BX49287`, `FEWEWA?10` and `474D` remain visible.

Lasry and colleagues explicitly discuss the adjacent **p64 Hagelin/Nobel
body** in §6.6 and Table 5. That record is not included in this package.
The absence of an individual p62/p63/p65 body reference in that paper is not
a claim of first historical decipherment. These are new source editions in
this repository using an earlier published key. No p73 reading or cross-period
key assignment follows from them. The package is separate from the frozen
radio-domain training snapshot.
