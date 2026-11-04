# p79 — medical formations lost in Palestine and their dissolution

The telegram reports the loss of field hospitals and medical companies in Palestine, apart from some of their personnel. It requests formal dissolution of the formations and directs the remaining personnel to replacement units at home.

**Complete edition by printed page:** [p. 79](../pages/079.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Status:** A complete two-part source edition. The second part is identical in all 336 observed coordinates to the previously reviewed p83 B. Its immediately preceding first part supplies the medical-formation antecedent that was missing from the p83-only edition.

Source edition and comparison: **icekylinx and GPT-6 Astra Pro**. The unchanged **Oct28–31** key is credited to Lasry, Niebel, Kopal and Wacker. The existing [p83 dissolution reading](formation_dissolution.md) and earlier unreviewed p79 A1 candidate retain prior credit; no existing physical record is added again.

## Meaning

The telegram reports that field hospitals labelled 212,213 and 219, medical company 300 and a replacement medical company in Palestine have been lost, except for portions of their personnel. A request has been made to declare these formations dissolved, and their remaining personnel are to proceed to replacement units at home.

This identifies the antecedent of “these formations” in p83 B. The reading is evidence of what the telegram reports; it does not independently establish the circumstances of the losses or a casualty total. Unit numbers remain the literal labels supplied by the published key, without a new numerical interpretation.

## Source

Childs printed page 79 / PDF page 82 gives:

<details>
<summary>Literal source transcription</summary>

**Source transcription — clear header and/or literal source record:**

```text
A) OSM v LP (4.02 p.m., October 30th)
SS DD AN TUERK GR H QU (GEN V SEECKT)
1310 (30/10) 2 TEILE
1 TL RICHI-262
2 TL RICHI-336
```

</details>

The first and second parts contain 262 and 336 printed slots. The first includes one P-shaped glyph outside the ADFGVX alphabet; it is retained literally in the input and treated as an unknown coordinate. The second is entirely valid coordinate text.

The p83 repeat is separately headed4.09 p.m. on30 October. Both interception times remain as printed. The exact ciphertext equality connects the second parts without assuming a particular relay or retransmission chronology.

## p79 A1

Raw decryption:

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
NACHMELDUNGDESFELDSANCHEFSSINDDIEF?LDLAZX212X213X219XSANXKPX300XUNDXERSXSANXKPXINXPALAESTINABISAUFTEILEDESPERSONALSVERLORENGEGANGEN
```

**Edited output:**

```text
NACHMELDUNGDESFELDSANCHEFSSINDDIEFELDLAZX212X213X219XSANXKPX300XUNDXERSXSANXKPXINXPALAESTINABISAUFTEILEDESPERSONALSVERLORENGEGANGEN
```

</details>

The E in `FELDLAZ` fills the invalid-glyph coordinate at index 134. It costs **one source-mask fill and zero observed-coordinate substitutions**. All other 130 plaintext positions are direct readings.

## p79 A2

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
BEIMXKXMXISTBEANTRAGTSIEFUERAUFGELOESTZUERKLAERENXXNOCHVORHANDENESPERSONALDIESERFORMATIONENISTZUDENHEIMISCHENERSATZTRUPPENTEILENINMARSCHZUSETZENXOHLXRMX1XCXNRX103577XOP
```

</details>

This is a direct168-position reading with no source repairs. The verifier checks its full336-coordinate equality with the frozen p83 B transcription; the match is not limited to a selected plaintext passage. `K.M.` and the closing reference remain source abbreviations and labels.

## Counts and verification

The two new physical records contain **598 native coordinate slots and 299 plaintext positions**, with 298 raw fixed positions and 299 in the edition. There are **zero known-coordinate substitutions**, one mask fill, and no added, deleted or reordered coordinates. The published key remains unchanged.

The total includes the repeated second part; it is not299 entirely new message characters. The new contextual result is the explicit link from p83's dissolution instruction to the named medical formations in the contiguous p79 first part.

[Inputs](../../experiments/palestine_medical_dissolution/inputs.json) preserve both manual transcriptions, header information and exact crop provenance. [The certificate](../../experiments/palestine_medical_dissolution/certificates.json) verifies all repairs, source positions, round trips and the complete duplicate. [The README](../../experiments/palestine_medical_dissolution/README.md) gives reproduction commands and attribution limits.

</details>
<!-- CASE-EDITION:END -->
