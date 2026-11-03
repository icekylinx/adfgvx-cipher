# November 15: Warsaw radio personnel and a repeated key notice

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

[Read the source edition](../../cases/radio/nov15_radio_personnel_and_key_notice.md).

Three physical source records contain **461 printed slots**. The declared
frames contain **466 coordinates** and **233 plaintext positions**, of which
**221 are fixed raw labels**. The complete proposals fix 229 positions and
preserve four unresolved numerical positions in A2. Every price is separate:
**4 observed-coordinate substitutions**, **1 source-mask fill**, and **5 fills
in five hypothesized missing slots**. There are no source exclusions or
reorderings and no published-key changes.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## The personnel order

p197 A1 has 193 source slots against its advertised 198. A single five-slot
gap at source boundary 165 gives a readable partial Warsaw personnel order;
the complete candidate needs one observed substitution, one printed-dash
fill and five inserted-slot fills. All 194 possible boundaries are priced
against this exact candidate, using both the position-level repair routine
and an independent direct comparison of the encrypted candidate with the
source. Boundary 165 is uniquely cheapest within that stated family. This
is not a uniqueness claim about the historical wording or error process.

A2 is a complete native 144-slot continuation and directly reads
`FESTUNGSFUNKA POSEN IN MARSCH ZU SETZEN`. Its `INACH` and final `???6?5`
remain literal. The repeated unknown square cell in the second and third
reference positions remains coupled, with distinct values for different
cells.

## The repeated key notice

p197 B differs from the existing p189 C source at only one observed
coordinate. That difference supplies independent raw support for one of
p197's three proposed letters. The remaining two word repairs are shared
by both damaged copies and receive no independent raw support. The source
word `IRRTUM` remains uninterpreted.

## Reproduce

```sh
python experiments/nov15_radio_personnel_and_key_notice/verify.py --verify
python experiments/nov15_radio_personnel_and_key_notice/verify.py --verify --pdf /path/to/childs.pdf
```

- `inputs.json` binds the source transcriptions, unchanged published key, exact frame and readable proposals.
- `certificates.json` records every raw domain, source-to-frame position, repair, gap price, copy comparison and global completion witness.
- `sources/` contains the inspected p197 and p189 crops; the optional PDF check compares all RGB pixels with the identified original.
- `ocr_snapshot.json` and `prior_candidates.json` retain earlier OCR and explicitly recomputed unchanged-key comparison outputs.
- `catalog_proposal.json` lists the three new physical records. The already published p189 C reference is not counted again.

The source edition and explicit reconstruction are credited to icekylinx and
GPT-6 Astra Pro. Published period-key recovery and earlier repository work
retain their separate attribution. No universal first-decipherment priority
is asserted.
