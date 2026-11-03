# Tobacco ready for loading at Poti: a November 3 inquiry

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p113 section C reports tobacco at Poti ready for loading and asks
when loading will be possible. Its native **212-slot frame** gives **106/106
fixed output positions** under the unchanged published **Nov1–3** key. The
edited reading makes **one observed-coordinate substitution**, supported by
an unedited repetition of the same abbreviation at the end of the message.
There are no source-mask fills, insertions, deletions or source reorderings.


**Reviewed source crops:** [p113_reviewed.png](../../experiments/nov3_poti_tobacco_loading/sources/p113_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## p113 C

[Reviewed source image — source-PDF reference](../../experiments/nov3_poti_tobacco_loading/inputs.json).

**Source transcription — header:**

```text
Page heading: 3rd NOVEMBER, 1918.
C) POT v NKJ (8.42 a.m., November 4th)
SS FÜR POT V OSM (3) 1430
RICHI-212
```

The embedded `28X10` is retained as a separate date-like label. Its readable
rendering as `28/10` does not replace the November 3 page heading or
November 4 intercept date. The literal header and complete grouped
ciphertext are preserved in the
[inputs](../../experiments/nov3_poti_tobacco_loading/inputs.json).

**Raw output — native 212-slot frame; 106/106 fixed positions:**

```text
28X10XSCHUTZOFFZRSCHIFFZAUSGLXPOTIXKXAXSAGTPOTI2400TONSTABAKVERLADEBEREITXWANVERLADGMOEGLICHXSCHIFFSAUSGLX
```

**Edited output — 1 observed-coordinate substitution; no fills; 106/106 fixed positions:**

```text
28X10XSCHUTZOFFZRSCHIFFSAUSGLXPOTIXKXAXSAGTPOTI2400TONSTABAKVERLADEBEREITXWANVERLADGMOEGLICHXSCHIFFSAUSGLX
```

The proposed change is **source index 81 F→V**, changing the first
`SCHIFFZAUSGL` to `SCHIFFSAUSGL`. The closing raw `SCHIFFSAUSGL` already
supplies this spelling without any repair. The exact internal match and
complete re-encryption are checked in the certificate; this is a local
editorial proposal, not a change to the key or the literal transcription.

**Readable German — complete edited stream, with spacing and punctuation only:**

> 28/10. Schutzoffz. R. Schiffsausgl. Poti. K. A. sagt Poti 2400 Tons Tabak verladebereit. Wan Verladg moeglich. Schiffsausgl.

The isolated **R**, the abbreviation **K. A.**, the single-N spelling **Wan**
and the shortened **Verladg** remain visible. The text does not silently
supply a second N, turn R into a separator, or expand an abbreviation into
an identified office. `2400` is the literal numerical field returned by
the published square; its historical numeral assignment is not independently
proved by this reading.

**Meaning:** A report that tobacco is ready to load at Poti is followed by
an inquiry about when loading will be possible. The message reports
readiness and asks a question; it does not establish that a shipment left,
identify a vessel, or authenticate the quantity independently of the
cipher's numerical labels.

## Source restoration and prior credit

The source's final row visibly prints **ADVXD**. Earlier repository OCR had
**ADV?D**. Restoring that observed X gives the complete native raw reading;
it is an OCR correction, not a supplied historical coordinate. The old OCR
block is frozen with its recomputed unchanged-key output in
[prior candidates](../../experiments/nov3_poti_tobacco_loading/prior_candidates.json).

J. Rives Childs's historical scan remains the source. Published period-key
recovery by George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker, and Lasry's
2017 key list, retain their credit. This is a source-reviewed edition and
explicitly priced word repair; no first-decipherment priority is asserted.

[Inputs](../../experiments/nov3_poti_tobacco_loading/inputs.json),
[certificates](../../experiments/nov3_poti_tobacco_loading/certificates.json)
and [reproduction instructions](../../experiments/nov3_poti_tobacco_loading/README.md)
preserve the key, all source and plaintext positions, the one changed
coordinate, the internal word witness and a complete re-encryption.
