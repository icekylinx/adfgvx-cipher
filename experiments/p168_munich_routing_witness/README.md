# Full p168 C retransmission and KDO support

Research and review: **icekylinx and GPT-6 Astra Pro**. Apache-2.0.

The earlier p158 component certificate omitted a full p168 C decode because its
six-coordinate `VDADDD` group was unresolved. The new source review also retains
the separate four-coordinate `VVVG` group: the literal total is 280, matching the
header, but the two local length errors still disrupt ordinary transposition.

A conditional frame excludes one repeated D and inserts one unknown in the
short group. It fixes 139/140 raw positions with all 279 retained observations
unchanged. Thirty source-directed frames are compared against original p159 B
observations; twelve ownership aliases attain six disagreements. They comprise
three equivalent D exclusions and four insertion positions. The four unfilled
streams agree at 136/140 positions.

A V observed in p159 B supplies the added coordinate in each alias. All twelve
then produce the same 140-position source-linked text. Garbled words and digit
labels remain literal. The square's unassigned 5/6 cells are not assigned.

The fully observed p168 pair VG supplies K in `GEN KDO`. Applying its G to p159
source 169 is an explicit X→G substitution that changes only the H of its earlier
`GEN HDO` reading. It does not silently normalize the rest of that message.

The optional joint reconciliation prices both sides. The two-witness version
uses five observed substitutions in p168 plus its single V fill, and the one
KDO substitution in p159; it retains `1ABEL`. Adding the V at original p158 source 7
allows a sixth p168 substitution and selects `KABEL`. This sixth observation
is not attributed to p159's invalid R. Every changed coordinate has an original
printed donor, and `DOWPELT` remains unnormalized.

## Verify

```sh
python experiments/p168_munich_routing_witness/verify.py --verify
python experiments/p168_munich_routing_witness/verify.py --verify --pdf /path/to/childs.pdf
```

Verification checks literal source bytes, domains, all 30 frames, every optimal
ownership description, the observed donor V, the one-coordinate KDO change,
two fresh same-shape controls and complete roundtrips for both global 5/6 orders.
Source pixels are explicitly unchecked unless the original PDF is supplied.

- [Source edition](../../pages/168.md#edition-cases-radio-p168-munich-routing-witness)
- [Inputs and source-crop recipe](inputs.json)
- [Recomputed certificate](certificates.json)
- [Earlier p158 composite edition and historical credit](../../pages/158.md#edition-cases-p158)

This is an improved certificate for an existing catalogue record. Childs's
wartime reading and Lasry and colleagues’ 2016 discussion retain prior body
credit; the source-frame review and coordinate comparison are the current work.
