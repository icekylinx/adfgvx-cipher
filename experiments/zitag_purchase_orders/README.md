# Repeated ZITAG stop-order and contract cancellation

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

This source edition covers five physical records: **p102 A, p103 D,
p106 B, and p103 B1–B2**. The first three are closely matching copies of
an order to stop buying and loading goods and secure what is available.
The separate two-part message allows loading only consignments already
paid for, cancels other contracts and renews a request for Westernhagen's
return. Their different instructions and headers are preserved in the
[case](../../cases/finance/zitag_purchase_orders.md).

## Actual cross-copy support

The three short copies each contain exactly 180 observed coordinates.
They differ only at source indices **29, 55 and 162**:

| Source index | p102 A | p103 D | p106 B | Readable common candidate |
|---:|---|---|---|---|
| 29 | G | X | G | X |
| 55 | G | D | D | D |
| 162 | F | G | F | F |

Every coordinate in the candidate has a literal witness in at least one
source copy. The candidate is not a majority vote: index 29 follows the
single p103 D witness. The selection uses the common-original hypothesis
and ordinary wording. All three uncorrected readings remain available.
The required observed-coordinate substitutions are **2, 1 and 1**.

```text
FUERXZITAGXOHNENUMMERNICHTSWEITERKAUFENUNDNICHTSWEITERVERLADENALLESMOEGLICHSTSICHERNXZITAG
```

## Separate two-part message

The source prints **274** coordinates in B1, ending with the four-letter
group `DXGV`. Earlier OCR made that final group five slots and badly
degraded the whole reading. The source-aligned body is readable; its
explicit ordinary-word candidate costs **10 coordinate substitutions**.
The transmitted labels `NR X 5`, `6 MILLIONEN` and `NR X 3` remain unchanged.
Raw `4`, `1`, `5` and `Q` inside damaged words are fully retained before
their separately priced repairs.

B2 prints **254 slots**, including two dashes and an invalid `C`.
Filling these three erasures gives the complete continuation with
**zero observed-coordinate substitutions**. `WESTERNHAGEN` is already
fully observed in the raw plaintext, while the heading prints
`WESTGRNHAGEN`. Neither spelling is used to assign a historical identity.

The five records have **1,068 printed slots**, **1,065 valid coordinates**
and **534 modeled plaintext positions**. The unchanged key fixes 531 raw
positions; the candidates fix all 534. Total repair cost is 14 observed
substitutions and three printed-erasure fills. There are no insertions,
deletions, rank changes or key-cell assignments.

## Provenance and limits

The period key is the published Nov1–3 key. Earlier repository screens
already contained the short copies and B2 as readable, unreviewed
OCR-derived candidates. Their exact cached bodies and the degraded B1
candidate are frozen in `inputs.json`. A bounded prior-body check did not
locate explicit discussion in the paper, dissertation chapter or cached
comment thread; this does not establish historical priority.

The neighboring two-part message is not treated as a retransmission of
the short stop-order. No agency abbreviation is expanded from guesswork,
no raw number is relabeled, and the instructions are not described as
completed purchases, cancellations, shipments or a completed return.

## Reproduce

```bash
python experiments/zitag_purchase_orders/verify.py --verify
python experiments/zitag_purchase_orders/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier independently checks transposition, plaintext domains,
every repair, complete re-encryption and all 180 cross-copy coordinate
witnesses. The optional PDF check verifies the full source hash and the
pixels of every crop. The five proposed catalog rows are separate from
the shared catalog.
