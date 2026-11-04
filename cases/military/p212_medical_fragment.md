# p212 A4: hospitals, patients and transport

The conditional fragments concern hospitals or institutions where sick people can remain, medical transports, personnel and allocation of medicines. Much of the connecting text is lost.

**Complete edition by printed page:** [p. 212](../pages/212.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition: icekylinx and GPT-6 Astra Pro.** This conditional fragment concerns institutions where patients can remain, transport, personnel and medicines. It retains all **197 printed coordinates**, uses the unchanged published **Nov22–24** key, and assumes a **302-coordinate frame with 105 missing transmitted-prefix slots**. The source gives no total length.

## p212 A4

Childs, printed page 212 / PDF page 215: `22nd NOVEMBER, 1918`; `XYZ v LP (03.54 p.m., November 22nd); ----- 7 TLE`. This block is explicitly **4 TL (Missed start)**.

<details>
<summary>Literal source transcription</summary>

**Source transcription — all 197 printed coordinates:**

```text
DVAAA XAXGF FAVXA AAVAG GVXFA FVVDD FXVDG AFAXX
FFADF AAFDX VDAGD ADADV FFAFF GXVDX DAGAD VVXFF
FFFVA DGFAD VXDXD FVGGV AXAVA FDAVG VVFXF VDAXF
DVFVF AAGAD VXDVX AAFVF AVXGA VFAGV VAFFD VVFFV
XVXVF FFVVD VXDVV DFAAA VDXFA FGAGD FAVAD AG
```

</details>

[Previously archived source crop](../../experiments/p212_p218_crosscopy/sources/p212_A4.png) · [Original PDF](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). The [inputs](../../experiments/p212_medical_fragment/inputs.json) give the exact PDF crop recipe; no image is duplicated.

Prepending 105 unassigned slots and undoing the published transposition yields **46 fully observed pairs and 105 pairs with one observed half**. No plaintext position is wholly unobserved.

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional 302-slot frame; all missing coordinates unassigned:**

```text
??ZA???T?????ST???E?????HI???K?????UG???N?????AN???E?????BE???E?????3X???9?????RA???O?????YA???M?????ER???S?????ME?I?A?????NZ?T?I?????SS?N?N?????DE?Z?G
```

</details>

Each `?` has an exact six-label domain. Five selected lexical spans fit those domains and require **83 missing-half fills, zero observed-coordinate changes**.

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same frame and key; 83 inserted-half fills, 22 positions unresolved:**

```text
LAZARETT???ANSTALTENDORTHINBEKANNTZUGEBENXWOKRANKEVERBLEIBENKOENNENX3X???9????TRANSPORT???YA???M?????ERPERSONAL?MEDIKAMENTENZUTEILENLASSENUNDIN9EDEMZUG
```

</details>

| Plaintext span, zero-based end exclusive | Selected wording |
|---|---|
| 0–8 | `LAZARETT` |
| 11–68 | `ANSTALTENDORTHINBEKANNTZUGEBENXWOKRANKEVERBLEIBENKOENNENX` |
| 78–87 | `TRANSPORT` |
| 103–111 | `PERSONAL` |
| 112–151 | `MEDIKAMENTENZUTEILENLASSENUNDIN9EDEMZUG` |

**Readable German — selected fragments only; literal 9 retained:**

> Lazarett […] Anstalten dorthin bekanntzugeben, wo Kranke verbleiben koennen […] Transport […] Personal […] Medikamenten zuteilen lassen und in9edem Zug.

**Conditional interpretation:** the fragments mention hospitals or institutions where sick people can remain and assigning medicines. The final phrase could mean “in every train” under the [separate globally injective J/numeral hypotheses](../../experiments/nov22_nikolajew_constraint/README.md). This edition retains `IN9EDEM` without a local square change. It does not establish that the described arrangements were implemented.

The joins remain uncertain. Received `3X`, the fully observed `9` at position 73, and opaque `YA`, `M` and `ER` are preserved. The selected `9` at position 143 requires one missing-half fill. The following [A5 starts EINEN…](medical_return_transports.md#p212-a5), consistent with a continuation; it did not determine the new frame. The page also interposes an oil query and a [part-2 copy under another dated key](../caucasus/p212_p218_crosscopy.md), so the whole seven-part assembly remains unresolved.

## Exact account and limits

| Account | Count |
|---|---:|
| Original observed coordinates, all retained in order | 197 |
| Conditional frame / plaintext positions | 302 / 151 |
| Fixed raw / edited positions | 46 / 129 |
| Proposed lexical positions / other retained raw labels | 121 / 8 |
| Added prefix slots / filled / unassigned | 105 / 83 / 22 |
| Observed substitutions, printed-mask fills, exclusions or reorderings | 0 |

These are lexical proposals, not uniquely forced completions. Each newly fixed label consumes one missing-half fill. An arbitrary full [reencryption witness](../../experiments/p212_medical_fragment/certificates.json) proves compatibility with every original coordinate; its remaining 22 supplied values are not part of the reading.

The frame emerged from **6,300 half-coordinate-aware hypotheses**: 25 registered keys and every even total from 198 to 700. Its score was 78.3508, versus 6.9540 for the next length under the same key. In 100 frequency-preserving shuffles, each screened over those lengths under the already selected Nov22–24 key, the largest score was 19.4420. This is a finite same-key comparison, not a global probability of correctness. Three synthetic controls ranked their true lengths 1, 1 and 2; the imperfect result remains recorded.

Word-lattice decoding, independent compatible-word enumeration and source/mapping review support the fragments. They do not authenticate the missing transmission or prove a unique complete text. [Inputs and method](../../experiments/p212_medical_fragment/README.md) retain the neighboring-length checks, control witnesses and diagnostic limits.

## Optional lexical extension: hospital support staff

A separate [optional six-half proposal](../../experiments/p212_medical_fragment/optional_underpersonal.json) extends positions 95–124 to `MITUNTERPERSONALUMEDIKAMENTEN`. It preserves the primary edition and every observed coordinate, adding only six missing-half values at plaintext positions 96, 97, 98, 99, 100 and 111.

**Optional edited output — 135/151 positions; 89 total inserted-half fills; 16 unresolved:**

`LAZARETT???ANSTALTENDORTHINBEKANNTZUGEBENXWOKRANKEVERBLEIBENKOENNENX3X???9????TRANSPORT???YA???MITUNTERPERSONALUMEDIKAMENTENZUTEILENLASSENUNDIN9EDEMZUG`

**Optional readable German — U expanded as u[nd]; literal 9 retained:** mit Unterpersonal u[nd] Medikamenten zuteilen lassen und in9edem Zug.

| Optional account | Count |
|---|---:|
| Additional missing-half fills / total fills / unassigned slots | 6 / 89 / 16 |
| Observed-coordinate substitutions / source-mask fills | 0 / 0 |

The term *Unterpersonal* has independent period medical support. [Kowalk's fourth enlarged edition, Berlin 1898, printed p162 / PDF p186](https://storage.lib.uchicago.edu/pres/2015/pres2015-0552.pdf) uses it after describing hospital attendants, servants, heating, cooking and laundry staff. [Die Gartenlaube, no. 2 (1879), p39](https://de.wikisource.org/wiki/Seite:Die_Gartenlaube_(1879)_039.jpg) likewise applies it to a hospital's cook and ward attendants. The original pages and title metadata were visually checked; compact hashes and crop recipes are in the optional file, with no added images.

Those examples support the meaning **hospital auxiliary/support staff**. They do not witness this telegram or prove its missing text. The U-to-u[nd] expansion remains editorial, and the unresolved joins and literal 9 remain. Verify this layer separately with `python experiments/p212_medical_fragment/verify_optional_underpersonal.py --verify`.

## Further optional extension: a doctor for each transport train

Two further lexical stencils, positions 70–78 `XZU9EDEM` and 87–95 `ZUGYARZT` (end exclusive), add **13 missing-half values** while retaining all 135 earlier proposed labels and all 197 observations. This identifies a coherent candidate by separating `Y|ARZT`, rather than the also source-compatible word `YACHT`. The three positions after LAZARETT remain unfilled.

**Further optional edited output — 148/151 positions; 102 total inserted-half fills; 3 unresolved:**

`LAZARETT???ANSTALTENDORTHINBEKANNTZUGEBENXWOKRANKEVERBLEIBENKOENNENX3XXZU9EDEMTRANSPORTZUGYARZTMITUNTERPERSONALUMEDIKAMENTENZUTEILENLASSENUNDIN9EDEMZUG`

| Further optional account | Count |
|---|---:|
| Additional missing-half fills / total fills / unassigned slots | 13 / 102 / 3 |
| Observed-coordinate substitutions / source-mask fills | 0 / 0 |

The baseline output keeps `3XX`, both 9 labels and Y literal. A separate conditional interpretation reuses the [published numeric+J conjunction](../../experiments/nov22_nikolajew_constraint/README.md): clear all unproved numeral/J/Q/Y cells, then assign raw Y→1, J→2, 2→6 and 9→J. The [new optional certificate](../../experiments/p212_medical_fragment/optional_transport_extension.json) supplies one globally injective full-square and reencryption witness. It interprets only positions 71–151; `3XX` is not identified as a historical instruction number.

**Conditional readable German — positions 71–151, end exclusive; published numeric+J assumptions:** Zu jedem Transportzug 1 Arzt mit Unterpersonal u[nd] Medikamenten zuteilen lassen und in jedem Zug […]

This proposes arranging a doctor with support staff and medicines for each transport train. The excerpt ends mid-clause; the continuation is not supplied. It remains a lexical and key-interpretation hypothesis, not a uniquely recovered historical sentence. In particular, `ZUGYACHT` also fits the surviving coordinates; the certificate preserves that counterexample. Verify the 13 fills, unchanged earlier layers and global square separately with `python experiments/p212_medical_fragment/verify_optional_transport_extension.py --verify`.

## Reproduce and attribution

```sh
python experiments/p212_medical_fragment/verify.py --verify
python experiments/p212_medical_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

The standard-library verifier checks the actual displays, all 151 domains, source mappings, 83 fills, 22 unresolved positions and forward witnesses. The PDF option authenticates the existing crop with PyMuPDF and Pillow. Search scores are frozen diagnostics; default verification does not replay the external language model.

Historical key: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and Lasry's 2017 key list. New source review, retrieval, conditional edition and exact accounting: icekylinx and GPT-6 Astra Pro. Earlier source editions retain their credits; no first historical decipherment claim is made.

</details>
<!-- CASE-EDITION:END -->
