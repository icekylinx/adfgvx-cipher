# Danube and Arad: restoration from parallel source witnesses

**Source recovery and review: icekylinx and GPT-6 Astra Pro.**

[Read the source editions](../../cases/pages/164.md#edition-cases-military-danube-arad-witnesses) · [Exact certificate](certificates.json) · [Original Childs scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)

Reviewed source crops: [p164 C1](sources/p164_C1.png) · [p168 E](sources/p168_E.png).

The newly reviewed **p168 E Arad copy** supplies all **11 original coordinates** missing from the earlier p159 primary reconstruction. The p159 source-linked raw output rises **124 → 135 of 136 positions**, with every retained received coordinate unchanged. The new witness's own complete observed pairs fix **80000 MANN**. Its native duration separator is **X**, replacing the earlier optional U proposal in the improved collation.

A separate **p164 C1 glyph correction** restores raw UEBER and provides independently observed support for the p153 Danube report. The p153 witness supplies two p164 mask values in return.

| Source edition | Printed / model slots | Fixed raw / linked / word-layer positions | Observed substitutions in the word layer | Fills |
|---|---:|---:|---:|---|
| p164 C1 | 248 / 248 | 119 / 121 / 122 of 124 | 4 | 3 printed masks, including 2 parallel-passage-supported values |
| p168 E | 271 / 272 | 132 / 135 / 135 of 136 | 4 | 2 printed masks and 1 added coordinate, all supplied by p159 observations |

## Arad source origins

The p168 short group DDGX corresponds to p159's observed DDGGX. Inserting G before source 52 or 53 gives the same completed ciphertext; all 30 single-coordinate completions in that short group are checked. The p159 row containing VFVGF supplies the two printed masks in p168's VF--F.

In the other direction, every coordinate donated to p159 comes directly from an observed p168 slot. None uses p168's missing slot or its two borrowed mask values. The certificate checks the origin graph, every source index and all 11 added-coordinate values. The p168 **80000** pair ledger is entirely native.

Five coordinate disagreements between the retained received copies remain explicit. The common edited Arad stream costs **7 observed substitutions in p159** and **4 in p168**. These source-specific prices preserve the raw differences; no whole-copy identity is silently imposed. The p159 improvement now holds for all eight source-only minimizing maps described below; all produce the same linked ciphertext.

**14 TAGE X 10 TAGE**, the repeated ARAD, STAEKE, 80000 and 30000 remain literal. No R is inserted into STAEKE. The two unassigned key cells are completed both ways: one global VF assignment supplies the shared footer label, giving **18{5,6}GEH** in p168 and raw **18{5,6}GLH** in p159.

## Source-only geometry selection

The verifier compares the **unfilled p168 primary frame** with the entire earlier p159 family: five possible short-slot boundaries and every ordered pair of five-slot gap boundaries in the 262-slot stage. This is **173,580 canonical layouts**, or **694,320 source-origin maps** after the four duplicated-group choices.

The objective counts only disagreements where both coordinates were originally observed. It uses **no plaintext template** and leaves p168's missing coordinate and two printed masks unassigned. The exact minimum is **5 disagreements in 258 observed comparisons**. Only `(short boundary, first gap, second gap) = (118,15,110)` and `(118,16,110)` attain it. Both apply to each duplicate-origin choice, leaving **8 source maps**. All eight yield the same completed ciphertext, with **135/136 fixed plaintext positions**. Each map fills its eleven missing coordinates from directly observed p168 origins.

The new evidence narrows the separate earlier **64 word-conditioned minima to 8** and eliminates **all 48 P0000 alternatives**. The earlier word objective had minimum 6 against a supplied partial plaintext; the source-only objective has minimum 5 against received coordinates. Their costs are not interchangeable.

The certificate retains the complete price histogram, a digest over every canonical `(one,a,b,cost,comparisons)` tuple, all eight exact source maps and their observed-coordinate fill origins. This is an exhaustive result within the stated finite edit family.

## Danube source correction and parallel support

The source prints **GDXVV**, not the earlier GDXXV, in p164 C1's fourth row. The correction at source index 148 restores E at plaintext index 110, with zero historical-coordinate repair cost.

Native p164 pairs support three word-letter proposals in p153: U3BER → UEBER, BELGR4D → BELGRAD and UEBSR → UEBER. The p153 native pairs in turn supply U in p164's DONA? and S in UEBER?ETZ. The native formation labels remain **219** and **21B**; the matching p164 unit also supports a separately priced [219 proposal for p153](../nov7_danube_and_message_reports/README.md#the-219th-infantry-division-proposal).

## Danube date and army completion

A further conditional layer completes **p164 C1 to 124/124 positions**.
It reads `8XC1X1?` as **8.11.18** and `?1 ARMEE` as **11 ARMEE**. The
first interpretation follows the day.month.year form directly observed in
the [p155 D morning report](../../cases/pages/155.md#edition-cases-military-nov7-derailment-and-trains-p155-d);
the second repeats the native `AOK11` at the start of p164 itself.

Compared with the earlier word layer, this costs **one additional observed
substitution** (source 139 `D` → `G`) and **two mask fills** (source 52 `C` →
`G`, source 164 dash → `A`). The complete proposal therefore has **five
substitutions and five source-mask fills**. The three changed plaintext
positions are 20, 24 and 33; two were previously unknown.

The certificate records this under `records[0].date_army_completion`, with
the native `AOK11` pairs, the independently decoded p155 date-format
witness, all source changes and exact re-encryption under both unused 5/6
assignments. The date and army identification remain stated assumptions;
the earlier source and word layers retain their original counts.

## Reproduce

```sh
python experiments/danube_arad_witnesses/verify.py --verify
python experiments/danube_arad_witnesses/verify.py --verify --pdf /path/to/childs.pdf
```

The portable verifier checks source rows, frame maps, all repair prices, directly observed coordinate origins, literal quantity pairs, both global footer assignments, exact re-encryption and the actual Markdown quotations and fenced streams. The optional PDF check reproduces both reviewed crops from the authenticated original scan.

The [prior snapshot](prior_snapshot.json) retains the earlier p164 contextual source, p159 reconstruction and p153 passage. The period key belongs to the Lasry–Niebel–Kopal–Wacker work and Lasry's published key list. The present contribution is the independently inspected source correction, new source edition and exact cross-copy restoration.
