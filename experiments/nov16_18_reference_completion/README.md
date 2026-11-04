# Completing references across the November 16–18 traffic

**Research and edition: icekylinx and GPT-6 Astra Pro.**

Two existing constraints, **FD=8** from a Monday date and **VA=5** from a
matched reporting order, determine **13 further numeral positions in seven
records**. A separate source-mask completion restores one repeated reference
prefix on p206. There are **no additional observed-coordinate substitutions**.

## Shared constraints and additional readings

The [earlier analysis](../open_targets_continuation/README.md) established
the two conditional assignments. On p204 A, `MONTAG 1?` is compatible with
**18 November 1918** under the unchanged known square cells. On p201 and
p206, the matching order number and reporting subject link a transmitted
`1? November` date to the clear **15/11** origin stamp. The assignments
retain those assumptions; the new records propagate them.

The six remaining digits are `034679`. They form **720** complete square
assignments, with repeated cells retaining the same value throughout all
records.

| Record | Earlier → conditional fixed positions | Additional reading |
|---|---:|---|
| [p201 A1](../../cases/finance/odessa_wagon_sale.md#p201-a1) | 124 → **125/127** | Consular reference **8?** |
| [p202 B4](../../cases/military/military_intendant_remit.md#b4-clothing-meat-sutlery-and-wartime-services) | 106 → **109/112** | `RM ? A 5?5? A 11 18` |
| [p204 D](../../cases/radio/nov16_18_command_inquiries.md#p204-d) | 39 → **40/42** | `VOM 15`, followed by the preserved separators |
| [p206 B1](../../cases/military/nov18_negotiation_repetition.md#p206-b1) | 120 → **122/124** | **1125?**; one additional `1XA` separator |
| [p206 B2](../../cases/military/nov18_negotiation_repetition.md#p206-b2) | 113 → **114/118** | **11225** |
| [p207 A2](../../cases/military/repatriation_orders.md#equipment-and-horses-p207-a1a2) | 102 → **107/110** | `5?18 / 11 / 18` and `25?? / 18` |
| [p207 C1](../../cases/military/repatriation_orders.md#finland-p207-c1c2) | 101 → **102/104** | Finland-report reference **?8?** |

The numeral positions all retain both observed coordinates. The source
exclusion of p207 A2's final X remains part of its earlier conditional
frame; this comparison neither adds nor removes a source slot. Existing
word repairs and unrecovered numbers remain in the certificate.

## The p206 reference prefix

Part B1 has `1?A` at plaintext positions 102–104. The middle position
has observed first coordinate `X` and one printed dash, with domain
`ACKMOX`. Three fully received prefixes read `1XA`: B1 positions 38–40
and B2 positions 14–16 and 33–35. Completing the same format supplies
**F at source position 219**, giving separator pair `XF`.

This is a local formula-based completion, rather than a second reception
of the whole damaged reference. It leaves all reference digits untouched
and raises B1's total mask-fill count from five to **six**. Its three
observed-coordinate word repairs are unchanged.

The combined result adds fourteen fixed positions: thirteen numerals and
one separator. These are additions to the seven-record snapshot here;
the earlier p204, p205, p206 A and p203 C consequences are not counted again.

## Reproduce

```sh
python experiments/nov16_18_reference_completion/verify.py --verify
```

The verifier reads the previous source editions, checks every affected
native pair, re-encrypts each record under all 720 surviving squares, and
compares the two current p206 quotations and displayed reference fields
with their exact streams. The input pins the earlier evidence files;
their source images and original repair ledgers remain with those packages.

[Inputs](inputs.json) · [Position certificates](certificates.json).
