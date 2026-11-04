# Radio reception instructions and a brief no-events report

Staff the station with especially good listeners; transmit at a moderate speed with clear signs and spaces between groups. The sentence continues in part 2.

**Complete edition by printed page:** [p. 224](../pages/224.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The two-part p224 A telegram asks for experienced listeners, clear transmission and a suitable reception wavelength. The separate p224 B report states that nothing special has happened. This edition preserves the source-length spellings SICERES and MORENMELDUNG and the date-like field 17XJJ.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed page excerpt](../../experiments/nov27_receiving_instructions/sources/p224_reviewed.png) · [Exact inputs](../../experiments/nov27_receiving_instructions/inputs.json) · [Position-by-position certificates](../../experiments/nov27_receiving_instructions/certificates.json)

The unchanged published key is `Nov25-28`. The [earlier unreviewed candidates](../../experiments/nov27_receiving_instructions/prior_candidates.json) and [original OCR records](../../experiments/nov27_receiving_instructions/ocr_snapshot.json) are preserved. The present work supplies an image-reviewed source edition and a reproducible repair account; it does not claim that every body is a first public decipherment.

| Record | Source slots | Fixed raw positions | Coordinate substitutions | Source-mask fills |
|---|---:|---:|---:|---:|
| [p224 A1](#p224-a1) | 238 | 116 / 119 | 5 | 3 |
| [p224 A2](#p224-a2) | 176 | 88 / 88 | 3 | 0 |
| [p224 B](#p224-b) | 92 | 46 / 46 | 6 | 0 |

## p224 A1

**Source transcription — header:** `A) BSL v UKS (11.20 p.m., November 27th); 172- 2 TLE; 1 TL RIZI-238`

**Readable German** — based on the explicitly repaired output below.

> Bitte Station mit besonders guten Hoerern zu besetzen. Maessig schnell, deutliche Zeichen in Gruppenabstaenden zu senden. Da Funkstation

**Meaning:** Staff the station with especially good listeners; transmit at a moderate speed with clear signs and spaces between groups. The sentence continues in part 2.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
BITTESTATIONOITBESONDERS9UTENHOERERNZUBESETZENXMAESSIGS?HNELLXDEUTLICDEZEICHENING?UPPENATSTAENDENZUSGNDENXDAFUN?STATION
```

**Edited output** — 5 observed-coordinate substitutions and 3 source-mask fills; no coordinate inserted, deleted or moved.

```text
BITTESTATIONMITBESONDERSGUTENHOERERNZUBESETZENXMAESSIGSCHNELLXDEUTLICHEZEICHENINGRUPPENABSTAENDENZUSENDENXDAFUNKSTATION
```

</details>

**Unresolved details and editorial limits.**

- The literal noncoordinate C in VXACX is masked, together with the two printed dashes; none is silently accepted as an ADFGVX coordinate.
- The source ends VX- and contains the complete five-slot group VFVFD. Restoring these actually printed slots to the OCR record is not adding historical coordinates.

## p224 A2

**Source transcription — header:** `A) same two-part telegram; 2 TL RICHI-176`

**Readable German** — based on the explicitly repaired output below.

> einziges, siceres Nachrichtenmittel mit Heimat. Welche stoerungsfreie Empfangswelle erwuenscht?

**Meaning:** The radio station is described as the only secure communication link with home; the recipient is asked which interference-free receiving wavelength is desired.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
EINQIGESXSICERESN6CHRICHTENMITTELMITHEIMATXWELCHESTOERUNGSFREIEEMPFANGSWELLEERWUENSCHTXX
```

**Edited output** — 3 observed-coordinate substitutions and 0 source-mask fills; no coordinate inserted, deleted or moved.

```text
EINZIGESXSICERESNACHRICHTENMITTELMITHEIMATXWELCHESTOERUNGSFREIEEMPFANGSWELLEERWUENSCHTXX
```

</details>

**Unresolved details and editorial limits.**

- SICERES is retained exactly in the edited output and readable text. The intended word is plausibly [sicheres], but supplying H would add a plaintext position and is not claimed by this native-frame edition.
- The two changed labels are Q to Z in EINQIGES and 6 to A in N6CHRICHTEN; the latter is a disclosed word repair, not a global reassignment of the square label 6.

## p224 B

**Source transcription — header:** `26th NOVEMBER, 1918; B) UKS v ZON (07.51 a.m., November 26th); 0800; RICHI-92`

**Readable German** — based on the explicitly repaired output below.

> Morenmeldung 17XJJ. Keine besonderen Ereignisse.

**Meaning:** A short report says there are no special events. Its apparent morning-report heading lacks a letter in this source-length reading; the field 17XJJ stays literal.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
MMRENMOLDUNG17XJJXXKETNEBESOGDERENERETGNISSEXX
```

**Edited output** — 6 observed-coordinate substitutions and 0 source-mask fills; no coordinate inserted, deleted or moved.

```text
MORENMELDUNG17XJJXXKEINEBESONDERENEREIGNISSEXX
```

</details>

**Unresolved details and editorial limits.**

- MORENMELDUNG is retained, rather than silently lengthened to [Morgenmeldung]. The 92 source slots permit 46 plaintext positions, not 47.
- The raw date-like field 17XJJ is not changed to match the printed 26 November heading. The two date layers are reported separately.

## Evidence and credit

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are preserved separately. This is a source edition and explicit repair review, not a claim of universal first-decipherment priority.

The certificates replay every coordinate alteration, compare the independent column/domain reconstruction with the cipher implementation, and re-encrypt every complete edited output. Each readable passage preserves every nonseparator output label; literal protected fields are also checked without removing their internal separators. Source crops are bound to the original PDF by page, rectangle, scale, file digest and RGB-pixel digest.

Reproduce with `python experiments/nov27_receiving_instructions/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to regenerate and compare the delivered source pixels.

A roundtrip proves compatibility with a stated reading. Editorial spelling repairs remain proposals, and literal number labels are not automatically historical dates, quantities or reference numbers.

</details>
<!-- CASE-EDITION:END -->
