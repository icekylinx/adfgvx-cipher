# Naval inquiry: has the referenced SKL item arrived?

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

## p108 A

Childs p108 A, PDF p111, is headed
`OSM v LP (1.00 p.m., November 3rd)` and
`1900 (2/11) SONDERKOMMANDO IN DER TUERKEI`.
The [source crop](../../experiments/p108_naval_and_personnel/sources/p108_A.png)
contains **282 valid coordinates**, matching `RICHI-282`.
The unchanged published **Nov1–3** key gives a complete reading without
source-coordinate repairs.

**Raw output — native 282-coordinate frame:**

```text
SLX4314XAUFXGGX2890XEINSXFRAGEDOPPELPUNKTXISTXSKLXBNRXGGX546XROEMX3XNUNMEHRDORTHINGELANGTFRAGEZEICHENXADMIRALSTABSEEKRIEGSLTGXGX1121XROEMX3XX
```

**Edited output — unchanged, with zero substitutions or fills:**

```text
SLX4314XAUFXGGX2890XEINSXFRAGEDOPPELPUNKTXISTXSKLXBNRXGGX546XROEMX3XNUNMEHRDORTHINGELANGTFRAGEZEICHENXADMIRALSTABSEEKRIEGSLTGXGX1121XROEMX3XX
```

**Readable German — spacing and punctuation; DOPPELPUNKT and FRAGEZEICHEN are rendered as their punctuation marks:**

> SL. 4314. Auf GG. 2890. Eins. Frage: Ist SKL, BNr. GG. 546, Röm. 3,
> nunmehr dorthin gelangt? Admiralstab, Seekriegsltg. G. 1121. Röm. 3.

The message asks whether the item identified by **SKL BNR GG 546 ROEM 3**
has arrived. It does not report an arrival. Routing and reference
abbreviations remain unexpanded, and no numerical label is reassigned.

## Conditional interpretation and the OCR correction

The earlier corpus OCR retained only 280 coordinates, omitting the final
standalone **FX** row that is plainly visible at the bottom of the body.
It also masked source index **11**, the F in **GFGXV**. Recovering those
three visible glyphs from the scan restores the printed 282-coordinate
frame and all **141 / 141 fixed plaintext positions**. This is a correction
to the OCR transcript, not a conjectural insertion into the historical
source. The unchanged complete plaintext re-encrypts to the visible
ciphertext exactly.

The [frozen OCR snapshot](../../experiments/p108_naval_and_personnel/ocr_snapshot.json)
and [certificate](../../experiments/p108_naval_and_personnel/certificates.json)
retain the old 280-coordinate input, its output under the same key and
the exact source-visible difference. The old shared corpus is unchanged.
The neighboring personnel message has a different header and is treated
separately; adjacency alone is not used to join it to this inquiry.

The edition retains published key credit and the earlier unread OCR
candidate. Bounded prior-publication checks do not establish historical
priority, and no first-solution claim is made. See the
[inputs](../../experiments/p108_naval_and_personnel/inputs.json) and
[reproduction instructions](../../experiments/p108_naval_and_personnel/README.md).
