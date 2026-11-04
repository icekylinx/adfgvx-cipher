# An award notification and a congratulation

[Case index](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)


**Reviewed source crops:** [p193_F.png](../../experiments/nov13_congratulation_conditional_frame/sources/p193_F.png) · [p193_date_heading.png](../../experiments/nov13_congratulation_conditional_frame/sources/p193_date_heading.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## p193 F

**Status:** The source and its header both have **75 coordinates**. The conditional 74-coordinate edition excludes one observed terminal X and changes one observed D to G. Its baseline fixes **36/37** positions; the separate class interpretation below completes the remaining label.

**Source and dates:** Page heading 14 November 1918; F) CM v CZ (1.24 a.m., November 13th); separate label `2.10`; RIZI-75. The date layers and the label 2.10 are retained without reconciliation.

[Source p193 F — source-PDF reference](../../experiments/nov13_congratulation_conditional_frame/inputs.json)

### Conditional award-class reading

**Readable German — EK interpreted as an Iron Cross class and numerical DD=1 retained; existing terminal-X frame and word repair retained:**

> JTN. KR. EK2 verliehen. Glueckwunsch. S. R.

The message reports an award and offers congratulations. If `EK` denotes
the Iron Cross and the following character its class, **and the separate
DD cell retains numerical value 1**, the remaining square domain admits
only **2**. Numerical DD=1 is a contextual interpretation, not a fact
established by the published label alone. The independent native
`10X11` in [p186 B1](../military/oberost_troop_movement_obliterations.md#p186-b1)
supports it if that field is a day/month date: its repeated month can only
be 11. The [joint source account](../../experiments/nov13_joint_completion/README.md#the-award-class)
replays all ten untouched coordinates and states the date condition.

The resulting representative text has **37/37** fixed labels, with the
earlier **one observed-coordinate exclusion and one substitution**, and no
new source edit. `JTN`, `KR` and `S R` remain opaque. Without retaining DD's
numerical value, the distinct square cells alone do not exclude class 1.

The royal decree of 5 August 1914 specifies two classes and a Grand Cross.
Its contemporary reprint in *Die Presse*, 8 August 1914, p1, supplies the
[class-system evidence](../../experiments/nov13_joint_completion/sources/die_presse_1914_decree.png)
and [continuation](../../experiments/nov13_joint_completion/sources/die_presse_1914_classes.png).
It does not identify this recipient. The resulting **VG=2** assignment
also gives `ALLE 2 TAGE` in the [p188 supply request](../military/armistice_provisions_requests.md#c1-flour-and-oats-to-szolnok).

All four endpoint alternatives below retain the same received `VG` pair
at source positions 19 and 60. The class interpretation leaves those
geometries unresolved. [Joint certificate](../../experiments/nov13_joint_completion/certificates.json).

### Native odd frame retained

<details>
<summary>Raw decoded text</summary>

**Raw output — paired portion of the unmodified 75-coordinate frame:**

```text
JGXVER5EZNEAXRLHEMKNUIL?ICS0RK1AM1OCK
```

</details>

The unmodified inverse transposition leaves one orphan **A at inverse-stage index 74, originating at source index 27**. The 37 paired labels above are not the displayed congratulation. Excluding the last received X is therefore a different model from dropping the native orphan.

### Conditional terminal-X model

Exclude the **observed X at source index 74 before inverse transposition**. This is an explicitly priced exclusion, not a source-mask fill, a claim that the source printed 74, or a correction to the header. All other 74 observed positions remain in order.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 74-coordinate model:**

```text
JTNXKRXEK?XVERLIEHENXGLUECKWUN5CHXSXR
```

**Edited output — one additional observed-coordinate substitution:**

```text
JTNXKRXEK?XVERLIEHENXGLUECKWUNSCHXSXR
```

**Readable German — the same candidate labels with spacing and punctuation:**

> JTN. KR. EK? verliehen. Glueckwunsch. S. R.

</details>

**Explicit source changes:**

| Source index | Printed | Treatment | Cost |
|---:|---|---|---|
| 74 | X | Exclude before inverse transposition | One observed-coordinate exclusion |
| 12 | D | Propose G | One observed-coordinate substitution; GLUECKWUN5CH → GLUECKWUNSCH |

The baseline label after EK is **plaintext index 9, pair VG, source indices 19 and 60**. Both source coordinates are observed; the published square leaves VG unassigned, with domain `234789QY`. The separate class interpretation above assigns 2; it is not a source erasure fill.

### Endpoint alternatives remain open

The same congratulation core survives four source-exclusion choices, yielding three distinct streams. Each excludes one observed coordinate and changes the **same source index 12 from D to G**. The first two V exclusions are exact ciphertext aliases. These alternatives prevent a claim that the terminal-X error is historically unique.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — alternative excluding source 0 or 1 (V):**

```text
K?XVERLIEHENXGLUECKWUN5CHXSXR?JKCJOEK
```

**Edited output — the same one-coordinate word repair:**

```text
K?XVERLIEHENXGLUECKWUNSCHXSXR?JKCJOEK
```

**Raw output — alternative excluding source 73 (D):**

```text
JTNXKRXEK?XVERLIEHENXGLUECKWUN5CHXSCR
```

**Edited output — the same one-coordinate word repair:**

```text
JTNXKRXEK?XVERLIEHENXGLUECKWUNSCHXSCR
```

</details>

The V-exclusion alternative retains opaque opening K? and closing ?JKCJOEK. Excluding source 73 retains SCR at the end. None of these endpoints is expanded into a person, rank, unit or signature. The source-74 version above provides one convenient full-message presentation; the stable finding is the shared VERLIEHEN / GLUECKWUNSCH core.

### Exact prices and their limits

The certificate prices **all 75 received-source exclusions and all 75 inverse-stage exclusions** against the stated 37-position primary candidate. Two conventions are recorded: one prices only its 36 fixed labels, and the stricter one also requires EK? to occupy an unassigned cell of the unchanged published square. Under either convention, the full primary layout uniquely costs one substitution at source exclusion 74. This is conditional on that full layout, including the chosen opaque endpoints.

For inverse-stage exclusions, the minimum is **37 substitutions when EK? is an unconstrained wildcard**, or **38 when its unfilled-key-cell domain is enforced**. These are fixed-target prices, not a proof that no other plaintext is possible. The other endpoint alternatives above have their own one-substitution readings and are not hidden by the primary-target comparison.

The verifier preserves all paired coordinates, including the unresolved VG pair, and reproduces the conditional 74-coordinate ciphertext. Reattaching the explicitly excluded terminal X restores the full 75-position received shape with only the charged D→G substitution. This coordinate-level forward check is distinct from a complete plaintext re-encryption: the EK? symbol remains unassigned.

[Page date heading — source-PDF reference](../../experiments/nov13_congratulation_conditional_frame/inputs.json)

### Reproducibility and attribution

The [input](../../experiments/nov13_congratulation_conditional_frame/inputs.json) binds literal rows and date layers to exact source crops. The [certificate](../../experiments/nov13_congratulation_conditional_frame/certificates.json) retains the native odd frame, conditional models, full coordinate ledgers, all 150 exclusion prices and forward checks. The [verifier](../../experiments/nov13_congratulation_conditional_frame/verify.py) checks these values, the live German quotation and the unchanged published partial key.

Source edition and verification: icekylinx and GPT-6 Astra Pro (2026). Historical source: J. Rives Childs. Published partial-key credit remains with Lasry, Niebel, Kopal and Wacker. The [attribution record](../../experiments/nov13_congratulation_conditional_frame/prior_candidates.json) preserves earlier OCR and the bounded discovery diagnostic. Search scores are not used as historical evidence.
