# November 7–8: embassy, legation and Etappe address parts

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

Source review and editorial work: **icekylinx and GPT-6 Astra Pro**. Published Nov7–9 key: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker; unchanged here. The earlier repository OCR and explicitly recomputed unchanged-key outputs are retained. No universal first-decipherment priority is asserted.


**Reviewed source crops:** [p156_reviewed.png](../../experiments/nov7_8_embassy_address_parts/sources/p156_reviewed.png) · [p158_reviewed.png](../../experiments/nov7_8_embassy_address_parts/sources/p158_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Scope and evidence

Seven physical first/address parts on printed pp156 and 158 contain embassy,
legation or Etappe addresses and signatures. They are not seven recovered
substantive message bodies. Most headings announce additional parts that are
absent from the relevant section; the two printed p158 A parts themselves
both contain address/signature language.

The source edition has **568 native coordinate slots and 284 plaintext
positions**. Under the primary p156 A1 overstrike reading, all 284 positions
are fixed directly by the published key. Eleven observed-coordinate
substitutions produce the displayed ordinary-word proposals. There are no
insertions, exclusions, reorderings, source-mask fills or key changes. The
retained alternative p156 A1 glyph changes one raw letter and raises that
record's proposal cost from two substitutions to three.

| Record | Native slots | Raw fixed positions | Observed substitutions | Source fills |
|---|---:|---:|---:|---:|
| p156_A1 | 84 | 42/42 | 2 | 0 |
| p156_B1 | 80 | 40/40 | 0 | 0 |
| p156_D1 | 44 | 22/22 | 1 | 0 |
| p156_E1 | 78 | 39/39 | 0 | 0 |
| p158_A1 | 100 | 50/50 | 4 | 0 |
| p158_A2 | 106 | 53/53 | 2 | 0 |
| p158_B1 | 76 | 38/38 | 2 | 0 |

The three p162 D1 source masks receive independent character support from
these address witnesses; conversely, p162 D1's raw output supports all four
p158 A1 and both p158 A2 ordinary-word repairs. This is evidence for the
shared address formula, with different headers retained. It does not
establish identical missing payloads or a historical copying mechanism.

## p156 A1

**German embassy address with Bussche signature.**

**Literal header:** `A) YZ v LP (6.11 a.m., November 8th); FUER YZ 2200 (7/11) [2/3] TLE; 1 TL RICHI-84`

**Raw output:**

```text
DERTSCHEXBOTSCHAFTXKSNSTANTIOPELXXBUSSCHEX
```

**Edited output — 2 observed-coordinate substitutions:**

```text
DEUTSCHEXBOTSCHAFTXKONSTANTIOPELXXBUSSCHEX
```

**Readable German:**

> Deutsche Botschaft Konstantiopel. Bussche.

**Conditional interpretation:** An address to the German embassy and a Bussche signature. The transmitted place-name lacks the second N of Konstantinopel and is preserved as Konstantiopel.

The two proposed ordinary-word repairs change DERTSCHE to DEUTSCHE and KSNSTANTIOPEL to KONSTANTIOPEL. The missing N is not inserted into the plaintext or the source.

The overstruck second character in the third group of source row 2 is transcribed X in the primary VXXVX reading. A V alternative, VVXVX, is retained independently; the alternative changes the raw H in DERTSCHE to X and does not establish a different historical message.

The faint part-count digit admits 2/3 readings. The header display uses editorial brackets to retain both alternatives; only the first part is printed in this section. The advertised 84-coordinate body length is clear and does not depend on that header digit. The Bussche signature is not expanded to a named historical person.

All indices below are zero-based. The exact source remains unchanged in the raw layer.

| Source index | Printed | Edited |
|---:|:---:|:---:|
| 22 | D | F |
| 42 | D | V |

**Retained overstrike alternative:** `VVXVX` instead of primary `VXXVX`, changing source index 51 from X to V, gives:

**Raw output — retained V overstrike alternative:**

```text
DERTSCXEXBOTSCHAFTXKSNSTANTIOPELXXBUSSCHEX
```

The same readable proposal then costs **three observed substitutions**, including V→X at source index 51. The stronger German produced by the primary X reading is not treated as independent proof of that glyph. Both variants and their repair ledgers are verified.

## p156 B1

**German embassy at Constantinople and Stumm signature.**

**Literal header:** `B) YZ v LP (5.52 a.m., November 8th); 1835 (7/11) 2TLE; 1 TL RICHI-80`

**Raw output:**

```text
DEUTSCHEBOTSCHAFTKONSTANTINOPELXXSTUMMXX
```

**Edited output:** identical to raw; zero repairs.

**Readable German:**

> Deutsche Botschaft Konstantinopel. Stumm.

**Conditional interpretation:** A directly readable embassy address and Stumm signature, with its advertised second part absent from this section.

All 80 source coordinates directly decrypt. The source time is 1835, not the earlier OCR 1838.

The first printed part is a complete address and signature field, not a recovered substantive telegram body.

## p156 D1

**Etappe address at Constantinople.**

**Literal header:** `D) YZ v LP (6.21 a.m., November 8th); FUER YZ 0127 2 TLE; 1 TL RICHI-44`

**Raw output:**

```text
ETAPPEXKHNSTANTINOPELX
```

**Edited output — 1 observed-coordinate substitution:**

```text
ETAPPEXKONSTANTINOPELX
```

**Readable German:**

> Etappe Konstantinopel.

**Conditional interpretation:** A short Etappe address at Constantinople. The missing continuation is not supplied.

The native final XDVA is visible below the first source row and restores the advertised 44-coordinate frame without inserting anything into the source.

One observed-coordinate substitution changes raw KHNSTANTINOPEL to KONSTANTINOPEL. ETAPPE remains the literal transmitted designation.

All indices below are zero-based. The exact source remains unchanged in the raw layer.

| Source index | Printed | Edited |
|---:|:---:|:---:|
| 42 | V | F |

## p156 E1

**French-language German legation address at Constantinople.**

**Literal header:** `E) YZ v LP (6.15 a.m., November 8th); FUER YZ 2330 (8/11) 2 TLE; 1 TL RICHI-78`

**Raw output:**

```text
FUERXLEGATIONXALLEMANDEXKONSTANTINOPELX
```

**Edited output:** identical to raw; zero repairs.

**Readable German:**

> Fuer Legation Allemande Konstantinopel.

**Conditional interpretation:** An address for the German legation at Constantinople; the transmitted designation Legation Allemande is French and is retained as printed in the decoded text.

All 78 source coordinates directly decrypt, including the final three-coordinate AGV.

The heading literally combines a 6.15 a.m. reception on November 8 with 2330 (8/11); the edition does not silently reconcile that chronology.

Only the first of two advertised parts is visible in this section.

## p158 A1

**German embassy address and Stumm signature, first printed part.**

**Literal header:** `A) YZ v LP (05.05 p.m., November 8th); 1331 (7/11) 2 TTLE; 1 TL RICHI-100`

**Raw output:**

```text
DEUTSCHEBOTSAHAFTKONSTCNTINOPELXDNTERSCHRIOTSTUMMX
```

**Edited output — 4 observed-coordinate substitutions:**

```text
DEUTSCHEBOTSCHAFTKONSTANTINOPELXUNTERSCHRIFTSTUMMX
```

**Readable German:**

> Deutsche Botschaft Konstantinopel. Unterschrift Stumm.

**Conditional interpretation:** An embassy address with an explicit Stumm signature label. Four raw letter errors are repaired at their full coordinate cost.

The source supplies 100 native coordinates; the earlier OCR lost one, so its odd-length output is not used as the physical frame.

The raw BOTSAHAFT, KONSTCNTINOPEL, DNTERSCHRIOT letter errors are not source-transcription changes: the literal source remains fixed and all proposed replacements are priced in the edited layer.

The two printed A parts both contain address/signature language. Their headings are retained without inventing a distinct substantive payload.

All indices below are zero-based. The exact source remains unchanged in the raw layer.

| Source index | Printed | Edited |
|---:|:---:|:---:|
| 1 | X | F |
| 2 | F | X |
| 3 | X | A |
| 4 | F | X |

## p158 A2

**Repeated embassy address with literal UPK3 prefix.**

**Literal header:** `2 TL RICHI-106; following control: LP`

**Raw output:**

```text
UPK3DEWTSCHEBOTSCHAATKONSTANTINOPELXUNTERSCHRIFTSTUMM
```

**Edited output — 2 observed-coordinate substitutions:**

```text
UPK3DEUTSCHEBOTSCHAFTKONSTANTINOPELXUNTERSCHRIFTSTUMM
```

**Readable German:**

> UPK3. Deutsche Botschaft Konstantinopel. Unterschrift Stumm.

**Conditional interpretation:** The second printed part repeats the embassy address and Stumm signature, preceded by the unresolved literal field UPK3. Its purpose is not inferred.

The first row repeats GDDGV in adjacent five-coordinate groups. Both are retained in the full native 106-slot frame; visible repetition is not a license to remove a group.

The raw DEWTSCHE and BOTSCHAAT are ordinary-word repair proposals with explicit coordinate costs. UPK3 is retained unchanged and is not expanded as a unit, station or reference.

The final D is part of the encrypted body; the following LP is a source control.

All indices below are zero-based. The exact source remains unchanged in the raw layer.

| Source index | Printed | Edited |
|---:|:---:|:---:|
| 17 | D | X |
| 65 | X | V |

## p158 B1

**German embassy address with an explicit Stumm signature.**

**Literal header:** `B) YZ v LP (05.15 p.m., November 8th); FUER YZ 1325 (7/11) 2 TEILE; 1 TL RICHI-76; following control: LP`

**Raw output:**

```text
DNDEUTSCHEBOTSCHAFVUNTERSCHRIFTXSTUMMX
```

**Edited output — 2 observed-coordinate substitutions:**

```text
ANDEUTSCHEBOTSCHAFTUNTERSCHRIFTXSTUMMX
```

**Readable German:**

> An deutsche Botschaft. Unterschrift Stumm.

**Conditional interpretation:** A separate embassy address and signature part; it does not itself name the embassy city.

The visible final G completes the native 76-coordinate frame; the following LP is excluded as source control.

The raw DN and BOTSCHAFV become AN and BOTSCHAFT through two explicitly priced observed-coordinate substitutions.

The second of two advertised parts is absent from this section. The adjacent Constantinople addresses do not license inserting that city into this record.

All indices below are zero-based. The exact source remains unchanged in the raw layer.

| Source index | Printed | Edited |
|---:|:---:|:---:|
| 36 | A | V |
| 42 | V | D |

## Independent address witness on p162

The earlier [p162 D1 edition](../people/constantinople_embassy_signature.md)
preserves three C-like source glyphs as masks. Its independently recomputed
raw output is:

**Raw output — independently recomputed p162 D1 witness:**

```text
DEUTSCHEBOTSCHAFTKONSTA??INOPELXUNTERSCHRIF?STUMMX
```

Its literal header is `D) XYZ v LP (06.12 a.m., November 10th); 1330 (8/13)
2 TEILE; 1 TL RICHI-100`. The unusual `8/13` field remains literal. This
differs from p158 A's `1331 (7/11)` header.

| Comparison | Aligned plaintext positions | Agreeing known labels | Disagreeing known labels | p162 unknowns supported by new raw labels | New repairs supported by p162 raw labels |
|---|---:|---:|---:|---:|---:|
| p158 A1 from position 0 / p162 D1 from position 0 | 50 | 43 | 4 | 3 | 4 |
| p158 A2 from position 4 / p162 D1 from position 0 | 49 | 44 | 2 | 3 | 2 |

The p158 A2 offset skips only its literal `UPK3` prefix. The comparison
neither deletes that prefix nor changes its numerical label. The final
separator that is present in p162 D1 and absent from p158 A2 is outside the
49-position comparison. Every agreeing, disagreeing and mask-supporting
position is listed with its coordinate pair in the certificate. The p162
record is a previously reviewed witness and is not added to this package's
physical-record count.

## Reproduction and credit

[Inputs](../../experiments/nov7_8_embassy_address_parts/inputs.json) preserve
all literal rows, headers, competing overstrike readings, proposals,
published-key provenance and source-image bindings. The
[certificate](../../experiments/nov7_8_embassy_address_parts/certificates.json)
recomputes raw domains, every repair cost, complete readable-label
preservation, exact re-encryption and the independent p162 comparisons.
The existing p162 source record and crop are bound by hashes. A complete
square witness demonstrates consistency only; it is not a recovered
historical digit assignment.

The [package README](../../experiments/nov7_8_embassy_address_parts/README.md)
gives the portable verification commands, including exact RGB pixel
regeneration of the two new crops and the existing p162 crop from the
pinned PDF. The [earlier address-part edition](constantinople_address_parts.md)
and [p167 embassy address](../finance/nov9_crown_airlift_and_embassy.md#p167-e1)
provide additional separately received address context; neither supplies
missing substantive text for these records.
