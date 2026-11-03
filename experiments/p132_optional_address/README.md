# Optional address spelling in p132 A

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The [existing p132 primary reading](../../cases/radio/p132_radio_service.md)
remains unchanged. Its raw addressee field is `KOSJOII`. The spelling `KOSPOLI` is a
useful **optional** proposal because this exact token is independently fixed
in other source-reviewed telegrams from the same traffic. It costs **two
additional observed-coordinate substitutions**. This supplement adds no new
physical record or decipherment and does not identify the officer named in
p132 A.

## The unchanged reading and the separate proposal

The [p132 A image](../november_radio_service/sources/childs_p132_A.png)
is headed `OSM v OUI (9.29 p.m., November 5th)`, `HIER 13 2207`,
`RICHI-242`. Its 242 source slots include one printed dash. The unchanged
`Nov4-6` period key fixes 120 of 121 raw positions.

**Raw output — p132 A, unchanged:**

```text
MILLTAEGMISZIONKOSJOIIXUEBERTENDUNGEILESKRIEGSRANGLI?TRNAUSZUGESDESGENERALMAJRHYDEWALDERBETENXFELDEISENBAHNNHEFPAFR53540X
```

The existing six observed-coordinate substitutions and one printed-dash
fill produce the current primary edited stream:

**Edited output — existing primary edition, unchanged:**

```text
MILITAERMISZIONKOSJOIIXUEBERSENDUNGEINESKRIEGSRANGLISTENAUSZUGESDESGENERALMAJRHYDEWALDERBETENXFELDEISENBAHNCHEFPAFR53540X
```

Changing only `KOSJOII` to `KOSPOLI` gives the following separate candidate.
Its total cost is **eight observed-coordinate substitutions and one source
mask fill**, of which precisely two substitutions are additional to the
primary edition. No gap, exclusion, reordering or key change is involved.

**Edited output — optional KOSPOLI proposal, excluded from the primary edition:**

```text
MILITAERMISZIONKOSPOLIXUEBERSENDUNGEINESKRIEGSRANGLISTENAUSZUGESDESGENERALMAJRHYDEWALDERBETENXFELDEISENBAHNCHEFPAFR53540X
```

**Readable German — complete optional stream, retaining the uncertain name and footer:**

> Militärmiszion `KOSPOLI`. Übersendung eines Kriegsranglistenauszuges des `GENERALMAJRHYDEWALD`
> erbeten. Feldeisenbahnchef `PAFR53540`.

This is a proposal for the spelling of one token. The literal `MISZION`
spelling, name field `GENERALMAJRHYDEWALD`, numerical labels and footer
`PAFR53540` remain unchanged. The supplement does not expand the name into a
historical person or establish this telegram's intended destination.

## Exact additional cost

All source and plaintext indices below are zero-based; printed group and
position numbers are one-based.

| Source index | Printed group / position | Printed row / group | Change | Plaintext index and effect |
| ---: | --- | --- | --- | --- |
| 187 | 38 / 3 | 5 / 6 (`XXAVA`) | `A` → `X` | 18: `J` → `P` |
| 216 | 44 / 2 | 6 / 4 (`VVAAG`) | `V` → `A` | 20: `I` → `L` |

The paired coordinate at source index 101 remains `D` in the first change;
source index 2 remains `X` in the second. Thus the original pairs `DA` and
`VX` become `DX` and `AX`. The unchanged square maps these respectively
from `J` to `P` and from `I` to `L`. Both changed source glyphs are visible
coordinates, so neither is charged as an erasure fill.

## Independent raw occurrences

Each witness is decoded again from its own complete literal source and
published period key. No editorial replacement is used to create the
following spans. The certificate records every witness letter's two source
indices and observed coordinate pair.

| Physical witness | Source image | Unmodified raw span | What it contributes |
| --- | --- | --- | --- |
| p90 A5 | [p90 source](../black_sea_evacuation_routes/sources/p90_A5.png) | `BVGXKOSPOLIX` | Exact `KOSPOLI` token in a distribution list; the clear header also prints `SSD BVG KOSPOLI (1/11) 1400 5 TEILE`. |
| p98 A2 | [p98 source](../black_sea_disembarkation/sources/p98_A2.png) | `VONKOSPOLINACHODESSA` | Exact token in a shipping-route clause under the independently published `Nov1-3` key. |
| p148 B1 | [p148 source](../constantinople_address_parts/sources/p148_B1.png) | `ANXMILXMISSIONCOSPOLIX` and `FUERXKOSPOLIX` | Literal mission-address context with `COSPOLI`, and the exact `KOSPOLI` spelling later in the same record under `Nov4-6`. |

These are **independent attestations of wording**, not repeated copies of
p132 A. None repeats its officer-register request or unresolved name.
The p148 record has an above-line `X` annotation over source index 37 and
an `L`-shaped noncoordinate at index 49. Both remain documented in its
original input; the witness calculation here uses the unmodified baseline
and does not apply that annotation or fill the mask. Every letter in the
listed spans is nevertheless fixed by observed coordinate pairs.

## Reproducibility and limits

[Inputs](inputs.json) pin all four live source records, their unchanged keys
and already published source images. [The certificate](certificates.json)
contains the raw decoding, existing and optional complete forward witnesses,
exact incremental edit ledger, numeral preservation and the independent
span mappings. The verifier also checks that the existing case's headings,
fenced displays and quoted displays retain their original bytes.

The [live readable mapping](../../data/reviews/p132_optional_address_readable_mapping_20261103.json)
separately binds the complete optional quotation to 118 ordered
nonseparator labels, including the unchanged opaque name and footer.
It adds no display-only letters or new source positions.

The period keys remain credited to **George Lasry, Ingo Niebel, Nils Kopal
and Arno Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
and the [2017 key republication](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
printed pp90, 98, 132 and 148, [collected scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).

```sh
python experiments/p132_optional_address/verify.py --verify
python data/reviews/verify_live_readable_mappings.py --manifest data/reviews/p132_optional_address_readable_mapping_20261103.json
python experiments/p132_optional_address/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```
