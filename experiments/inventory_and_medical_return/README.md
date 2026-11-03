# Inventory and medical-return source records

Prepared by **icekylinx and GPT-6 Astra Pro**. This package verifies
[p86 A's MG08 inventory query](../../cases/military/mg08_inventory.md) and
[the two-part p104 C medical-return report](../../cases/people/medical_return_to_unit.md).

| Record | Observed slots / advertised | Raw labels under stated geometry | Known-coordinate substitutions | Source-erasure fills | Additional geometry |
| --- | ---: | ---: | ---: | ---: | --- |
| p86 A | 298 / 298 | 149 / 149 | 2 | 0 | Ordinary frame |
| p104 C1 | 227 / 228 | 113 / 114, conditional | 3 | 0 | One missing transmitted A; three arithmetic placements, two source-local |
| p104 C2 | 140 / 140 | 70 / 70 | 1 | 0 | Ordinary frame |

There are **665 observed slots, all valid coordinates**, six known-coordinate
substitutions and one separately charged missing coordinate. The two
ordinary frames have 219 fixed plaintext labels. C1's 113/114 count depends
on its conditional 228-slot geometry; the original odd-frame reading also
remains in the certificate. Published keys are unchanged: `Oct28-31` for
p86 A and `Nov1-3` for p104 C.

## Source decisions

p86 A asks about numbers of German `MG08` with tripod mounts and their
caliber. It does not provide the inventory answer. The address
`MGKOMMANDEUROSMANHGRXOST` and closing `OSMAN19ABTLGXGRXHXQUXNO835C120X10X18`
remain unexpanded. All numerical fields are literal. The sole numeral
change is an explicitly priced word repair, raw `BER4ICH` to `BEREICH`,
without any square-digit reassignment.

p104 C1 visibly prints the four-character group `GAGA` at original source
index 165, printed group 34. One missing coordinate is therefore supported
by both its 227/228 length mismatch and its group shape. For the later
114-character template, all **228 insertion positions** were evaluated.
Minimum cost is three substitutions at indices **168, 169 and 170**, inserting
`A`; each yields the same full cipher and repaired received witness.
Only 168/169 lie inside or at the visible group's boundary. Position 170
is an equal-A ambiguity just beyond it, not another independently observed
gap. All three coordinate-origin maps remain in the certificate.

The medical report retains `DTSCHXSTAAT`, the spelling `MARSH`, and the
adjacent `RETTERL`/`KETTERL` name tokens. No institutional or personal identity
is invented to smooth the prose. The source reports treatment/recovery as
the reason for the return; the edition does not independently establish a
particular person's medical history.

## Reproduce

```sh
python experiments/inventory_and_medical_return/verify.py --verify
```

The standalone verifier uses only the Python standard library and imports
no shared cipher engine. It independently reconstructs variable-height
columns, checks all source strings and raw domains, rebuilds each edit and
numeral ledger, prices all 228 C1 insertion positions, and verifies the
full and received witnesses for all three equal-A variants. Default
verification passed.

Optional PDF regeneration requires PyMuPDF:

```sh
python experiments/inventory_and_medical_return/verify.py --verify \
  --pdf /path/to/adfgvx-childs.pdf
```

PDF SHA-256:
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
Printed pp86/104 are PDF pp89/107. The five images have frozen page
rectangles, scales, PNG hashes and raw-pixel hashes. Full PDF regeneration
passed. `inputs.json` holds the original transcription and separate
proposals; running without `--verify` regenerates `certificates.json`.

## Attribution and scope

J. Rives Childs's intercept collection is the primary source. The published
keys retain credit to **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**,
[DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also published in Lasry's 2017 key comment; full provenance accompanies
each key. Earlier unreviewed OCR-derived candidates existed. A bounded
author-paper review found no explicit examples of these bodies, which does
not establish universal first-decipherment priority.

The complete source witnesses verify the stated arithmetic and repair costs.
C1's insertion remains conditional and its template retrospective. Neither
a readable sentence nor a minimal local repair establishes unique historical
wording, an office identity, or a surname correction.
