# Poti horse transport: a conditional first-part edition

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

This is a conditional partial edition of the previously uncounted first part of the [Poti horse-delivery exchange](poti_horse_delivery.md). The original source has **225 positions** under the printed label **RICHI-220**. Its two transport clauses and footer can be repaired at a small explicit cost. A separate repeated-field extension now supplies three conditional letters, reaching **108/110** positions while retaining the original frame alternatives, unread opening and competing vessel-like labels.

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

The two `AUF DAMPFER` clauses and the `INSGESAMT52PFERDENACH` footer support a limited horse-transport interpretation toward the literal `POTI0` ending. The separately printed second and third parts concern horses and Poti, which supplies context but does not identify the names or restore the opening. In this earlier 105/110 layer, `VUR?A4VA?NA`, `BURDAL` and `BYRDA?` remain opaque. The separate extension below transfers three missing letters; it does not identify either vessel with certainty.

## Conditional repeated-field completion

Each `AUF DAMPFER` clause is followed by two similar short fields. If each
pair repeats one label, and extra observed-coordinate changes are minimized,
three missing letters are common to every minimum-cost reconstruction:
**N at position 35**, **R at 40**, and **L at 81**. The corresponding letters
are directly present in the other copy at positions 41, 34 and 74.

| Raw pair in every retained frame | Minimum equal-copy alternatives | Common missing-letter transfers |
|---|---|---|
| `VUR?A` / `VA?NA` | `VARNA` or `VURNA` | N into the first copy; R into the second |
| `BURDAL` / `BYRDA?` | `BURDAL` or `BYRDAL` | L into the second copy |

These are conditional repetition inferences. The source itself still fixes
103/110 positions under the five-exclusion frame. Transferring just the
three common letters gives **108/110**, at **four additional printed-mask
fills and no additional observed-coordinate substitutions**. N and R each
need one missing half; L needs both halves. The totals are **five observed
substitutions, six mask fills and five separately declared source
exclusions**. All 21 previously minimizing source maps remain represented.

**Readable German — the common extension, with the three conditional letters bracketed:**

> 6 X ??FFQ274 X HG6 am 11 X 9 X auf Dampfer X VUR[N]A4VA[R]NA X 5 X BATT A am 15 X 9 X auf Dampfer X BURDAL X BYRDA[L] X insgesamt 52 Pferde nach X POTI0.

The differing U/A and U/Y letters and the raw `4` remain literal in this
common layer. Enforcing identical complete copies costs one further observed
substitution for each pair and leaves **four joint minimum variants**; all
are retained. The extension does not silently choose `VARNA`, replace `4`
with a separator, or turn `BURDAL`/`BYRDAL` into a different ship name. The
two opening unknowns still permit **36** complete strings in each frame.

<details>
<summary>Common conditional extension and exact machine labels</summary>

**Edited output — three repetition-based letters; five substitutions and six mask fills after the existing five exclusions:**

```text
6X??FFQ274XHG6AM11X9XAUFDAMPFERXVURNA4VARNAX5XBATTAAM15X9XAUFDAMPFERXBURDALXBYRDALXINSGESAMT52PFERDENACHXPOTI0
```

</details>

For limited context, the shipping company's own
[history](https://navibulgar.com/en/company/history/index.php) records a
steamer *Varna* among deliveries in 1903–1906 and wartime mobilization of its
vessels in 1916–1918. A separate public
[photograph caption](https://www.flickr.com/photos/39631091@N03/15359293270/)
is titled *Poti, Ship Varna* and attributed by its uploader to a German
officer in winter 1918. Only the caption was inspected; this metadata does
not verify a September voyage or identify the telegram's vessel. These
contextual sources make `VARNA` plausible without selecting it by arithmetic.

The [extension package](../../experiments/p59_repeated_vessel_labels/README.md)
records all label costs, all four equal-copy variants and exact source
ledgers for every retained frame. The original first-part edition and its
source inputs are preserved.

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
