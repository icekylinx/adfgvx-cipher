# November 7: Danube crossings and short message reports

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

This edition reviews five separate physical records on printed pages 152–153 of J. Rives Childs’s *General Solution of the ADFGVX Cipher System*. The useful readings concern a reported attack near Belgrad after a crossing, a short morning report, the receipt of a message, a prescribed line, and Danube crossing traffic. Each body keeps its **native printed length and order**. The explicit word proposals cost **14 observed-coordinate substitutions and four fills of source dashes** across the five records. One character in `EB?Q` remains unresolved.

The two page-153 records are the printed third and first parts under separate reception headers. Their common `2010` label and station pair do not supply the absent second part or establish a complete assembled message. These records are separate from the original challenge entries [p153a](../p153a.md) and [p153b](../p153b.md), which are the later fifth and sixth parts on that page and are not counted here.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## Evidence and costs

All coordinates and plaintext positions below use **zero-based indices**. A fixed plaintext position means that the published key and the stated coordinate frame determine that label; it does not mean that the resulting word is historically correct.

| Record | Native source slots | Source dashes | Raw fixed positions | Edited fixed positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [p152_B2](#p152-b2) | 190 | 5 | 90/95 | 94/95 | 3 | 4 |
| [p152_C](#p152-c) | 108 | 0 | 54/54 | 54/54 | 2 | 0 |
| [p152_D](#p152-d) | 140 | 0 | 70/70 | 70/70 | 2 | 0 |
| [p153_A3](#p153-a3) | 180 | 0 | 90/90 | 90/90 | 2 | 0 |
| [p153_B1](#p153-b1) | 160 | 0 | 80/80 | 80/80 | 5 | 0 |
| **Total** | **778** | **5** | **384/389** | **388/389** | **14** | **4** |

The three masked or overlong earlier OCR bodies are retained in [the frozen OCR snapshot](../../experiments/nov7_danube_and_message_reports/ocr_snapshot.json) and [prior unchanged-key diagnostics](../../experiments/nov7_danube_and_message_reports/prior_candidates.json). Restoring what the scan actually prints is an OCR transcription correction, not a deletion or insertion in a received ciphertext. The printed `p152_C` length field is dash-only: its 108-slot count is measured from the body, not advertised by its header.

[Printed page 152, B2 through D — source-PDF reference](../../experiments/nov7_danube_and_message_reports/inputs.json)

[Printed page 153, A3 and B1 — source-PDF reference](../../experiments/nov7_danube_and_message_reports/inputs.json)

The unchanged published `Nov4-6` key reads `p152_B2` and `p152_D`; the unchanged `Nov7-9` key reads the other three. A key’s period label is not used to rewrite a reception date. The exact key tables, publication credit, image bounds and hashes are in [inputs.json](../../experiments/nov7_danube_and_message_reports/inputs.json).

## p152 B2

Security force near Belgrad attacked after a crossing.

Literal header: `B) UKS v ZON (--- November 7th); 2 TL RICHI-190`.

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

**Readable German — the complete edited stream, with punctuation and spacing:**

> erreicht 9 H. EB?Q. TITEL. Sicherung 219 I. D. noordl. Belgrad durch dort uebergegangene Serben angegriffen.

**Conditional interpretation — scope and limits:**

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

## p152 C

Morning report: no special events.

Literal header: `C) --- v ZON (--- November 7th); 1235; RICHI----`.

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

**Readable German — the complete edited stream, with punctuation and spacing:**

> O. K. M. Morgenmeldung 7.11. Keine bes. Ereignisse. A. O. K. 11.

**Conditional interpretation — scope and limits:**

A short morning report states that there are no special events. The internal 7.11 and AOK11 labels are retained as transmitted.

The source prints a dash-only length field, not 108. The body itself has 108 native coordinates. The earlier OCR appended five mask slots after the final XDV; these are absent from the body in the image and are not treated as received coordinates.

One substitution changes UORGENMELDUNG to MORGENMELDUNG. A second replaces the raw Q between BES and EREIGNISSE with the X separator; the abbreviation BES is not expanded by inserting extra plaintext letters.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 66 | `V` | `F` | Observed-coordinate substitution |
| 85 | `F` | `V` | Observed-coordinate substitution |

## p152 D

Receipt of a FunkSpruch with literal numerical fields.

Literal header: `D) UKS v ZON (--- November --); 1850 1010; RICHI-140`.

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

**Readable German — the complete edited stream, with punctuation and spacing:**

> Fuer O. K. M. Funkspruch EINSA11205BM4 1189 35 vorm. eingetroffen. A. O. K. 11.

**Conditional interpretation — scope and limits:**

The message reports that a FunkSpruch has arrived, addressed for OKM and ending with the proposed AOK11 signature. Its compact reference and time-like numerical fields are retained without reconstructing an exact calendar date or clock time.

The source header leaves the reception day blank and separately prints 1850 1010. Neither that line nor the decoded 1189 35 field is silently converted to a date/time.

The raw O K C M becomes O K M by changing C to the X separator. The raw A O W11 becomes A O K11 by changing W to K. These are two explicit observed-coordinate substitutions; the arrival wording itself is native.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 8 | `X` | `F` | Observed-coordinate substitution |
| 39 | `A` | `F` | Observed-coordinate substitution |

## p153 A3

A prescribed line and a Temesvar headquarters field.

Literal header: `A) UKS v ZÖN (10.55 p.m., November 7th); 2010; 3 TL RICHI-180`.

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

**Readable German — the complete edited stream, with punctuation and spacing:**

> in befohlene Linie NAGYBECSKEREK VERSECZ an, die 10.11 erreicht. A. H. Q. 9.11 TEMESVAR. A. O. K. 11.

**Conditional interpretation — scope and limits:**

This third-part fragment refers to a prescribed line through the transmitted place labels NAGYBECSKEREK and VERSECZ, an internal 10.11 label, and an AHQ field with 9.11 and TEMESVAR. The missing preceding text does not establish a complete movement order or prove that a move occurred.

The native body has 180 coordinates. Earlier OCR attached an extra mask to the five-coordinate VGVGV group, producing 181; it is removed from the OCR comparison rather than excluded from the physical source.

Two ordinary-word/place-spelling proposals change NAYYBECSKEREK to NAGYBECSKEREK and VERSSCZ to VERSECZ. The forms VERSECZ and TEMESVAR remain unexpanded; no modern-place identification is required for the reading.

The printed reception is November 7, while the body retains 9.11 and 10.11. The edition does not rewrite the header to fit those internal labels.

The header visibly places two short marks above the O in the sender label; the transcription preserves this as ZÖN without identifying a different station.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 156 | `X` | `V` | Observed-coordinate substitution |
| 163 | `A` | `D` | Observed-coordinate substitution |

## p153 B1

Danube crossing completed and busy crossing traffic.

Literal header: `B) UKS v ZÖN (9.42 p.m., November 7th); 2010 3 TLE; 1 TL RICHI-160`.

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

**Conditional interpretation — scope and limits:**

The first part reports completion of a Danube crossing by a formation transmitted as 21B I D and busy crossing traffic at the labels Belgrad and SEMUM. The unit label is not changed to a plausible number, and SEMUM is not identified with a modern or alternative place-name.

The native body is 160 coordinates. Earlier OCR turned the first-row VDGVV into a six-slot masked group, producing 161; the image restores the actual five-coordinate group without a source insertion or deletion.

DONAUU3BERGANG→DONAUUEBERGANG, BEENDUT→BEENDET, BELGR4D→BELGRAD and UEBSRSETZVERKEHR→UEBERSETZVERKEHR together cost five observed-coordinate substitutions. The raw digits in the damaged words remain visible in the raw layer.

21B and SEMUM remain literal. The first- and third-part records share 2010 and the same station pair but have different reception times; this edition does not supply a missing second part or claim a complete assembled message.

The header visibly places two short marks above the O in the sender label; the transcription preserves this as ZÖN without identifying a different station.

| Source index | Printed coordinate | Proposed coordinate | Cost class |
| ---: | :---: | :---: | --- |
| 11 | `A` | `D` | Observed-coordinate substitution |
| 20 | `V` | `X` | Observed-coordinate substitution |
| 97 | `A` | `V` | Observed-coordinate substitution |
| 102 | `X` | `V` | Observed-coordinate substitution |
| 140 | `A` | `D` | Observed-coordinate substitution |

The wording repairs include digits occurring inside damaged words (`3` in `U3BERGANG` and `4` in `BELGR4D`). Their exact changes are visible in the two full streams and charged in the ledger. This does not authorize changing the independent unit label `21B`, which stays literal in every layer.

## Reproduction and credit

From any working directory, run the verifier by its filesystem path. From the repository root:

```bash
python experiments/nov7_danube_and_message_reports/verify.py --verify
python experiments/nov7_danube_and_message_reports/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier binds the native transcriptions to raw output, prices every proposed coordinate change and source-mask fill, checks each complete readable quote against its decoded stream, preserves protected labels, verifies the six unresolved `EB?Q` completions, and checks exact re-encryption under consistent global squares. With `--pdf`, it regenerates both crops and compares their pixels exactly. The live case headers and all source/raw/edited/readable displays are also bound to the inputs. The arbitrary completions used solely for roundtrip witnesses are explicitly nonhistorical.

[Certificate](../../experiments/nov7_danube_and_message_reports/certificates.json) · [Experiment notes](../../experiments/nov7_danube_and_message_reports/README.md) · [Verifier](../../experiments/nov7_danube_and_message_reports/verify.py)

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
