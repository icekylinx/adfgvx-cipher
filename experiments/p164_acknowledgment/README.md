# Central source gaps: partial receipt acknowledgement

**Source edition and review: icekylinx and GPT-6 Astra Pro.**

[Read p164 D](../../pages/164.md#edition-cases-radio-p164-acknowledgment) · [Certificate](certificates.json) · [Original Childs scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)

The native **116-coordinate / 58-position** p164 D source partly reads as an acknowledgement addressed to O.H.L. and closing with O.K.M. Its raw word ERHAITEN becomes the ordinary ERHALTEN after **two observed-coordinate substitutions**, at zero-based source indices 50 and 73. The complete reference groups remain literal.

The earlier p164 contextual output already contains all 58 raw labels. This package adds a separately readable partial source edition and exact word-repair account. It does not present the opaque references as recovered prose.

| Layer | Fixed positions | Source changes |
| --- | ---: | --- |
| Native raw output | 58/58 | None |
| Partial acknowledgement reading | 58/58 | Two substitutions; zero fills, additions, exclusions or reorderings |

DORTNO, GEH, RM 1A11329OP and RM 1AI1312OP are preserved. ERHALTEN supports the receipt interpretation; GEH is not expanded and no reference number is selected.

```sh
python experiments/p164_acknowledgment/verify.py --verify
python experiments/p164_acknowledgment/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks the exact source, published key, native and edited re-encryption, repair ledger and actual Markdown strings. The optional PDF check reproduces the reviewed crop. The [prior snapshot](prior_snapshot.json) retains the earlier contextual output and source credit. The Lasry-team period key remains unchanged.
