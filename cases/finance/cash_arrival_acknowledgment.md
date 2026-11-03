# Money-transport arrival acknowledgment

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

## p122 C

Childs p122, PDF p125; [reviewed source crop](../../experiments/nov4_repetition_and_connections/sources/p122_C.png). The unchanged published **Nov4–6** key uses the native **114-slot** frame.

**Raw output — 57/57 fixed positions:**

```text
OXKXMXWISTABXXGELDTRANSPORTANGEKOMMENXXKXMXKRIEGSAMTXAX8X
```

**Edited output — 0 observed-coordinate substitutions and 0 source-mask fills; 57/57 fixed positions:**

```text
OXKXMXWISTABXXGELDTRANSPORTANGEKOMMENXXKXMXKRIEGSAMTXAX8X
```

The edited stream is identical to the raw stream and re-encrypts to every source coordinate without repair.

**Readable German — complete edited stream, with spacing and punctuation only:**

> O. K. M. Wistab. Geldtransport angekommen. K. M. Kriegsamt A. 8.

**Meaning:** A message to O. K. M. Wistab reports arrival of a money transport. No amount, route, sender identity beyond the literal signature, or contents are inferred.

## Source limits and attribution

The header reads `NKJ v LP (08.42 p.m., November 4th)` and `FUER UKS 1405 (4).`; the ciphertext label is `RICHI-114`. The 114 source coordinates give **57/57 fixed positions**, with no repair, fill or change of key. The address and signature abbreviations are not expanded into an asserted historical identity. This acknowledgment is not used to decide the route or amount of any other money message.

An earlier unreviewed repository OCR candidate already supplies the body. This is the source-audited edition, with original key credit preserved and no first-solution assertion. [Inputs](../../experiments/nov4_repetition_and_connections/inputs.json), [certificates](../../experiments/nov4_repetition_and_connections/certificates.json), [earlier candidate](../../experiments/nov4_repetition_and_connections/prior_candidates.json), and [reproduction](../../experiments/nov4_repetition_and_connections/README.md) give the complete evidence.
