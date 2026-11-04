# Von Schorlemer: demobilization work inquiry and reply

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

A clear-address request on p122 and an encrypted reply on p155 form a source-linked exchange about von Schorlemer's availability for demobilization work. The earlier request asks whether he can be released to the Trade Ministry; the later administrative-staff reply says he cannot currently be spared. Both native frames and every repair remain explicit. The later reply supports the name and topic; the 33 supplied mask values in the first request remain editorial proposals.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed page excerpt](../../experiments/schorlemer_demobilization_inquiry/sources/p122_reviewed.png) · [Second source excerpt](../../experiments/schorlemer_demobilization_inquiry/sources/p155_reviewed.png) · [Exact inputs](../../experiments/schorlemer_demobilization_inquiry/inputs.json) · [Position-by-position certificates](../../experiments/schorlemer_demobilization_inquiry/certificates.json) · [Reading conventions](../../docs/reading-conventions.md)

The unchanged published keys are `Nov4-6`, `Nov7-9`. The [earlier unreviewed candidates](../../experiments/schorlemer_demobilization_inquiry/prior_candidates.json) and [original OCR records](../../experiments/schorlemer_demobilization_inquiry/ocr_snapshot.json) are preserved. The present work supplies an image-reviewed source edition and a reproducible repair account; it does not claim that every body is a first public decipherment.

| Record | Source slots | Fixed raw positions | Coordinate substitutions | Source-mask fills |
|---|---:|---:|---:|---:|
| [p122 B](#p122-b) | 252 | 93 / 126 | 5 | 33 |
| [p155 B](#p155-b) | 160 | 76 / 80 | 3 | 4 |

## p122 B

**Source transcription — header:** `B) NKJ v LP (08.40 p.m., November 4th); FUER UKS 1400 (4). OBERLEUTNANT VON SCHORLEMER OBERKOMMANDO M VERWALTUNGSSTAB; RICHI-252`

**Readable German** — based on the explicitly repaired output below.

> Erbitte Rueckantwort durch Funkspruch, ob Sie zur Beschaeftigung im Handelsministerium, Demobilmachungsgruppe, abkoemmlich. Handelsminister.

**Meaning:** The Trade Minister asks for a radio reply on whether the addressee can be released for work in the ministry demobilization group. The clear header names First Lieutenant von Schorlemer at the Oberkommando M administrative staff.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
E?BI?TERUE?KA?TFOT?DU?CHFUN?SP?UCHO?SI?ZU?BE?CH?E?TI?UN?IM?ANDEL?M?NISTE?GU?XDEMO?I?MACHU??S?RPPPE?A?KOESM?IC?XHAND?L?MINIS?ER
```

**Edited output** — 5 observed-coordinate substitutions and 33 source-mask fills; no coordinate inserted, deleted or moved.

```text
ERBITTERUECKANTWORTDURCHFUNKSPRUCHOBSIEZURBESCHAEFTIGUNGIMHANDELSMINISTERIUMXDEMOBILMACHUNGSGRUPPEXABKOEMMLICHXHANDELSMINISTER
```

</details>

**Unresolved details and editorial limits.**

- The source contains 33 printed dashes, including six complete masked groups. They are part of the native 252-slot frame. Their supplied values are editorial source-mask fills, not recovered visible coordinates.
- The five observed-coordinate substitutions are separately priced. They repair word-level corruptions; there is no source insertion or change of key.
- The clear address is an independent source witness for the surname in the later p155 B response. The two bodies were enciphered under different published period keys.

## p155 B

**Source transcription — header:** `B) LP v NKJ (7.09 p.m., November 7th); 0800 VON UKS (7/11); RICHI-160`

**Readable German** — based on the explicitly repaired output below.

> Handelsminister Berlin. Oblt. v. Schorlemer z. Zeit hier nicht abkoemmlich. OKM Verw. Stab.

**Meaning:** The administrative staff informs the Trade Minister in Berlin that First Lieutenant von Schorlemer cannot currently be released.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
KANDELSMINISTERBERLINXOBLTXVXSCKORLEMERXZXZEIT?IERNI?HTABKOEM?LICKXOKMX?ERWXSTAB
```

**Edited output** — 3 observed-coordinate substitutions and 4 source-mask fills; no coordinate inserted, deleted or moved.

```text
HANDELSMINISTERBERLINXOBLTXVXSCHORLEMERXZXZEITHIERNICHTABKOEMMLICHXOKMXVERWXSTAB
```

</details>

**Unresolved details and editorial limits.**

- The source visibly prints four dashes. The 160-slot native frame is unchanged.
- The name repair SCKORLEMER to SCHORLEMER is supported by the independent clear p122 B address, not by a guessed biography. No first name or unique historical person is supplied.
- The exchange concerns availability for duty; it does not itself establish that a reassignment or recall actually occurred.

## Evidence and credit

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates replay every coordinate alteration, compare the independent column/domain reconstruction with the cipher implementation, and re-encrypt every complete edited output. For a partial output, an injective global completion of the square and residual source masks supplies an explicitly nonhistorical roundtrip witness. Each readable passage preserves every nonseparator output label; literal protected fields are also checked without removing their internal separators. Source crops are bound to the original PDF by page, rectangle, scale, file digest and RGB-pixel digest.

Reproduce with `python experiments/schorlemer_demobilization_inquiry/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to regenerate and compare the delivered source pixels.

A roundtrip proves compatibility with a stated reading. Editorial spelling repairs remain proposals, and literal number labels are not automatically historical dates, quantities or reference numbers.
