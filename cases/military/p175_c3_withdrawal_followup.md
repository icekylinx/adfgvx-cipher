# Withdrawal from the Danube and Sereth front: p175 C3

The conditional third part reports withdrawal from the Danube and Sereth front toward the mountains, with a route through Kronstadt and Hermannstadt. Several equally compatible locations of the missing source block remain in the edition.

**Complete edition by printed page:** [p. 175](../pages/175.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source analysis and edition: icekylinx and GPT-6 Astra Pro.**

This source-defined third part becomes readable under an explicit
five-coordinate loss model. It reports a withdrawal toward the mountains
from the Danube and Sereth front, with a route via Kronstadt and
Hermannstadt. **The plaintext and source alignment remain conditional**:
six placements of one contiguous missing block fit the edited candidate
at the same observed-coordinate cost, and a broader loss family has
six lower-cost alignments.

## The source and its length

Childs printed p175 C3, PDF p178, belongs to the six-part message under
`LP v NKJ (5.40 p.m., November 10th); VON UKS KR 0915 (10/11) 6 TLE`.
The [literal part](../../experiments/romanian_ultimatum_companions/sources/p175_C3.png)
contains **217** printed slots, including four dashes. The enlarged
[header](../../experiments/romanian_ultimatum_companions/sources/p175_C3_heading_detail.png)
reads **RICHI-222**. The length difference is therefore **five**, but
the page does not mark where those missing coordinates belong.

The older source package keeps this part as frozen unread context.
This follow-up adds one newly cataloged reading of the same physical
record; the other five source parts and the existing p176a challenge
are not counted again.

## Raw and edited output

For display, insert one five-coordinate erased block before source
coordinate **95**. This is the smallest of six equally cheap placements
for the candidate, chosen as a stable representative. All indices are
zero-based. The published **Nov10–12** square and ranks are unchanged.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional frame with five missing coordinates:**

```text
OK?XG?HTHE?TENACHT?ONDONAU?UND?ERETHFR?NTAUFGE?IRGQQURUECKXWIRDUEBERXKRONSTADTXHERMANNSTADTXRIWHTUNGXKLUZ?NBUR0
```

**Edited output — same conditional frame:** Four observed-coordinate
substitutions, four printed-dash fills and five unprinted-coordinate
fills give the following **111-position candidate**:

```text
OKMXGEHTHEUTENACHTVONDONAUXUNDSERETHFRONTAUFGEBIRGEZURUECKXWIRDUEBERXKRONSTADTXHERMANNSTADTXRICHTUNGXKLUZENBURG
```

</details>

**Readable German — punctuation and word spacing of the conditional candidate; the final ellipsis marks continuation into the next part:**

> O.K.M. geht heute Nacht von Donau- und Serethfront auf Gebirge zurück.
> Wird über Kronstadt, Hermannstadt Richtung Kluzenburg …

The second sentence continues into the next source part. That part is
the separately attributed [p176a challenge](../p176a.md), whose earlier
breakthrough proposal has its own missing-block and editorial assumptions.
Its wording is not imported as independent proof of this reconstruction.

The source-derived spelling **KLUZENBURG** remains visible. The raw final
`0` is repaired through one specific observed-coordinate change; this
does not assign a new value to the key's `0` label. The interpretation
of `OKM` and the report's actual historical fulfillment are not separately
established by this source edition.

## Why there is no unique recovered gap

Every possible position for one contiguous five-coordinate loss was
checked: **218** source positions. Two frozen language models both rank
position **96** first, while several neighboring positions also produce
coherent partial readings. Ranking supplied a useful interval for
inspection, not a proof of a unique historical location.

For the complete candidate, the exact minimum over this family is four
observed-coordinate substitutions at each of these six gap starts:

```text
95, 96, 98, 99, 100, 101
```

If a whole five-letter group is assumed to have disappeared between
surviving printed groups, **95 and 100** remain tied. The source provides
no fixed omission marker to choose between them.

Allowing the five missing coordinates to be distributed arbitrarily
reduces the candidate's minimum to **three substitutions**. An exact
dynamic program over all missing-position sets finds **six** optimal
alignments, all with a local 1 + 3 + 1 loss pattern. Those six are also
fully retained. This broader result changes the loss assumption; it
does not prove that three separate losses actually occurred.

## Repair costs and evidence

The displayed placement at 95 changes source coordinates
**97 G→X, 172 D→A, 174 F→D, and 209 V→F**. It fills printed dashes
**57→D, 58→D, 59→F, and 119→V**, and inserts `VVGXX`.
The resulting candidate re-encrypts exactly. Every tied alternative
has its own source mapping and equally explicit certificate.

This one record has **217 printed slots**, **213 observed coordinates**,
a **222-coordinate conditional frame**, and **111 plaintext positions**.
The displayed raw frame fixes **102** labels; the edited candidate fixes
111. Across all 218 unselected one-block frames, the common singleton
reading fixes **zero** positions. Thus the readable raw text itself
depends on choosing a frame; the complete candidate is a further
editorial layer.

Twelve newly composed synthetic controls test the screening procedure.
Both models' predeclared primary objective places a truth-compatible
layout first in all twelve. Secondary objectives fail on some controls,
and the controls have no added observed-coordinate errors. They support
this bounded method, without providing a historical confidence percentage.
The models are also correlated through their shared book component.

The [full analysis](../../experiments/p175_c3_gap_followup/README.md),
[screen results](../../experiments/p175_c3_gap_followup/screen_results.json),
and [certificate](../../experiments/p175_c3_gap_followup/certificates.json)
preserve all layouts, controls, rankings, exact minima and source indices.
No key cell is changed, no first historical decipherment claim is made,
and no exact cross-copy was accepted from the bounded corpus search.

</details>
<!-- CASE-EDITION:END -->
