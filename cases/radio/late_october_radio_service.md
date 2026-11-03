# Late October radio service — calls, garbled traffic and network routing

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[All cases](../README.md) · [ADFGVX Cipher](../../README.md)

**Source edition and review: icekylinx and GPT-6 Astra Pro.** Five physical
records on pp. 74–75 describe daily calls, a garbled CHI telegram, and questions
about message routing between radio stations and the German wire network.
The five typed frames contain 756 slots. Their unchanged-key outputs fix
348 of 378 plaintext positions. The proposed readings use five observed-
coordinate substitutions and 30 printed-dash fills; all 30 fills belong to
p74 C1 and remain an explicitly conditional reconstruction.

The three routing parts are printed as p74 C1/C2 and p75 A3. The change of
section letter is retained. The repeated recipient line, `1900 (28.10)`,
`3 TEILE`, numbered parts and page continuation support treating them as one
three-part source sequence.

## p74 A

**Daily calls from Deutsch-Altenburg.**

[Source crop](../../experiments/late_october_radio_and_materials/sources/p74_A.png). `A) OSM, NKJ, COS v LP (3.50 p.m., October 28th)` | `1630` | `RIZI-154`.

The typed frame has **154 slots** and fixes **77 of 77 raw plaintext positions** under the unchanged published key.

**Raw output — typed source frame; no word repairs.**

```text
DEUTSIHALTENBURGXOHDXWIRDSIEVOMX29XABTAEGLICHUMX1120XMXEXZXWELLEX5200XANRUFEN
```

**Edited output — only the coordinate changes recorded below.**

```text
DEUTSCHALTENBURGXOHDXWIRDSIEVOMX29XABTAEGLICHUMX1120XMXEXZXWELLEX5200XANRUFEN
```

**Readable German — with the one recorded word repair:**

> Deutsch-Altenburg, OHD, wird Sie vom 29. ab taeglich um 11:20 M. E. Z., Welle 5200, anrufen.

The printed source has `RIZI-154`. The repair changes `DEUTSIH` to
`DEUTSCH`; it does not assign the station code or any numeral. The time colon,
hyphen and punctuation are display formatting. `OHD`, `29`, `1120` and `5200`
are unchanged literal labels under the published full square. The ciphertext
does not print a wavelength unit, so this edition does not add one.

| Typed source index, zero based | Printed | Proposed | Plaintext effect |
|---:|---|---|---|
| 85 | `A` | `G` | Position 5: `I` → `C` |

The total is **1 observed-coordinate substitutions and 0 printed-dash fills**. No key cell or rank changes.

## p74 B

**Repeat the garbled parts of a CHI telegram.**

[Source crop](../../experiments/late_october_radio_and_materials/sources/p74_B.png). `B) NKJ v LP (6.10 a.m., October 29th)` | `FUER COS 2200 (28.10)` | `RICHI-170`.

The typed frame has **170 slots** and fixes **85 of 85 raw plaintext positions** under the unchanged published key.

**Raw output — typed source frame; no word repairs.**

```text
KAUKASUSDELEGAXSPRUCHTLGRLEITSTX639XOSKACHIX212GR3TLVERSTX2U3TLWHXNACHCHEFRM5X15031UX
```

**Readable German — abbreviations retained or explicitly expanded:**

> Kaukasus-Delega[tion]: Spruch Tlgr.-Leitst. 639, OSKA, CHI, 212 Gr., 3 Tl., verst[ümmelt]. 2 u[nd] 3 Tl. w[ieder]h[olen]. Nach[richten]chef RM 5, 15031 U.

The brackets are proposed expansions of telegram shorthand, not supplied
ciphertext. The message refers to a three-part CHI telegram as garbled and
requests repetition of its second and third parts. `OSKA` and the reference
fields remain unexpanded. The word `CHI` belongs to the decoded report;
this physical record is headed `RICHI-170` and uses the ordinary period key.

No observed-coordinate substitutions or erased-coordinate fills are needed.

## p74 C1

**First routing part with six erased groups.**

[Source crop](../../experiments/late_october_radio_and_materials/sources/p74_C1.png). `C) FUER CVS, TAGANROG, POT (ASO) v LP (6.15 a.m., October 29th)` | `1900 (28.10) 3 TEILE` | `1 TL RICHI-148`.

The typed frame has **148 slots** and fixes **44 of 74 raw plaintext positions** under the unchanged published key.

**Raw output — typed source frame; no word repairs.**

```text
ZUR?G???FTVE?K???SHAN?E???CHIF?E???EIST?T???LLEA?D???SCHESD???NETZAG???HLX
```

**Edited output — conditional supplied reading of the printed erasures.**

```text
ZUREGELNFTVERKEHRSHANDELSSCHIFFEXWIEISTFTSTELLEANDEUTSCHESDRHTNETZAGESCHLX
```

**Conditional interpretation:** The source begins with six printed
five-dash groups, exactly 30 erased coordinate slots. The full edited string
is one ordinary-language fill candidate consistent with every observed
coordinate. The 44 fixed raw labels and all partial-cell domains are preserved
in the certificate. This is not a uniqueness result for the missing wording.

The candidate opening `ZUREGELNFTVERKEHRSHANDELSSCHIFFE` is retained literally.
This edition does not choose a grammatical expansion for its `S` or silently
rewrite the phrase. The following readable excerpt begins at the next
sentence; only that already displayed opening is omitted from the excerpt.

**Readable German — excerpt of the conditional fill candidate:**

