# Research status

**icekylinx and GPT-6 Astra Pro · 4 November 2026**

[Historical showcase](historical-showcase.md) · [Catalogue](../cases/README.md) · [Methods](methods.md) · [Experiments](../experiments/README.md)

## What we have established

Our principal cryptanalytic result is the **new shared 18-column key for the
two p153 CHI fragments**. It fixes **60/66 positions in part 5 without a source
change**, and gives **33/54 raw positions in part 6**, with a separately priced
50/54-position proposal. Independent searches over 3,492,604 length-class
layouts show that only width 18 fits the same sixty-letter crib among widths
14–26. The [recovery record](../experiments/p153_recovery/README.md) preserves
the discovery and exact checks.

Our source reconstructions also recover information that a single damaged
reception could not provide:

| Result | What the independent evidence adds |
|---|---|
| [Arad provisions](../cases/military/danube_arad_witnesses.md) | Eleven missing coordinates, including received support for **80000 MANN**; eight source maps give one completed stream. |
| [Silk resale](../cases/finance/nov6_silk_resale_continuation.md) | Two receptions jointly support all 135 continuation positions. |
| [November 14 radio copies](../cases/radio/nov14_radio_retransmissions.md) | An 85-coordinate missing prefix is restored from a separately inspected reception. |
| [Small banknotes](../cases/finance/crown_banknote_completion.md) | A later complete copy supplies the nineteen coordinates absent from the earlier crown-airlift request. |
| [Munich routing](../cases/radio/p168_munich_routing_witness.md) | A source-linked repair fixes 139/140 raw positions; another original observation supplies the remaining slot. |

The [historical studies](historical-studies/README.md) explain why these
recoveries matter. Earlier key recovery and published readings are credited
where they contribute; our new keys, copy restorations and source editions
are stated directly.

## A complete source register

The catalogue now contains **679 entries for 679 physical ciphertext bodies**
on **175 printed log pages**: 22 original challenges and 657 other sources.
The former p132/p132_B duplication has been merged into the canonical p132
entry. A historical package identifier remains an evidence alias, not an
extra source. The four wider unread bodies now have public OPEN pages.

The [material census](whole-material-coverage.md) distinguishes catalogue
coverage from quantified cipher coverage. The [twelve instructional examples](../experiments/childs_instructional_examples/README.md)
remain outside the intercept-body count. The [source identity check](../data/reviews/verify_catalog_source_identity.py)
rejects duplicate physical locations instead of allowing an overlap exception.

## Recent partial reconstructions

Each source edition records its proposed reading, coordinate costs and remaining ambiguity.

| Source | Present result and remaining limit |
|---|---|
| [p143 evening report](../cases/military/nov6_evening_danube_report.md) | The independently attested address formula **FUER OKM** supplies the final position in the existing geographical proposal: **94/94 conditional positions**, four substitutions and ten fills. |
| [p144 aerial reconnaissance](../cases/military/nov6_horse_loading_reconnaissance.md) | **Kladovo** completes the place fragment, with an 1893 General Staff map attesting the name. Two fills and one additional correction give **71/71 conditional positions**. |
| [p160 Alpenkorps report](../cases/military/nov8_alpenkorps_report.md) | All 28,680 two-exclusion maps against the native p170 copy leave two minimum frames. Both directly read **RD**, removing one extra substitution from the extended interpretation; the **UJVERBASZ / UZVERBASZ** choice remains unresolved by the source. |
| [p164a](../cases/p164a.md) | **BESATZUNGSHEER** matches all 18 received halves at zero substitutions; the combined conditional layer reaches 104/121 positions. |
| [p163, parts 13 and 15](../cases/military/p163_A.md) | Repeated **NACHHUTSTELLUNG** supports a 116/117-position part-15 proposal; the corps digit remains coupled and unresolved. |
| [p163 jammed continuation](../cases/military/p163_infrastructure_clause.md) | A 59-position infrastructure clause fits all 121 received coordinates; the inferred frame and six wholly absent letters remain conditional. |
| [p89 destination](../experiments/p89_destination_continuation/README.md) | Native word witnesses extend the conditional proposal to 176/179 positions, with ten new half-supported letters or separators and no new observed substitution. The shortened spelling DIENSTELLEN and three remaining unknowns stay explicit. |
| [p68 procurement](../experiments/p68_procurement_continuation/README.md) | The common proposal reaches 76/93 positions; competing internal verb letters remain unresolved. |
| [p137 personnel order](../experiments/p137_governing_clause/README.md) | An optional governing clause reaches 124/126 positions, with all seven observed substitutions explicit. |
| [p137 publicity fragment](../cases/military/p137_publicity_fragment.md) | **DER OEFFENTLICHKEIT … BLEIBEN** is a narrow 25-letter proposal; the intervening meaning and complete frame are unestablished. |
| [p176 coal-train fragment](../experiments/p176_repeated_place/README.md) | A repeated-place hypothesis reaches 59/80 positions; **BLANKENBURG** remains an equal-price rival to **KLAUSENBURG**. |
| [p84 illness fragment](../cases/radio/p84_mother_illness_extension.md) | A 52/122-position proposal preserves the competing **MUTTER** and **MITTEL** readings. |

The [experiment guide](../experiments/README.md) links the source certificates,
controls and exact algorithms. The current edition removes duplicated
machine displays and obsolete layout snapshots; it keeps the evidence needed
to reproduce these claims and the earlier contributions on which they rest.

## Unresolved sources

**Seven sources have no accepted body reading.** They are visible in the
[OPEN guide](../cases/open/README.md), alongside their original transcriptions.

| Target | Research question |
|---|---|
| [p73](../cases/p73.md) | Can key structure, contacts or a related message constrain the unknown square and transposition? |
| [p170 A](../cases/p170.md) | Which transmission frame and key family explain the damaged reception? |
| [p198 D](../cases/p198.md) | Is the five-loss model sufficient, or do the source and key need a different explanation? |
| [p70 B1](../cases/open/p70_B1.md) | Does the apparent period-rank signal survive a changed square or a different writing convention? |
| [p127 B2](../cases/open/p127_B2.md) | Do the repeated groups reveal source copying, a repeated plaintext pattern or the wrong frame? |
| [p145 A](../cases/open/p145_A.md) | What remains identifiable in the incomplete transmission without imposing a long guessed message? |
| [p194 D1](../cases/open/p194_D1.md) | Can the short reception be connected to an independently received overlap? |

For [p170 A](../cases/p170.md#coordinate-count-constraint-for-a-complete-body),
the seven received D coordinates now give exact ordinary-letter count bounds
under the Nov7–9 and Nov10–12 squares, independent of every column order and
direction. Neither pinned German reference book contains a 53-character window
meeting either bound under the two tested normalizations. This reduces the
priority of those complete-body models; it does not exclude the squares or
prove that the source is truncated.

The [all-seven contact diagnosis](../experiments/open_target_contact_diagnosis/README.md)
compares every tested key/frame family with matched shuffled sources. Six
nearby known-message controls recover their correct rank order; the open
fragments show no similarly clear separation. It also proves an exact
241,920-rank coincidence invariance for the p70 frame, explaining why
coincidence alone cannot recover word order.
