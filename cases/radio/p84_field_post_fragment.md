# p84 C — German field-post fragment

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[All cases](../README.md) · [ADFGVX Cipher](../../README.md)

**Recovery and review: icekylinx and GPT-6 Astra Pro, 4 November 2026.**
A source-directed frame and corpus phrase search identify **Deutsche Feldpost**
in this interrupted reception. The unchanged October 28–31 key fixes **14/122
raw positions**; the conditional word layer fixes **28/122**, with no observed
coordinate changed. Most of the message remains unread.

## Reading

**Readable German — the conditional word fragment; all surrounding passages remain unresolved:**

> […] Deutsche Feldpost […]

**Meaning:** The fragment names the German field-post service. It does not yet
establish a postal address, a post-office number, or the purpose of the message.
The raw `9` and `7` labels elsewhere in the stream remain literal.

## Source and frame

Childs, printed p84 / PDF p87, gives `C) FUER COS (4.30 a.m., November 1st)`
and `1810 (30); RICHI-244`. The page heading is October 30, and the explicit
`(30)` dating agrees with the October 28–31 key used here. The reception ends
with the annotation **Balance jammed**.

**Source transcription — all 118 printed slots, including seven dash masks and the four-character FDFG group:**

```text
AFDAX AXGFD GXAVV AXDVG DAADV VXAGX GDVAA AXGGX
AAAXA FXDDG DXXGX DFDVF FAXXX FXGGA AXGFG FDFG
DADDA AVAFV XGXAD AAAAX DVXAF XAXXG FA--- ----
```

The conditional frame inserts one unknown inside or immediately beside the
short group `FDFG`, then adds 125 unknown tail slots to reach the advertised
244. All **111 observations and seven printed masks** retain their source
identities, values and relative order. Nothing is excluded.

The missing short-group coordinate can occupy any of five positions, before
zero-based source indices 75–79. All five maps are retained. They have the
same 14 raw letters and the same word-layer price; other half-coordinate
domains differ. The primary map inserts before source 76, the leading score
in the length diagnostic. Its exact position is not established.

## Raw and edited output

**Raw output — common to all five 244-slot frames; 14/122 fixed positions; no coordinate substitutions or fills:**

```text
??9????????G????????U????????E????????R????????D????????E????????7????????S????????N????????M????????N????????E????????G??
```

**Edited output — DEUTSCHEFELDPOST at zero-based positions 47–62; zero observed substitutions, two printed-mask fills and 15 added-tail fills; 28/122 fixed positions:**

```text
??9????????G????????U????????E????????R????????DEUTSCHEFELDPOST??7????????S????????N????????M????????N????????E????????G??
```

The sixteen-letter proposal has **15 observed supporting coordinates**:
`D` at 47 and `E` at 56 are already fixed; eleven further letters retain one
observed half. Three letters are wholly absent and supplied by the word
hypothesis: **H at 53, F at 55, T at 62**. The inserted short-group slot itself
remains unknown. Ninety-four plaintext positions remain unresolved.

The proposal fits all five frames without changing a source observation.
Keeping the native prefix and placing all 126 added slots at the end instead
would require four observed substitutions for the same phrase at the same
position. That comparison is word-conditioned, not proof of a unique frame.

## Search and review

The length diagnostic tested **12,617 models**: eleven complete published
keys, every even total length from 118 to 500, and either no internal loss or
one loss inside `FDFG`. October 28–31 at the advertised 244 slots ranked first.
Four fresh source-shaped controls recovered all displayed letters while
sometimes preferring another loss position or nearby length.

A separate search compared every substring alignment in **331 strictly raw
corpus streams** against the target half-coordinate domains. Its sole phrase
with at least twelve letters and twelve observed supporting coordinates was
`XDEUTSCLEFELDPOST` from [p210 C](../people/richter_aleppo.md). The donor's raw
`L` is a known textual blemish; target position 53 has no observed half, so
**H is a lexical completion**, not a copied coordinate. This is a vocabulary
match, not evidence that the two telegrams repeat one another.

One hundred frequency-preserving shuffled sources were each searched across
all five frames and the full donor corpus. Their strongest matches had at
most eleven observed supporting coordinates, versus fifteen here. This
calibration is conditional on the already selected key and 244-slot family;
it does not account for earlier searches or prove the historical wording.

[Exact domains, fills and complete witnesses](../../experiments/p84_field_post_fragment/certificates.json)
· [Search controls and replay](../../experiments/p84_field_post_fragment/README.md).
Independent review checked the original PDF pixels, every source map, all
610 plaintext domains, the repair ledger and complete re-encryption. Residual
witness fills serve only to check the arithmetic.

## Credit

Historical source: J. Rives Childs. Published October 28–31 key: George Lasry,
Ingo Niebel, Nils Kopal and Arno Wacker (2016), and Lasry's 2017 key list.
Source-frame search, corpus retrieval and conditional edition:
**icekylinx and GPT-6 Astra Pro**.
