# Tiflis request for repetition of an encrypted telegram

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Childs p77 A, PDF p80, has exactly **314 valid coordinates**, as printed
in `RICHI-314`. The October 29 header and message time are retained. The
unchanged published **Oct28–31** key gives **157 / 157 fixed positions**.
Two local coordinate substitutions repair `ZUER` to `FUER` and `ERBITT4N`
to `ERBITTEN`. No erasure, insertion, deletion, frame or key change is used.

The [reading case](../../cases/radio/tiflis_repetition_request.md) preserves
the raw address `B D 5 M`, `CHI Z53 12 10`, and the closing
`1874 STRICH Z ROT 692`. It does not infer an organization or reconcile
the references by changing their letters or digits. The missing earlier
telegram is not identified merely from this request.

`inputs.json` freezes the source rows, headers, complete key provenance
and crop geometry. A detailed crop confirms that the third glyph of
`XXGGX` is G, like its neighbor; it is not silently treated as a source
C and then filled. `certificates.json` independently reproduces every
pair, source index and edit, and verifies the complete edited plaintext
by exact re-encryption. `prior_candidates.json` preserves the earlier
unreviewed repository body and bounded prior-publication checks. No
historical first-solution claim is made.

The proposal contains only **one physical record**. Neighboring p77 B
was already reviewed elsewhere and is not counted again.

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
then regenerates both source crops and compares their pixels. Scratch
caches are not runtime dependencies.
