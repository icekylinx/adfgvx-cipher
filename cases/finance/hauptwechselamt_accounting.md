# Payments through October and cheque acknowledgements

The fragment concerns marks paid through the end of October and asks for notice of the arrival of cheques. It retains the Hauptwechselamt designation; the preceding part and payment amount remain incomplete.

**Complete edition by printed page:** [p. 175](../pages/175.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition: icekylinx and GPT-6 Astra Pro.**

Childs printed p175 B, PDF p178, supplies a source-labeled **second
part**, received at **18:02 on 10 November**. Its 204 printed slots
include ten dashes. The native frame reads with the unchanged published
**Nov7–9** key. The receipt date is preserved; it is not used to substitute
the neighboring messages' Nov10–12 key.

The fragment concerns marks paid through the end of October, arrival
notices for cheques and `HAUPTWECHSELAMT`. Its missing first part is not
reconstructed, and no completed payment amount or transaction outcome
is inferred.

## Conditional digit reading

The [shared Nov7–9 digit interpretation](../../experiments/nov7_9_joint_digits/README.md) reads **am 6. gesandte Cheks** and the literal closing **892409116**, without additional coordinate changes or fills. The opposite assignment gives am 5. and 892409115. The final label is preserved as transmitted, rather than normalized to a date or matched to another reception’s separator.

## p175 B2

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 204-coordinate frame:**

```text
VO??8XBISENDUOCTOTE?GEZAHLT?N?ARKXFERNERANKUNFTSANZE?GEUEBERAM?XGESANDTE?HEKSXHAUPTWECHS?GA?T89240?11?
```

**Edited output — same native frame:** Four observed-coordinate
substitutions and eight printed-dash fills give:

```text
VOM?8XBISENDEOCTOBERGEZAHLTENMARKXFERNERANKUNFTSANZEIGEUEBERAM?XGESANDTECHEKSXHAUPTWECHSELAMT89240?11?
```

</details>

**Readable German — word spacing and punctuation of that candidate:**

> Vom ?8 bis Ende October gezahlten Mark. Ferner Ankunftsanzeige über
> am ? gesandte Cheks. Hauptwechselamt 89240?11?

The first sentence is a surviving clause fragment, not a reconstruction
of the missing first part. The spellings `OCTOBER` and `CHEKS` remain
visible. `VOM?8`, `AM?` and the final code are retained without normalizing
dates, amounts or reference numbers.

## What the question marks mean here

The four unknown positions have different origins:

| Literal field | Plaintext position | Full domain | Evidence |
|---|---:|---|---|
| `VOM?8` | 3 | `1GIKNY` | One unfilled printed coordinate; the value is not restricted to digits |
| `AM?` | 62 | `56` | Both coordinates are observed; square cell `VF` is unassigned |
| `89240?11?`, first question mark | 98 | `5679JMZ` | One unfilled printed coordinate |
| `89240?11?`, final question mark | 101 | `56` | The same unassigned `VF` cell as position 62 |

Positions 62 and 101 must agree under an unchanged key. The source
does not select 5 or 6. The separate historical military constraint
proposed elsewhere for this key is not applied here.

All **72** combinations of the two possible full-square completions and
the two remaining printed-coordinate fills are retained as complete
compatibility witnesses. They re-encrypt exactly with the stated edited
coordinates. This enumeration verifies the remaining ambiguity; it
does not supply a historical completion.

## Exact source scope

The [source crop](../../experiments/hauptwechselamt_accounting/sources/p175_B.png)
has **204 printed slots**, **194 observed coordinates**, and **102
plaintext positions**. The raw reading fixes 90 labels; the edited
candidate fixes 98. There are **four observed-coordinate substitutions**
and **eight printed-dash fills**, with two printed dashes still unfilled.
No length change, source deletion or key change is made.

The earlier OCR-derived stream was shorter and produced an unreadable
candidate. The present contribution is source retranscription and
explicit arithmetic under the published key, without a historical
first-decipherment claim. Lasry and colleagues retain credit for the
period key; the paper's separate p175 A travel discussion is not claimed
as a prior reading of this financial fragment.

[Inputs](../../experiments/hauptwechselamt_accounting/inputs.json),
[certificates](../../experiments/hauptwechselamt_accounting/certificates.json)
and [reproduction instructions](../../experiments/hauptwechselamt_accounting/README.md)
provide the literal source, every coordinate repair and all remaining
position domains.

**Later copy evidence.** The independently received p172 D2 supplies the two
remaining printed-dash values for `VOM18` and `89240911?` under the explicit
matching-second-part hypothesis. The conservative candidate keeps the four
original observed-coordinate substitutions and fixes 100/102 labels with
ten source-mask fills; its final `?` still shares cell VF with the date-like
field after AM. A separate common-copy ending X costs one additional
observed change. The [complete reconciliation](../../experiments/accounting_copy_reconciliation/README.md)
preserves both original editions, all five source disagreements, the two
unsupported ordinary-word repairs, and both global square completions.

</details>
<!-- CASE-EDITION:END -->
