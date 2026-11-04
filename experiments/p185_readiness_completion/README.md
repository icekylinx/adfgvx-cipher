# Trucks and readiness to depart — p185 D

**Research and edition: icekylinx and GPT-6 Astra Pro.**

The existing five-coordinate-loss frame now supports the conditional clause:

> […] marschiert Lastautos morgen 1500 ueber DHFN. Abmarschbereit sein. […] Seifert.

This completes the vehicle noun and the departure-readiness instruction,
fixing **95 of 99 positions**, up from 91. The opening designation, `1500`,
`DHFN` and the damaged closing instruction retain their literal labels.
See the [source and readable case](../../cases/pages/185.md#edition-cases-context-transport-truck-movement-and-readiness).

## Coordinate account

| Word or phrase | Observed substitutions | Printed-glyph fills | Missing-slot fills |
|---|---:|---:|---:|
| `LCST?UT?S → LASTAUTOS` | 2 | 1 | 0 |
| `AB?A6SCHBE?EITSEIN → ABMARSCHBEREITSEIN` | 1 | 0 | 2 |

The three substitutions are source **146 G→V**, **183 X→V** and **187 G→F**.
The invalid printed **Y at159** is filled as X. Model positions55 and56,
inside the earlier five-coordinate gap, are filled as A and F. Three gap
positions remain unknown. All indices are zero-based.

The original page and enlarged [p185 D source](../../sources/excerpts/childs_p185_D.png)
confirm the four printed glyphs. These are editorial changes and a fill,
not corrections to the source transcription. The published square is unchanged.

## Wording and geometry

The same-key source traffic supplies intact `LASTAUTO` in p198 C,
`ABMARSCH` in p193 C and `BEREIT` in p196 B. The certificate reconstructs
every coordinate pair in these vocabulary witnesses. They support the
proposed words without treating the messages as copies of one sentence.

The body stencil covers the central movement and readiness clause, masking
the time labels and everything outside that clause. All **194** placements
of a five-coordinate gap are checked. Exactly **52,53,54,55** attain the
minimum of three observed substitutions. Gap55 remains the earlier
representative; its lexical fit is not a unique reconstruction.

The complete raw stream, exact edited stream, source maps, remaining domains,
all gap costs and an injective reencryption witness are in
[certificate.json](certificate.json). The original source and earlier
heuristic rankings remain in the [transport certificate](../../data/certificates/p185_D_transport.json).

```sh
python experiments/p185_readiness_completion/verify.py --verify
```

[Inputs and dependencies](inputs.json) · [Verifier](verify.py).
