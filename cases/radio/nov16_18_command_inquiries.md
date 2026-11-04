# Armistice acknowledgments, personnel and Warsaw radio inquiries

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

Seven native source records cover an armistice-receipt query, nightly radio listening, an inquiry for Captain von Borries, the location of the Warsaw general government, and radio equipment and personnel. Two previously OCR-damaged short messages become clear when their actually printed final groups are restored. All unresolved fields and missing-letter spellings remain explicit.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [p202 source](../../experiments/nov16_18_command_inquiries/sources/p202_reviewed.png) · [p203 source](../../experiments/nov16_18_command_inquiries/sources/p203_reviewed.png) · [p204 source](../../experiments/nov16_18_command_inquiries/sources/p204_reviewed.png) · [Exact inputs](../../experiments/nov16_18_command_inquiries/inputs.json) · [Position-by-position certificates](../../experiments/nov16_18_command_inquiries/certificates.json)

The unchanged published keys are `Nov16-18`, `Nov13-15b`. The [earlier unreviewed candidates](../../experiments/nov16_18_command_inquiries/prior_candidates.json) and [original OCR records](../../experiments/nov16_18_command_inquiries/ocr_snapshot.json) are preserved. The present work supplies an image-reviewed source edition and a reproducible repair account; it does not claim that every body is a first public decipherment.

