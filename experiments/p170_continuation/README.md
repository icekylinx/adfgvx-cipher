# Source editions of neighboring station and operational traffic

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Fifteen checked source records on printed pp. 166–174 contain 2,161 received slots. Nine records provide seven message groups about radio-station control, destroyed records, retained cipher keys and Seifert's arrival, return and departure. Six further records preserve overlapping operational reports about Serbian cavalry and the northward movement of German formations. A full copy on p167 supplies the missing 20-coordinate prefix of p166 part 3. The records use the published November 7–9 and November 10–12 keys.

The readable editions are [Station control and the Seifert service exchange](../../cases/other/seifert.md) and [November 9 operational reports](../../cases/other/nov9_operational_reports.md).

The central p170 challenge is **section A** and remains open. These neighboring records are catalog additions; their source arithmetic and historical priority are recorded separately.

| Artifact | Purpose |
|---|---|
| [seifert_records.json](seifert_records.json) | Nine literal source records, partial keys, raw domains and explicit editorial variants |
| [verify_seifert.py](verify_seifert.py) | Independent column arithmetic and exact edit verification, using only the Python standard library |
| [military_records.json](military_records.json) | Six literal operational-report records, the source-derived prefix, all 21 possible contiguous placements, source-union domains and explicit editorial variants |
| [verify_military.py](verify_military.py) | Checks the operational parallels with the same independent arithmetic and globally consistent witnesses for the unresolved 5/6 cell |
| [military_context.json](military_context.json) | Separately sourced historical identification of the 6th Reserve Division, led by a contemporary French telegram; original key and raw domains remain unchanged |
| [verify_military_context.py](verify_military_context.py) | Verifies four contextual digit readings with no further cipher edits and retains exact witnesses for both cipher-only alternatives |
| [Source excerpts](../../sources/excerpts/) | `childs_p168_AB.png`, `childs_p169_A.png`, `childs_p172_AB.png`, `childs_p174_BCDE.png`, `childs_p166_A_military.png`, `childs_p167_A_military.png`, `childs_p170_B_military.png` |

```sh
python experiments/p170_continuation/verify_seifert.py
python experiments/p170_continuation/verify_seifert.py --json
python experiments/p170_continuation/verify_military.py
python experiments/p170_continuation/verify_military.py --json
python experiments/p170_continuation/verify_military_context.py
```

The verifiers reconstruct all even-length inputs independently of `adfgvx.cipher`. The station verifier rejects direct decoding of the 185-coordinate p169 repeat, validates both declared one-coordinate deletion aliases, checks every known-coordinate substitution and erasure fill, and constructs global square witnesses for all five possible hundreds digits in the identical p172 B/p174 D copies. The operational verifier checks the observed 20-coordinate prefix and all 184 retained p166 coordinates, the conservative 97/102-position combined template, and every declared coordinate edit. It confirms that all four reserve-division readings refer to the same global 5/6 square cell. Both check the committed crop hashes. Add `--pdf /path/to/childs.pdf` to compare the source-PDF hash.

The prior p168 A/B historical interpretations are credited to Lasry, Niebel, Kopal and Wacker's paper, printed p. 23 / PDF p. 24; their discussion also credits Childs's decipherment of p168 B. No new substitution key or first historical decipherment is claimed.
