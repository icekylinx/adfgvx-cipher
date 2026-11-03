# p151 fragments, annotated acknowledgment and Soldiers Council notice

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Four physical records are preserved under the unchanged published partial
**Nov7–9** key: A1/A2 are the two present parts of a source-labeled
five-part message; B is a separate acknowledgment with a handwritten
duplicate; C is a separate surrender notice. Read the
[fragments and acknowledgment](../../cases/military/nov7_fragment_and_acknowledgment.md)
and [Soldiers Council notice](../../cases/military/soldiers_council_surrender.md).
No missing parts 3–5 or reply relationship are invented.

## A1: a bounded, explicitly conditional short-group reconstruction

The page shows **189 typed coordinates** against `RICHI-190`. The fourth
group of its second row is **AVVG**, visibly four symbols. The stated model
is one missing coordinate somewhere inside that short group. The verifier
enumerates all **five positions × six coordinate values = 30
geometry-labeled completions**, or **26 distinct complete ciphertexts and
plaintexts**.

Under the additional lexical condition that positions **77:87** read
**GEMELDETEN**, exactly one complete candidate survives: insert D before
AVVG, producing **DAVVG**. The primary raw layer represents that frame as
**?AVVG**, leaving the E in GEMELDETEN unknown; the edited layer supplies
it with one missing-coordinate fill. This is uniqueness **only under the
stated one-loss model and crib**. The source does not independently name
the lost coordinate, and historical spelling errors are not excluded.
The opaque ending **STUR3FSS** remains unchanged.

A2 has its native **186** coordinates and one local substitution for
`ABMARSCH`. Its literal **O MOLDOVA**, date labels **8 / 11**, and unfinished
`ARMEETRITT...ABMARSCH` ending are preserved. These are fragments, not a
complete reconstructed five-part report.

## B: typed source versus handwritten material

B has **156 typed coordinates**, matching `RICHI-156`, and an additional
five handwritten glyphs after typed index 134. The primary D reading is
**VXXDV**, exactly repeating the preceding typed group. The composite has
**161 visible slots**, an odd length. Its native pair decryption is not
defined; no padding or missing-coordinate claim is added to make it even.

The primary reading uses the typed layer, with a complete map from each
working coordinate to the composite source. It costs **three observed
substitutions**, retaining the extra H before O K M. The five handwriting
slots are retained separately. If the composite is instead treated as
transmitted material, reaching the typed frame costs **five source-slot
deletions**, involving five known coordinates under the primary D reading.
A hypothetical D→O sensitivity leaves four known coordinates plus one
non-coordinate mask; it does not change the typed output. The detail crop
supports D; O is a sensitivity option, not an equally certified reading.
This separation is not a free correction to an assumed 161-coordinate
transmission.

The old OCR itself is also preserved. It omitted typed **XXVGF** and the
final typed D, misread one typed X as V, and masked one handwritten D and
one typed V. `ocr_snapshot.json` and the verifier replay the exact
155→161 composite reconstruction before selecting the independent
156-coordinate typed layer. The shared old corpus is unchanged.

## C and the total accounting

C has **154 valid coordinates**, fixes **77 / 77 positions**, and needs
zero edits. It reports that the Gouvernement and barracks around Radio
have surrendered to a Soldiers Council. **ROU** remains a literal station
label; the edition does not independently identify a location or event.

The four records contain **690 visible glyph slots including handwriting**,
**685 typed coordinates**, and **686 working coordinates** after excluding
the five annotation slots and modeling A1's one missing coordinate. There
are **343 plaintext positions**: raw **342**, edited **343** fixed under
the stated frames/layers. The primary cost is **four observed-coordinate
substitutions and one missing-coordinate fill**. The separate composite
transmission interpretation's exclusion cost is not hidden in that count.

The partial key remains unchanged. Its unresolved symbols 5 and 6 are
not assigned: every pair used in the primary edited records is already
resolved in the baseline square. All four complete edited candidates and
all 26 bounded A1 witnesses re-encrypt exactly without a key completion.

Earlier unreviewed A1/A2/C bodies, the B OCR artifact, published key credit
and bounded prior-publication checks are frozen. This source edition makes
no historical first-solution claim. `catalog_proposal.json` counts the
four physical records once each and excludes geometry/annotation variants.

## Reproduce

From the repository root:

```sh
python experiments/nov7_fragments_and_council/verify.py --verify
```

This uses the standard library and checked-in cipher module. Optional
source pixel verification requires PyMuPDF and Pillow:

```sh
python experiments/nov7_fragments_and_council/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The PDF's frozen byte count and SHA-256 are checked before all five crops
are regenerated and compared pixel for pixel. Scratch caches are not
runtime dependencies.