| Record | Source slots | Fixed raw positions | Coordinate substitutions | Source-mask fills |
|---|---:|---:|---:|---:|
| [p202 A1](#p202-a1) | 212 | 105 / 106 | 4 | 0 |
| [p202 A2](#p202-a2) | 142 | 67 / 71 | 1 | 0 |
| [p203 A2](#p203-a2) | 132 | 63 / 66 | 2 | 2 |
| [p203 B](#p203-b) | 164 | 81 / 82 | 0 | 0 |
| [p204 B](#p204-b) | 92 | 46 / 46 | 0 | 0 |
| [p204 C1](#p204-c1) | 244 | 116 / 122 | 2 | 3 |
| [p204 D](#p204-d) | 84 | 39 / 42 | 0 | 0 |

## p202 A1

**Source transcription — header:** `A) NKJ, UKS v LP (12.51 p.m., November 16th); FUER UKS 0900 (16), 2 TEILE; 1 TL RICHI-212`

**Readable German** — based on the explicitly repaired output below.

> An OKM. Sofortige Bestaetigung erforderlich, ob Funkspruch 1XAXC?XR vom 1RX11 betr. Waffenstillstandsbedingungen

**Meaning:** Immediate confirmation is requested that a telegram on armistice conditions has arrived. The reference and date labels remain unresolved; the sentence continues in A2.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
ANXOKMXXSOFORTIGEBESTAETIGUNGERFORDERLICHOBFUNKSYRUCHX1XAXC?XRXVOM1RX11MBETRXNAFFDNSTILLSTANDSBEDINGUNGENX
```

**Edited output** — 4 observed-coordinate substitutions and 0 source-mask fills; no coordinate inserted, deleted or moved.

```text
ANXOKMXXSOFORTIGEBESTAETIGUNGERFORDERLICHOBFUNKSPRUCHX1XAXC?XRXVOM1RX11XBETRXWAFFENSTILLSTANDSBEDINGUNGENX
```

</details>

**Unresolved details and editorial limits.**

- The word repairs include FUNKSYRUCH to FUNKSPRUCH, M to separator X before BETR, and NAFFDN to WAFFEN. All resulting coordinate changes are priced. The opaque C?XR and 1RX11 fields are not guessed.

## p202 A2

**Source transcription — header:** `A) same two-part telegram; 2 TL RICHI-142`

**Readable German** — based on the explicitly repaired output below.

> und Befehl zur Fortsetzung des Abmarsches dort angekommen. OHL 1XAXNRX1???12XOP.

**Meaning:** The continuation asks whether the order to continue the withdrawal has arrived. The OHL reference is preserved as a literal field.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
UNDBEFEHLZURFORTSETZUNGDESABMAR?CHESDORTANGEKOMMENXOHLX1XAXNRX1???12XOP
```

**Edited output** — 1 observed-coordinate substitution and 0 source-mask fills; no coordinate inserted, deleted or moved.

```text
UNDBEFEHLZURFORTSETZUNGDESABMARSCHESDORTANGEKOMMENXOHLX1XAXNRX1???12XOP
```

</details>

**Unresolved details and editorial limits.**

- The source clearly prints XFGDV where the earlier OCR had X?GDV. The remaining unknowns come from unassigned cells of the published square, not missing source coordinates.
- The raw letter in ABMAR?CHES is under an unfilled square cell. The proposed S is implemented by changing its observed ciphertext coordinate, not by assigning that unknown cell S globally.

## p203 A2

**Source transcription — header:** `A) --- v ZON (23.31 p.m., November 16th); 22.35 (16/11); 2 TL RIZI-132`

**Readable German** — based on the explicitly repaired output below.

> Stehet jede Nacht auf Empfang. Verbindung mit Deutschl. dringend benoetigt.

**Meaning:** Maintain reception every night; a connection with Germany is urgently needed. Only the source-labelled second part is present in this record.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
STE?ETJEDEN?CHTAUF?MPFANGXVERBINDUNGMITDEUTSCHLXRRINGENDBENOETIGTX
```

**Edited output** — 2 observed-coordinate substitutions and 2 source-mask fills; no coordinate inserted, deleted or moved.

```text
STEHETJEDENACHTAUFEMPFANGXVERBINDUNGMITDEUTSCHLXDRINGENDBENOETIGTX
```

</details>

**Unresolved details and editorial limits.**

- The printed 2 TL is retained. The absent first part is not reconstructed from this second part.
- Two opening dashes are source-mask slots. The unchanged Nov13–15b key produces this body despite the printed 16 November date; this is a documented key-use observation, not a silent redating.
- DEUTSCHL remains the transmitted abbreviation.

## p203 B

**Source transcription — header:** `B) IWE v LP (03.48 p.m., November 18th); FUER IWE v LP 14.55 (18/11); RICHI-164`

**Readable German** — based on the unchanged raw output.

> KM Abt. Nachrichtenmittel erbittet Nachricht ueber Verbleib Hptm. v. Borries, Gen. Kdo. ?2.

**Meaning:** The War Ministry communications-equipment section asks for information on the whereabouts of Captain von Borries. The general-command label ?2 is not numbered historically.

<details>
<summary>Raw decoded text</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
KMXABTXNACHRICHTENMITTELXERBITTETNACHRICHTUEBERVERBLEIBXHPTMXVXBORRIESXGENXKDOX?2X
```

</details>

**Unresolved details and editorial limits.**

- The OCR omitted the final four-coordinate group GVFD. The source visibly prints it, and restoring it yields the exact advertised 164-slot frame. This is a transcription correction, not a historical coordinate insertion.
- The body names VXBORRIES; no specific person is identified from the surname alone.

## p204 B

**Source transcription — header:** `B) WAU, IWE v LP (6 p.m., November 17th); ZWEI AR FUER WAU 1300 (17); RICHI-92`

**Readable German** — based on the unchanged raw output.

> Wo befindet sich jetzt Generalgouvernement Warschau?

**Meaning:** A direct query asks the present location of the Warsaw general government.

<details>
<summary>Raw decoded text</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
WOBEFINDETSICHJETZTGENERALGOUVERNEMENTWARSCHAU
```

</details>

**Unresolved details and editorial limits.**

- The unchanged native 92-coordinate frame yields a complete reading without a coordinate edit or fill.

## p204 C1

**Source transcription — header:** `C) KOW v WAU (1.50 a.m., November 18th); 0115 (17), 2 TLE; 1 TL RICHI-244`

**Readable German** — based on the explicitly repaired output below.

> GE?NACH2O2. Leichte in Lomza und Czenstochau, Verbleib unbekannt. Vermutl. mit ihren Gouvs. aberueckt. Besatzg beiden anderen Stat. ohne Geraet.

**Meaning:** The whereabouts of the light units or equipment in Lomza and Czenstochau are unknown; they are presumed to have departed with their governors. The crews of the other two stations have no equipment. The opening is opaque and several transmitted abbreviations and the missing-letter spelling ABERUECKT remain visible.

<details>
<summary>Source and cipher evidence</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
GE?NACH2O2LE?CHTEINLOMZAUNDCZENSTOCHAUXV?RBLEIBUNBEKANNTXVERMUTLMITI?RENGOUVSABERUECKTXBESATZGBEIDENANDERE?STATOHNEGERA?TX
```

**Edited output** — 2 observed-coordinate substitutions and 3 source-mask fills; no coordinate inserted, deleted or moved.

```text
GE?NACH2O2LEICHTEINLOMZAUNDCZENSTOCHAUXVERBLEIBUNBEKANNTXVERMUTLMITIHRENGOUVSABERUECKTXBESATZGBEIDENANDERENSTATOHNEGERAETX
```

</details>

**Unresolved details and editorial limits.**

- The source prints four dash slots: XD--- and GG-AX. The opening GE?NACH2O2 remains unresolved.
- The source-length output ABERUECKT is not silently expanded to [abgerueckt]. VERMUTL, GOUVS, BESATZG and STAT remain their transmitted abbreviated forms.
- Part 2 advertises 282 slots but the reviewed page prints 242. A 40-slot tail-loss hypothesis yields related fragments, but is not accepted as a complete source-length decipherment or counted as another reviewed reading here.

## p204 D

**Source transcription — header:** `D) --- v --- (8.43 a.m., November 18th); RICHI-84`

**Readable German** — based on the unchanged raw output.

> Zu 2??F vom 1?X: 1. Nein. 2. PSO BSL. Fusta WAU.

**Meaning:** A short numbered reply answers no to item 1 and gives the literal call-sign-like pair PSO BSL for item 2. The inquiry number, date and expansion of PSO remain unresolved.

<details>
<summary>Raw decoded text</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
ZU2??FVOM1?XX1XNEINXX2XPSOXBSLXXFUSTAWAUXX
```

</details>

**Unresolved details and editorial limits.**

- The source visibly prints VAXAX and the final AXGF, both omitted from the earlier OCR candidate. The native count is 84.
- The transmitted fragment 1?XX is shown as 1?X before the sentence separator; no value is supplied for its unresolved cell.

## Evidence and credit

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are preserved separately. This is a source edition and explicit repair review, not a claim of universal first-decipherment priority.

The certificates replay every coordinate alteration, compare the independent column/domain reconstruction with the cipher implementation, and re-encrypt every complete edited output. For partial outputs, each certificate also constructs one injective global completion of the square and residual masks and verifies its full roundtrip; the witness is explicitly nonhistorical. Each readable passage preserves every nonseparator output label; literal protected fields are also checked without removing their internal separators. Source crops are bound to the original PDF by page, rectangle, scale, file digest and RGB-pixel digest.

Reproduce with `python experiments/nov16_18_command_inquiries/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to regenerate and compare the delivered source pixels.

A roundtrip proves compatibility with a stated reading. Editorial spelling repairs remain proposals, and literal number labels are not automatically historical dates, quantities or reference numbers.
