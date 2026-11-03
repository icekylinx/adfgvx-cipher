# Turkish armistice report: stop supply shipments and send evacuation ships

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p90 B1 and p91 A2/A3, PDF pp93–94, form one source-labeled
three-part message. Both pages repeat the receiving header
`OSM v LP (12.52 p.m., November 1st)` and the line
`SSD SSD BVG KOSPOLI (1.11) 01.55 3 TEILE`. The consecutive 1, 2, 3
labels support the assembly. All parts use the unchanged **Nov1–3** key.

The message reports news from an intercepted radio transmission, then
gives shipping instructions. It should be read as a historical report
and order, rather than independent confirmation of the reported armistice
conditions or of ships actually sailing.

## p90 B1

The [first-part crop](../../experiments/turkish_armistice_shipping_order/sources/p90_B1.png)
has **338 valid coordinates**, matching `1 TL RICHI-338`.

**Raw output — native 338-coordinate frame:**

```text
BVGXKOSPOLIXXNACHAUFGEFANG7NEMFUNKSPRUCHWAFFENSTILLSTANDTUERHEIMITENTE8TAABGESCHLOSZENXBEDINGUNGENDOPPELTUNKTFREIEDURCHFAHRTXDARDANELLENXUNDXBOSPORUSXINSCHWARZESMEERSTOP
```

**Edited output — six observed-coordinate substitutions, with no fills:**

```text
BVGXKOSPOLIXXNACHAUFGEFANGENEMFUNKSPRUCHWAFFENSTILLSTANDTUERKEIMITENTENTEABGESCHLOSSENXBEDINGUNGENDOPPELPUNKTFREIEDURCHFAHRTXDARDANELLENXUNDXBOSPORUSXINSCHWARZESMEERSTOP
```

**Readable German — spacing and punctuation:**

> BVG, Kospoli. Nach aufgefangenem Funkspruch Waffenstillstand Türkei
> mit Entente abgeschlossen. Bedingungen, Doppelpunkt: freie Durchfahrt
> Dardanellen und Bosporus ins Schwarze Meer. Stop.

The raw labels **7** in `AUFGEFANG7NEM` and **8** in `ENTE8TA` are
repaired through the listed local source substitutions. This does not
relabel those symbols elsewhere or change the key. **BVGXKOSPOLI** is
already fully present in the raw output.

## p91 A2

The [second-part crop](../../experiments/turkish_armistice_shipping_order/sources/p91_A2.png)
has **344 valid coordinates**, matching `2 TL RICHI-344`.

**Raw output — native 344-coordinate frame:**

```text
KEINERLEIMATEVIALTRANSPORPEEINSCHLXKOHLEXUNDXOELXMEHRNACHXTUERKEIXABSENDENXLEDIGLICHLEERDAMPFERFUERRAEUMUNGSZWECKEIMEINVERNEHMENMITMITTELMEERDIVISIONNACHXKOSPOLIXSENDENSTOP
```

**Edited output — two observed-coordinate substitutions, with no fills:**

```text
KEINERLEIMATERIALTRANSPORTEEINSCHLXKOHLEXUNDXOELXMEHRNACHXTUERKEIXABSENDENXLEDIGLICHLEERDAMPFERFUERRAEUMUNGSZWECKEIMEINVERNEHMENMITMITTELMEERDIVISIONNACHXKOSPOLIXSENDENSTOP
```

**Readable German — spacing and punctuation:**

> Keinerlei Materialtransporte einschl. Kohle und Oel mehr nach Türkei
> absenden. Lediglich Leerdampfer für Räumungszwecke im Einvernehmen mit
> Mittelmeerdivision nach Kospoli senden. Stop.

The two changes are source **219 V→F** and **291 G→A**, repairing
`MATEVIAL` and `TRANSPORPE`. The destination and the order's distinction
between material shipments and empty evacuation ships remain as directly
decrypted in the source.

## p91 A3

The [third-part crop](../../experiments/turkish_armistice_shipping_order/sources/p91_A3.png)
contains **236 valid coordinates**, matching `3 TL RICHI-236`.

**Raw output — native 236-coordinate frame:**

```text
GLXSXMXSTXDTSCHXSGABXZUGLXFUERXSCHIFFSAUSQL7ICHXXETRASOXBVGXRUMXKOSPOLIXSXAXBERLINXXFECHXRMX2XGROSSXBXRMX5XBXFRX52758X
```

**Edited output — three observed-coordinate substitutions, with no fills:**

```text
GLXSXMXSTXDTSCHXSTABXZUGLXFUERXSCHIFFSAUSGLEICHXXETRASOXBVGXRUMXKOSPOLIXSXAXBERLINXXFECHXRMX2XGROSSXBXRMX5XBXFRX52758X
```

**Readable German — spacing and punctuation of the abbreviated distribution:**

> Gl. S. M. St. Dtsch. Stab, zugl. für Schiffsausgleich. Etra SO.
> BVG. Rum. Kospoli. S. A. Berlin. FECH. RM. 2. Gross B. RM. 5. B.
> FR. 52758.

The abbreviations, including **GL**, remain unexpanded. The candidate
repairs `SGAB` and `AUSQL7ICH`; it does not infer an organization from
the reference or change any surviving numerical field.

## Conditional interpretation, source qualifications and related traffic

The three primary records contain **459 / 459 algebraically fixed
positions**, before and after the eleven disclosed substitutions. Fixed
positions may still carry received errors. There are no erasure fills,
insertions, deletions, frame changes or key changes in the primary edition,
and all three complete edited candidates re-encrypt exactly.

Two faded D glyphs have separate masked sensitivity variants. A2 source
**39** gives plaintext position **28**, the I in `EINSCHL`; masking it
leaves domain **9FILOU**. A3 source **79** gives position **40**, the S
in `AUSGLEICH`; masking it leaves domain **3BFKQS**. The variants leave
these positions unknown and retain all six possible re-encryption
witnesses. They do not silently fill the glyphs from the desired words.

The separate [p112 D source edition](../../experiments/nov3_evening_and_nov4_radio/inputs.json)
also reports an armistice and access through the Straits, under the later
Nov4–6 key. A [frozen comparison](../../experiments/turkish_armistice_shipping_order/related_traffic.json)
retains its original source and records every raw **BVG** and **KOSPOLI**
occurrence in the present three-part message. These are useful contextual
parallels, but the messages differ in wording, length and headers. They
are not established as retransmissions of the same plaintext. In
particular, this edition leaves p112 D's **BVNXBEIBVGX7OSPOLIX?**
unchanged.

The bodies already appeared in earlier unreviewed repository screens,
and the published period key retains its credit. No historical
first-solution claim is made. The
[inputs](../../experiments/turkish_armistice_shipping_order/inputs.json),
[certificates](../../experiments/turkish_armistice_shipping_order/certificates.json)
and [reproduction instructions](../../experiments/turkish_armistice_shipping_order/README.md)
preserve the complete source, edited coordinates and limits.
