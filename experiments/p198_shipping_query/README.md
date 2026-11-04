# p198 A: wheat purchase price, freight and insurance

**icekylinx and GPT-6 Astra Pro** · [Read the recovered query](../../cases/pages/198.md#edition-cases-naval-p198-shipping-query)

The irregular p198 A transmission becomes a readable query under the
registered Nov7–9 key and a source-directed group model. It asks for the
purchase price, ship freight and transport insurance on wheat delivered to
Poti at the end of September. Names `??PASIA`/`IBALIA`, quantity `11??0K`
and the received `TRANSPOR` spelling remain visible.

| Measure | Count |
|---|---:|
| Native printed slots | 247 |
| Observed ADFGVX coordinates | 237 |
| Invalid letters and dashes | 10 |
| Excluded native slots in selected model | 4, including three observed coordinates |
| Added unknown slots | 1 |
| Conditional model positions | 122 |
| Fixed raw labels | 111 |
| Fixed edited labels | 118 |
| Observed-coordinate substitutions | 5 |
| Printed-mask fills | 6 |
| Added-slot fills | 1 |

## Exact source scope

The first two groups each have six glyphs, the `XGAX` group has four, and
the final six coordinates exceed the advertised 244-slot frame. The verifier
prices every allowed exclusion/insertion in this source-defined family:
6 × 6 × 5 × 15 = **2,700 maps**. Four attain the minimum five observed
substitutions for the stated readable template. The verifier recomputes every price. The certificate retains the complete
price-table digest, cost histogram, minimum origins, fill costs and unresolved
domains.

The selected map preserves more observed coordinates than the other minima.
It does not fix the first steamer's name. The exact globally coupled
quantity frontier has 12 strings; 432 complete plaintext/ciphertext witnesses
cover the remaining selected-frame uncertainty without independently
assigning the two unknown square cells.

The primary source preserves two C-like glyphs at indices 49 and 192 as
invalid letters. All four C/G readings are independently repriced. A G at
192 would fix another vessel-name label; the primary keeps it unresolved.

## Reproduce

```sh
python experiments/p198_shipping_query/verify.py --verify
python experiments/p198_shipping_query/verify.py --verify --pdf /path/to/childs.pdf
```

Default checks reproduce the source map, native odd-frame diagnostic,
conditional raw output, every coordinate edit/fill, all 2,700 geometry
prices, all 432 complete re-encryptions and the actual Markdown displays.
The PDF option also authenticates and regenerates the reviewed crop pixels.
New source-image bytes are not required: the original PDF reference and
exact crop recipe are retained in `inputs.json`.

The 15 November source dates remain unchanged. The registered key is cited
with its published earlier credit. The original p198 D challenge remains
separate from this source A edition.
