# Silk resale continuation confirmed by a third source

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[Case index](../README.md) · [ADFGVX Cipher](../../README.md)

## p144 A2

**Status:** 135 native plaintext positions, 0 unresolved in raw output; 1 observed-coordinate substitution and 0 source-mask fills in the proposal. No source position, frame length, key or numerical label is silently changed.

**Source and dates:** Page heading: 6th NOVEMBER, 1918; A) NKJ v LP (9.16 p.m., November 6th); 2 TL RICHI-270.

![Source p144 A2](../../experiments/nov6_resale_and_air_reconnaissance/sources/p144_A2.png)

**Raw output:**

```text
NICHTUNBEDINGTSICHERGESTELPTXISTNACHMOEGLICHKEITDORTWIEDERVERKAUFTWERDENXMERCATORKRIEGSAMTKRIEGSROHSTOFFABTEILUNGXRX138XSTRICHXELFXKRAX
```

**Edited output — counted proposal:**

```text
NICHTUNBEDINGTSICHERGESTELLTXISTNACHMOEGLICHKEITDORTWIEDERVERKAUFTWERDENXMERCATORKRIEGSAMTKRIEGSROHSTOFFABTEILUNGXRX138XSTRICHXELFXKRAX
```

**Readable German — the same candidate labels with spacing and punctuation:**

> Nicht unbedingt sichergestellt, ist nach Moeglichkeit dort wieder verkauft werden. Mercator, Kriegsamt, Kriegsrohstoffabteilung. R. 138, Strich, elf, KRA.

**Meaning:** A surviving second part directs local resale where transport cannot be assured. The sentence starts in the preceding part, known from p136 B1. The continuation names Mercator and the War Office raw materials department. The printed and decoded reference 138 is retained.

**Conditional interpretation and evidence:** This is the second part only. The p136 B1 witness supplies the preceding clause about silk purchases and uncertain transport; it is not reconstructed from p144 alone. The sole plaintext change is `GESTELPT` → `GESTELLT`, priced as source 146 `D` → `A`. Both older raw continuation witnesses already have `GESTELLT`. Every one of the 135 proposed positions is therefore supported by an unedited paired reading in native p144 or native p152. The p136 comparison retains its separately supplied missing `F`, as already documented in the older certificate.

The source group `XAFFF` at 160–164 independently confirms the full five-coordinate group corresponding to p136's short `XAFF`. This establishes the missing coordinate value and full group, not which indistinguishable `F` was historically omitted. See the [earlier challenge 152 case](../p152.md).

### Explicit source changes

All indices are zero-based. Unknown slots retain their position.

| Source index | Printed | Proposed | Cost |
|---:|---|---|---|
| 146 | `D` | `A` | Observed-coordinate substitution |

### Reproducibility and attribution

The [input](../../experiments/nov6_resale_and_air_reconnaissance/inputs.json) binds the literal transcription to exact PDF crops. The [certificate](../../experiments/nov6_resale_and_air_reconnaissance/certificates.json) gives the raw paired-coordinate domains, every source change, and the forward checks. The [verifier](../../experiments/nov6_resale_and_air_reconnaissance/verify.py) reproduces them without changing the published Nov4–6 key.

This edition is by icekylinx and GPT-6 Astra Pro (2026). Childs supplies the historical source; Lasry, Niebel, Kopal and Wacker supply the published reconstruction and key provenance. Earlier repository OCR and the p136/p152 continuation analysis are retained in the [attribution record](../../experiments/nov6_resale_and_air_reconnaissance/prior_candidates.json). No first-decipherment priority is claimed.
