# Grosswardein and Poestyen in the withdrawal traffic

**Source comparison and edition: icekylinx and GPT-6 Astra Pro.**

The repeated place fields in [p226 A2](../../cases/radio/radio_traffic_transfer_fragment.md#the-repeated-place-grosswardein)
restore **Grosswardein** in a radio-traffic transfer notice. A contemporary
newspaper adds context to the already established **Poestyen** reading in
[p217 A3](../../cases/military/p217_A.md#poestyen-and-the-contested-route).

## A repeated place in the radio notice

The first place is `GROSSW0RDEIN` under the published labels, or
`GROSSW7RDEIN` under the existing shared square. The later field is
`GROSSVARDEIN`, whose A is an original **VD** pair from source positions
57 and 149. The opening A requires **one observed substitution, source
81 G→D**, changing **VG** to **VD**. Its W is already received; the later
V spelling remains unchanged. All indices are zero based.

The original source visibly prints G, so the change is a word repair.
The *Bácskaer Volkszeitung*, no. 31, 3 August 1913, PDF p2, independently
prints **Großwardein**. The issue's scanned title says **IX Jahrgang**;
this differs from the online catalogue's year-volume label.

| Layer | Observed substitutions | Printed-mask fills | Fixed positions |
|---|---:|---:|---:|
| Earlier word edition, published labels | 1 | 3 | 92/93 |
| With Grosswardein repair, published labels | 2 | 3 | 92/93 |
| With the earlier calendar fill and shared square | 2 | 4 | 91/93 common to both branches |

The date remains **4 December / SCHWERE 15** or **5 December / SCHWERE 14**.
Each branch gives a complete 93-position string and re-encrypts exactly;
the place repair supplies no new date evidence. It identifies one damaged
word without increasing the fixed-label count. A, W and V have unchanged
square values in both branches.

## Poestyen in the contemporary press

The [earlier shared-Y result](../p215_hungarian_y/README.md) already gives
`POESTYEN` from p217 A3's native `POEST4EN`. It uses **DD**, source positions
139 and 222, at plaintext position 57. The new case display applies that
published interpretation; this package does not count it as a new recovery.

The *Hamburgischer Correspondent* of **22 November 1918**, morning issue,
Zweites Blatt p2 (PDF p7), carries a Budapest dispatch dated 21 November
and attributed to the *Pester Lloyd*. The report names Poestyen in a dispute
over Czech occupation. Its account of neighboring communities under Czech
control provides a contemporary comparison for the telegram's transit
and disarmament difficulties. It does not independently establish the
reported battalion movement.

## Sources and checks

[Grosswardein newspaper](https://epa.oszk.hu/05600/05686/00377/pdf/EPA05686_bacskaer_volkszeitung_1913_031.pdf#page=2)
· [Poestyen newspaper](https://img.sub.uni-hamburg.de/kitodo/PPN689065248_19181122/PDF/PPN689065248_19181122.pdf#page=7)
· [Inputs and original-PDF crop recipes](inputs.json)
· [Exact coordinate certificate](certificate.json).

The newspaper title and text regions were visually inspected. The input
records their full PDF hashes, page numbers, crop rectangles and RGB hashes;
no newspaper image is duplicated here. The source notices and historical
key retain their earlier Childs and Lasry-team attribution.

```sh
python experiments/late_place_comparison/verify.py --verify
```

The verifier reconstructs the inverse column map independently, checks the
native supporting letters, prices every source change, preserves both date
branches, and checks complete forward encryption. To reproduce the original
source crop and the four historical image regions:

```sh
python experiments/late_place_comparison/verify.py --verify \
  --pdf /path/to/childs.pdf \
  --grosswardein-pdf /path/to/EPA05686_bacskaer_volkszeitung_1913_031.pdf \
  --poestyen-pdf /path/to/PPN689065248_19181122.pdf
```
