# Poti horse transport: a conditional first-part edition

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

This is a conditional partial edition of the previously uncounted first part of the [Poti horse-delivery exchange](poti_horse_delivery.md). The original source has **225 positions** under the printed label **RICHI-220**. Its two transport clauses and footer can be repaired at a small explicit cost, but the source frame, opening and vessel-like fields remain unresolved.

## Source and complete frame comparison

The [existing public source crop](../../experiments/poti_horse_delivery/sources/p59_A1.png) retains every printed group and dash. Header: `SSD, COS v ASO (07.50 a.m., September 22nd); 2250 (21.9) 3 TLE; 1 TL RICHI-220`. The [literal inputs](../../experiments/poti_first_part_conditional/inputs.json) bind the earlier source edition without altering it.

The exact search prices **all 4,595,146,920 ways to exclude five of the 225 positions**, using dynamic programming. Only six ordinary transport-word spans are constrained; the opening, names and numbers are left free. The minimum is **five changed observed coordinates and two printed-mask fills**, after the separately declared **five exclusions**. There are **21 minimum source maps and eight distinct raw streams**. All are preserved, including their different prefix labels and first date-like fields. This is a bounded model result, not a proof that any five-coordinate deletion occurred historically.

The representative below excludes source indices 200–204, the visible `AFFDD` group. No cancellation mark on the source licenses that choice. It is retained because it was already one of the earlier illustrative frames, not because its prefix digits look more plausible.

## Representative raw and limited repair

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 220-coordinate frame after the five disclosed exclusions; unchanged Sep19–21 key:**

```text
6X??FFQ274XHG6AM11X9XAUF9AMPF?RXVUR?A4VA?NAX5XBATTAAM15X9XAUFDAM?FZRXBURDALXBYRDA?XINSGYSAWT52PFERDENAUHXPOTI0
```

**Edited output — the same conditional frame, five observed-coordinate substitutions and two printed-mask fills; all other labels retained:**

```text
6X??FFQ274XHG6AM11X9XAUFDAMPFERXVUR?A4VA?NAX5XBATTAAM15X9XAUFDAMPFERXBURDALXBYRDA?XINSGESAMT52PFERDENACHXPOTI0
```

</details>

**Readable German — all representative candidate labels retained; no vessel identification or date normalization:**

> 6 X ??FFQ274 X HG6 am 11 X 9 X auf Dampfer X VUR?A4VA?NA X 5 X BATT A am 15 X 9 X auf Dampfer X BURDAL X BYRDA? X insgesamt 52 Pferde nach X POTI0.

The two `AUF DAMPFER` clauses and the `INSGESAMT52PFERDENACH` footer support a limited horse-transport interpretation toward the literal `POTI0` ending. The separately printed second and third parts concern horses and Poti, which supplies context but does not identify the names or restore the opening. `VUR?A4VA?NA`, `BURDAL` and `BYRDA?` remain opaque; they are not silently converted into named ships.

## Alternative frames and withheld constraints

The complete certificate preserves every minimizing source map, raw stream, repaired stream and source-coordinate ledger. It does not collapse numerically different branches into the representative display.

| Constraints used | Minimum observed substitutions | Printed-mask fills | Minimum maps |
|---|---:|---:|---:|
| Both steamer clauses only |2|2|812|
| Transport footer, with NACH withheld |1|0|359630|
| All spans except NACH |4|2|1146|
| All six spans |5|2|21|

The five exclusions are a separate structural cost in every row. Withholding words leaves more possible maps; the retained 21 are conditional on the declared word stencil. The unchanged native 225-coordinate stream is also recorded with its orphan coordinate and no hidden truncation.

## Reproduce and credit

```sh
python experiments/poti_first_part_conditional/verify.py --verify
python experiments/poti_first_part_conditional/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Childs source p59 and the published Sep19–21 key; earlier source transcription and A2/A3 edition retained. Joint frame pricing, constrained partial edition and complete alternative accounting: icekylinx and GPT-6 Astra Pro. No first-decipherment claim.
