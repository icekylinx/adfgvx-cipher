# Approval-request clause in p116 A13

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The unchanged source in the [route edition](README.md) supports the conditional words
`EINVERSTAENDNIS` at positions 65–79 and `ERBETEN` at 81–87. Added to the
route proposal, they fix **90/111 positions**, with **zero observed-coordinate
changes, 11 printed-mask fills and 43 lost-tail fills**. This adds 15 letters:
13 retain an observed half-coordinate; V at 68 and N at 87 are wholly missing
and are supplied by the word proposal. The earlier 75-position route layer
remains reproducible unchanged.

**Edited output — optional route and approval proposal, 90/111 positions:**

```text
TEILENDERX???ARMEEDENMARSCHDURCHUNGARNAUFOBERSCHLESIENANZUTRETEN?EINVERSTAENDNIS?ERBETEN???XK????M???A?1G?????X
```

**Readable German — conditional word breaks, all unresolved positions retained:**

> TEILEN DER X ??? ARMEE DEN MARSCH DURCH UNGARN AUF OBERSCHLESIEN ANZUTRETEN ? EINVERSTAENDNIS ? ERBETEN ??? X K????M???A?1G?????X

The added words request agreement to the proposed withdrawal. The historical
English translation in [Table 3, row 13](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf#page=21)
says “Approval is requested.” It guided this
proposal, but supplies neither independent German wording nor missing cipher
coordinates. Childs and the 2016 authors retain the historical decipherment
credit.

Position 80 remains `?`, with the observed half-pair `?V` and domain `3BFKQS`.
An optional S at that position gives `EINVERSTAENDNISSERBETEN` and **91/111**
fixed positions, costing one further lost-tail fill (model slot 194). This
doubled-S spelling is a separate possibility. A separator X is incompatible
with the observed half-pair; it is not silently substituted. The army label
and closing fields remain unresolved.

Each proposed word has a unique zero-substitution placement in the fixed
frame. The [approval certificate](approval_extension.json) retains the
complete repair ledgers, full roundtrip witnesses and bounded comparisons
against fourteen specified word alternatives. This comparison tests those
words and this geometry, rather than all possible German texts.

```sh
python experiments/p116_optional_route_fragment/verify_approval.py --verify
```

Add `--pdf /path/to/childs.pdf` to authenticate the original page pixels.
