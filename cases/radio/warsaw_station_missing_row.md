# Warsaw station report: a conditional missing-row continuation

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and conditional reconstruction: icekylinx and GPT-6 Astra Pro.**

Childs p204 C2 prints **242 coordinate slots** but advertises **282**. Inserting a hypothetical row of eight five-coordinate groups before the terminal `GX` produces a coherent continuation of [part 1](nov16_18_command_inquiries.md#p204-c1): equipment has not arrived from home, operation is to pass to the Poles on Monday evening, and WAU is transferring personnel. The proposed words require **no change to any observed coordinate** and **36 fills in the 40 hypothesized missing slots**. Four plaintext positions remain unknown.

The longer frame and those 36 fills remain a **conditional reconstruction**. The scan does not visibly mark a lost row, and no complete independent copy supplies it. The native 242-slot decoding remains available below.

## p204 C2

[Reviewed source excerpt](../../experiments/warsaw_station_missing_row/sources/p204_C.png) · [Exact inputs](../../experiments/warsaw_station_missing_row/inputs.json) · [All gap placements and global witnesses](../../experiments/warsaw_station_missing_row/certificates.json)

**Source transcription — header:** `C) KOW v WAU (1.50 a.m., November 18th); 0115 (17), 2 TLE; 2 TL RICHI-282`.

The seven printed lines contain six lines of 40 coordinates and a final two-coordinate group `GX`. This count restores several groups omitted or damaged by OCR, but the remaining 40-slot discrepancy is in the reviewed source itself.

**Readable German — conditional interpretation**, from the edited 282-slot frame with the missing row inserted before `GX`:

> Das nicht aus Heimat eingetroffen. NO?A WAU. Festfern, Festfunk A uebergeben Betrieb Montag Abend Polen. S. R. WAU ueberweist Mannschaften Bezkdos des ?K? nach OA?.

**Meaning:** The preceding part ends with equipment; this continuation says it has not arrived from home. Under the stated lost-row hypothesis, the facilities designated FESTFERN and FESTFUNK A hand operation to the Poles on Monday evening, and S. R. WAU transfers personnel to the abbreviated Bezkdos. The opening token, final unit and destination are not identified.

The literal tokens `NO?A`, `A` after `FESTFUNK`, `DES?K?` and `OA?` are retained. `Bezkdos` is left as the transmitted abbreviation. The ending is not silently made into a fluent unit name or a plausible destination.

**Raw output — conditional 282-slot frame**, before filling any missing coordinate. Every one of the 242 printed coordinates remains unchanged.

```text
DASN?C?TAUSHE?MA?EINGET?O?F?NXNO?AW?U?FEST?E?N?FEST?UN?A?EBER?E?E?BETR?EB?O?TAGA?E?D?OLEN?SX?X?AUUE?E?W?ISTM?NN?C?AFTE?B?Z?DOSXDES?K?NACHOA?X
```

**Edited output — conditional 282-slot frame:** zero observed-coordinate substitutions, zero source-mask fills, and 36 inserted-slot fills; four inserted slots remain unknown.

```text
DASNICHTAUSHEIMATEINGETROFFENXNO?AWAUXFESTFERNXFESTFUNKAUEBERGEBENBETRIEBMONTAGABENDPOLENXSXRXWAUUEBERWEISTMANNSCHAFTENBEZKDOSXDES?K?NACHOA?X
```

## What the terminal alternatives establish

The verifier checks every possible start for one contiguous 40-slot gap against the same disclosed word template. Exactly three terminal placements allow the proposed wording without changing an observed coordinate. This is a compatibility result **conditioned on the proposed wording**, not an independent identification of the lost position.

| Missing gap starts at source index | Position relative to terminal GX | Inserted-slot fills | Fixed edited positions | Remaining ending |
|---:|---|---:|---:|---|
| 240 | Before GX | 36 | 137 / 141 | `DES?K?NACHOA?X` |
| 241 | Between G and X | 35 | 136 / 141 | `?ES?K?NACHOA?X` |
| 242 | After GX | 34 | 135 / 141 | `?ES?K?NACH?A?X` |

The before-`GX` placement preserves the printed five-coordinate group boundary. The other two possibilities are retained because the observed coordinates and the selected words do not exclude them. All three branches preserve the same substantive middle reading while leaving different terminal fields open. No global key cell is reassigned.

## Source and contextual limits

The [preceding source part](nov16_18_command_inquiries.md#p204-c1) ends with crews of two other stations lacking equipment; `DAS NICHT AUS HEIMAT EINGETROFFEN` continues that sentence naturally. The independently reviewed [p204 A telegram](p204_A.md) also reports a Monday handover to the Poles. These are useful contextual checks, but neither provides this part's missing ciphertext, final reference or destination.

<details>
<summary>Native 242-slot raw output</summary>

**Raw output — native 242-slot frame**, unchanged and without any hypothesized missing coordinate:

```text
OOXJSBN?N?NXR?MY?C?B??H2EWJ??UGH?ONGTRQEGGFWA?YSB?BT1WYU?SRD?CNTWR?E?SYCCWABOA?OCCOBNNBSTG?T?X?THG1GWJEWQSCEEBYWA?O?Q?OGW
```

This native output is not an accepted body reading. The proposed 282-slot reading is kept in its own conditional frame.

</details>

## Evidence and credit

Published Nov16–18 key: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016); George Lasry (2017 key list). Earlier unreviewed OCR candidates are preserved. New source review and conditional reconstruction: icekylinx and GPT-6 Astra Pro.

The certificates preserve all source rows, map every conditional frame position to its original source index or an explicitly inserted slot, and list every proposed fill. Separate injective global square completions and residual-coordinate fillings produce full re-encryption witnesses for all three branches. Those witnesses demonstrate consistency, not historical completeness. The readable passage maps exactly to every nonseparator label in the primary edited output, including all four question marks.

Reproduce with `python experiments/warsaw_station_missing_row/verify.py --verify`. Optional `--pdf /path/to/adfgvx-childs.pdf` regenerates the crop and checks every RGB pixel against the pinned original PDF.
