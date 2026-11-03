# Berlin newspapers via Orsova

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The [readable case](../../cases/radio/newspaper_dispatch.md) source-reviews
p171 B1–B2: Berlin newspaper sacks have arrived via Orsova, and Breslau's
postal directorate is asked to arrange immediate postal dispatch along that
route. The reference fields remain `7?3` and `308`.

The exact 200/186-slot frames provide 193 plaintext positions. Six
observed-coordinate substitutions and two printed-erasure fills take the
reading from 190 to 192 fixed positions, with no geometry or baseline-key
change. The remaining unknown is a fully observed `XA` square cell with
baseline domain `56`, not a missing source coordinate.

The optional `753` consequence is separately propagated from the existing
conditional Nov7 military-context map. It is not a new numerical inference
or independent corroboration from this telegram. Both baseline and optional
views are preserved in the certificate.

Earlier unreviewed OCR body candidates are retained for attribution. The
period key is prior work by Lasry, Niebel, Kopal and Wacker. Norbert's
separate p171 A1 challenge reading is explicitly distinguished and unchanged.

```sh
python experiments/newspaper_dispatch/verify.py --verify
python experiments/newspaper_dispatch/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Default verification uses the existing independent column/domain/reencryption
helpers and checks source hashes, all prices and unchanged key fields. The
optional PDF check regenerates and compares source-crop pixels using PyMuPDF.
Arbitrary global witness completions are not proposed original readings.
