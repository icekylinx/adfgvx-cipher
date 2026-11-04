# Radio notices, Tiflis personnel and internment on p230

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

Four source-length telegrams on Childs p230 become complete literal readings under the published Nov28–Dec1 square. All 490 coordinates are preserved: no coordinate substitution, source-mask fill or frame change is needed. The source itself gives two first-group readings for C; both are retained.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed page excerpt](../../experiments/nov30_radio_personnel/sources/p230_reviewed.png) · [Exact inputs](../../experiments/nov30_radio_personnel/inputs.json) · [Position-by-position certificates](../../experiments/nov30_radio_personnel/certificates.json)

The unchanged published key is `Nov28-Dec1`. The [earlier unreviewed candidates](../../experiments/nov30_radio_personnel/prior_candidates.json) and [original OCR records](../../experiments/nov30_radio_personnel/ocr_snapshot.json) are preserved. The present work supplies an image-reviewed source edition and a reproducible repair account; it does not claim that every body is a first public decipherment.

| Record | Source slots | Fixed raw positions | Coordinate substitutions | Source-mask fills |
|---|---:|---:|---:|---:|
| [p230 B](#p230-b) | 136 | 68 / 68 | 0 | 0 |
| [p230 C](#p230-c) | 78 | 39 / 39 | 0 | 0 |
| [p230 D](#p230-d) | 188 | 94 / 94 | 0 | 0 |
| [p230 E](#p230-e) | 88 | 44 / 44 | 0 | 0 |

## p230 B

**Source transcription — header:** `B) ZON v CV (06.33 p.m., December 3d); 2130 (30/11); RICHI-136`

**Readable German** — based on the unchanged raw output.

> Inspektion und Kriegsministerium verstaendigt. Antwort steht noch aus. Papp.

**Meaning:** The inspection and the War Ministry have been notified; a reply is still outstanding. Signed Papp.

<details>
<summary>Raw decoded text</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
INSPEKTIONUNDKRIEGSMINISTERIUMVERSTAENDIGTYYANTWORTSTEHTNOCHAUSYPAPP
```

</details>

**Unresolved details and editorial limits.**

- The page is headed 30 November; the intercept annotation says December 3 and the service line says 2130 (30/11). These are separate source dates.
- A small mark after the last V of VVGFV is not counted as a sixth coordinate. The source count is exactly 136.

## p230 C

**Source transcription — header:** `C) CV v ZON (11.15 p.m., December 6th); 1900 (30/11); RIZI-78; XAFFV (or XVFFV)`

**Readable German** — based on the unchanged raw output.

> Station baut 0ZXJ frueh 9 Uhr ab. Burkard.

**Meaning:** A station announces when it will dismantle. The printed key labels do not establish the historical day or hour; Burkard is the literal signature.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
STATIONBAUT0ZXJYFRUEH9YUHRABYYBURKARDYY
```

**Raw output — second printed source variant**, independently re-encrypted without repair.

```text
STATIONBAUT0ZXJZFRUEH9YUHRABYYBURKARDYY
```

</details>

**Unresolved details and editorial limits.**

- The source explicitly prints XAFFV (or XVFFV). Both complete 78-slot frames are decrypted and re-encrypted. Their only output difference is position 15: Y versus Z. Neither version is silently selected as historically authentic.
- The readable text uses the first printed variant. Its literal field 0ZXJ and its hour label 9 stay unassigned. Under the alternative, the token immediately before FRUEH is 0ZXJZ rather than 0ZXJ followed by Y.
- The intercept annotation says December 6; the service line says 1900 (30/11).

## p230 D

**Source transcription — header:** `D) NKJ v LP (05.47 p.m., December 4th); Fuer COS 1225 (30/11); RICHI-188`

**Readable German** — based on the unchanged raw output.

> Zentralfunkleitg erbitten Nachricht ueber Verbleib Funker und Baupersonal der Funkenstation Tiflis. 54X05.

**Meaning:** The central radio command asks where the radio operators and construction personnel of the Tiflis station have gone. The final 54X05 remains a literal reference.

<details>
<summary>Raw decoded text</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
ZENTRALFUNKLEITGERBITTENNACHRICHTUEBERVERBLEIBFUNKERUNDBAUPERSONALDERFUNKENSTATIONTIFLISY54X05
```

</details>

**Unresolved details and editorial limits.**

- ZENTRALFUNKLEITG is kept as the transmitted abbreviation; the readable display does not insert its omitted letters.
- The source header says December 4; the service line says Fuer COS 1225 (30/11).

## p230 E

**Source transcription — header:** `E) ZON v CV (04.43 p.m., December 6th); 0930 (30/11); RICHI-88`

**Readable German** — based on the unchanged raw output.

> Internierung rechtzeitig hierher mitteilen. Papp.

**Meaning:** Give timely notification here of the internment. Signed Papp. The short message does not name the persons or formation to be interned.

<details>
<summary>Raw decoded text</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
INTERNIERUNGRECHTZEITIGHIERHERMITTEILENYPAPP
```

</details>

**Unresolved details and editorial limits.**

- The intercept annotation says December 6; the service line reads 0930 (30/11). The earlier OCR gave 0830, which is not retained as the primary source transcription.

## Evidence and credit

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are preserved separately. This is a source edition and explicit repair review, not a claim of universal first-decipherment priority.

The certificates replay every coordinate alteration, compare the independent column/domain reconstruction with the cipher implementation, and re-encrypt every complete edited output. Each readable passage preserves every nonseparator output label; literal protected fields are also checked without removing their internal separators. Source crops are bound to the original PDF by page, rectangle, scale, file digest and RGB-pixel digest.

Reproduce with `python experiments/nov30_radio_personnel/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to regenerate and compare the delivered source pixels.

A roundtrip proves compatibility with a stated reading. Editorial spelling repairs remain proposals, and literal number labels are not automatically historical dates, quantities or reference numbers.
