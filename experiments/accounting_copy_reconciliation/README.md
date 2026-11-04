# Accounting copies: two recovered labels and a retained ending disagreement

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

The already published [p172 D2](../../cases/pages/172.md#edition-cases-finance-staatsbank-accounting-cheques-p172-d2)
and [p175 B2](../../cases/pages/175.md#edition-cases-finance-hauptwechselamt-accounting-p175-b2)
are closely matching second parts of an accounting and cheque-arrival
inquiry. Comparing their native sources supplies two previously unresolved
labels in the conservative p175 reading: **`VOM?8` becomes `VOM18`**, and
**`89240?11?` becomes `89240911?`**. This adds no observed-coordinate change
to its existing four-change edition. Its final question mark remains,
coupled to the unresolved label after `AM`.

This package adds **no physical source record**. Both original editions,
their raw streams, source images, dates, certificates and earlier credits
remain unchanged. The comparison is supplementary evidence, with the
common-second-part hypothesis stated explicitly.

## What the sources agree on

Both records have exactly **204 native source slots**, use the unchanged
published **Nov7–9** key and decode to **102 positions**. Their source masks
are disjoint: four in p172 D2 and ten in p175 B2. At the 190 positions
observed in both copies, **185 coordinates agree and five disagree**.
Every coordinate is observed in at least one source.

The headings remain distinct:

| Source | Received header | Additional source information |
| --- | --- | --- |
| p172 D2 | `LP v NKJ`, 6.06 p.m., 11 November | `VON UKS LP 2127 (9/11) 2 TLE`; second part, `RICHI-204` |
| p175 B2 | `LP v NKJ`, 6.02 p.m., 10 November | Second part, `RICHI-204`; the corresponding first part is not printed here |

The immediate radio hop is NKJ to LP in both headers. Neither the different
receipt dates nor the distinction between an originating station and a
radio hop is normalized away. The repeated body and coordinate agreement
support comparison of these second parts. They do not recover the absent
p175 first-part ciphertext or establish every detail of the complete
transmissions' identity.

## Transfer observed coordinates before editing words

First fill only an existing printed mask from the other source's observed
coordinate at the same position. No observed coordinate is changed, no
slot is inserted or removed, and the five disagreements stay in their
respective source records.

**Raw output — p175 after ten copy-supported source-mask fills; conditional
on the matching-second-part relation; 100/102 fixed positions:**

```text
VOM18XBISENDUOCTOTERGEZAHLTENYARKXFERNERANKUNFTSANZEIGEUEBERAM?XGESANDTECHEKSXHAUPTWECHSEGAMT89240911?
```

**Raw output — p172 after four copy-supported source-mask fills; conditional
on the same relation; 101/102 fixed positions:**

```text
VOM18XBISENDEOOTOBERGEZAHLTENYAYKXFERNERANKUNFTSANZEIGEUEBERAM?XGESANDTECHEKSXHAUPTWECHSEGAMT89240911X
```

The unchanged words `YARK`/`YAYK` and `HAUPTWECHSEGAMT` matter. A second
copy does not automatically authenticate the earlier lexical emendations
`MARK` and `HAUPTWECHSELAMT`.

## Conservative p175 improvement

Retain the original p175 word proposal and its four observed-coordinate
substitutions, and use the other source only to fill the two previously
unfilled printed dashes:

| New fill | Other-source observation | Newly fixed plaintext label |
| --- | --- | --- |
| p175 source index 154: `- → F` | p172 source index 154 is `F` | Position 3: `? → 1`, giving `VOM18` |
| p175 source index 203: `- → G` | p172 source index 203 is `G` | Position 98: `? → 9`, giving `89240911?` |

Indices are zero-based. The two fills add no source slots and no change to
an observed coordinate. All ten p175 mask values in this candidate are
observed in p172. The four existing word substitutions remain at source
indices **1, 32, 38 and 165**.

**Edited output — conservative p175 candidate; four observed substitutions
and ten source-mask fills, including the two new copy-supported fills;
100/102 fixed positions:**

```text
VOM18XBISENDEOCTOBERGEZAHLTENMARKXFERNERANKUNFTSANZEIGEUEBERAM?XGESANDTECHEKSXHAUPTWECHSELAMT89240911?
```

**Readable German — complete conservative edited stream; the numeral labels
remain literal and the two unknown positions remain displayed:**

> Vom 18 bis Ende October gezahlten Mark. Ferner Ankunftsanzeige ueber am ? gesandte Cheks. Hauptwechselamt 89240911?

The final `?` is an unresolved field position, not question punctuation.
Both position **62** after `AM` and position **101** at the end are the
observed pair **`VF`**. Under the unchanged partial square, they must be
equal and have the shared domain **`{5, 6}`**. The other unknown cell `XA`
takes the other member of that pair. Neither copy selects the historical
digit assignment. The literal closing reference is not a payment amount.

## A separate common-copy ending

p172 ends in the observed pair **`VV`**, labelled `X`. p175 instead ends in
**`VF`**. To make the complete candidates identical, p175 needs the
additional observed substitution **source index 153, `F → V`**. That
change is not a fill of a printed dash.

**Conditional interpretation — complete common-copy candidate; p172 costs
three observed substitutions and four mask fills; p175 costs five observed
substitutions and ten mask fills:**

```text
VOM18XBISENDEOCTOBERGEZAHLTENMARKXFERNERANKUNFTSANZEIGEUEBERAM?XGESANDTECHEKSXHAUPTWECHSELAMT89240911X
```

The candidate fixes **101/102 labels**. Of those 101 fixed labels, **99 have
a complete, unchanged coordinate-pair witness in at least one source**.
The two exceptions are the proposed M at plaintext position 29 and L at
position 89. These remain ordinary-word proposals:

| Position | Native pair evidence | Proposed repair | Observed-coordinate cost across both copies |
| --- | --- | --- | ---: |
| 29 | p172 `AG → Y`; p175 `?G` | `AF → M` | 2, because both sources print `G` at source index 32 |
| 89 | p175 `DG → G`; p172 `D?` | `DD → L` | 1, at p175 source index 38; p172 separately needs a mask fill |

The unknown `AM` field has a complete observed pair in both sources but
still lacks an assigned square label. Pair support and fixed-label support
are therefore different counts.

## Exact scope of the finite comparison

At each of the five observed disagreements, choose either printed value;
at every other source position, keep its observed value. Because the masks
are disjoint, these choices produce exactly **32 complete ciphertexts**.
Each costs exactly **five observed-coordinate changes across both source
records**, the minimum possible in this particular common-copy model.
The verifier checks all 32 and both injective completions of the partial
square, giving **64 distinct complete literal plaintexts**.

None of those 32 ciphertexts is the edited common-copy candidate above.
That candidate additionally needs the two changes at shared source index
32 and the one change at source index 38. Consequently its exact joint
observed-change cost is **5 + 2 + 1 = 8**: three in p172 and five in p175.
All 14 mask fills are counted separately. Thirteen take an observed value
from the other source; the p172 fill at index 38 instead follows the
explicit `HAUPTWECHSELAMT` word proposal.

This exhaustive calculation verifies costs and retained alternatives for
the stated sources, key and candidate. It is not a claim of unique
historical wording or of an identified copying-error mechanism.

## Reproduce and credit

```sh
python experiments/accounting_copy_reconciliation/verify.py --verify
python experiments/accounting_copy_reconciliation/verify.py --verify --pdf /path/to/childs.pdf
```

The ordinary check uses the standard library, independently reconstructs
the ragged-column inverse permutation, compares decoded domains with the
core implementation, checks both global square assignments, re-encrypts
every enumerated complete witness, and binds every unchanged original
source artifact by SHA-256. The optional PDF check replays the two original
source editions' exact crop-pixel checks; no new image or new transcription
is introduced here.

[Inputs](inputs.json) and [certificates](certificates.json) retain the full
comparison, conservative and stronger candidates, mask provenance,
coordinate conflicts, unsupported word repairs and all finite alternatives.
The original [Hauptwechselamt](../hauptwechselamt_accounting/README.md) and
[Staatsbank](../staatsbank_accounting_cheques/README.md) editions keep their
own contributions and limitations. Published period-key recovery remains
credited to George Lasry and collaborators. This reconciliation claims no
first-decipherment priority.
