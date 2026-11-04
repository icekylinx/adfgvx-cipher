# p137 A6 — Conditional publicity fragment in an interference-damaged report

Only fragments about “the public” and something that is to “remain” can be proposed. The damaged clause does not establish whether information was to be withheld, disclosed or kept available.

**Complete edition by printed page:** [p. 137](../pages/137.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and conditional reconstruction: icekylinx and GPT-6 Astra Pro.**
The sixth part preserves 74 coordinate slots after an explicit interference
annotation. A language-guided proposal places `DER OEFFENTLICHKEIT` and
`BLEIBEN` in a conditional 254-slot frame. Its **25 proposed letters retain
15 observed halves and supply 35 absent halves**. None of the 71 received
valid coordinates is changed. These words are conditional proposals, not
cipher-only recoveries or a completed sentence.

## p137 A6

**Readable German — conditional word fragments only; the intervening fourteen positions remain unresolved:**

> […] der Oeffentlichkeit […] bleiben […]

The central noun means “the public.” The excerpt does not establish whether
something was to remain hidden, become known, or remain available to the public.
Both the polarity and the intervening verb have materially different
zero-change alternatives. No event or policy is inferred from this fragment.

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional 254-slot frame with 180 added leading unknown coordinates; published Nov4–6 key; 0/127 fixed plaintext positions:**

```text
???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
```

</details>

Every plaintext position lacks at least one coordinate in this frame. The
received halves still constrain letter domains, but do not independently
fix even one complete letter pair.

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — 25 proposed letters at positions 13–30 and 45–51; zero observed substitutions, zero printed-mask fills and 35 added-slot fills:**

```text
?????????????DEROEFFENTLICHKEIT??????????????BLEIBEN???????????????????????????????????????????????????????????????????????????
```

</details>

**102 plaintext positions remain unassigned**, including all fourteen positions
31–44. Of the 180 inferred leading coordinates, 145 remain unknown, and all
three original printed dashes remain unfilled. The candidate is a partial
assignment within a proposed frame; the original gives no total length.

## Exact support and semantic alternatives

All indices below are zero-based. A received half is a constraint on a letter,
not an independently fixed letter.

| Proposed word | Plaintext positions, inclusive | Observed halves retained | Added-slot fills | Wholly absent letters |
|---|---:|---:|---:|---:|
| `DER` | 13–15 | 2 | 4 | 1 |
| `OEFFENTLICHKEIT` | 16–30 | 9 | 21 | 6 |
| `BLEIBEN` | 45–51 | 4 | 10 | 3 |
| **Primary proposal** | **25 positions** | **15** | **35** | **10** |

The ten wholly unobserved proposed letters are **15 R, 17 E, 19 F, 22 T,
25 C, 26 H, 29 I, 46 L, 49 B and 51 N**. Their two coordinates are both
supplied. The fifteen remaining proposed letters each retain exactly one
received half.

The discovery model suggested the fuller wording
`DEROEFFENTLICHKEITNICHTVERBORGENBLEIBEN`. Its apparent fluency does not resolve
two independent ambiguities:

| Unresolved span | Equal-price examples | Consequence |
|---|---|---|
| 31–35 | `NICHT`, `IMMER`, `LANGE` | “Not,” “always” and “for a long time” differ materially. |
| 36–44 | `VERBORGEN`, `VERGOENNT` | “Hidden” and “granted/allowed” support different readings. |

All six combinations have **39 assigned letters, 23 observed halves and
55 added-slot fills**, with zero observed-coordinate changes. Each has
sixteen wholly unobserved letters. They are separately priced alternatives,
not equally established historical sentences. The primary output therefore
leaves both spans unread. Other local dictionary matches also exist;
this list does not exhaust all possible wording. Even `DER` and `BLEIBEN`
remain language-guided choices within their coordinate domains.

## Conditional length and neighboring parts

| Frame | Added leading unknown coordinates | Raw fixed positions | Primary proposed positions |
|---|---:|---:|---:|
| 254 slots | 180 | 0/127 | 25/127 |
| 256 slots | 182 | 0/128 | 25/128 |
| 258 slots | 184 | 0/129 | 25/129 |

The **entire first 127 plaintext positions have identical received-source
ownership** in these three frames. The longer two merely add one or two
wholly unobserved positions. The source cannot choose among them. The
254-slot frame is a representative of this equivalence, not a recovered
transmitted length. An independent check of the exact sparse 25-letter
pattern examined 106,953 placements across every even length 74–1000. Of
3,724 placements retaining at least fifteen observed halves, only these
three models at offset 13 fit without a change. This bounded compatibility
check excludes neither lower-support placements nor other loss patterns,
wording or longer frames.

A separately priced `VON` at 124–126 is compatible in the 254-slot model:
it retains two observed halves and supplies four missing coordinates.
Its `V` is wholly absent, and it is excluded from the primary output.
The proposed neighboring p129 A7 begins with the fully observed
`ALLGEMEINERHIERNICHTBEKANNTERPOLITISCHERLAGE`, which makes a connection through
“von” plausible. The [cross-page report assembly](transylvania_situation_report.md)
remains conditional: the 5/6 November headings and receipt times conflict.
That context supplies no missing A6 coordinate. The earlier A5 repairs and
A7 printed-dash fill retain their separate costs.

## Source and verification

<details>
<summary>Literal source transcription</summary>

**Source transcription — all 74 printed slots, preserving the three dashes:**

```text
DXXAF FVAAG FAVDA VVFAX VAXVV
---FV AAXGX VGGAV GXDGF XFAFG DAAGX FXVFA
GXXAF FVXGA XGVX
```

</details>

The original labels this `6TL` and prints `RICHI` without a length. The leading
`(interference)` annotation supports a loss hypothesis but supplies no count.
The source edition retains the three dashes at source positions 25–27 and
keeps the inferred leading loss separate from them.

The [experiment and exact certificates](../../experiments/p137_publicity_fragment/README.md)
provide the source crop, source-owner maps, forward-encryption witnesses,
letter-level repair costs, frame-equivalence proof and adverse semantic
alternatives. Discovery uses the already audited exact word/bigram dynamic
program; its optimum is exact only within that declared scoring model.
Full-length-family shuffled controls are diagnostic comparisons, not a
probability that the proposed text is correct. A fresh 127-letter control
ranked its true frame first among 264 lengths but recovered only 54 true
letters, directly demonstrating that fluent model wording can be wrong.
No independent native copy
of this clause or of `OEFFENTLICHKEIT` has been found in the searched corpus.

**Verification command — independent source and candidate checks:**

```sh
python experiments/p137_publicity_fragment/verify.py --verify
```

The historical source is J. Rives Childs, *General Solution of the ADFGVX
Cipher System*, printed p137 / PDF p140. The period key and prior cryptanalysis
retain their attribution to George Lasry, Ingo Niebel, Nils Kopal and Arno
Wacker. The new conditional fragment, counterexamples and source audit are
by **icekylinx and GPT-6 Astra Pro**.

</details>
<!-- CASE-EDITION:END -->
