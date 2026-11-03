# Citadel surrender, local armistice terms and home leave

**Source editions: icekylinx and GPT-6 Astra Pro.**

Four physical parts on Childs p179 concern surrender terms, a request for
the armistice conditions applicable to Mackensen's front, and postponement
of discharge and urgent home leave. The source's dates, abbreviated words,
unresolved reference fields and unusual year form are preserved separately
from the ordinary-word repairs.

The source is Childs, *General Solution of the ADFGVX Cipher System*,
[printed p179, PDF p182](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The adjacent A record is a separate
[radio-equipment transfer order](../radio/right_rhine_equipment.md).

## B: abandon resistance and determine surrender terms

The [158-coordinate telegram](../../experiments/november_armistice_orders/sources/p179_B.png)
has `WAU v LP (15.50, November 11th); KR (15.53)` and a separate `NF NF NF`
postamble outside the ciphertext. Its direct reading is:

```text
ZITADELLEXWIDERSTANDAUFGEBENUEBERGABEBEDINGUNGENGORTFESTSETZENXKMX2??3X1?GXANCH
```

One observed-coordinate substitution proposes `DORT` for `GORT`:

```text
ZITADELLEXWIDERSTANDAUFGEBENUEBERGABEBEDINGUNGENDORTFESTSETZENXKMX2??3X1?GXANCH
```

The instruction is to abandon resistance at the citadel and set surrender
terms there. The message does not name the citadel's city. Its final
`KMX2??3X1?GXANCH` reference remains unresolved; the three question marks
come from the partial square, with all source coordinates present.

## C: what armistice conditions apply to this front?

The [232-coordinate source](../../experiments/november_armistice_orders/sources/p179_C.png)
has `--- v ZO'N (10.25 p.m., November 11th)` and several routing lines,
including `2000 FUER LP KK 11 KK (11) KR`. The full routing text and the
interstitial `WP WP WP FF NKJ v ZO'N` are preserved in the input record.

The raw output is:

```text
ANOHLXOBERKOMMANDOMACKE1SENUND11XARMEEERBITTENMITTEILUNGDERBESONDERENWAFFENSTILLSTANDSBESINGXFUERHIESIGEFRONTXAOK11X
```

Three observed-coordinate substitutions repair the two word fragments
`MACKE1SEN→MACKENSEN` and `BESING→BEDING`:

```text
ANOHLXOBERKOMMANDOMACKENSENUND11XARMEEERBITTENMITTEILUNGDERBESONDERENWAFFENSTILLSTANDSBEDINGXFUERHIESIGEFRONTXAOK11X
```

Mackensen's high command and the 11th Army ask OHL to communicate the
particular armistice conditions for their front. The abbreviation
`BEDING` is retained, without inserting letters to spell out *Bedingungen*.
B and C use the unchanged published Nov10–12 key.

## D: discharge delayed, and urgent home leave suspended

The [two-part source](../../experiments/november_armistice_orders/sources/p179_D.png)
is separately headed:

```text
12th NOVEMBER, 1918.
D) FUER UKS (18.50, November 12th) 2 TLE
```

Its actual part lengths are **190 and 212 coordinates**, matching their
printed labels. The earlier D1 OCR stream had 191 slots. Manual
retranscription restores the received 190-slot frame, with no insertion
or deletion of the printed source itself.

Both parts read under the unchanged published key labelled **Nov13–15b**.
That label differs from the source's **November 12** heading. The dates
and the successful working-key identity remain recorded together; their
chronology is unresolved.

D1's direct output, with **zero source repairs**, is:

```text
INFLGTRANSPTSCHWIERIGKINHEIMATISTDURCHKMDX????AMANGEORDNENTLASSGLDSTURMJAHRGX1560U61VERSCHOBENX
```

It reports that transport difficulties at home have caused a previously
ordered discharge of Landsturm year groups to be postponed. The reference
after `KMD` remains unknown. The year-like text **`1560U61`** is preserved
literally. The edition does not normalize it to a historically plausible
year or assign a new digit value.

D2's direct output, also with **zero source repairs**, is:

```text
DRINGENDEHEIMATSURLAUBEHABENBISAUFWEITERESGAENZLICHZUUNTERBLEIBENXCHEFDESGENSTABESNRXRM1A11???GEHOPEZ??0?X
```

Urgent home leave is to cease entirely until further notice. The signatory
is the chief of the general staff; the remaining reference string is not
completed. The question marks in these two parts are unassigned key cells,
not printed erasures, and their domains share one global square bijection.

## Exact accounting and attribution

| Part | Received coordinates | Raw fixed labels | Edition fixed labels | Known-coordinate substitutions | Source insertions/deletions/fills |
|---|---:|---:|---:|---:|---:|
| B | 158 | 76 / 79 | 76 / 79 | 1 | 0 |
| C | 232 | 116 / 116 | 116 / 116 | 3 | 0 |
| D1 | 190 | 91 / 95 | 91 / 95 | 0 | 0 |
| D2 | 212 | 100 / 106 | 100 / 106 | 0 | 0 |
| **Total for these four parts** | **792** | **383 / 396** | **383 / 396** | **4** | **0** |

The arithmetic certificate additionally contains the separate p179 A
record, whose printed five-coordinate cancellation is counted explicitly.
It must not be confused with the zero geometry changes in B–D above.

The [inputs](../../experiments/november_armistice_orders/inputs.json) and
[certificate](../../experiments/november_armistice_orders/certificates.json)
retain full source rows, header differences, all source images and every
digit/`J/Q/Y` occurrence, including changes made only by priced ordinary-word
repairs. Global re-encryption witnesses check compatibility and costs;
their arbitrary missing-key assignments are not proposed original numbers.

The keys are prior work by **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**. B, C and D2 already had unreviewed OCR-derived body candidates,
also represented in the frozen p73 retrieval corpus. D1 gains a coherent
source reading from the corrected transcription length. The bounded
publication check is recorded, with no universal priority claim.

```sh
python experiments/november_armistice_orders/verify.py --verify
```

The optional `--pdf` check regenerates all source crops from the pinned scan
and compares their pixels.
