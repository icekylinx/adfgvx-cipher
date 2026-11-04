# p219 C — Kiev unrest and the soldiers' council

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Conditional recovery: icekylinx and GPT-6 Astra Pro.** Resolving printed
group alternatives and the marked jamming loss reveals a Kiev report.
The selected frame fixes **122/147 raw positions**. Seventeen inserted-slot
fills give **139/147 with zero observed-coordinate substitutions**.

The later [shared-square reading](../../experiments/nov25_treaty_digits/README.md#the-kiev-report-outside-the-original-snapshot)
reduces the optional `PETLJURA` spelling from four to **two observed-coordinate changes**.
The received name becomes `PEDFJ?RA` under the independently proposed
`VD=J` assignment. Reading its remaining damaged letters as `PETLJURA`
keeps the same 18 inserted-slot fills and all four minimum source models.
The two preserved source coordinates are V at index 181 and D at 212;
the remaining substitutions are V→X at 10 and A→F at 155.

## p219 C

**Readable German — three excerpts from the zero-substitution lexical completion; intervening clause and footer omitted:**

> Heeresgruppe Kiew. Unruhen zwischen Regierung Hetman und PEDF9?RA. […] Soldatenrat beschloss Neutralitaet.

The report concerns unrest between the Hetman government and the unresolved
name `PEDF9?RA`, and says that a soldiers' council resolved on neutrality.
The incomplete modifier `VORSTEHEND?`, the intervening `7?` field and the
full footer remain visible in the complete streams below. The quotation
uses plaintext spans 0–16, 19–64 and 79–112, all zero-based.

## Printed alternatives and jamming

The source contains 284 coordinate observations and advertises `RICHI-294`.
It prints three parenthesized groups, a repeated initial `XFXDD`, and a
`(jammed)` note with no stated length. The model retains those observations
as data and tests how to use them in the cipher frame.

`{JAMMED}` in the transcription marks the original `(jammed)` annotation;
the braces are a boundary marker, not coordinate observations.

The selected model excludes source 0–4 (one duplicate), 25–29 (parenthesized
`GXAFV`) and 200–204 (`VDGDD`, choosing its parenthesized `VDFDD` alternative).
The later parenthesized `FXVDD` remains in sequence. Twenty-five unknown
slots are inserted at the printed jamming boundary before original source
85. The model has 294 coordinates and uses the published Nov25–28 key.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 294-slot frame; all 25 added coordinates unassigned:**

```text
HEER?SGRU?PEXKIE?XXUN?UHENX?WISC?ENXREG?ERUN?XHETM?NXUN?XPEDF9?RAX7?VORST?HEND?SOLDAT?NRAT?BESCH?OSSX?EUTRAL?TAET?X7XVX?XODELSA?RM1?3230TMA?KO?SKQX
```

**Edited output — same conditional frame; zero observed substitutions and 17 inserted-slot fills; eight positions unresolved:**

```text
HEERESGRUPPEXKIEWXXUNRUHENXZWISCHENXREGIERUNGXHETMANXUNDXPEDF9?RAX7?VORSTEHEND?SOLDATENRATXBESCHLOSSXNEUTRALITAETXX7XVX?XODELSA?RM1?3230TMA?KO?SKQX
```

</details>

Choosing the printed `VDFDD` alternative matters: its surviving half-pair
permits E in `HEERESGRUPPE`. The other printed group would require a
separately priced coordinate change for that E. The primary edition fills
only compatible erased half-pairs and preserves the remaining labels.

## Optional name spellings

The same-length proposals `PETLJURA`, `ODESSA` and `MARKOWSKY` have separate
prices. They do not replace the primary raw names or establish historical
identities from an external document.

The following table records the earlier prices under the unchanged
published labels. The joint `J` interpretation above has its own
[certificate](../../experiments/nov25_treaty_digits/kiev_certificate.json).

| Proposal | Baseline observed substitutions | Total added-slot fills | Fixed positions |
|---|---:|---:|---:|
| Primary lexical completion | 0 | 17 | 139/147 |
| `PEDF9?RA → PETLJURA` | 4 | 18 | 140/147 |
| `ODELSA → ODESSA` | 1 | 17 | 139/147 |
| `MA?KO?SKQ → MARKOWSKY` | 2 | 19 | 141/147 |
| All three proposals together | 7 | 20 | 142/147 |

**Readable German — the same excerpt spans under the optional combined name proposal:**

> Heeresgruppe Kiew. Unruhen zwischen Regierung Hetman und Petljura. […] Soldatenrat beschloss Neutralitaet.

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — optional combined names; seven observed substitutions and 20 inserted-slot fills; five positions unresolved:**

```text
HEERESGRUPPEXKIEWXXUNRUHENXZWISCHENXREGIERUNGXHETMANXUNDXPETLJURAX7?VORSTEHEND?SOLDATENRATXBESCHLOSSXNEUTRALITAETXX7XVX?XODESSA?RM1?3230TMARKOWSKYX
```

</details>

No extra letter is inserted to complete `VORSTEHEND?`. Numerical and compact
footer fields such as `7XVX?`, `RM1?3230T` remain literal.

## Complete declared source-model check

For each parenthesized group the check retains both observations, retains
the preceding group only, or retains the parenthesized group only. It also
retains both initial duplicates or excludes either copy: **27 × 3 = 81 maps**.
Each model adds enough unknown slots at the marked jamming boundary to reach
294 coordinates.

Four maps attain the primary template's zero-substitution minimum. The
combined optional names also have four minimum maps, at seven substitutions.
Both scopes retain two edited streams: an opaque field reads `7?` or `B?`
depending on the first printed alternative. All prices, origins and streams
are retained. The templates leave that field unconstrained rather than using
it to choose a historical label.

## Source and credit

Childs, printed p219 / PDF p222, `C) IWE v RAT (------- November 25th)`;
`1900 (KR)`; `RICHI-294`.
[Original PDF](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
· [Edition and verifier](../../experiments/p219_kiev_unrest/README.md)
· [Complete certificate](../../experiments/p219_kiev_unrest/certificates.json).

<details>
<summary>Literal source transcription</summary>

**Source transcription — all 284 coordinate observations; parentheses and the jamming annotation retained separately:**

```text
XFXDD XFXDD VFDAD XVDFX GXAGV (GXAFV) FVFDA VDXDX
VVFFD XFDFX GFAXA XFFVV FXVGG XDXGG DAXAF VFVFD
XXGVX {JAMMED} XFAXA XAFFG DFAXD FXXGF VGVGG VGAXV
FDXGF AGVDV AGAAA AAXVX VGFFF XVGAD AXVDV DADXD
AGAFX VXGGG FFXFA DDFXV GGFVX VVVFA GVVFG XFXFX
ADFFV VDGDD (VDFDD) DDDFV GXXGF GGFDX DGVFV GVDFA
FVGFD GDADX ADAAA DDFFF GDDDX (FXVDD) XFDFV XXFGF
XVADX DFVX
```

</details>

The key retains the Lasry–Niebel–Kopal–Wacker work and Lasry's 2017 list.
The earlier unverified repository OCR block is preserved. The source-model
recognition, conditional reading and exact repair account are by
**icekylinx and GPT-6 Astra Pro**.
