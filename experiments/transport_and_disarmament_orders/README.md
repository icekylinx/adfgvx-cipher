# Native p209 transport and disarmament traffic

Prepared by **icekylinx and GPT-6 Astra Pro**. Published Nov19–21 key: Lasry, Niebel, Kopal and Wacker. See the complete [source edition](../../cases/military/transport_and_disarmament_orders.md).

Five physical records are supplied: A1, B1/B2 and C1/C2. A1 is only the first part of a source-marked two-part message; its Prague/Mackensen/Teschen clause is incomplete. B concerns priority for Ukrainian provisions over raw materials. C reports arms handed to the Poles in Warsaw and instructs units against disarmament without fighting.

## Accounting

| Record | Source slots | Raw fixed → edited fixed | Observed substitutions | Dash fills |
|---|---:|---:|---:|---:|
| p209 A1 | 224 | 104/112 → 112/112 | 0 | 8 |
| p209 B1 | 310 | 155/155 → 155/155 | 4 | 0 |
| p209 B2 | 230 | 115/115 → 115/115 | 3 | 0 |
| p209 C1 | 242 | 121/121 → 121/121 | 4 | 0 |
| p209 C2 | 182 | 91/91 → 91/91 | 4 | 0 |

Total: 1,188 source slots, comprising 1,180 valid ADFGVX coordinates and eight printed dashes; 594 plaintext positions, 586 raw fixed → 594 edited fixed, 15 observed substitutions and 8 printed-dash fills. There are no coordinate additions/deletions/reorderings or new key/numeral assignments. All five frames match their printed RICHI lengths.

A1's `TS8HESCHICHE`, B1's `ABMMD`/final `LEBENSMITTELM`, B2's `NOXJ0192SMXBEWEGEXBERLIN`, C1's `HABENGROSSEANZAHL` and C2's `RMJAJJ970GEHXOP` remain explicit. Fixed labels are not independently authenticated numerals. Restoring first rows missed by OCR is not charged as received-source insertion. C1's `GFXAF` is entirely visible, so its earlier OCR masks are not source erasures.

Earlier readable B2/C machine candidates and the other unsuccessful OCR frames are retained in `prior_candidates.json`. No universal decipherment-priority claim is made.

## Reproduction

From the repository root, Python3.10 or later:

```sh
python experiments/transport_and_disarmament_orders/verify.py --verify
```

The default verifier uses the standard library and repository code. It checks all input/image hashes, the published key, independent column inversion against the project decoder, every source position and exact repair price, and re-encryption consistency.

With PyMuPDF and the pinned primary scan:

```sh
python experiments/transport_and_disarmament_orders/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

This also checks the full PDF digest and independently regenerates all crop pixels from the recorded page/rectangle/scale. Source is printed209/PDF212. These checks authenticate the delivered source edition and its stated costs, not unique historical wording or unseen continuations.