> Wie ist FT-Stelle an deutsches Dr[a]htnetz a[n]geschl[ossen]?

The bracketed letters are prose expansions of the edited abbreviations
`DRHTNETZ` and `AGESCHL`; they do not add decoded positions. The question asks
how the FT station is connected to the German wire network. Its appearance
inside the three-part routing sequence supports this reading, but does not
turn the 30 missing source coordinates into observations.

There are **30 printed-dash fills**, listed individually with their original row, group, source index and plaintext effect in the certificate. The total is **0 observed-coordinate substitutions and 30 printed-dash fills**. No key cell or rank changes.

## p74 C2

**Lines used to exchange foreign-station telegrams.**

[Source crop](../../experiments/late_october_radio_and_materials/sources/p74_C2.png). `Continuation of p74 C, 1900 (28.10) 3 TEILE` | `2 TL RICHI-130`.

The typed frame has **130 slots** and fixes **65 of 65 raw plaintext positions** under the unchanged published key.

**Raw output — typed source frame; no word repairs.**

```text
AUFWELCHENLTGNERFLGTAUSTAUSCH5ERTELGRMHTFREMDLAENDSCHENSTATIONENX
```

**Edited output — only the coordinate changes recorded below.**

```text
AUFWELCHENLTGNERFLGTAUSTAUSCHDERTELGRMITFREMDLAENDSCHENSTATIONENX
```

**Readable German — with the two priced repairs and marked expansions:**

> Auf welchen Ltgn [Leitungen] erf[o]lgt Austausch der Telgr. [Telegramme] mit fremdlaend[i]schen Stationen?

The bracketed full words expand the literal abbreviations `LTGN` and
`TELGR`; `[o]` and `[i]` are prose spelling completions of `ERFLGT` and
`FREMDLAENDSCHEN`. They are not extra decoded letters. The two coordinate
repairs instead change raw `5ER` to `DER` and raw `MHT` to `MIT`.
The raw numeral label `5` is retained in the raw block and is priced as a
word repair; no numerical field or key-square digit is reassigned.

| Typed source index, zero based | Printed | Proposed | Plaintext effect |
|---:|---|---|---|
| 46 | `D` | `V` | Position 29: `5` → `D` |
| 47 | `A` | `D` | Position 38: `H` → `I` |

The total is **2 observed-coordinate substitutions and 0 printed-dash fills**. No key cell or rank changes.

## p75 A3

**Via the German station or a separate line.**

[Source crop](../../experiments/late_october_radio_and_materials/sources/p75_A3.png). `A) FUER CVS, TAGANROG, POT (ASO) v LP (6.15 a.m., October 29th)` | `1900 (28.10) 3 TEILE` | `3 TL RICHI-154`.

The typed frame has **154 slots** and fixes **77 of 77 raw plaintext positions** under the unchanged published key.

**Raw output — typed source frame; no word repairs.**

```text
DURCHVERMITTLGDERDEUTSSCHENSTATIONOZUEAERRBESONDLTGNUWOHINXNACHCHEF3AX110701X
```

**Edited output — only the coordinate changes recorded below.**

```text
DURCHVERMITTLGDERDEUTSSCHENSTATIONODUEBERRBESONDLTGNUWOHINXNACHCHEF3AX110701X
```

**Readable German — spelling peculiarities retained:**

> Durch Vermittlg [Vermittlung] der deutsschen Station od[er] ueberr besond[ere] Ltgn [Leitungen], u[nd] wohin? Nach[richten]chef 3 A, 110701.

The doubled `S` in `DEUTSSCHEN` and doubled `R` in `UEBERR` are present in
both raw and edited streams and are deliberately retained here. The brackets
expand abbreviations only. The message asks whether routing is through the
German station or separate lines, and where those lines lead. The two priced
repairs are `OZ` → `OD` and `UEAERR` → `UEBERR`; the `3A` and `110701` fields
remain unchanged.

| Typed source index, zero based | Printed | Proposed | Plaintext effect |
|---:|---|---|---|
| 55 | `V` | `F` | Position 38: `A` → `B` |
| 72 | `X` | `V` | Position 35: `Z` → `D` |

The total is **2 observed-coordinate substitutions and 0 printed-dash fills**. No key cell or rank changes.

## Evidence, verification and credit

The [literal inputs](../../experiments/late_october_radio_and_materials/inputs.json),
[coordinate certificates](../../experiments/late_october_radio_and_materials/certificates.json)
and [source images](../../experiments/late_october_radio_and_materials/README.md)
preserve the complete source, unchanged published key, raw outputs and every
proposed repair. The source is J. Rives Childs, *General Solution of the ADFGVX
Cipher System*, printed pp. 74–76 / PDF pp. 77–79. Its page heading is
28 October 1918; the printed reception times include 29 October and are not
silently reconciled.

The October 28–31 key is prior work credited to George Lasry and colleagues.
The [prior-evidence snapshot](../../experiments/late_october_radio_and_materials/prior_evidence.json)
retains the earlier unreviewed repository OCR candidates, including mostly
readable p74 A/B and p75 A3. The present contribution is the source edition,
additional complete bodies, explicit source-layer separation and reproducible
repair ledger by **icekylinx and GPT-6 Astra Pro**. No first-historical-
decipherment priority is claimed.

```sh
python3 experiments/late_october_radio_and_materials/verify.py --verify
python3 experiments/late_october_radio_and_materials/verify.py --verify --pdf /path/to/childs.pdf
```
