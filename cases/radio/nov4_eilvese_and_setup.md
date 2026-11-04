# November 4: Eilvese reception and a setup notice

The proposed reading addresses the German military attache, refers to 8303.18 and asks whether the embassy can also receive undamped Eilvese transmissions. It does not establish the reception equipment or the outcome of that request.

**Complete edition by printed page:** [p. 120](../pages/120.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

The embassy reception query contains an ambiguous overprint; its declared frame makes that uncertainty explicit. The separate short setup notice is a native 56-coordinate record. Both preserve all reference and location labels.

## p120 A

Childs p120, PDF p123; [source crop](../../experiments/nov4_radio_and_departure_queries/sources/p120_A.png). Key: unchanged published **Nov4–6**.

<details>
<summary>Source and cipher evidence</summary>

**Source transcription — literal received header:**

```text
4th NOVEMBER, 1918.
A) OSM v OUI (11.16 p.m., November 4th)
1950 (4)
RICHI-236
```

**Raw output — conditional 236-slot frame, excluding the overprinted source slot 188; 117/118 fixed positions:**

```text
DEU?SCHMILIATTACHEXXKJDORTX8303X18XISTHELTERTSVERANLASSTXKANN8ORSCHAFTAUCHUNGEDAEMPFTXEILVESEEMPFANGENNACHCHEF4B47883X
```

**Edited output — 7 observed-coordinate substitutions and 1 source-mask fill; same conditional exclusion; 118/118 fixed positions:**

```text
DEUTSCHMILIATTACHEXXZUDORTX8303X18XISTWEITERESVERANLASSTXKANNBOTSCHAFTAUCHUNGEDAEMPFTXEILVESEEMPFANGENNACHCHEF4B47883X
```

</details>

Observed source changes, with zero-based indices: **2 F→V**, **7 V→X**, **34 D→G**, **169 A→V**, **171 G→F**, **186 X→F**, **200 A→V**.

Source-mask fills: **0→A**.

The full edited stream re-encrypts under its stated frame and listed changes.

**Readable German — complete edited stream, with spacing and punctuation only:**

> Deutsch Miliattache. Zu dort 8303.18 ist Weiteres veranlasst. Kann Botschaft auch ungedaempft Eilvese empfangen? Nachchef 4 B 47883.

**Meaning:** The proposed reading addresses the German military attache, refers to 8303.18 and asks whether the embassy can also receive undamped Eilvese transmissions. It does not establish the reception equipment or the outcome of that request.

### Six printed slots and a conditional exclusion

The sixth group of ciphertext row 5 has six spatial glyph positions:
`XXF[T-like overprint]VA`. The literal transcription uses `XXFTVA`, with T
masked as outside the coordinate alphabet. The [detail crop](../../experiments/nov4_radio_and_departure_queries/sources/p120_A_overprint.png)
shows the overstrike. There are **237 source slots**, against `RICHI-236`.
The displayed frame excludes source slot **188**, the masked overprint,
retaining every one of the source's **235 valid coordinates**. A cancellation
is possible, but its intention is not proved; this is a conditional one-slot
exclusion, not a claim of a native five-letter group.

Every local single-slot exclusion is priced against the same proposed text:

| Excluded source slot | Literal | Observed coordinates excluded | Observed substitutions | Source-mask fills |
|---|---|---:|---:|---:|
|185|X|1|6|2|
|186|X|1|6|2|
|187|F|1|7|2|
|188|T-like overprint|0|7|1|
|189|V|1|7|2|
|190|A|1|8|2|

The fewer substitutions in two alternatives are accompanied by deletion of
an observed coordinate and an extra fill. The table is a cost vector, not an
invented single numerical ranking. No other historical damage geometry is
excluded by this local comparison.

The restoration `HELTERTS→WEITERES` is an editorial lexical proposal. It is
not authenticated by a second source. The complete reading preserves the
abbreviations `DEUTSCH MILIATTACHE`, `NACHCHEF` and reference `8303.18`.
The question mark after *empfangen* is editorial question punctuation,
not an extra unresolved decoded position.

## p120 C

Childs p120, PDF p123; [source crop](../../experiments/nov4_radio_and_departure_queries/sources/p120_C.png). Key: unchanged published **Nov4–6**.

<details>
<summary>Source and cipher evidence</summary>

**Source transcription — literal received header:**

```text
C) UKS v ZON (2.10 a.m., November 5th)
2332 (4)
RIZI-56
```

**Raw output — native 56-slot frame; 28/28 fixed positions:**

```text
0500ABBAUXAPFBAUNAGQBESCEREK
```

**Edited output — 1 observed-coordinate substitution and 0 source-mask fills; 28/28 fixed positions:**

```text
0500ABBAUXAUFBAUNAGQBESCEREK
```

</details>

Observed source changes, with zero-based indices: **51 X→V**.

The full edited stream re-encrypts under its stated frame and listed changes.

**Readable German — complete edited stream, with spacing and punctuation only:**

> 0500 Abbau. Aufbau NAGQBESCEREK.

**Meaning:** A short notice gives 0500, dismantling and setup, followed by the literal location-like token NAGQBESCEREK. That spelling is not replaced with a modern place-name identity.

### Literal locality and time labels

The source-visible second group on the last row is `VFVFX`; an early low-resolution transcription of its third glyph as T is rejected by the crop. No historical mask or fill is introduced there. Only `APFBAU→AUFBAU` is proposed. `0500` and `NAGQBESCEREK` stay literal; the latter is not silently changed to a familiar locality spelling.

## Attribution and evidence

Earlier unreviewed repository candidates already suggested these bodies. This edition checks the primary images, preserves conflicting source labels and publishes every frame operation, coordinate substitution and fill. Prior published key recovery keeps its original credit; no first-solution priority is claimed.

[Inputs](../../experiments/nov4_radio_and_departure_queries/inputs.json), [certificates](../../experiments/nov4_radio_and_departure_queries/certificates.json), [earlier candidates](../../experiments/nov4_radio_and_departure_queries/prior_candidates.json) and [reproduction](../../experiments/nov4_radio_and_departure_queries/README.md) provide complete source and positional evidence.

</details>
<!-- CASE-EDITION:END -->
