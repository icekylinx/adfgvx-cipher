# Hermannstadt radio setup and a request for armistice clarification

Prepared by **icekylinx and GPT-6 Astra Pro**.

This edition recovers the four source-defined parts of Childs p216 A. The origin header is `VON UKS 2245 (24/11) 4 TLE`; the receiving header is 06.38 p.m. on 25 November. The page heading says 24 November 1918. All dates and raw numerical labels are retained. The adjacent financial request p216 B is a separate message.

The report says that a radio station was established close to Hermannstadt, with construction delayed by railway authorities. It describes unsuccessful or intermittent communication, unsuccessful attempts through Budapest, Vienna and Munich, and eventual reception through Breslau. It then asks for repetitions of missing messages, an assessment of the situation, and an interpretation of the armistice for OKM.

Lasry and coauthors already discuss the loss of the Nikolajev relay and communication through Breslau in section 6.3 (author-PDF page 21), citing p224 A for a later request for good radio operators. This edition does not claim discovery of that broad historical narrative. Its contribution is the exact four-part p216 source assembly, raw readings, source-coordinate repair costs, and uncertainty record.

## Part 1: construction near Hermannstadt

Raw:

```text
ANOHLXXFUNK6NSTATXUNMITTELBARBEIHERMANNSTADTAUFGEBAUTXNACHDEMAUFBAUXDERDURCHSCHWIERIGKEITENDERBAHNBEHOERDENSEHRVERLANGSAMTX
```

One observed-coordinate change, source 56 G→F, gives the ordinary-word candidate:

```text
ANOHLXXFUNKENSTATXUNMITTELBARBEIHERMANNSTADTAUFGEBAUTXNACHDEMAUFBAUXDERDURCHSCHWIERIGKEITENDERBAHNBEHOERDENSEHRVERLANGSAMTX
```

The printed 246 coordinates match the advertised length. `FUNKENSTAT` remains an abbreviation; missing letters are not supplied.

## Part 2: unsuccessful or intermittent reception

Raw:

```text
AMYQXBEENDETXWARVERSTAENTIGUN6NICHTMOEGLICHXDANIKOLA3EWGARTICHTUNDWUSTERHAUSENNURREITWEISEAUZNAHMENXVERSUCHEUEBERBUDAPEST
```

Six observed-coordinate substitutions yield:

```text
AMYQXBEENDETXWARVERSTAENDIGUNGNICHTMOEGLICHXDANIKOLA3EWGARNICHTUNDWUSTERHAUSENNURZEITWEISEAUFNAHMENXVERSUCHEUEBERBUDAPEST
```

The 242 printed coordinates match the advertised length. The repairs concern `VERSTAENDIGUNG`, `GARNICHT`, `ZEITWEISE` and `AUFNAHMEN`. The date field `AMYQ` and the name-like field **NIKOLA3EW** are unchanged.

### The name is adverse evidence for automatic normalization

At plaintext position 52, raw 3 comes from pair **FD**, source indices **26=`F`, 180=`D`**. All eighteen coordinates of `NIKOLA3EW` are directly observed and unchanged by the candidate.

The separate optional Nov22 hypothesis assigns J to **GD**, not FD. It therefore does not turn this field into `NIKOLAJEW`. In an injective square, if GD already holds J, FD cannot also hold J. A same-spelling reading here would need an additional source/copying assumption: changing source 26 F to G would change FD to GD. That possible one-coordinate repair is calculated but **not applied**. A familiar name is not used to conceal this discrepancy.

## Part 3: Breslau reception and missing messages

With the conditional deletion described below, raw text is:

```text
WIENMUENCHEQKRFOLGLOSXERSTSEITBRESLAUAUFNIMMTXJ7XYYXVERBINDUNGGESICHERTXDORTXOUNKSPRUECUERMYANRYY837XYY3J7NJCHTEINGEGANGEN
```

Five observed-coordinate substitutions give:

```text
WIENMUENCHENERFOLGLOSXERSTSEITBRESLAUAUFNIMMTXJ7XYYXVERBINDUNGGESICHERTXDORTXFUNKSPRUECHERMYANRYY837XYY3J7NICHTEINGEGANGEN
```

The date/reference sequences `J7XYY` and `RMYANRYY837XYY3J7` remain raw. No message number, date or office prefix is expanded from plausibility.

The page advertises 244 coordinates but prints 245, including the six-letter group `VFAFDV`. Deleting source index 56, its second glyph F, gives the five-letter group `VAFDV`. Among **all 245 single-coordinate deletions**, this is the unique minimum for the declared candidate, at five observed-coordinate substitutions. Every trial's cost is retained. The result is a conditional language fit, not an independently attested original plaintext.

## Part 4: repeat the situation and armistice instructions

Raw:

```text
ERBITTENWIEDERHOLUNGBEURTEILUNGDERLAGEBESONDERSAUSLEGUNGDESWAFFENSTILLSTANDESFU?ROKMXXOKMYAYY7Y1OPX
```

The candidate fills the printed dash for `FUER`, with no observed-coordinate substitutions:

```text
ERBITTENWIEDERHOLUNGBEURTEILUNGDERLAGEBESONDERSAUSLEGUNGDESWAFFENSTILLSTANDESFUEROKMXXOKMYAYY7Y1OPX
```

Here 199 slots are printed against the advertised 198, including `XXVGGD`. All **199 single-coordinate deletions** are evaluated. Three adjacent X positions—source indices **34, 35 and 36**—tie at zero observed-coordinate substitutions. They produce identical corrected ciphertext but different source ownership maps. Two Xs are in the six-letter group; the third is the last glyph of the preceding group `GDAAX`. All three maps are retained; presentation uses index 35, the first glyph inside the overlong group. The printed dash is source 197 and is filled only for `FUER`.

## Totals and reproduction

| Quantity | Four physical parts |
| --- | ---: |
| Printed source slots | 932 |
| Valid printed coordinates | 931 |
| Modeled coordinates | 930 |
| Plaintext positions | 465 |
| Raw fixed positions | 464 |
| Candidate fixed positions | 465 |
| Observed-coordinate substitutions | 12 |
| Printed-dash fills | 1 |
| Source-coordinate deletions | 2 |

The full 465-position candidate remains a diplomatic cryptanalytic reading with raw dates, references and `NIKOLA3EW`. Fixed substitution labels are not equivalent to confirmed historical numerals or names.

The earlier OCR screen partially recognized the fourth part. The exact source separates the parts correctly, restores omitted trailing groups, and retains the two overlong groups instead of silently reshaping them. Prior caches and their hashes are frozen in [inputs.json](inputs.json). Bounded checks of the paper, dissertation and comments do not establish historical priority.

```bash
python experiments/hermannstadt_radio_report/verify.py --verify
python experiments/hermannstadt_radio_report/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command uses the standard library and repository cipher code. It independently checks column offsets, domains, source mappings, every deletion trial, repair coordinates and re-encryption. The optional PDF check additionally uses PyMuPDF and Pillow to compare the full PDF hash and crop pixels. See [certificates.json](certificates.json), [catalog_proposal.json](catalog_proposal.json), and the [reading page](../../cases/pages/216.md#edition-cases-radio-hermannstadt-radio-report).
