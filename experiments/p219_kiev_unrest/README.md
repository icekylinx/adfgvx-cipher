# Kiev unrest: printed alternatives recover the p219 C body

**icekylinx and GPT-6 Astra Pro** · [Read the recovered report](../../pages/219.md#edition-cases-military-p219-kiev-unrest)

The source's parentheses, duplicate prefix and jamming annotation supply a
working 294-coordinate model under the published Nov25–28 key. It describes
Kiev unrest, the Hetman government, an unresolved opposing name, and a
soldiers' council decision for neutrality.

The selected frame excludes 15 observed coordinates from 284 printed
observations and inserts 25 unknown coordinates at the marked jamming
boundary. Before filling them it fixes **122/147 raw labels**. Seventeen
compatible lexical fills give **139/147**, without changing any retained
observed coordinate. The incomplete modifier and all opaque footer fields
remain literal.

`PETLJURA`, `ODESSA` and `MARKOWSKY` are separately priced spelling proposals.
Their combined candidate costs seven observed-coordinate substitutions and
20 inserted-slot fills, reaching **142/147**. Neither that candidate nor the
source-compatible primary is a claim of a unique historical error mechanism.

## Exact annotation model

Each of three parenthesized groups has three treatments: keep both printed
observations, keep the preceding group, or keep the parenthesized group.
The initial duplicate likewise has three treatments. All **81 maps** are
priced independently for the primary and combined optional templates.

The primary has four zero-substitution minima. They choose the printed
`VDFDD` alternative, which permits the E in `HEERESGRUPPE` as a fill.
The first parenthesized alternative leaves two distinct edited streams with
`7?` or `B?` in an opaque field. Both duplicate origins remain available.
The certificate records all prices and minimum-map evidence.

## Reproduce

```sh
python experiments/p219_kiev_unrest/verify.py --verify
python experiments/p219_kiev_unrest/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks annotation parsing, every native coordinate, source-map
retention, unchanged key, all 81 prices for each main template, every edit
and fill, complete re-encryption witnesses, and the actual Markdown strings
and quoted excerpt spans. The PDF option authenticates the original scan
and reproduces the reviewed crop pixels.

`inputs.json` and `prior_ocr.json` preserve provenance. `certificates.json`
contains native and conditional raw outputs, detailed position ledgers,
separate name prices and full source-model results. `catalog_proposal.json`
proposes this one physical source. New crop bytes are not distributed.
