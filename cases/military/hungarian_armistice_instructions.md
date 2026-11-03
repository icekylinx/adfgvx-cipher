# Hungarian armistice negotiations: troop departure and instructions requested

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p124 A1/A2/A3, PDF p127, are one source-labeled three-part message:
`LP v NKJ (7.17 p.m., November 5th)`; `1715 (4/11) 3 TLE`.
The consecutive part labels and native lengths **352 / 266 / 48** establish
the assembly. All three use the unchanged published **Nov4–6** key.

## p124 A1

The [first-part crop](../../experiments/hungarian_armistice_instructions/sources/p124_A1.png)
contains **352 valid coordinates** and **176 / 176 fixed plaintext positions**.

**Raw output — native 352-coordinate frame:**

```text
ANOXHXLXOPXHEERESGRUPPEKOOVESHATWAFFENSTILLSTANDSVERHANDLUNGENFDERUNGARISCHETRUPPENEINGELEITETXDEUTSCHETRUPPENSOLLENSOBALDALSMOEGLICHPNGARISCHENUNDSUEDSLAVISC3ENBODENVERLASSEN0
```

**Edited output — three observed-coordinate substitutions, with no fills:**

```text
ANOXHXLXOPXHEERESGRUPPEKOOVESHATWAFFENSTILLSTANDSVERHANDLUNGENFUERUNGARISCHETRUPPENEINGELEITETXDEUTSCHETRUPPENSOLLENSOBALDALSMOEGLICHUNGARISCHENUNDSUEDSLAVISCHENBODENVERLASSEN0
```

The changes are source **80 G→A**, **110 F→V** and **306 X→V**. They
repair `FDER`, `PNGARISCHEN` and `SUEDSLAVISC3EN`. The name string
**KOOVES** and the final **0** are unchanged.

**Readable German — spacing, punctuation and umlauts; the literal closing 0 is retained:**

> An O. H. L. Op. Heeresgruppe KOOVES hat Waffenstillstandsverhandlungen
> für ungarische Truppen eingeleitet. Deutsche Truppen sollen sobald
> als möglich ungarischen und südslavischen Boden verlassen. 0.

The final 0 remains an uninterpreted label. The edition does not turn
KOOVES into an independently identified person's name. The message
reports negotiations and says German troops are to leave; it does not
show that the departure occurred.

## p124 A2

The [second-part crop](../../experiments/hungarian_armistice_instructions/sources/p124_A2.png)
contains **266 valid coordinates** and **133 / 133 fixed plaintext positions**.

**Raw output — native 266-coordinate frame:**

```text
AXOXKX11NSTBEAUFTRAGTXZWEIGENERLSTABSOFFIZIEREZUDENVERHANDLUNGENZUENTSENDENXWEISUNGENANAXJXKX11UNDHIER3ERFUERDIEVERHANDLUNGENERBETENX
```

**Edited output — three observed-coordinate substitutions, with no fills:**

```text
AXOXKX11ISTBEAUFTRAGTXZWEIGENERLSTABSOFFIZIEREZUDENVERHANDLUNGENZUENTSENDENXWEISUNGENANAXOXKX11UNDHIERHERFUERDIEVERHANDLUNGENERBETENX
```

The changes are source **16 X→V**, **88 D→G** and **106 G→A**. They
repair `11NST`, the second `A J K` sequence, and `HIER3ER`. The first
`A O K 11` and both occurrences of 11 remain as already decoded.

**Readable German — spacing, punctuation and one explicitly supplied spelling letter in brackets:**

> A. O. K. 11 ist beauftragt, zwei Gener[a]lstabsoffiziere zu den
> Verhandlungen zu entsenden. Weisungen an A. O. K. 11 und hierher für
> die Verhandlungen erbeten.

The source-derived string is **GENERLSTABSOFFIZIERE**, with no A between
R and L. The bracketed A appears only in the readable display. It is not
a recovered plaintext position, an insertion into the cipher, or part of
the repair count. The message reports an assignment and requests
instructions; it does not state that the officers had already arrived.

## p124 A3

The [third-part crop](../../experiments/hungarian_armistice_instructions/sources/p124_A3.png)
contains **48 valid coordinates** and **24 / 24 fixed plaintext positions**.

**Raw output — native 48-coordinate frame:**

```text
OXKXMXROEMX1XAX11222XOPX
```

**Edited output — unchanged, with zero substitutions or fills:**

```text
OXKXMXROEMX1XAX11222XOPX
```

**Readable German — spacing and punctuation, with abbreviations unexpanded:**

> O. K. M. Röm. 1. A. 11222. Op.

## Conditional interpretation and source-defined OCR correction

Earlier OCR merged the second part with the first 40 coordinates of the
third part, introduced extra symbols into two groups, and omitted A3's
final **VDFFA FAA** row. The scan explicitly labels separate **2 TL**
and **3 TL** frames and supplies the eight omitted coordinates. The
[frozen OCR snapshot](../../experiments/hungarian_armistice_instructions/ocr_snapshot.json)
and [certificate](../../experiments/hungarian_armistice_instructions/certificates.json)
replay the exact correction: two OCR-only symbol deletions, two resolved
OCR masks, the part boundary after 266 coordinates, and the visible A3
final row. A1's separate masked F at source index 194 is also resolved
visually. The old shared OCR corpus is unchanged.

These transcript corrections are distinct from the six proposed changes
to visible historical coordinates. Across the three records, **666 valid
coordinates** give **333 / 333 fixed positions** in the source-defined
frames. All three edited streams re-encrypt exactly. There are **six
observed-coordinate substitutions, zero fills and no historical source
insertions, deletions or key changes**. A2's bracketed display letter
adds nothing to those counts. The damaged separate p124 B is excluded.

A1's body already appeared in an earlier unreviewed repository candidate;
the old A2/A3 OCR artifacts and published key credit are also preserved.
This source edition makes no historical first-solution claim. See the
[inputs](../../experiments/hungarian_armistice_instructions/inputs.json)
and [reproduction instructions](../../experiments/hungarian_armistice_instructions/README.md).
