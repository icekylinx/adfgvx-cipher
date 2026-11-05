# Completing references across the 16–18 November traffic

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
| --- | ---: | --- |
| [p201 A1](../../pages/201.md#edition-cases-finance-odessa-wagon-sale-p201-a1) | 124 → **125/127** | Consular reference **8?** |
| [p202 B4](../../pages/202.md#edition-cases-military-military-intendant-remit-b4-clothing-meat-sutlery-and-wartime-services) | 106 → **109/112** | `RM ? A 5?5? A 11 18` |
| [p204 D](../../pages/204.md#edition-cases-radio-nov16-18-command-inquiries-p204-d) | 39 → **40/42** | `VOM 15`, followed by the preserved separators |
| [p206 B1](../../pages/206.md#edition-cases-military-nov18-negotiation-repetition-p206-b1) | 120 → **122/124** | **1125?**; one additional `1XA` separator |
| [p206 B2](../../pages/206.md#edition-cases-military-nov18-negotiation-repetition-p206-b2) | 113 → **114/118** | **11225** |
| [p207 A2](../../pages/207.md#edition-cases-military-repatriation-orders-equipment-and-horses-p207-a1a2) | 102 → **107/110** | `5?18 / 11 / 18` and `25?? / 18` |
| [p207 C1](../../pages/207.md#edition-cases-military-repatriation-orders-finland-p207-c1c2) | 101 → **102/104** | Finland-report reference **?8?** |

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

## Odessa courier footer

The same assignments add one further native position in [p201 C](../../pages/201.md#edition-cases-radio-odessa-courier-pretransposition): **ZT? Nr. 1?1118**, taking the existing word edition from **160 to 161/163** fixed positions. The final **8** uses the observed **FD** pair at received positions **187** and **289**. Both retained fractionation-loss maps and the conservative overstrike branch preserve it; the latter advances from **158 to 159/163**.

The four earlier observed substitutions and two fractionation fills remain the full repair cost. The [courier certificate](courier_certificate.json) checks both forward models under all **720** surviving squares, retains all **30** ordered alternatives for the two remaining reference cells, and checks all **36** fillings of the two source-glyph masks in each geometry.

## Reproduce

```sh
python experiments/nov16_18_reference_completion/verify.py --verify
python experiments/nov16_18_reference_completion/verify_courier.py --verify
```

The verifier reads the previous source editions, checks every affected
native pair, re-encrypts each record under all 720 surviving squares, and
compares the two current p206 quotations and displayed reference fields
with their exact streams. The input pins the earlier evidence files;
their source images and original repair ledgers remain with those packages.

[Inputs](inputs.json) · [Position certificates](certificates.json).
