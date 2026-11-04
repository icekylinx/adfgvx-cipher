# September radio listening and acknowledgment procedure

Source edition and independent verification: **icekylinx and GPT-6 Astra Pro**.

The three cipher frames on Childs printed p60 yield a two-part instruction
to listen at agreed daily times and a separate request to send traffic
continuously during reception of the Nauen press, with acknowledgment afterward.
The [reader edition](../../cases/pages/060.md#edition-cases-radio-september-radio-procedure) provides
the German text, English explanation, literal headers and numerical caveats.

## Evidence and scope

| Physical record | Advertised / transcribed slots | Valid received coordinates | Raw fixed positions | Editorial substitutions | Erasure fills |
| --- | ---: | ---: | ---: | ---: | ---: |
| p60 A1 | 176 / 176 | 174 | 86 / 88 | 0 | 2 |
| p60 A2 | 154 / 154 | 154 | 77 / 77 | 0 | 0 |
| p60 B | 226 / 226 | 224 | 112 / 113 | 3 | 2 |
| Total | 556 / 556 | 552 | 275 / 278 | 3 | 4 |

The total uses a conservative transcription of B's damaged group-7 initial
glyph as an erasure. A separate conditional reading of that glyph as `F`
reduces B's erasure-fill cost from two to one and restricts its one unknown
plaintext label to `8EHISY`. It does not add a second physical record or
increase the number of raw fixed plaintext positions.

There are no inserted, deleted or moved source slots. An older OCR screen
had omitted a visible `G` from A1 and inserted an extra `X` in A2. The manual
source transcription restores the printed 176- and 154-slot frames. These
are corrections to OCR, not changes to the historical ciphertext.

## Reproduction

```sh
python experiments/september_radio_procedure/verify.py --verify
```

The default verifier uses only Python's standard library. It checks every
bundled image hash, the rows and exact source lengths, independent ragged
column inversion, all plaintext domains and source-position pairs, the
proposed edit/fill ledger, raw numeral preservation, and exact re-encryption.
The 22-column ranks and complete square are frozen in `inputs.json`; no
search, dictionary or mutable model is needed. The script implements its
own arithmetic and does not import the repository cipher engine.

Optional verification against the complete source PDF also checks its
SHA-256 and regenerates all seven image crops at their recorded coordinates:

```sh
python experiments/september_radio_procedure/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

That option requires PyMuPDF. Source PDF SHA-256:
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
Printed p60 is PDF page 63. `inputs.json` records the crop rectangles, render
scales, image-file hashes and uncompressed-pixel hashes. The default and PDF
verification commands both passed when this package was prepared.

`certificates.json` is deterministic. Running the command without `--verify`
rebuilds it. The certificate counts 272 editorial positions directly supported
by unchanged, complete received coordinate pairs. The remaining six positions
are three plaintext repairs and three unknown positions requiring four
coordinate fills. All repeated numerical fields remain literal.

## Credit and interpretation limits

The unchanged `Sep19-21` key is prior published work by **George Lasry, Ingo
Niebel, Nils Kopal and Arno Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also reproduced in George Lasry's [24 February 2017 comment 4](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
Childs's collected intercepts are the primary source. Earlier unreviewed
OCR-derived candidate strings existed; this edition claims source checking,
frame recovery, readable presentation and exact repair accounting. It makes
no universal first-decipherment claim.

Exact re-encryption establishes the proposed reading's arithmetic consistency
and its stated edit cost. It does not prove that an editorial fill, repair,
abbreviation expansion, numeral interpretation or damaged-glyph reading is
historically unique. The clear B service annotation and its referenced parts
remain separate from the recovered 226-slot body.
