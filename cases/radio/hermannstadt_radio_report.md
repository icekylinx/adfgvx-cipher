# Hermannstadt radio station and armistice instructions

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

Prepared by **icekylinx and GPT-6 Astra Pro**.

Childs p216 A is explicitly a four-part report. Its origin is 2245 on 24 November 1918; the receiving header is 06.38 p.m. on 25 November. The published Nov22–24 key is unchanged.

It reports construction of a radio station near Hermannstadt, railway difficulties, unsuccessful or intermittent communications, and eventual reception through Breslau. The final part requests repeated messages, a situation assessment, and an interpretation of the armistice. Lasry and coauthors already describe the broad Nikolajev/Breslau communication problem in section 6.3; this page adds the source-specific transcript, exact repairs and uncertainty record.

## p216 A1

Radio station construction near Hermannstadt.

**Raw output:**

```text
ANOHLXXFUNK6NSTATXUNMITTELBARBEIHERMANNSTADTAUFGEBAUTXNACHDEMAUFBAUXDERDURCHSCHWIERIGKEITENDERBAHNBEHOERDENSEHRVERLANGSAMTX
```

**Edited output:**

```text
ANOHLXXFUNKENSTATXUNMITTELBARBEIHERMANNSTADTAUFGEBAUTXNACHDEMAUFBAUXDERDURCHSCHWIERIGKEITENDERBAHNBEHOERDENSEHRVERLANGSAMTX
```

One observed-coordinate substitution; no length change.

## p216 A2

Reception difficulties and raw NIKOLA3EW.

**Raw output:**

```text
AMYQXBEENDETXWARVERSTAENTIGUN6NICHTMOEGLICHXDANIKOLA3EWGARTICHTUNDWUSTERHAUSENNURREITWEISEAUZNAHMENXVERSUCHEUEBERBUDAPEST
```

**Edited output:**

```text
AMYQXBEENDETXWARVERSTAENDIGUNGNICHTMOEGLICHXDANIKOLA3EWGARNICHTUNDWUSTERHAUSENNURZEITWEISEAUFNAHMENXVERSUCHEUEBERBUDAPEST
```

Six observed-coordinate substitutions. **NIKOLA3EW and AMYQ are unchanged.** Raw 3 is FD at source positions 26 and 180. Assigning J to GD elsewhere does not fix this occurrence; a same-spelling reading would require an additional copying/source assumption, which is not applied.

## p216 A3

Breslau reception and missing message references.

**Raw output — conditional deletion of source 56 F from the six-coordinate group:**

```text
WIENMUENCHEQKRFOLGLOSXERSTSEITBRESLAUAUFNIMMTXJ7XYYXVERBINDUNGGESICHERTXDORTXOUNKSPRUECUERMYANRYY837XYY3J7NJCHTEINGEGANGEN
```

**Edited output — same conditional deletion model, followed by five word repairs:**

```text
WIENMUENCHENERFOLGLOSXERSTSEITBRESLAUAUFNIMMTXJ7XYYXVERBINDUNGGESICHERTXDORTXFUNKSPRUECHERMYANRYY837XYY3J7NICHTEINGEGANGEN
```

The source prints 245 coordinates against 244 advertised, with six-letter VFAFDV. Deleting source 56 F is the unique minimum among all 245 single-coordinate deletions, followed by five ordinary-word coordinate repairs. Every date/reference label is retained. The minimum is conditional on the explicit candidate.

## p216 A4

Request to repeat situation and armistice instructions.

**Raw output — conditional deletion of one source X at 34, 35 or 36; aliases retained:**

```text
ERBITTENWIEDERHOLUNGBEURTEILUNGDERLAGEBESONDERSAUSLEGUNGDESWAFFENSTILLSTANDESFU?ROKMXXOKMYAYY7Y1OPX
```

**Edited output — same conditional deletion model, with one printed-dash fill:**

```text
ERBITTENWIEDERHOLUNGBEURTEILUNGDERLAGEBESONDERSAUSLEGUNGDESWAFFENSTILLSTANDESFUEROKMXXOKMYAYY7Y1OPX
```

The source prints 199 slots against 198 advertised. Deleting any one of three adjacent Xs at source 34, 35 or 36 produces the same ciphertext. All three source maps are retained. One printed dash is filled for FUER; no observed coordinate is substituted.

## Evidence

The edition contains 465 plaintext positions, 12 observed-coordinate substitutions, one printed-dash fill and two conditional source-coordinate deletions. The source-defined four-part assembly does not include the adjacent cash request. Fixed raw labels do not certify historical numbers or names.

[Source inputs and attribution](../../experiments/hermannstadt_radio_report/inputs.json), [exact certificates](../../experiments/hermannstadt_radio_report/certificates.json), and [complete method and verification instructions](../../experiments/hermannstadt_radio_report/README.md).
