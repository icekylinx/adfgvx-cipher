# Tiraspol fragment: fire at the border

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Source edition and verification: **icekylinx and GPT-6 Astra Pro**.

## p162 C2

Childs printed p162 (PDF p165), C, has an unknown recipient identifier,
`v NKJ`, and receipt `09.45 a.m., November 9th`. The page explicitly says
`missed first part of this message`. A separate 117-coordinate C1 fragment
remains unread and is excluded from the three new accepted records in
this package. The following body is independently labeled `2 TL RICHI-100`.

The [source crop](../../experiments/nov8_map_and_boundary/sources/p162_C_detail.png)
contains **100 slots**, including a printed dash at source 36 in `D-XDF`.
The unchanged published **Nov7–9** key gives 49 of 50 fixed positions.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 100-slot frame:**

```text
TIRASPOLERHIEL?MXGXFEUERANDERGRENZEXAKONACH17ROEM4
```

**Edited output — one printed-dash fill, with no observed-coordinate substitutions:**

```text
TIRASPOLERHIELTMXGXFEUERANDERGRENZEXAKONACH17ROEM4
```

</details>

**Readable German — exact nonseparator labels of the edited layer, with spacing, punctuation and conventional umlaut rendering:**

> Tiraspol erhielt M. G. Feuer an der Grenze. Akonach 17 Röm. 4.

The single fill supplies the T in `ERHIELT`; the edited body has **50 / 50
fixed positions** and re-encrypts exactly under the recorded source repair.
The terminal cleartext `NKJ UM` is outside the cipher frame and these counts.

## Scope and uncertainty

The fragment reports `M G FEUER` at a border, with the literal label
`TIRASPOL`. It does not identify a specific person, unit, border or event
from outside history. The incomplete surrounding message is not silently
restored from this short clause. The ending `AKONACH17ROEM4` remains
unexpanded, and all numeral labels remain literal.

The earlier unreviewed OCR screen already identified this body; this edition
adds source inspection and explicit fill accounting. Published key credit
and prior candidate status are retained in the
[inputs](../../experiments/nov8_map_and_boundary/inputs.json),
[certificates](../../experiments/nov8_map_and_boundary/certificates.json)
and [reproduction guide](../../experiments/nov8_map_and_boundary/README.md).
No first historical decipherment priority is claimed.

A later [p162/p166 source-family collation](../radio/nov9_wire_return_source_family.md) conditionally restores the p162 C1 prefix from the independently observed p166 copy and supplies a received-coordinate witness for this C2 dash fill. The original raw, edited and readable displays above remain unchanged.
