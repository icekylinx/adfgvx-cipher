# Oil cartel at Tiflis: details of shipments from Poti

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition: icekylinx and GPT-6 Astra Pro.** Childs p212, 22 November 1918; published `Nov22-24` key, unchanged. [Source crop](../../experiments/medical_return_transports/sources/p212_A3.png), [inputs](../../experiments/medical_return_transports/inputs.json), [exact certificate](../../experiments/medical_return_transports/certificates.json).

This query asks the oil cartel at Tiflis to report when, where, to which address and by which ship their consignments were loaded from Poti. It does not provide the requested answers.

## p212 A3

The source prints `RICHI 224` but **no visible “3 TL” label**. `A3` is the catalog's positional identifier for the block between numbered parts 2 and 4. The query is kept separate from the surrounding medical passages; a shared subject or complete seven-part assembly is not assumed.

All 224 coordinates are observed. Raw, 112 positions:

**Raw output:**

```text
OELKARTELLVIFLISXNUMM3R2XDRAHTETWANNWOHINWOLCHEADRESSEMITWELCHEMSCHCFFUNSEREPARTIENVONPOTIVERLADENSINDXXDEUTKAUF
```

Five observed-coordinate substitutions yield the conservative candidate:

**Edited output:**

```text
OELKARTELLTIFLISXNUMMER2XDRAHTETWANNWOHINWELCHEADRESSEMITWELCHEMSCHIFFUNSEREPARTIENVONPOTIVERLADENSINDXXDEUTKAUF
```

The candidate repairs `VIFLIS`, `NUMM3R`, `WOLCHE` and `SCHCFF`. The reference label `2`, `POTI` and `DEUTKAUF` remain unchanged. The raw 3 in the damaged word is retained in the certificate; no digit is globally relabeled.

An earlier unreviewed repository candidate already recognized the body. This edition adds literal source checking, all coordinate indices, full re-encryption and the explicit separation from the neighboring medical report. It does not claim first historical decipherment.
