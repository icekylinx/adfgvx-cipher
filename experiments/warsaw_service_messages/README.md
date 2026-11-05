# Warsaw and LP service messages, 14–16 November 1918

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

This source edition adds four physical ciphertext records from Childs pp192
and 194. It retains the published `Nov13-15b` partial square without filling
unknown cells or relabelling digits. The record on p192 B is missing one
coordinate; its two exact, tied gap placements are both retained.

| Record | Literal slots | Valid coordinates | Model length | Fixed raw letters | Subject |
| --- | ---: | ---: | ---: | ---: | --- |
| p192 A | 350 | 349 | 350 | 171 / 175 | Request to Oberleutnant Kretzschmar in Bucharest |
| p192 B | 267 | 267 | 268 | 131 / 134 | LP forwarding important traffic for home offices and OHL |
| p194 C | 224 | 224 | 224 | 111 / 112 | Army Group Kiev's chosen march route |
| p194 E | 240 | 239 | 240 | 119 / 120 | `FRANZ` and `EMIL` control markers |
| **Total** | **1,081** | **1,079** | **1,082** | **532 / 541** | |

The p192 B fixed count is measured after inserting an **unknown** coordinate
at the declared gap, not after filling it. The conservative readable candidates
fill three erased coordinates in total and propose two changes to observed
coordinates, yielding 535 fixed plaintext positions. They preserve six unresolved
reference/garble positions and the unusual original spellings and labels.

## Recovered service messages

<a id="what-was-recovered"></a>

- **p192 A:** a request to Kretzschmar at the OKM economic staff, department 1,
  Bucharest, for news on conditions, prospects and decisions affecting the
  sender's interests. The overstruck coordinate at source index 120 can be filled
  as `F` to recover the `D` of `UND`. `OBLT0`, `LAGEN`, `DEUTKAUF5` and the three
  unknown reference symbols remain literal.
- **p192 B:** LP relays all important available messages for home offices and OHL,
  and in the reverse direction. The source contains a four-letter `FVGA` group
  and 267 coordinates against the printed `RICHI-268`. Inserting `F` at source
  gap 109 or 110 gives the same repaired ciphertext and no changes to any
  observed coordinate. The raw numerical field remains `?5?1115`.
- **p194 C:** an urgent request asking which march route Army Group Kiev will
  choose. Two observed-coordinate changes restore `MARSCHWEG` and `HEERESGRUPPE`.
  The raw `C?` after `WELCHEN` remains unresolved. An optional `XX` reading costs
  three further observed-coordinate changes and is separately certified.
- **p194 E:** future unchecked Warsaw soldiers' council messages are to carry
  `FRANZ`, and checked messages `EMIL`. The first group is literally `XFYGF`,
  containing an invalid `Y`. Filling it as `X` gives a complete 120-character
  reading without changing any valid coordinate. The plaintext itself spells
  `UNKONTOLLIERTE`, omitting the expected `R`, and uses `FRANZXXX`; both survive
  unchanged in the exact re-encryption.

## Source and uncertainty

`inputs.json` holds the literal rows, source headers, declared gap model,
editorial candidates, PDF identity and crop coordinates. In the p192 A/B headers,
the receipt/page date is 14 November while the originating date is `15/11`.
The p192 B receipt time reads **06.56 p.m.** in the source. These are retained as
printed, rather than reconciled by inference.

`certificates.json` records every plaintext pair, its exact source indices and
its domain under the published partial square. Every candidate includes its
coordinate edits and a reversible ciphertext. Full plaintext re-encryption is
claimed only where no `?` remains. The exhaustive 268-boundary p192 B screen
uses a declared ordinary-word stencil, with unknown reference symbols masked.
Its zero-change minimum is conditional on that stencil and one-coordinate-loss
model, not a proof of the historical copying event.

The certificate also applies the separate, conditional Tydelski-derived
`Nov13-15b FX=Y` assignment to all four source models, all five editorial
candidates and the second p192 B gap model. Across these ten variants it fixes
**no additional raw letter**. It only narrows explicitly listed marginal
domains. The `Nov13-15a DG=Y` transfer does not apply to these four records.

## Reproduce

```bash
python experiments/warsaw_service_messages/verify.py --verify
python experiments/warsaw_service_messages/verify.py --verify --pdf /path/to/ADFGVX.pdf
```

The second command verifies the full PDF hash and checks every retained crop
pixel against a fresh render. The [case study](../../pages/192.md#edition-cases-radio-warsaw-service-messages)
gives the literal raw and conservative candidate text.
