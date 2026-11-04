# 3 November radio, morning and pioneer reports

Prepared by **icekylinx and GPT-6 Astra Pro**.

Three native source frames on Childs p110 contain **828 printed slots**:
826 visible ADFGVX coordinates and two C-shaped glyphs retained as masks.
They model 414 plaintext positions, with 412 raw fixed labels and 414 fixed
after ten observed-coordinate substitutions and two source-mask fills.
There are no inserted, deleted or reordered source coordinates.

| Source | Native slots | Raw fixed | Edited fixed | Substitutions | Mask fills |
| --- | ---: | ---: | ---: | ---: | ---: |
| p110 A2 | 280 | 140 | 140 | 2 | 0 |
| p110 B | 150 | 73 | 75 | 0 | 2 |
| p110 C | 398 | 199 | 199 | 8 | 0 |

The [radio schedule](../../cases/pages/110.md#edition-cases-radio-nov3-transmission-schedule) is
explicitly a second part; no first part is identified. It retains all
clock-like strings and the shortened received `VERKER` spelling.
The [morning and pioneer messages](../../cases/pages/110.md#edition-cases-military-kiew-morning-and-pioneer-reports)
are separate telegrams. Independent high-resolution review of source62
confirms G and the literal reference6915 in the former. The latter regains a readable body from the actual398-coordinate
source: the earlier OCR had a spurious399th coordinate. That correction is
source transcription, not a zero-cost cryptographic repair of an original
extra symbol.

Every proposed local edit has an exact source index, printed row/group,
plaintext index and forward witness. The complete witness is an arithmetic consistency example, not independent
authentication of the historical wording. All raw numerals and X symbols are preserved except two explicitly
priced numeral-shaped spelling repairs inside words.

## Prior work

The Nov1–3 square and ranks belong to the published key work of George Lasry,
Ingo Niebel, Nils Kopal and Arno Wacker, as documented in the preserved key
provenance. Earlier machine candidates already showed much of the schedule
and morning report; [prior_candidates.json](prior_candidates.json) retains
them, including the unreadable399-slot pioneer candidate. This source edition
makes no first historical decipherment claim.

## Reproduce

```sh
python experiments/nov3_radio_and_pioneer/verify.py --verify
python experiments/nov3_radio_and_pioneer/verify.py --verify --pdf /path/to/childs.pdf
```

Default verification uses the Python standard library and independently
implements inverse/forward column transposition, square domains, local costs,
numeral preservation and complete consistency witnesses. Optional PDF mode
checks the full source hash and every crop pixel using the stated fresh-cache
rendering policy. [Inputs](inputs.json) and [certificates](certificates.json)
retain all source and editorial layers.
