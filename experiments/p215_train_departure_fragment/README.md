# p215 B1: conditional train-departure fragment

**icekylinx and GPT-6 Astra Pro** · [Read the partial edition](../../pages/215.md#edition-cases-military-p215-train-departure-fragment)

The original prints 145 coordinate slots against an advertised 220 and marks
missing groups after the first ten. The resulting conditional frame fixes
**37/110 raw positions**. Limited word proposals reach **77/110 with zero
observed substitutions**, using three printed-mask fills and 39 added-slot
fills. All 33 remaining unknowns stay in the displayed text.

The proposal retains `ALPEN????`, the opaque fields and `DIV ST ?U`. It does
not complete the Alpine unit name or supply a preposition before the second
proposed `SZEGED`. The damaged coordinate at native index 42 is carried as
both X and A; each source layer has its own complete global re-encryption
witness and the same displayed partial proposal.

## Reproduce

```sh
python experiments/p215_train_departure_fragment/verify.py --verify
python experiments/p215_train_departure_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks the source snapshot, unchanged registered square and ranks,
all native-coordinate origins and half-pair domains, exact edit/fill prices,
both source-glyph alternatives, complete re-encryption, and the actual Markdown
quotation and raw/edited/source displays. The optional PDF check authenticates
the original source and reproduces its crop pixels.

A separate diagnostic prices the proposed twelve-letter opening under 21
even frame lengths from 200 through 240, for both glyph readings. This is a
candidate-conditioned diagnostic, not a uniqueness theorem about the source.
The accepted layer remains explicitly conditioned on the advertised 220-slot
frame and the printed missing-groups note.

`inputs.json` contains the source, assumptions and declared words;
`certificates.json` contains both full coordinate ledgers and the remaining
domains. `prior_ocr.json` preserves the earlier unreviewed block. Only B1 is
proposed for the catalogue; the existing B2 edition retains its own record.

Historical source: J. Rives Childs. Period-key credit: Lasry, Niebel, Kopal and
Wacker (2016), and Lasry's 2017 key list. Conditional partial recovery and exact
source accounting: **icekylinx and GPT-6 Astra Pro**.
