# Turkish armistice report and shipping order

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.**

The source explicitly joins **p90 B1** to **p91 A2/A3**: both pages repeat the
receiving header `OSM v LP (12.52 p.m., November 1st)`, the address/message line
`SSD SSD BVG KOSPOLI (1.11) 01.55 3 TEILE`, and consecutive part labels 1, 2, 3.
The assembly rests on those source headings and numbering, not just a shared
topic. It uses the unchanged published **Nov1–3** key.

The message reports an intercepted announcement of a Turkish armistice and
free passage through the Dardanelles and Bosporus into the Black Sea. It then
orders an end to material, coal and oil shipments to Turkey, allowing empty
ships to be sent for evacuation in agreement with the Mittelmeerdivision. The
third part gives distribution and reference fields. The order is what the
telegram says; this package does not independently verify the reported treaty
conditions or the execution of the transport instruction.

| Record | Native valid coordinates | Plaintext positions | Raw fixed | Edited fixed | Observed substitutions |
| --- | ---: | ---: | ---: | ---: | ---: |
| p90 B1 | 338 | 169 | 169 | 169 | 6 |
| p91 A2 | 344 | 172 | 172 | 172 | 2 |
| p91 A3 | 236 | 118 | 118 | 118 | 3 |
| Total | 918 | 459 | 459 | 459 | 11 |

All primary source slots contain coordinates. There is no erasure fill,
insertion, deletion, frame change or key change. “Fixed” measures single-symbol
algebraic domains, not correctness of the received characters. The eleven
word-level substitutions remain explicit, including raw numeral labels inside
ordinary words. No global numeral interpretation is altered.

## Faded glyphs

The D at **p91 A2 source39**, at the end of `VVDXD`, has a faded top.
The D at **p91 A3 source79**, at the end of `DXDXD`, has a worn right side like
several D glyphs in the same column. The primary transcriptions accept D from
their remaining shapes. Separate sensitivity variants mask each one:

- A2 plaintext position28, the I in `EINSCHL`, becomes domain **9FILOU**.
- A3 plaintext position40, the S in `AUSGLEICH`, becomes domain **3BFKQS**.

The masked variants leave those positions unresolved and retain all six exact
compatibility witnesses. They do not add a historical reading, mask fill or
physical record to the primary table. The two detail crops permit independent
inspection of the source qualification.

## Related p112 D traffic: context only

[related_traffic.json](related_traffic.json) freezes the separately reviewed
p112 D source record from
[the November3/4 radio package](../nov3_evening_and_nov4_radio/inputs.json),
including its input-file hash at the time of the snapshot. The verifier
independently decrypts that 230-coordinate record with **Nov4–6**, verifies its
already documented six substitutions and one dash fill, and compares the
relevant words and address strings. This is comparison evidence and is excluded
from all new-record counts.

The two messages differ in wording, length, headers and reference fields. Shared
terms such as `WAFFENSTILLSTAND`, `DARDANELLEN` and `BOSPORUS` establish a topic
parallel, not a same-plaintext copy. The new records have direct raw occurrences
of **BVG** and **KOSPOLI**; every occurrence in the three-record scope is listed.
Those address parallels do **not** replace p112 D's literal closing
**BVNXBEIBVGX7OSPOLIX?**. No p112 source field, key or numerical label is changed.

## Reproduction and attribution

```bash
python experiments/turkish_armistice_shipping_order/verify.py --verify
python experiments/turkish_armistice_shipping_order/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The standard-library verifier independently computes the inverse transposition,
compares it with the repository implementation, checks every source/edited pair,
and re-encrypts the full candidates. It also verifies all faded-glyph witnesses
and the frozen p112 D comparison. The optional PDF mode requires PyMuPDF and
Pillow and verifies the original PDF hash, byte length and five local crops
pixel for pixel. It does not require the temporary screening caches or any
language model.

[Inputs](inputs.json), [certificates](certificates.json),
[prior candidates](prior_candidates.json), [catalog proposal](catalog_proposal.json)
and the [readable case](../../pages/090.md#edition-cases-military-turkish-armistice-shipping-order)
retain the complete edition. All three bodies were already present in earlier
unreviewed repository screens. The bounded paper/thesis search found coal
references in the previously published Mackensen withdrawal narrative, without
an explicit separate discussion of this order. That absence is not proof of
priority. The earlier key and body-candidate credit remain explicit.
