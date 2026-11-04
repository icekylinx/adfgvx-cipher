# A conditional governing clause for p137 A5

[Reading conventions](../../docs/reading-conventions.md)

**Source review and reconstruction: icekylinx and GPT-6 Astra Pro.**

The damaged personnel-removal passage can be extended from the existing
**116/126-position staff proposal to 124/126 positions**. The new proposal is
`VORBEGINN MILITAERISCHER BEWEGUNGEN` and the marker `AB6X`. It adds four
observed-coordinate substitutions, one printed-mask fill and seven fills of
unprinted coordinates. Every newly fixed position retains an observed
half-coordinate.

The two additions are separately reviewable. `AB6X` needs only two
missing-coordinate fills and leaves the observed numerical label `6`
untouched. The governing clause requires the four observed substitutions;
it is a contextual editorial proposal, with its exact price below.

## Source frame and reading

The [original p137 A5 image](../transylvania_situation_report/sources/p137_A5.png)
prints 215 coordinate slots, including four dashes, against `RICHI-252`.
This supplement uses the earlier conditional **0/37 allocation** of the
37 absent coordinates between the two `INTERFERENCE` annotations. The
existing prefix crib selects that allocation. The source, period key and
all 38 allocations remain in the [original edition](../transylvania_situation_report/README.md).

**Raw output — conditional 252-slot frame, before repairs or fills:**

```text
ANS?HLI?SSE?DMUE?SEN?ORB?GNN?MI?I?AER?SC??RSO?RG?N?ENP?RS??ALD?RW?R?SSH?FT??UNQ?ER?K?TUN?SS??EBE?B6?N?VEM?ER??GES?HO?E?WER?EN?
```

**Edited output — optional governing-clause and date-marker proposal:**

```text
ANSCHLIESSENDMUESSENVORBEGINNMILITAERISCHERBEWEGUNGENPERSONALDERWIRTSCHAFTS?UNDVERWALTUNGSSTAEBEAB6XNOVEMBERABGESCHOBENWERDEN?
```

**Readable German — complete optional stream:**

> Anschliessend muessen vor Beginn militaerischer Bewegungen Personal der Wirtschafts`?` und Verwaltungsstaebe ab `6 X` November abgeschoben werden`?`.

**Meaning:** Under this proposal, personnel of the economic and administrative
staffs are to be sent away before military movements begin. The proposed
start marker reads `AB6XNOVEMBER`. The original `MUESSEN`, literal `6`,
separator `X`, and two unresolved positions are retained.

The governing-clause proposal uses the existing removal context and its
surviving letter pattern. No independently received duplicate of this
clause has been found. The earlier [staff-vocabulary witnesses](../p137_optional_staff_vocabulary/README.md#independent-vocabulary-witnesses)
continue to support the two staff compounds, without supplying the new clause.

## Cumulative prices

Counts use the established F transcription at source 68. Fixed positions
include raw garbles wherever a layer has not repaired them.

| Layer | Fixed positions | Observed substitutions | Printed-mask fills | Missing-coordinate fills |
|---|---:|---:|---:|---:|
| Raw conditional frame | 85/126 | 0 | 0 | 0 |
| Original four-span edition | 106/126 | 0 | 3 | 18 |
| Original edition plus `AB6X` | 108/126 | 0 | 3 | 20 |
| Earlier staff-vocabulary proposal | 116/126 | 3 | 3 | 28 |
| Staff vocabulary plus `AB6X` | 118/126 | 3 | 3 | 30 |
| New governing-clause proposal | **124/126** | **7** | **4** | **35** |

The four new observed substitutions are:

| Source index | Change | Plaintext index and effect |
|---:|---|---|
| 5 | V → F | 46: R → E in `BEWEGUNGEN` |
| 137 | X → V | 26: N → I in `VORBEGINN` |
| 139 | X → V | 43: S → B in `BEWEGUNGEN` |
| 198 | G → F | 44: O → E in `BEWEGUNGEN` |

The newly filled printed mask is source 213 → V. The seven new missing-slot
fills are model indices 219, 225, 226, 228, 234, 240 and 243 with values
`D F X F F A V`. Coordinates already supplied by the staff proposal are
preserved. The separately retained source-68 **V alternative** reduces the
final observed-substitution total to six; it does not alter any other price.

Only positions **75** and **125** remain unresolved. Their observed pair
patterns are `F?` and `?D`, with domains `9EKVXZ` and `0578CX` respectively.
Neither is silently changed into punctuation. The date marker's `6` is still
the observed `GX` cell at source indices 189 and 55.

## Declared word comparison and verification

At the ten-position noun slot, six explicit candidates have these exact
observed-coordinate prices under the same frame:

| Candidate | Observed substitutions |
|---|---:|
| `BEWEGUNGEN` | 3 |
| `STOERUNGEN` | 4 |
| `VORGAENGEN` | 5 |
| `HANDLUNGEN` | 8 |
| `EINGRIFFEN` | 10 |
| `MASSNAHMEN` | 12 |

This finite comparison explains the preferred proposal; it does not claim
uniqueness over German. The certificate also prices the complete fixed
proposal under all 38 interference allocations. Allocation 0/37 alone
achieves its seven-substitution minimum.

[Inputs](inputs.json) bind the original source and staff package by hash.
[The certificate](certificates.json) contains every raw domain, coordinate
origin, cumulative and incremental edit, both source-68 variants, all 38
allocation prices and exact re-encryption witnesses. The witnesses complete
the two residual positions only for arithmetic verification and are not
additional readings.

```sh
python experiments/p137_governing_clause/verify.py --verify
```

The verifier independently rebuilds the column map, cross-checks it against
the project cipher, and proves that all eight new fixed labels retain one
observed half-coordinate. This strengthens an existing physical body's
conditional reading; it adds no body or key to the catalogue.

**Sources and credit:** J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed p137 / PDF p140, and the published Nov4–6 key credited to
George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. Earlier source and
staff-vocabulary work retain their linked attribution.
