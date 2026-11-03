# p164 D — Partial receipt acknowledgement

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and review: icekylinx and GPT-6 Astra Pro.** The 116 native coordinates fix all 58 raw output positions. The readable portion addresses O.H.L., acknowledges receipt and ends with O.K.M.; its reference fields remain opaque.

## p164 D

**Readable German — partial acknowledgement; opaque fields retained verbatim:**

> An O. H. L. DORTNO RM 1A11329OP GEH erhalten. O. K. M. RM 1AI1312OP.

The ordinary-word proposal ERHALTEN supports a receipt acknowledgement. DORTNO, GEH, RM 1A11329OP and RM 1AI1312OP remain literal. The edition does not expand GEH or select a document number.

**Source transcription — all 116 native coordinates:**

```text
FXDDV FVVVG AAVAF XVGXD VGGVX DDVAX AFVFX XGFVV
GVVGV AFDAA GAFVG GVVXG AVGGD DGXXD DFAGD XXVFX
FGGVG VVGVF GAVDV VVVFA VDXDV DFXDX FXFDD V
```

**Raw output — unchanged Nov7–9 key, complete native frame:**

```text
ANOXHXLXDORTNOXRMX1A11329OPXGEHXERHAITENOXKXMXRMX1AI1312OP
```

**Edited output — two observed-coordinate substitutions, zero fills or frame changes:**

```text
ANOXHXLXDORTNOXRMX1A11329OPXGEHXERHALTENOXKXMXRMX1AI1312OP
```

Changing source indices 50 and 73 from G to D replaces raw I with L in ERHAITEN → ERHALTEN. Every other coordinate and output position is retained. All 58 positions are fixed in both layers; the word repair improves interpretation without adding recovered labels.

## Source and credit

Childs printed p164 / PDF p167, section D. Literal header: `D) LP v NKJ (6.38 p.m., November 9th); 1230 VON UKS; RICHI-116`.

[Original source PDF](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Source package](../../experiments/p164_acknowledgment/README.md) · [Exact certificate](../../experiments/p164_acknowledgment/certificates.json).

The earlier p164 constraint certificate already records the complete raw contextual output. This edition promotes it to a separately readable partial source edition with a precise acknowledgement interpretation and repair account. Earlier context and the published Lasry-team period key retain their credits in the [prior snapshot](../../experiments/p164_acknowledgment/prior_snapshot.json).

## Reproduce

```sh
python experiments/p164_acknowledgment/verify.py --verify
python experiments/p164_acknowledgment/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks source length, unchanged key, both re-encryptions, exact word-repair indices and the actual displayed source, raw output, edited output and readable quotation. The optional PDF check verifies the original crop pixels.
