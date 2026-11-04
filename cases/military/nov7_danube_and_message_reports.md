# November 7: Danube crossings and short message reports

The report states that the division has completed its Danube crossing and describes busy crossing traffic at `BELGRAD` and `SEMUM`. The latter place label retains its source spelling.

**Complete edition by printed page:** [p. 152](../pages/152.md) · [p. 153](../pages/153.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Five telegrams on Childs pp. 152–153 report a Serbian attack near Belgrad,
Danube crossing traffic, a prescribed march line and short service messages.
The [p164 C1 parallel report](danube_arad_witnesses.md#p164-c1) supports three
word repairs and a conditional **219 I. D.** reading in [p153 B1](#p153-b1).
Its native unit label is `21B`.

The page-153 first and third parts have separate reception headers; their
second part is absent from this edition. The later fifth and sixth parts
belong to the original challenge cases [p153a](../p153a.md) and
[p153b](../p153b.md).

**Reviewed source crops:** [p152_reviewed.png](../../experiments/nov7_danube_and_message_reports/sources/p152_reviewed.png) · [p153_reviewed.png](../../experiments/nov7_danube_and_message_reports/sources/p153_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).

<details>
<summary>Source counts, keys and earlier OCR</summary>

## Evidence and costs

All five bodies retain their native printed order and length. The word proposals cost **14 observed-coordinate substitutions and four source-mask fills**; the `EB?Q` field remains unresolved. Machine indices below are **zero-based**.

| Record | Native source slots | Source dashes | Raw fixed positions | Word-layer fixed positions | Word-layer substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [p152_B2](#p152-b2) | 190 | 5 | 90/95 | 94/95 | 3 | 4 |
| [p152_C](#p152-c) | 108 | 0 | 54/54 | 54/54 | 2 | 0 |
| [p152_D](#p152-d) | 140 | 0 | 70/70 | 70/70 | 2 | 0 |
| [p153_A3](#p153-a3) | 180 | 0 | 90/90 | 90/90 | 2 | 0 |
| [p153_B1](#p153-b1) | 160 | 0 | 80/80 | 80/80 | 5 | 0 |
| **Total** | **778** | **5** | **384/389** | **388/389** | **14** | **4** |

The optional p153 unit reading adds one observed substitution to the word-layer prices above. It changes a known `B` to `9`, leaving the fixed-position counts unchanged.

The three masked or overlong earlier OCR bodies are retained in [the frozen OCR snapshot](../../experiments/nov7_danube_and_message_reports/ocr_snapshot.json) and [prior unchanged-key diagnostics](../../experiments/nov7_danube_and_message_reports/prior_candidates.json). Restoring what the scan actually prints is an OCR transcription correction, not a deletion or insertion in a received ciphertext. The printed `p152_C` length field is dash-only: its 108-slot count is measured from the body, not advertised by its header.

[Printed page 152, B2 through D — source-PDF reference](../../experiments/nov7_danube_and_message_reports/inputs.json)

[Printed page 153, A3 and B1 — source-PDF reference](../../experiments/nov7_danube_and_message_reports/inputs.json)

The unchanged published `Nov4-6` key reads `p152_B2` and `p152_D`; the unchanged `Nov7-9` key reads the other three. A key’s period label is not used to rewrite a reception date. The exact key tables, publication credit, image bounds and hashes are in [inputs.json](../../experiments/nov7_danube_and_message_reports/inputs.json).

</details>

## p152 B2

Security force near Belgrad attacked after a crossing.

**Readable German — the complete edited stream, with punctuation and spacing:**

> erreicht 9 H. EB?Q. TITEL. Sicherung 219 I. D. noordl. Belgrad durch dort uebergegangene Serben angegriffen.

Literal header: `B) UKS v ZON (--- November 7th); 2 TL RICHI-190`.

<details>
<summary>Source, raw and edited streams, and coordinate repairs</summary>

**Source transcription — 190 native printed slots:**

```text
AF-VD FFDFF AFDVG GVDAF X-VGX GVFDA VAVXG FVFGF
AVAAG GDVXA DFAVV VAAAD DDVXG VFXXX AAVFV AFXVD
VDFAV AFGFD ---XD FAVVX VAFAX AVAGV XVFAF AFXAF
XVVVX FXVGX AAXFF XVXDF VVFXF XAAXA XDFVA FAAVF
XXAXG FXAFD FAFXD AVAVA FGDAV GVXXA
```

**Raw output — unchanged Nov4-6 key, native frame:**

```text
ERREI?HT9XHXEB?QXTIT?L?XSICHERUNG219IXDXNOORDLXBELGRADDUECHDORTUEBERGEGANGENESERVENANZEGRIFFE?X
```

**Edited output — 3 observed-coordinate substitutions and 4 source-mask fills:**

```text
ERREICHT9XHXEB?QXTITELXXSICHERUNG219IXDXNOORDLXBELGRADDURCHDORTUEBERGEGANGENESERBENANGEGRIFFENX
```

The surviving second part reports an attack on a security force labelled 219 I D near Belgrad by Serbs who had crossed there. The literal NOORDL suggests north of the city but retains its extra O. The opening fragment, EB?Q field and exact role of TITEL remain limited by the absent preceding part.

The 190-slot native frame contains five source dashes: source 2,21 and 90–92. Four are filled by the proposal; source 91 remains unresolved and gives the internal character of EB?Q with exact domain {4,F,G,U,Y,Z}. No specific name, station or unit is inferred for that field.

DUECH→DURCH, SERVEN→SERBEN and ANZEGRIFFE?→ANGEGRIFFEN require three observed-coordinate substitutions in total. Four source-mask fills separately supply C, E, a separator and the final N.

NOORDL is preserved exactly, including its double O. The preceding part is not supplied from another report, and 219 remains the literal key-derived label.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 9 | `F` | `V` | Observed-coordinate substitution |
| 39 | `F` | `V` | Observed-coordinate substitution |
| 76 | `F` | `V` | Observed-coordinate substitution |
| 2 | `-` | `A` | Source-mask fill |
| 21 | `-` | `X` | Source-mask fill |
| 90 | `-` | `D` | Source-mask fill |
| 92 | `-` | `D` | Source-mask fill |

The fifth source dash, at index 91, is not filled in the displayed proposal. Its coordinate is the first member of plaintext pair `?V` at position 14. The full `Nov4-6` square fixes the exact domain below; all six choices have exact re-encryption witnesses in the certificate. These are alternatives, not six independent recoveries or a historical selection.

| Source 91 coordinate | Complete four-label field |
| :---: | :---: |
| `A` | `EBFQ` |
| `D` | `EBUQ` |
| `F` | `EBZQ` |
| `G` | `EBYQ` |
| `V` | `EBGQ` |
| `X` | `EB4Q` |

No missing first part is invented to select among `EBFQ`, `EBUQ`, `EBZQ`, `EBYQ`, `EBGQ` and `EB4Q`. The edited stream retains `EB?Q`.

</details>

## p152 C

Morning report: no special events.

**Readable German — the complete edited stream, with punctuation and spacing:**

> O. K. M. Morgenmeldung 7.11. Keine bes. Ereignisse. A. O. K. 11.

Literal header: `C) --- v ZON (--- November 7th); 1235; RICHI----`.

<details>
<summary>Source, raw and edited streams, and coordinate repairs</summary>

**Source transcription — 108 native printed slots:**

```text
VAFDD FFXGG FVXVA XGVVG GVVGV VVFDF GGVVX VDDFA
DVDVA ADDVD GGGVG FGXXG XVFXG VVVVV VFDVV VVGVV
XGVDF FDVXG GGXVV GDDDV DXVAD XDV
```

**Raw output — unchanged Nov7-9 key, native frame:**

```text
OXKXMXUORGENMELDUNGX7X11XKEINEBESQEREIGNISSEXAXOXKX11X
```

**Edited output — 2 observed-coordinate substitutions:**

```text
OXKXMXMORGENMELDUNGX7X11XKEINEBESXEREIGNISSEXAXOXKX11X
```

A short morning report states that there are no special events. The internal 7.11 and AOK11 labels are retained as transmitted.

The source prints a dash-only length field, not 108. The body itself has 108 native coordinates. The earlier OCR appended five mask slots after the final XDV; these are absent from the body in the image and are not treated as received coordinates.

One substitution changes UORGENMELDUNG to MORGENMELDUNG. A second replaces the raw Q between BES and EREIGNISSE with the X separator; the abbreviation BES is not expanded by inserting extra plaintext letters.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 66 | `V` | `F` | Observed-coordinate substitution |
| 85 | `F` | `V` | Observed-coordinate substitution |

</details>

## p152 D

Receipt of a FunkSpruch with literal numerical fields.

**Readable German — the complete edited stream, with punctuation and spacing:**

> Fuer O. K. M. Funkspruch EINSA11205BM4 1189 35 vorm. eingetroffen. A. O. K. 11.

Literal header: `D) UKS v ZON (--- November --); 1850 1010; RICHI-140`.

<details>
<summary>Source, raw and edited streams, and coordinate repairs</summary>

**Source transcription — 140 native printed slots:**

```text
ADGDA VAFXX XFDXF DFDXA AGFDG XFDFF GADXX VDFVA
FVFGV AVDAD VGXDX AADFD FFDVX AAFAD XFAFV XAVVF
XXAAA DAAGA VFGXG GAAFD XDGDX AGVFV ADFVF AFFVD
FDADV VAAAA XFFDX XGVVF
```

**Raw output — unchanged Nov4-6 key, native frame:**

```text
FUERXOXKCMXFUNKSPRUCHXEINSA11205BM4X1189X35XVORMXEINGETROFFENXAXOXWX11
```

**Edited output — 2 observed-coordinate substitutions:**

```text
FUERXOXKXMXFUNKSPRUCHXEINSA11205BM4X1189X35XVORMXEINGETROFFENXAXOXKX11
```

The message reports that a FunkSpruch has arrived, addressed for OKM and ending with the proposed AOK11 signature. Its compact reference and time-like numerical fields are retained without reconstructing an exact calendar date or clock time.

The source header leaves the reception day blank and separately prints 1850 1010. Neither that line nor the decoded 1189 35 field is silently converted to a date/time.

The raw O K C M becomes O K M by changing C to the X separator. The raw A O W11 becomes A O K11 by changing W to K. These are two explicit observed-coordinate substitutions; the arrival wording itself is native.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 8 | `X` | `F` | Observed-coordinate substitution |
| 39 | `A` | `F` | Observed-coordinate substitution |

</details>

## p153 A3

A prescribed line and a Temesvar headquarters field.

**Readable German — the complete edited stream, with punctuation and spacing:**

> in befohlene Linie NAGYBECSKEREK VERSECZ an, die 10.11 erreicht. A. H. Q. 9.11 TEMESVAR. A. O. K. 11.

Literal header: `A) UKS v ZÖN (10.55 p.m., November 7th); 2010; 3 TL RICHI-180`.

<details>
<summary>Source, raw and edited streams, and coordinate repairs</summary>

**Source transcription — 180 native printed slots:**

```text
GGDDX AVGXD XADVV GGVFD VDFGF DVGGG DGVGD GVGDD
GDXVV GDAVX VVFVX DGGVD XVVXG DDDDV AFVVD FVFVD
VVDVV GVVDG XGVVV DVVDG VGVGV VGVXV VDDDV XGXGX
XVVVF XGDXA VVDVV DXFAG AVDVD GDFVX FAVXV GXGGV
VVXAV XFVFA FDXDV FGVXF
```

**Raw output — unchanged Nov7-9 key, native frame:**

```text
INBEFOHLENELINIEXNAYYBECSKEREKXVERSSCZXANXDIE10X11XERREICHTXXAXHXQX9X11XTEMESVARXXAXOXKX11
```

**Edited output — 2 observed-coordinate substitutions:**

```text
INBEFOHLENELINIEXNAGYBECSKEREKXVERSECZXANXDIE10X11XERREICHTXXAXHXQX9X11XTEMESVARXXAXOXKX11
```

This third-part fragment refers to a prescribed line through the transmitted place labels NAGYBECSKEREK and VERSECZ, an internal 10.11 label, and an AHQ field with 9.11 and TEMESVAR. The missing preceding text does not establish a complete movement order or prove that a move occurred.

The native body has 180 coordinates. Earlier OCR attached an extra mask to the five-coordinate VGVGV group, producing 181; it is removed from the OCR comparison rather than excluded from the physical source.

Two ordinary-word/place-spelling proposals change NAYYBECSKEREK to NAGYBECSKEREK and VERSSCZ to VERSECZ. The forms VERSECZ and TEMESVAR remain unexpanded; no modern-place identification is required for the reading.

The printed reception is November 7, while the body retains 9.11 and 10.11. The edition does not rewrite the header to fit those internal labels.

The header visibly places two short marks above the O in the sender label; the transcription preserves this as ZÖN without identifying a different station.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 156 | `X` | `V` | Observed-coordinate substitution |
| 163 | `A` | `D` | Observed-coordinate substitution |

</details>

## p153 B1

**Readable German — optional unit reading supported by the parallel p164 report:**

> An O. K. M. Donauuebergang 219 I. D. beendet. Belgrad SEMUM. Lebhafter Uebersetzverkehr.

The report states that the division has completed its Danube crossing and
describes busy crossing traffic at `BELGRAD` and `SEMUM`. The latter place
label retains its source spelling.

The unit reading **219 I. D.** follows the matching passage in
[p164 C1](danube_arad_witnesses.md#p164-c1). Both passages contain 63
nonseparator characters, of which 56 agree directly in the native readings.
The unit's first two digits agree; p164's observed `GF` pair supplies **9**
where p153 has `GX`, **B**. Reading the same unit here requires one additional
observed substitution at source **98**, `X` → `F`: **six substitutions in
total, with no source fills or length changes**. The messages have different
headers and openings; the proposal rests on their shared crossing report.
The nearby [p152 B2 report](#p152-b2) independently names `219 I D` in its
Belgrad passage under the different Nov4–6 key.

Literal header: `B) UKS v ZÖN (9.42 p.m., November 7th); 2010 3 TLE; 1 TL RICHI-160`.

<details>
<summary>Source, earlier 21B word layer and conditional 219 reading</summary>

**Source transcription — 160 native printed slots:**

```text
VXXGD AAGAG VAVVA VVAFX VDGVV DVVVX VVXDG VGVVV
XXDXG AGGXF XVDAD DVAGD ADDAV DGXXG DDVVG VXDXD
VGGXD FDADV GVXFV VVAXV VXXVV VDVDD VDGXD VVVVF
FXDDD VADFX VVVXD XGVGG AVXGV AVVDX DVVDG GDXDA
```

**Raw output — unchanged Nov7-9 key, native frame:**

```text
ANXOXKXMXXDONAUU3BERGANG21BXIXDXBEENDUTXBELGR4DXSEMUMXLEBHAFTERUEBSRSETZVERKEHRX
```

**Edited output — 5 observed-coordinate substitutions:**

```text
ANXOXKXMXXDONAUUEBERGANG21BXIXDXBEENDETXBELGRADXSEMUMXLEBHAFTERUEBERSETZVERKEHRX
```

**Readable German — the complete edited stream, with punctuation and spacing:**

> An O. K. M. Donauuebergang 21B I. D. beendet. Belgrad SEMUM. Lebhafter Uebersetzverkehr.

The earlier word layer preserves the native unit label `21B I D`. Its
five repairs address ordinary words and leave the unit unresolved.

The native body is 160 coordinates. Earlier OCR turned the first-row VDGVV into a six-slot masked group, producing 161; the image restores the actual five-coordinate group without a source insertion or deletion.

DONAUU3BERGANG→DONAUUEBERGANG, BEENDUT→BEENDET, BELGR4D→BELGRAD and UEBSRSETZVERKEHR→UEBERSETZVERKEHR together cost five observed-coordinate substitutions. The raw digits in the damaged words remain visible in the raw layer.

The first- and third-part records share 2010 and the same station pair but
have different reception times. The second part is absent from this edition.

The header visibly places two short marks above the O in the sender label; the transcription preserves this as ZÖN without identifying a different station.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 11 | `A` | `D` | Observed-coordinate substitution |
| 20 | `V` | `X` | Observed-coordinate substitution |
| 97 | `A` | `V` | Observed-coordinate substitution |
| 102 | `X` | `V` | Observed-coordinate substitution |
| 140 | `A` | `D` | Observed-coordinate substitution |

**Conditional interpretation — native p164 unit witness; 6 observed substitutions and no fills:**

```text
ANXOXKXMXXDONAUUEBERGANG219XIXDXBEENDETXBELGRADXSEMUMXLEBHAFTERUEBERSETZVERKEHRX
```

The native p153 unit positions 24–26 use `GD FG GX` at source pairs
`[58,106]`, `[18,138]` and `[66,98]`. The corresponding p164 positions 69–71
use `GD FG GF` at `[230,43]`, `[69,144]` and `[82,181]`. All twelve
coordinates are observed. The certificate binds the 63-character comparison
to both literal source transcriptions and checks the completed p153 text by
exact re-encryption without assigning either unknown square cell.

</details>

## Reproduction and credit

```bash
python experiments/nov7_danube_and_message_reports/verify.py --verify
python experiments/nov7_danube_and_message_reports/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier checks the literal source rows, coordinate costs, quoted readings, all six `EB?Q` alternatives and the native p164 unit witness. The PDF option reproduces the two declared source crops and compares their pixels.

[Certificate](../../experiments/nov7_danube_and_message_reports/certificates.json) · [Experiment notes](../../experiments/nov7_danube_and_message_reports/README.md) · [Verifier](../../experiments/nov7_danube_and_message_reports/verify.py)

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

</details>
<!-- CASE-EDITION:END -->
