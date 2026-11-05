# Exact completion of the p155 shipping reading

The [case edition](../../pages/155.md#edition-cases-context-p155-completed-reading) already
proposed Asgard's arrival at Poti, the troop pickup and the acknowledgment
request in a bracketed reconstruction. This supplement supplies exact
repaired streams for both parts and binds the vocabulary to observed words
elsewhere in the collection.

| Part | Completed positions | Observed substitutions | Printed-mask fills | Added-slot fills |
| --- | ---: | ---: | ---: | ---: |
| p155 A1 | 85/85 | 2 | 1 | 0 |
| p155 A2 | 93/93 | 3 | 2 | 1 |

A1 keeps its native frame. A2 uses the advertised 186-coordinate frame;
placing the missing coordinate before source 183 or 184 gives the same
completed plaintext and ciphertext at the same cost. All 186 possible gap
positions are priced against the fixed proposed body. The four earlier raw
variants and their source transcript remain in the [original certificate](../../data/certificates/p155.json).

## Verify

```sh
python -m adfgvx.context155
python experiments/p155_shipping_completion/verify.py --verify
```

The verifier checks both legacy source readings, both minimum-cost repairs,
every source-mask and inserted-slot fill, and the live two-part quotation.
It independently decodes the cited words in p182 B, p222 A2 and p129 A8,
and the intact ASGARD occurrences in both source parts. Those witnesses
support vocabulary and the repeated name; the shipping event was already
identified in the earlier reading.

The published Nov7–9 square is unchanged. `TRESIVOLUS`, repeated names,
`7X11` and `BQZXK` remain literal. The diary context remains in the case's
existing [source review](../../data/reviews/hopman_context.json).

Source edition and verification: **icekylinx and GPT-6 Astra Pro**.
Published period key: **Lasry, Niebel, Kopal and Wacker**.
