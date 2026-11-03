# Railway message: Laz. Zug 42 from Chemnitz and Zug 34 to VERBETZ

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p107 B1/B2, PDF p110, form the two-part message headed
`UKS v ZÖN (4.48 a.m., November 3rd)` and
`VEVE 1905 (2) AN LP 2 TLE`. The consecutive labels and repeated railway
subject support the assembly. Both use the unchanged published
**Nov1–3** key.

## p107 B1

The [source crop](../../experiments/p107_railway_and_dragoman/sources/p107_B.png)
contains **164 valid coordinates**, matching `1 TL RICHI-164`.
The earlier OCR omitted the final **FDGD** row and masked source **152 D**.
Restoring those visible glyphs recovers the native frame; the exact old
OCR is retained in a [frozen snapshot](../../experiments/p107_railway_and_dragoman/ocr_snapshot.json).

**Raw output — native 164-coordinate frame:**

```text
EISMNBAHNTRANB6ORTABTLGXSXOXPFESSXGXHX1XQXXBEILINIEN1DTXGXLAZXZUGX42XVONXCHEMNITZX
```

**Edited output — five observed-coordinate substitutions, with no fills:**

```text
EISENBAHNTRANSPORTABTLGXSXOXPFESSXGXHX1XQXXBEILINIENKDTXGXLAZXZUGX42XVONXCHEMNITZX
```

The changes are source **43 D→G**, **44 G→D**, **62 X→V**, **66 X→V** and
**160 F→V**. The last is a genuine proposed source change within the
restored final row; it is counted separately from correcting the OCR.
The candidate repairs the railway-transport wording and `LINIEN1DT`;
the opaque **PFESS** and **G H 1 Q** fields remain unchanged.

**Readable German — spacing and punctuation, keeping abbreviations and opaque fields literal:**

> Eisenbahntransportabtlg. S. O. PFESS. G. H. 1. Q. Bei Linienkdt.
> G. Laz. Zug 42 von Chemnitz.

The routing abbreviations, including **G** before **LAZ**, are not
expanded. This part fixes **82 / 82 positions**; its complete edited
candidate re-encrypts exactly.

## p107 B2

The same crop has **110 visible slots** for `2 TL RICHI-110`, including
the printed dash in **DGFG-** at source index **39**.

**Raw output — native 110-coordinate frame:**

```text
WAZXZUGX34XNACHXVERBETZXA5ROLIENLASSENXX?BAXAEK11X10502
```

**Edited output — three observed-coordinate substitutions, with no fills:**

```text
LAZXZUGX34XNACHXVERBETZXABROLLENLASSENXX?BAXAEK11X10502
```

The changes are source **12 G→A**, **21 D→F** and **54 X→V**. The printed
dash remains unresolved. No character in the closing is supplied merely
to produce a familiar command abbreviation.

**Readable German — spacing and punctuation:**

> Laz. Zug 34 nach VERBETZ abrollen lassen. ?BA. AEK11. 10502.

**VERBETZ** is the literal decoded destination; no independent location
identification or spelling correction is imposed. The dispatch wording
is an instruction, not proof that either train moved.

## Conditional interpretation and remaining ambiguity

The candidate for B2 fixes **54 / 55 positions**. Its unknown position
**40** has pair **?V**, source indices **39** and **67**, and domain
**3BFKQS**. All six possible complete ciphertexts and plaintexts are
retained as exact re-encryption witnesses; none is selected as the
historical closing.

Across these two records there are **274 visible slots**, **273 valid
coordinates** and **136 / 137 fixed plaintext positions**. The main
edition uses **eight observed-coordinate substitutions and no fills**,
with no frame, length or key change. Local changes to `TRANB6ORT`,
`LINIEN1DT` and `A5ROLIEN` do not establish global numeral mappings.

The package retains earlier unread OCR frames and candidate readings,
along with the published key's provenance. It makes no historical
first-solution claim. See [inputs](../../experiments/p107_railway_and_dragoman/inputs.json),
[certificates](../../experiments/p107_railway_and_dragoman/certificates.json)
and [reproduction instructions](../../experiments/p107_railway_and_dragoman/README.md).
