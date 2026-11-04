# Wishing to travel home and uncertainty over Baltic transport

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

Two native source bodies need no coordinate repairs: one describes soldiers wishing to travel home without authorization; the other links transport difficulty to uncertainty in the Baltic Sea and begins an incomplete statement about Graf Goltz. The shared unknown GA cell remains globally coupled across their separate references. Missing context and abbreviated source spellings stay explicit.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p186 excerpt](../../experiments/home_departures_baltic_transport/sources/p186_reviewed.png) · [Exact inputs](../../experiments/home_departures_baltic_transport/inputs.json) · [Position-by-position certificates](../../experiments/home_departures_baltic_transport/certificates.json) · [Reading conventions](../../docs/reading-conventions.md)

The unchanged published keys are `Nov13-15b`. The [earlier unreviewed candidates](../../experiments/home_departures_baltic_transport/prior_candidates.json) and [original OCR records](../../experiments/home_departures_baltic_transport/ocr_snapshot.json) are preserved. The present work supplies an image-reviewed source edition and a reproducible repair account; it does not claim that every body is a first public decipherment.

| Record | Source slots | Fixed raw positions | Coordinate substitutions | Source-mask fills |
|---|---:|---:|---:|---:|
| [p186 B2](#p186-b2) | 242 | 120 / 121 | 0 | 0 |
| [p186 C1](#p186-c1) | 182 | 89 / 91 | 0 | 0 |

## p186 B2

**Source transcription — header:** `B) NKJ v LP (06.23 a.m., November 13th); FUER WAU 07.00 2 TLE; 2 TL RICHI-242`

**Readable German** — based on the unchanged raw output.

> Die Schwierigkeiten, dass Mannschaften eigenmaechtig nach Hause fahren wollen, sind ueberall die gleichen. OHL. RM 1A Nr. 11?01 Geh. Op.

**Meaning:** The second part states that the difficulty is the same everywhere: soldiers want to travel home on their own authority. It closes with OHL and an unresolved office reference. It reports the problem; it does not itself authorize those departures.

<details>
<summary>Raw decoded text</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
DIESCHWIERIGKEITENXDASSMANNSCHAFTENEIGENMAECHTIGNACHHAUSEFAHRENWOLLENXSINDUEBERALLDIEGLEICHENXOHLXRMX1AXNRX11?01XGEHXOPXX
```

</details>

**Unresolved details and editorial limits.**

- All 242 printed coordinates are preserved and decode without repairs. The earlier OCR separated the first row and omitted additional source material; those OCR defects are not historical ciphertext losses.
- The heading explicitly identifies this as part 2. The independently handled first part has two group-width obliterations and a conditional exclusion model; this native part does not rely on that model.
- The literal reference 11?01 retains one globally coupled unknown square cell. No historical file number or date is inferred.
- The unknown in 11?01 is the same GA square cell as the first unknown in p186 C1's DRTRM1A?5?; both must have the same unresolved label. The second unknown in that C1 field is AF and must have a different label.

## p186 C1

**Source transcription — header:** `C) KOW v LP (06.26 a.m., November 13th); 17.40 (13/11) 2 TLE; 1 TL RICHI-182; (Continued)`

**Readable German** — based on the unchanged raw output.

> Zu DRTRM1A?5?. ABTRSPRT z. Zt. wegen unklarer Lage in Ostsee UNMOGLCH. Gen. Graf Goltz hat jedoch VORBEREITG

**Meaning:** This first part concerns transport that is currently described as impossible because the situation in the Baltic Sea is unclear. It then begins a statement about preparations associated with the literal name and title GEN GRAF GOLTZ. The statement is incomplete in this source body, so no completed plan or action is supplied.

<details>
<summary>Raw decoded text</summary>

**Raw output** — every native source slot in printed order, under the stated published key.

```text
ZUDRTRM1A?5?XABTRSPRTXZXZTWEGENUNKLARERLAGEINOSTSEEUNMOGLCHXGENGRAFGOLTZHATJEDOCHVORBEREITG
```

</details>

**Unresolved details and editorial limits.**

- All 182 coordinates are preserved; no source substitution or mask fill is needed. The scan labels two parts and prints “Continued,” but only this first body is included here. No missing continuation is reconstructed from context.
- DRTRM1A?5?, ABTRSPRT, UNMOGLCH and VORBEREITG are retained literally. The English meaning interprets the abbreviated transport statement; no missing I, vowel or grammatical ending is added to the decoded stream.
- The two question marks in the opening reference come from different unresolved square cells; their labels remain globally injective rather than being independently guessed.
- The literal name GRAF GOLTZ is not used to add a first name or identify a historical biography.

## Evidence and credit

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates replay every coordinate alteration, compare the independent column/domain reconstruction with the cipher implementation, and re-encrypt every complete edited output. For a partial output, an injective global completion of the square and residual source masks supplies an explicitly nonhistorical roundtrip witness. Each readable passage preserves every nonseparator output label; literal protected fields are also checked without removing their internal separators. Source crops are bound to the original PDF by page, rectangle, scale, file digest and RGB-pixel digest.

Reproduce with `python experiments/home_departures_baltic_transport/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to regenerate and compare the delivered source pixels.

A roundtrip proves compatibility with a stated reading. Editorial spelling repairs remain proposals, and literal number labels are not automatically historical dates, quantities or reference numbers.
