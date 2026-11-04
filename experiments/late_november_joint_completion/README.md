# Late-November word and shared-key completion

**icekylinx and GPT-6 Astra Pro.** Published keys retain the Lasry–Niebel–Kopal–Wacker attribution.

## p225 A: six missing letters

The native 232-coordinate key-service notice has five printed dashes and one
invalid `R`. Completing `STATION`, `DA`, `EINGEGANGEN`, `TELEGD` and
`SCHLUESSELN` fills six half-pairs and advances **110/116 to 116/116 positions**.
All **226 valid coordinates** survive. The literal `NICGT` and `TELEGD` can
then be read as `NICHT` and `TELEGR` at **two separately counted substitutions**.
`NSL` occurs twice and remains unchanged.

The [source edition](../../cases/pages/225.md#edition-cases-radio-late-november-cipher-instructions)
connects this notice about missing December tables with the separate agreement
on p228 to share a key. No particular November day is supplied.

## p225 B2 and p227 D: the same J cell

Two complete native sources independently preserve the pair `FA` where their
phrases require `JEDE` or `JEDER`:

| Record | Native phrase | Plaintext position | Original source positions | Pair |
| --- | --- | ---: | --- | --- |
| p225 B2 | `1EDE UNTERSTUETZUNG GEFUNDEN` | 67 | 194, 48 | `FA` |
| p227 D | `IST 1EDER KAMPF ZT VERMEIDEN` | 31 | 3, 105 | `FA` |

The published label at `FA` is `1`. The earlier
[late-key interpretation](../late_key_interpretation/README.md) already leaves
this cell among the unused symbols `0457J`; its separate historical map
assigns the baseline `J` cell, `VV`, to `2`.
A shared lexical **`FA = J`** therefore fits both unmodified pairs without
assigning J twice. The two baseline editions each changed `FA` into `VV` to
read J. Keeping their original coordinates instead reduces their combined
word-repair cost from **six to two substitutions**:

| Record | Baseline-key word repairs | Shared-J word repairs |
| --- | ---: | ---: |
| p225 B2 | 2 (`1EDE → JEDE`) | 0 |
| p227 D | 4 (`1EDER → JEDER`, `ZT → ZU`) | 2 (`ZT → ZU`) |

This adds a lexical interpretation to the prior historical, separator, Y and Q
layers. Their assumptions remain attached, including the contemporary source's
questioned identification of the 89th Division. Four cells remain unassigned,
with distinct values from `0457`: **24 globally consistent squares**, down
from 120. No remaining digit or date is chosen.

The prior Y and numeral layers also read p225 B2's `POEST7EN` as `POESTYEN`
and its final `RGTJX` as `RGT21`. The native spelling `SILEIN`, intervening
`I` labels and arrival-day field `2?` remain as transmitted.

## Reproduce

```sh
python experiments/late_november_joint_completion/verify.py --verify
```

The verifier reads the existing literal inputs and source crops, checks their
hashes, reconstructs column offsets independently, and prices every proposed
coordinate. All 24 complete-square witnesses re-encrypt both the native and
edited donor records. The six service-message fills are also re-encrypted
with the unchanged published key. The [inputs](inputs.json) and
[certificate](certificates.json) retain the separate layers and exact costs;
source images and earlier certificates are reused.
