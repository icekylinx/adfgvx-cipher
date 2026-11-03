# Payments through October and cheque acknowledgements

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

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

## p175 B2

**Raw output — native 204-coordinate frame:**

```text
VO??8XBISENDUOCTOTE?GEZAHLT?N?ARKXFERNERANKUNFTSANZE?GEUEBERAM?XGESANDTE?HEKSXHAUPTWECHS?GA?T89240?11?
```

**Edited output — same native frame:** Four observed-coordinate
substitutions and eight printed-dash fills give:

```text
VOM?8XBISENDEOCTOBERGEZAHLTENMARKXFERNERANKUNFTSANZEIGEUEBERAM?XGESANDTECHEKSXHAUPTWECHSELAMT89240?11?
```

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
