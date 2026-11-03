# Optional staff vocabulary in the interference-damaged p137 A5

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The [existing Transylvania report edition](../../cases/military/transylvania_situation_report.md#p137-a5)
keeps p137 A5 partial. A separately priced proposal completes the staff
vocabulary as `WIRTSCHAFTS?UNDVERWALTUNGSSTAEBE`, retaining the intervening
unknown position. It adds **three observed-coordinate substitutions and ten
fills of unprinted coordinates** under the existing conditional frame.
The primary zero-substitution edition and all its readings remain unchanged.

## Same explicit source-loss model

The [published p137 A5 crop](../transylvania_situation_report/sources/p137_A5.png)
contains 215 source slots, four of them printed dashes, against `RICHI-252`.
Two `INTERFERENCE` annotations fall after original source slots 189 and 214.
The prior edition preserves all 38 allocations of the 37 missing coordinates.
Its selected allocation is 0/37, conditional on the declared opening
`ANSCHLIESSENDMUESSEN` matching its observed coordinates without error.
The present vocabulary proposal retains that conditional assumption.

**Raw output — existing conditional 252-slot frame, before any fills:**

```text
ANS?HLI?SSE?DMUE?SEN?ORB?GNN?MI?I?AER?SC??RSO?RG?N?ENP?RS??ALD?RW?R?SSH?FT??UNQ?ER?K?TUN?SS??EBE?B6?N?VEM?ER??GES?HO?E?WER?EN?
```

The original four completed spans leave 106 of 126 labels fixed, with no
observed-coordinate change:

**Edited output — existing primary partial edition, unchanged:**

```text
ANSCHLIESSENDMUESSEN?ORB?GNN?MILITAERISCHERSO?RG?N?ENPERSONALDERW?R?SSH?FT??UNQ?ER?K?TUN?SS??EBE?B6?NOVEMBERABGESCHOBENWERDEN?
```

The three additional spans occupy positions 64–74, 76–78 and 79–95, all
zero-based. Position 75 remains `?`. Their separate proposed reading is:

**Edited output — optional staff vocabulary; 116/126 fixed labels:**

```text
ANSCHLIESSENDMUESSEN?ORB?GNN?MILITAERISCHERSO?RG?N?ENPERSONALDERWIRTSCHAFTS?UNDVERWALTUNGSSTAEBE?B6?NOVEMBERABGESCHOBENWERDEN?
```

**Readable German — complete optional stream, retaining every unresolved position:**

> Anschliessend muessen `?ORB?GNN?` militaerischer `SO?RG?N?EN` Personal der Wirtschafts`?` und Verwaltungsstaebe `?B6?` November abgeschoben werden`?`.

Under this proposal the personnel-removal passage names economic and
administrative staffs. The governing condition remains damaged. The literal
`?B6?` is not silently changed to a date expression, and the final unknown
is not silently filled as punctuation or a separator. The text does not
prove that the personnel were actually moved.

## Exact additional cost

| Original source index | Printed row / group / character | Change | Plaintext effect |
| ---: | --- | --- | --- |
|68 |2 /7 /4, `AVGFA` |`F` → `V` |83: `K` → `A` in `VERWALTUNGSSTAEBE` |
|201 |7 /2 /2, `DGGVF` |`G` → `D` |69: `S` → `C` in `WIRTSCHAFTS` |
|202 |7 /2 /3, `DGGVF` |`G` → `D` |78: `Q` → `D` in `UND` |

The ten additional fills occur only in the unprinted final run, at model
indices 215, 216, 217, 218, 231, 232, 233, 245, 247 and 248, with respective values
`X X F X V G V X A F`. None is relabelled as a recovered visible coordinate.
The original three printed-dash fills and 18 missing-coordinate fills are
unchanged. The optional total is therefore **three observed substitutions,
three printed-mask fills and 28 missing-coordinate fills**. One printed dash
and nine missing coordinates remain unresolved.

The certificate retains the ten unresolved plaintext positions, their full
letter domains and both coordinate origins. It also evaluates the fixed
optional template against every one of the 38 original interference
allocations. This comparison remains conditional on the template and does
not measure the duration or size of the historical interference.

## The dark source glyph has a separate alternative

The fourth glyph of row 2's last group is dark and appears overtyped. The
existing transcript records `AVGFA`, with `F` at source 68. The original
[published crop](../transylvania_situation_report/sources/p137_A5.png) permits
review of that glyph alongside ordinary `F` and `V` forms. A **V alternative**
is retained explicitly as `AVGVA`; it is not silently substituted into the
primary source.

Under V, the administrative-staff word needs no observed-coordinate change;
the optional total becomes **two** observed substitutions, while every fill
and the two clear `G` → `D` changes remain the same. Both source variants
retain complete raw readings, mappings and exact witnesses. The displayed
primary price remains three, using the established F transcript. The word
proposal itself cannot decide which overtyped stroke is historical.

## Independent vocabulary witnesses

The [p184 B1 source](../hungary_transport_warning/sources/p184_B1.png), under
the unchanged `Nov13-15a` key, independently gives the raw span
`MACKENSENXWIRTSCHAFTSSTABXMINERALOELABTEILUNG`. This whole span is decoded
again without repairs, with every letter bound to its observed coordinate
pair. It attests the economic-staff compound in this traffic.

The [p122 B source](../schorlemer_demobilization_inquiry/sources/p122_reviewed.png)
has the clear address `OBERKOMMANDO M VERWALTUNGSSTAB`. That primary header
attests the administrative-staff compound. The witness is clear text, not a
claim that the p122 encrypted body contains the same phrase.

Neither witness repeats the p137 clause, establishes its plural inflection,
or identifies the personnel mentioned there. They support vocabulary only;
there is no transfer of dates, orders or whole plaintext between records.

## Reproduce

[Inputs](inputs.json) bind the existing p137 record, source image, unchanged
key and the two independent witnesses. [The certificate](certificates.json)
replays both F/V alternatives, all 38 allocations, the exact incremental
cost, and every still-open label. Its arbitrary complete roundtrip witness
is explicitly mathematical and is not accepted as historical plaintext.
The verifier also preserves the existing case's headings and every fenced
and quoted display byte.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
[printed pp122,137 and 184](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
Published period keys retain the credit of **George Lasry, Ingo Niebel,
Nils Kopal and Arno Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
This supplement adds no newly recovered physical record or priority claim.

```sh
python experiments/p137_optional_staff_vocabulary/verify.py --verify
python experiments/p137_optional_staff_vocabulary/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```
