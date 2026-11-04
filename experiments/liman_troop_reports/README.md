# Liman troop-report request, p222 A

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**
The period key is prior published work by George Lasry, Ingo Niebel,
Nils Kopal and Arno Wacker. The two bodies had appeared as unreviewed
OCR-derived candidates; this package supplies a visual source edition,
exact repair price and explicit separation of unresolved symbol labels.

The [two-part source](sources/childs_p222_A.png) contains exactly **214 + 200
coordinates**, agreeing with its length headings. The unchanged published
`Nov25-28` square and ranks produce **207 raw-label positions**. A1 needs no
coordinate repair. In A2, one observed coordinate, source index 132
(`V` to `A`, printed group 27, coordinate 3), changes `BESOXDERE` to
`BESONDERE`. There are no insertions, deletions, erasure fills, block moves,
or baseline-square changes.

The message asks General von Liman for regular reports on the transport,
strength, condition and special requirements of troops at Constantinople
and Haidarpascha, and requests acknowledgment. The literal `9EDE` and the
footer `ROEMXJAXJJ201` remain in the edition. Reading `9EDE` as *jede* is a
separate lexical interpretation, consistent with `MA9OR` in the independently
edited [p224 C1](../breslau_staff_transfer/). Both occurrences use `VD`.
This does not assign the remaining rare-letter or numerical labels, or
complete a globally bijective replacement square.

The page heading says **26 November 1918**, and the origin line says
`0900 (26/11)`. The parenthetical reception line says **18 December**.
These literal dates are preserved without choosing an explanation.

## Files and reproduction

- [inputs.json](inputs.json): manual rows, literal headers, unchanged key,
  prior credits, source-image hash and proposed text.
- [certificates.json](certificates.json): exact raw and edited strings,
  coordinate-pair/source-position mapping, repair and untouched label fields.
- [Readable edition](../../cases/pages/222.md#edition-cases-military-liman-troop-reports).

```sh
python experiments/liman_troop_reports/verify.py --verify
```

The standard-library verifier independently reconstructs physical columns
and checks exact re-encryption of both the raw and proposed readings.
An optional `--pdf /path/to/adfgvx-childs.pdf` also checks the complete
source PDF's SHA-256. No model, optimizer or guessed numerical assignment
is needed. Exact arithmetic establishes source consistency and the stated
repair price; it does not establish universal historical priority.
