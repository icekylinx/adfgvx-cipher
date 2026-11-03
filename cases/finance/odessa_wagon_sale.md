# Odessa consular routing and a Magdeburg wagon-sale instruction

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

Two native parts give the consular and export-company routing of an instruction involving the sale of a railway wagon. The primary edition retains the opaque DAMM LADWIG phrase and all incomplete references. More fluent cargo-word proposals are priced separately rather than silently treated as source wording.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p201 excerpt](../../experiments/odessa_wagon_sale/sources/p201_reviewed.png) · [Inputs](../../experiments/odessa_wagon_sale/inputs.json) · [Position and change certificates](../../experiments/odessa_wagon_sale/certificates.json)

The published `Nov16-18` key is unchanged. [Original OCR records](../../experiments/odessa_wagon_sale/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/odessa_wagon_sale/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p201 A1](#p201-a1) | 254 | 124 / 127 | 0 | 0 |
| [p201 A2](#p201-a2) | 236 | 117 / 118 | 1 | 0 |

## p201 A1

**Source transcription — header:** `A) NKJ FUER RAT (6.50 a.m., November 16th); 0700 (16) 2 TLE; 1 TL RICHI-254`

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
DEUTSCHESGENERALKONSULATODESSAXNRX??XAUSSENUKRAANDEUTSCHEENBEVOLLMAECHTIGTENODESSAXFUERAUSFUHRGESELLSCHAFTXABTXRMX?IHRTELEGRAMM
```

**Readable German — exact nonseparator labels of the unchanged raw output:**

> Deutsches Generalkonsulat Odessa. Nr. ?? AUSSENUKRA. An DEUTSCHEEN Bevollmaechtigten Odessa. Fuer Ausfuhrgesellschaft. Abt. RM ? Ihr Telegramm

**Meaning:** The first part gives the German consulate at Odessa, an unresolved numbered reference, the Odessa representative and an export company as address or routing information. It then begins a reference to a previous telegram. The spelling DEUTSCHEEN and AUSSENUKRA are retained without silently normalizing them.

**Editorial limits.**

- All 254 coordinates are present in the printed source and decode without repair. The earlier OCR split the first row from the rest; the complete native body is now used.
- DEUTSCHEEN is retained with both E letters. AUSSENUKRA, ABT and RM remain unexpanded, and RM is not treated as a currency amount.
- The three question marks are different unresolved square cells FD, GF and GD. They cannot be assigned independently or given the same label under an injective completion. No reference number is inferred.

## p201 A2

**Source transcription — header:** `A) NKJ FUER RAT (6.50 a.m., November 16th); 0700 (16) 2 TLE; 2 TL RICHI-236`

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
?WEITAUSENDUNDACHTZIGERSUCHENWAGGONMAGDEBURGNEUNTAUSENDNEUNHUNDERTZEHNXDAMMXLADWIGBESTMOEGLICHSTZUVERKAUFENXAUSWAERTIG
```

**Edited output — 1 observed-coordinate substitution and 0 source-mask fills; no insertion, deletion or reordering:**

```text
ZWEITAUSENDUNDACHTZIGERSUCHENWAGGONMAGDEBURGNEUNTAUSENDNEUNHUNDERTZEHNXDAMMXLADWIGBESTMOEGLICHSTZUVERKAUFENXAUSWAERTIG
```

**Readable German — exact nonseparator labels of the edited output:**

> Zweitausendundachtzig. Ersuchen Waggon Magdeburg neuntausendneunhundertzehn. DAMM LADWIG bestmoeglichst zu verkaufen. Auswaertig.

**Meaning:** The continuation refers to the telegram with the spelled-out number zweitausendundachtzig and requests a sale on the best possible terms involving the wagon identified by Magdeburg and neuntausendneunhundertzehn. DAMM LADWIG remains opaque in the primary edition; it is not treated as a confirmed person, cargo description or instruction to sell the contents.

**Editorial limits.**

- The native 236-coordinate body is preserved. The initial unresolved square label is changed to Z in ZWEITAUSEND as one observed-coordinate substitution; this is not a free fill of an unknown square cell.
- Both long numbers remain spelled out exactly as recovered. No wagon identity is independently established from those words.
- The primary reading retains DAMM LADWIG. Conditional LADUNG, SAMT LADUNG and DANN LADUNG alternatives are separately priced, and none is silently substituted into the primary meaning.
- SAMT LADUNG and DANN LADUNG each require nine observed changes from the source, including the initial Z proposal; coordinate cost alone does not choose between them.

## Conditional interpretation: cargo wording

The primary reading leaves DAMM LADWIG unresolved. Replacing LADWIG with LADUNG would make a cargo reading possible, but costs four further observed-coordinate changes. The longer phrase SAMT LADUNG would suggest selling the wagon together with its load; DANN LADUNG is an equally costly alternative under the same coordinate metric. These are proposals, not independent source recoveries.

| Phrase retained or proposed | Total observed substitutions from the native source, including initial Z | Additional substitutions beyond the primary edition |
| --- | ---: | ---: |
| DAMM LADWIG — primary | 1 | 0 |
| DAMM LADUNG | 5 | 4 |
| SAMT LADUNG | 9 | 8 |
| DANN LADUNG | 9 | 8 |

All three conditional streams and their exact coordinate edits re-encrypt under the unchanged published key. Equal cost does not select the historical phrase. The edition therefore does not present the sale of the wagon’s contents as established. The spelled-out references remain the source’s words; neither consular routing nor a plausible commercial sentence identifies the particular wagon independently.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/odessa_wagon_sale/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
