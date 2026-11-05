# Tiflis request for repetition of an encrypted telegram

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Childs p77 A, PDF page 80, has exactly **314 source slots**, as printed in
`RICHI-314`: **313 unambiguous coordinates and one damaged glyph**. The
29 October header and message time are retained. The unchanged published
**Oct28–31** key gives **156/157 raw fixed positions**. Two local coordinate
substitutions repair `ZUER` to `FUER` and `ERBITT4N` to `ERBITTEN`, while
one damaged-glyph fill supplies the separator between Z and ROT. The
unchanged edited candidate fixes **157/157 positions**. No source insertion,
deletion, frame change or key change is used.

The [reading case](../../pages/077.md#edition-cases-radio-tiflis-repetition-request) preserves
the raw address `B D 5 M`, `CHI Z53 12 10`, and the closing
`1874 STRICH Z ROT 692`. It does not infer an organization or reconcile
the references by changing their letters or digits. The missing earlier
telegram is not identified merely from this request.

`inputs.json` freezes the source rows, headers, complete key provenance
and crop geometry. A detailed crop confirms that the third glyph of
`XXGGX` is G, like its neighbor; it is not silently treated as a source
C and then filled. `certificates.json` independently reproduces every
pair, source index, substitution and fill, and verifies the complete edited
plaintext by exact re-encryption. `prior_candidates.json` preserves the earlier
unreviewed repository body and bounded prior-publication checks. No
historical first-solution claim is made.

The proposal contains only **one physical record**. Neighboring p77 B
was already reviewed elsewhere and is not counted again.

## Source 67: an additional conditional separator fill

The second row's sixth group now reads **`DX?XF`**. Its third glyph has
recognizable X-like crossing strokes and an additional near-vertical or
curved stroke on the right, unlike the neighboring clear X glyphs. The
scan does not establish the original layer of this damaged or overstruck
shape. D describes its appearance only; no D coordinate branch is adopted.

The [detail crop](sources/p77_A_source67.png) is bound to original PDF
page 80, display rectangle `[370,331,412,349]`, scale 16, dimensions
672×288, PNG hash and RGB pixel hash. The page's native **180-degree
rotation is retained**, matching the existing full-crop rendering.

All source and plaintext indices are zero-based. Source **67** is the
second coordinate of plaintext position **147**: source pair **[242,67]**,
coordinate pair **`A?`**, domain **`02HISX`**. The main candidate fills
67 with X and retains the separator in `Z X ROT`. Its other changes
remain source **91 V→F** and **244 X→G**. The old definite X had not been
edited, so the account rises from **two substitutions** to **two
substitutions plus one fill**, or **three coordinate operations**. This
means preserving the unchanged template requires an additional assumption;
it supplies no new observed label and does not improve the repair cost.

The compact certificate retains the former X stream as an explicit
assumption. Both its complete raw output and the unchanged main candidate
are re-encrypted; all unaffected raw positions are compared. The X
assumption restores the old two-substitution account only conditionally.
It is not an independent observation or parallel copy and does not replace
the primary two-substitution, one-fill account.

The earlier frozen OCR already marked source 67 `?`. Its complete cipher
stream and raw output match the conservative source now used. This is
same-source transcription history, not independent corroboration. Original
solver and prior-candidate credits remain unchanged.

## Reproduce

From the repository root, using Python 3 and the checked-in cipher module:

```sh
python experiments/tiflis_repetition_request/verify.py --verify
```

For original-PDF pixel verification, also install PyMuPDF and Pillow:

```sh
python experiments/tiflis_repetition_request/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier checks the original PDF's frozen byte count and SHA-256,
then regenerates all three source crops and compares their pixels. It
also checks the damaged-glyph mapping, compact X hypothesis, complete
repair and fill ledgers, and readable-label mapping. Scratch caches are
not runtime dependencies.
