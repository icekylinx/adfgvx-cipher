# p79 — medical formations lost in Palestine and their dissolution

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Status:** A complete two-part source edition. The second part is identical in all336 observed coordinates to the previously reviewed p83 B. Its immediately preceding first part supplies the medical-formation antecedent that was missing from the p83-only edition.

Source edition and comparison: **icekylinx and GPT-6 Astra Pro**. The unchanged **Oct28–31** key is credited to Lasry, Niebel, Kopal and Wacker. The existing [p83 dissolution reading](formation_dissolution.md) and earlier unreviewed p79 A1 candidate retain prior credit; no existing physical record is added again.

## Meaning

The telegram reports that field hospitals labelled212,213 and219, medical company300 and a replacement medical company in Palestine have been lost, except for portions of their personnel. A request has been made to declare these formations dissolved, and their remaining personnel are to proceed to replacement units at home.

This identifies the antecedent of “these formations” in p83 B. The reading is evidence of what the telegram reports; it does not independently establish the circumstances of the losses or a casualty total. Unit numbers remain the literal labels supplied by the published key, without a new numerical interpretation.

## Source

Childs printed page79 / PDF page82 gives:

```text
A) OSM v LP (4.02 p.m., October 30th)
SS DD AN TUERK GR H QU (GEN V SEECKT)
1310 (30/10) 2 TEILE
1 TL RICHI-262
2 TL RICHI-336
```

The first and second parts contain262 and336 printed slots. The first includes one P-shaped glyph outside the ADFGVX alphabet; it is retained literally in the input and treated as an unknown coordinate. The second is entirely valid coordinate text.

The p83 repeat is separately headed4.09 p.m. on30 October. Both interception times remain as printed. The exact ciphertext equality connects the second parts without assuming a particular relay or retransmission chronology.

## p79 A1

Raw decryption:

```text
NACHMELDUNGDESFELDSANCHEFSSINDDIEF?LDLAZX212X213X219XSANXKPX300XUNDXERSXSANXKPXINXPALAESTINABISAUFTEILEDESPERSONALSVERLORENGEGANGEN
```

Edition:

```text
NACHMELDUNGDESFELDSANCHEFSSINDDIEFELDLAZX212X213X219XSANXKPX300XUNDXERSXSANXKPXINXPALAESTINABISAUFTEILEDESPERSONALSVERLORENGEGANGEN
```

The E in `FELDLAZ` fills the invalid-glyph coordinate at index134. It costs **one source-mask fill and zero observed-coordinate substitutions**. All other130 plaintext positions are direct readings.

## p79 A2

```text
BEIMXKXMXISTBEANTRAGTSIEFUERAUFGELOESTZUERKLAERENXXNOCHVORHANDENESPERSONALDIESERFORMATIONENISTZUDENHEIMISCHENERSATZTRUPPENTEILENINMARSCHZUSETZENXOHLXRMX1XCXNRX103577XOP
```

This is a direct168-position reading with no source repairs. The verifier checks its full336-coordinate equality with the frozen p83 B transcription; the match is not limited to a selected plaintext passage. `K.M.` and the closing reference remain source abbreviations and labels.

## Counts and verification

The two new physical records contain **598 native coordinate slots and299 plaintext positions**, with298 raw fixed positions and299 in the edition. There are **zero known-coordinate substitutions**, one mask fill, and no added, deleted or reordered coordinates. The published key remains unchanged.

The total includes the repeated second part; it is not299 entirely new message characters. The new contextual result is the explicit link from p83's dissolution instruction to the named medical formations in the contiguous p79 first part.

[Inputs](../../experiments/palestine_medical_dissolution/inputs.json) preserve both manual transcriptions, header information and exact crop provenance. [The certificate](../../experiments/palestine_medical_dissolution/certificates.json) verifies all repairs, source positions, round trips and the complete duplicate. [The README](../../experiments/palestine_medical_dissolution/README.md) gives reproduction commands and attribution limits.
