# Troop crossing in boats: a fragmentary November 6 report

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[Case index](../README.md) · [ADFGVX Cipher](../../README.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The 192-slot section B on Childs p144 supports a short passage concerning troops crossing in boats and a routine no-further-events ending. Its opening, one intervening token and the location remain garbled. The edition retains those labels and gives a limited ordinary-word proposal with its exact source cost.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed source excerpt — source-PDF reference](../../experiments/nov6_boat_crossing_fragment/inputs.json) · [Literal inputs](../../experiments/nov6_boat_crossing_fragment/inputs.json) · [Position and repair certificates](../../experiments/nov6_boat_crossing_fragment/certificates.json)

The published `Nov4-6` key is unchanged. [Earlier OCR evidence](../../experiments/nov6_boat_crossing_fragment/ocr_snapshot.json) and its [recomputed decode](../../experiments/nov6_boat_crossing_fragment/prior_candidates.json) are retained. This edition adds checked framing, explicit reading limits and a readable display; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p144 B](#p144-b) | 192 | 93 / 96 | 5 | 2 |

## p144 B

**Source transcription — header:** `B) UKS v ZON (---- November 7th); RICHI-192; page heading 6th NOVEMBER, 1918`

**Raw output — every native source slot in printed order:**

```text
SOCSTDENVU4RONEE4HEXXLUHLEGKU?GXUEBERSETZECVONTRUPPEIXINBOOJENBEIBRFIRBD9SONSTNI?HTS?ESENELICWES
```

**Edited output — 5 observed-coordinate substitutions and 2 source-mask fills; no insertion, deletion or reordering:**

```text
SOCSTDENVU4RONEE4HEXXLUHLEGKU?GXUEBERSETZENVONTRUPPENXINBOOTENBEIBRFIRBD9SONSTNICHTSWESENTLICHES
```

**Readable German — the same nonseparator labels as the edited output:**

> SOCSTDENVU4RONEE4HE. LUHLEGKU?G. Uebersetzen von Truppen in Booten bei BRFIRBD9. Sonst nichts Wesentliches.

**Meaning:** The ordinary-word proposal describes troops crossing in boats and ends with nothing further of significance. The preceding 19-label field, the LUHLEGKU?G token and the place-like BRFIRBD9 remain uninterpreted; no particular river, town, formation or successful crossing is independently established.

### Editorial limits

- The proposal repairs only five ordinary-word labels and fills two source-mask coordinates; the exact coordinate cost is listed in the certificate. No source position or key cell is changed without pricing.
- The opening, the apparent reconnaissance token and the place-like string remain exactly as decoded. Their appearance in the readable display does not turn them into accepted German words.
- The date heading and November 7 intercept header are both retained. The adjacent p144 C1 aerial report is a separate physical record; thematic proximity does not join their plaintexts.
- The literal 4 and 9 labels in the opaque fields are retained. They are not relabeled as letters, separators or historical numbers to make an assumed geographical interpretation fit.

### Exact repair account

The five observed-coordinate changes repair `UEBERSETZEC` to `UEBERSETZEN`, `TRUPPEI` to `TRUPPEN`, `BOOJEN` to `BOOTEN`, and two letters in `?ESENELICWES` to `WESENTLICHES`. Two separate mask fills supply the `C` in `NI?HTS` and the initial `W` of the last word. The remaining `?` in `LUHLEGKU?G` is kept.

| Source index, zero-based | Printed | Proposed | Cost |
| ---: | --- | --- | --- |
| 17 | `D` | `X` | Observed-coordinate substitution |
| 66 | `F` | `X` | Observed-coordinate substitution |
| 72 | `D` | `X` | Observed-coordinate substitution |
| 78 | `F` | `G` | Observed-coordinate substitution |
| 85 | `V` | `X` | Observed-coordinate substitution |
| 65 | `-` | `D` | Source-mask fill |
| 190 | `-` | `A` | Source-mask fill |

The resulting proposal fixes **95 / 96** positions. Fixed labels in an opaque string are not the same as understood words. The primary reading adopts neither an expansion of the first line nor a particular town. A separately priced opening hypothesis follows below. The nearby [aerial-reconnaissance record](nov6_horse_loading_reconnaissance.md) remains separate.

### An independently attested closing formula

The unedited [p127 A3 aerial-reconnaissance report](nov4_march_air_reconnaissance.md)
contains the exact phrase **NICHTSWESENTLICHES** in fixed raw output.
The verifier independently decodes that source and maps its letters against
the proposed ending here. This supports the ending as a formula actually
present elsewhere in the collection; it does not identify these reports as
copies or as descriptions of the same event. It supplies no evidence for
the optional opening below.

### Optional reading of the opening, outside the primary totals

**Conditional interpretation — a separately priced lexical hypothesis:**

The nineteen-position opening could be read as **SONST DONAUFRONT RUHE**.
This is an ordinary-language proposal, not a reading independently supplied
by another copy. It changes seven output labels at **eight additional
observed-coordinate substitutions**. The full optional candidate therefore
costs **13 observed substitutions and the same 2 source-mask fills**, with
no frame or key change. It remains outside the primary totals.

**Edited output — optional opening proposal; 13 observed substitutions, 2 source-mask fills; 95/96 fixed positions:**

```text
SONSTDONAUFRONTRUHEXXLUHLEGKU?GXUEBERSETZENVONTRUPPENXINBOOTENBEIBRFIRBD9SONSTNICHTSWESENTLICHES
```

**Readable German — optional opening, with the remaining opaque fields unchanged:**

> Sonst Donaufront Ruhe. LUHLEGKU?G. Uebersetzen von Truppen in Booten bei BRFIRBD9. Sonst nichts Wesentliches.

The additional source changes are **11 F→V, 46 F→V, 68 G→F, 92 F→X,
114 D→X, 148 X→A, 159 F→G and 182 X→D**. These are changes to observed
coordinates, not newly resolved square cells. Both raw 4 labels in the
opening are affected only within this explicit proposal; the primary raw
and edited streams retain them.

**Meaning — conditional on the optional opening:** The first clause would
say that the Danube front is otherwise quiet. This does not identify the
place-like BRFIRBD9, restore LUHLEGKU?G, link the adjacent reconnaissance
telegram into this one, or establish the military events as historical
facts. The exact cost makes this possible interpretation reviewable without
promoting it to the primary reading.

## Reproduction and credit

Run `python experiments/nov6_boat_crossing_fragment/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and the exact rendered pixels of the preserved source excerpt.

The verifier reconstructs source-coordinate pairs, checks raw domains, replays all priced changes, verifies the readable display without dropping unresolved labels, and checks a global completion witness where required. Such a completion is mechanical evidence, not a historical guess.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
