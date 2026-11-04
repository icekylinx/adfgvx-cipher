# Braila inquiry about dragoman Schaefer's return from leave

The Foreign Office asks whether Dragoman Schaefer's return, as his leave nears its end, is feasible, desirable and expedient. A reply by telegram is requested.

**Complete edition by printed page:** [p. 107](../pages/107.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

## p107 C

Childs p107 C, PDF p110, is a separate message headed
`UKS v LP (3.04 a.m., November 3rd)` and `SS 2025 (2/11)`.
The [source crop](../../experiments/p107_railway_and_dragoman/sources/p107_C.png)
contains **348 source slots**, matching `RICHI-348`: **347 unambiguous
coordinates and one damaged or overstruck glyph** at source index 45.
It uses the unchanged published **Nov1–3** key.
Source and plaintext indices below are zero-based; printed rows and groups
are counted from one.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 348-coordinate frame:**

```text
GEHEIMRATENDERHEIDENBRAILAXXISTRUECKKEHRDRAGOMANSXSCHAEFERXDESSENURLAUBBALDABLAEUFTSO?ERNUEBERHAUPTAUSFUEHRBARJETZTERWUENSCHTUNDZWECKMAESSIGDRAHTBERIC1TXXAUSWAERTCGESXA2TX1XB
```

**Edited output — three observed-coordinate substitutions and one damaged-glyph fill:**

```text
GEHEIMRATENDERHEIDENBRAILAXXISTRUECKKEHRDRAGOMANSXSCHAEFERXDESSENURLAUBBALDABLAEUFTSOFERNUEBERHAUPTAUSFUEHRBARJETZTERWUENSCHTUNDZWECKMAESSIGDRAHTBERICHTXXAUSWAERTIGESXAMTX1XB
```

</details>

The observed-coordinate changes are source **182 F→V**, **253 X→V** and
**292 D→A**, repairing `DRAHTBERIC1T` and `AUSWAERTCGES A2T`.
The separate fill **45 ?→V** supplies F in `SO?ERN`. The conservative raw
layer fixes **173/174 positions**; the unchanged edited candidate fixes
**174/174** and re-encrypts exactly. There are still **four coordinate
operations**. Reclassifying the damaged glyph does not reduce the total
repair count or add a newly observed plaintext letter.

**Readable German — spacing, punctuation and umlauts; the opaque address remains unexpanded:**

> GEHEIMRATENDERHEIDEN, Braila. Ist Rückkehr Dragomans Schaefer, dessen
> Urlaub bald abläuft, sofern überhaupt ausführbar, jetzt erwünscht und
> zweckmäßig? Drahtbericht. Auswärtiges Amt. 1. B.

The question explicitly retains both conditions: whether return is
feasible at all, and whether it is now desired and expedient. It requests
a telegraphic report; it does not establish a completed return or replace
the question with a return order.

## Conditional interpretation and source qualifications

### Source 45: preserve the damaged glyph

The first glyph of the second row's second group is conservatively recorded
as **`?XGFF`**. The [detail crop](../../experiments/p107_railway_and_dragoman/sources/p107_C_source45.png)
comes directly from PDF page 110, rectangle `[188,551,227,568]`, rendered
at scale 16. Its upper strokes look V-like, while lower feet suggest an
overprint or damage; it differs from the adjacent clear X and nearby clear
V. Visual review does not establish an unconditional X or V. The `?`
records this uncertainty in one existing source slot, without adding a gap.

That slot supplies the second coordinate of plaintext position **85**.
The conservative pair **`A?`** permits **`9FILOU`**. The main reading selects
F by filling the glyph with V; the source does not independently fix F.
The certificate retains two explicit, separately identified glyph assumptions:

| Source handling | Fixed raw positions | Plaintext 85 | Changes from that stated branch to the unchanged main candidate |
|---|---:|:---:|---|
| Conservative `?` | 173/174 | `?` | 3 observed substitutions and 1 damaged-glyph fill |
| Assume X | 174/174 | `9` | 3 observed substitutions and 1 replacement of the assumed X |
| Assume V | 174/174 | `F` | 3 observed substitutions; V has already been assumed |

The two fully assigned branches are **hypotheses about the same glyph**,
not independent observations, parallel copies or additional records. Their
branch-relative costs do not replace the primary three-substitution,
one-fill account. The former definite-X transcription is retained through
the X branch, including its `SO9ERN` output.

The frozen earlier OCR already marked this slot `?` and produced `SO?ERN`.
It is an earlier transcription of this same source, not independent evidence
for a different transmission. The new image review restores the conservative
uncertainty instead of claiming a new decipherment.

### Preserved labels and a separate clear glyph

The continuous address **GEHEIMRATENDERHEIDENBRAILA** and surname string
**SCHAEFER** remain as decoded. The displayed boundary before Braila does
not establish a particular person's identity, nor does it normalize the
opaque address into an assumed historical name. The final **1 B** labels
remain literal.

The [detail crop](../../experiments/p107_railway_and_dragoman/sources/p107_C_VDVGV.png)
shows G at source **133** in **VDVGV**. A preliminary C reading from the
small full-page image was rejected before publication; no extra erasure
or fill is introduced at that position. This clear-G check is separate from
the damaged source 45 and the three observed-coordinate substitutions above.

The earlier unreviewed repository candidate already contained this body.
The source edition adds exact transcription, repair accounting and
re-encryption, with published key credit retained. It makes no historical
first-solution claim. See the [inputs](../../experiments/p107_railway_and_dragoman/inputs.json),
[certificates](../../experiments/p107_railway_and_dragoman/certificates.json)
and [reproduction instructions](../../experiments/p107_railway_and_dragoman/README.md).

</details>
<!-- CASE-EDITION:END -->
