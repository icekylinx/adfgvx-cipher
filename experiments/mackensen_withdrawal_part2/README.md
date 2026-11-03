# Mackensen withdrawal report: separately received part 2

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.
Historical report decipherment remains credited to **J. Rives Childs**;
the published reconstruction and Nov1–3 key retain the attribution to
**George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**.

The [new p118 source edition](../../cases/military/mackensen_withdrawal_part2.md)
supplies the second physical part missing from the earlier twelve-part
repository report. Its header explicitly names the second part of the
thirteen-part message sent at 20:00 on 11/3. The source contributes 377 valid
coordinates; the native odd frame and its orphan remain in the certificate.

A conditional insertion of one coordinate at source boundary 283 restores
the advertised 378-slot frame. This lies inside the visibly short FGAD group.
Across all 378 single-insertion boundaries, 283 uniquely minimizes the exact
baseline template at **13 observed-coordinate substitutions** plus **one
inserted V fill**. The modeled raw stream fixes **188/189 positions**; the
baseline edited proposal fixes **189/189** and re-encrypts exactly.

The baseline keeps SHMENDRIA, VID8N and OO2PALANKA literally. Optional familiar
geographical spellings cost four additional substitutions and are separately
certified. The date 1/11/18 and count 3 are unchanged. Neither a complete fixed
stream nor a minimum template cost proves every historical word or a unique
damage model.

`inputs.json` holds the full source rows, key, header, two crop bindings and
pinned source-assembly evidence from the earlier report package.
`certificates.json` checks the original odd frame, conditional frame, all 378
insertion prices, every repair, the optional names and complete readable
quote. The prior OCR candidate is retained without a first-solution claim.

## Reproduce

```sh
python experiments/mackensen_withdrawal_part2/verify.py --verify
python experiments/mackensen_withdrawal_part2/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The PDF option verifies the original hash and regenerates both crops for
pixel comparison with PyMuPDF/Pillow. The normal check uses checked-in code
and the standard library; no external scratch cache is required.
