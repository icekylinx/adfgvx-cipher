# October delegation, staffing and service traffic

**Six additional source-reviewed records are readable with the previously
published Oct4–6 key.** Their exact printed frames contain **1,264 coordinate
slots**, giving **632 plaintext positions**. The raw inverse fixes **630** of
those positions; four fixed characters are explicitly corrected in the edition,
and two coordinate erasures are filled. Thus **626 proposed plaintext
positions are directly supported without a correction or fill**.

The principal new reading is the two-part personnel order on printed pp66–67:
Graf von Seyboltstorff is to move from command of the 4th Bavarian Chevaulegers
to command of the 4th Bavarian Cavalry Brigade; Oberstlt. Karl von Grundherr,
marked `ROEM1`, has already been ordered as the replacement. Both unit numerals
`4` are directly fixed. Other records concern a garbled medical telegram,
suspension of manganese-ore purchases, a Tiflis unit-location response, and
acknowledgment of a travel telegram.

Source review and certificates: **icekylinx and GPT-6 Astra Pro**. The earlier
key is credited to **J. Rives Childs**, **George Lasry**, and the
**Lasry–Niebel–Kopal–Wacker** research, as recorded in [inputs.json](inputs.json).
This is a source edition under a known key, with no first historical
decipherment or new key claim. The broader [p73 challenge](../../pages/073.md#edition-cases-p73)
remains open.

## Readings and arithmetic

The [case note](../../pages/066.md#edition-cases-caucasus-october-staffing) gives the German readings,
headers, translations and qualifications. All records use exactly the printed
coordinate frame; there is no insertion, deletion, guessed length or changed
transposition order.

| Record | Literal slots | Raw fixed positions | Proposed positions supported directly | Known-coordinate substitutions | Erasure fills |
| --- | ---: | ---: | ---: | ---: | ---: |
| p66 A |190 |95/95 |95 |0 |0 |
| p66 B |284 |142/142 |140 |2 |0 |
| p66 C1 |286 |143/143 |142 |1 |0 |
| p67 A2 |220 |110/110 |109 |1 |0 |
| p67 B |224 |110/112 |110 |0 |2 |
| p67 C |60 |30/30 |30 |0 |0 |

“Raw fixed” includes garbled but unambiguous decoded characters. It is not the
number of characters agreeing with the proposed edition. The separate direct
support column makes that distinction explicit.

The complete source rows, six source crops, header fields, literal and masked
coordinate layers, and proposed texts are in [inputs.json](inputs.json).
[certificates.json](certificates.json) records every plaintext domain, both
source-coordinate origins of every character, all edits and fills, and the
complete re-encrypted witness. The surname ending in p66 C1 and the first
letter of `[F]ISCHER` in p67 B are qualified in the case note. The original
unit abbreviations and reference numbers remain visible.

## Reproduce

From the repository root:

```sh
python experiments/october_staffing/verify.py --verify
python experiments/october_staffing/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier computes the inverse through independent column-height offsets,
compares that result with `adfgvx.cipher`, verifies every cost and re-encryption,
and checks the source-crop hashes. With the pinned PDF it also regenerates the
six crops and compares their pixels. The PDF's expected SHA-256 is stored in
the input file.

This separate package preserves the earlier October corpus and the frozen
radio-model training snapshot unchanged. The six new records have not been
added to that model's training data.
