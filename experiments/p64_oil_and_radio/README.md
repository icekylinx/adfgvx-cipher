# p64: the Nobel oil inquiry and the Damascus radio report

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

This package supplies three physical source records from Childs printed
p64, PDF p67, using the unchanged published **Oct4–6** key. A's two parts
ask for oil-related information and contain the names **BENEDIKT**,
**NOBEL**, and **HAGELIN**. B is a separate report about the Damascus
radio station and a smaller transmitter at Aleppo.

**The two-part oil body was already published by Lasry, Niebel, Kopal
and Wacker in 2016, §6.6 and Table 5, author PDF pp25–26.** Their body
and historical discussion receive explicit prior credit. All three
parts also appeared in earlier unreviewed repository screening. This
edition contributes exact source transcription, coordinate repair
certificates and explicit limits on annotated or unresolved fields.

Read the [oil inquiry](../../cases/caucasus/nobel_oil_inquiry.md) and
the [radio report](../../cases/radio/damascus_aleppo_report.md).

## Native frames and source annotations

| Record | Source slots | Valid coordinates | Raw fixed / positions | Edited fixed / positions | Observed substitutions | Printed-dash fills |
|---|---:|---:|---:|---:|---:|---:|
| p64 A1 | 346 | 345 | 172 / 173 | 173 / 173 | 4 | 1 |
| p64 A2 | 354 | 354 | 177 / 177 | 177 / 177 | 5 | 0 |
| p64 B | 176 | 175 | 87 / 88 | 87 / 88 | 1 | 0 |
| **Total** | **876** | **874** | **436 / 438** | **437 / 438** | **10** | **1** |

Every native frame matches its printed RICHI length. There is no modeled
insertion, deletion, group movement or change to the published square.
The figures use the accepted source glyphs described below; they are
counts of fixed model outputs, not independently authenticated historical
characters or amounts.

A's first surviving block has no printed `1 TL`; **A1** is this edition's
catalog label. The following block explicitly says `2 TL`. The header
also says **Beginning lost** and leaves one call sign blank. That note
is retained, while the surviving 346-slot body already matches its
advertised length. No extra prefix is supplied from conjecture.

Three right-edge glyphs in A1 are faded. The primary readings at source
indices **39, 119, 159** are **V, X, F**, with a separate enlarged
[glyph crop](sources/p64_A1_faint_glyphs.png). A sensitivity variant masks
all three without changing their slots or the literal transcript. It
has 169 / 173 raw fixed positions; the same edited candidate then needs
four mask fills instead of one, in addition to the same four observed
substitutions. That alternative is excluded from the primary totals.

A2 contains the printed groups **`(X)XVVG`** and **`GFD(X)`**. Each marked
X is one coordinate, at source indices **90** and **353**. The parentheses
are preserved in `source_rows` as qualification punctuation; they are
not additional cipher coordinates. The main reading accepts both
printed X values. All three nonempty subsets of those two positions
are also evaluated as masks, without a length change.

## Exact coordinate repairs

All indices are zero-based in the original native source frame.

| Part | Observed-coordinate substitutions | Printed-dash fills |
|---|---|---|
| A1 | 3 D→V; 42 A→F; 123 F→D; 251 G→F | 0→V |
| A2 | 19 D→X; 90 X→A; 91 X→F; 105 D→F; 272 X→D | None |
| B | 28 G→X | None |

The A2 substitution at **90** acts on one of the parenthesized X values.
If that marked coordinate is instead treated as unknown, the same word
repair becomes one mask fill and the observed-substitution count falls
from five to four. This price change is explicit in the alternative
certificate; it is not hidden in the primary accounting.

[certificates.json](certificates.json) includes each raw pair, its complete
domain, both source indices, and every change. It uses an independent
column-offset inverse and compares the result with the project cipher
implementation. Both complete oil candidates re-encrypt exactly. The
radio fragment and the reference sensitivity variants receive complete
enumerations of their remaining one-coordinate masks.

## Native wording versus the prior paper

The A1 candidate retains **DRINGENE** and the A2 candidate retains
**BETREFFEN**. The paper's word-spaced table uses **DRINGENDE** and
**BETREFFEND**, respectively. This edition does not add the extra D
to either exact decoded stream. A readable German presentation may
explicitly bracket the first grammatical normalization, without
counting it as an encoded character.

The candidate also retains the repeated **ATOM** and does not silently
replace it with another place. The paper discusses a possible identity
for Hagelin, but the literal name and its position in a relayed or quoted
message do not independently establish the individual, author or sender.

The main A2 raw reference is **12059**. Its `5` at plaintext position
175 depends on the **parenthesized X at source 353**. Masking that value
gives pair `?G` and domain **57DSTU**. The sensitivity edition leaves
`120?9` unresolved. Only an extra assumption that the field is decimal
reduces the alternatives to **12059 or 12079**; it does not select one.
All six source-coordinate completions are retained and re-encrypted.

## The radio hour is an optional interpretation

B's edited stream retains **`?600UHR`**. The unknown at plaintext
position **30** uses observed source **82 = F** and the printed dash
at source **162**, giving pair **F?** and domain **1EKLOS**. The main
edition leaves this coordinate unfilled.

There are six complete, exactly re-encrypting possibilities. If a separate
assumption requires the unknown to be a decimal digit, its domain contains
only **1**, giving **1600UHR**. That interpretation has its own additional
one-mask-fill certificate and is excluded from the primary totals. The
literal date-like field `1X10` and references `70` and `30056` remain
unchanged. The two header times are preserved without resolving their
chronology from this fragment.

## Reproduce and prior scope

From the repository root:

```sh
python experiments/p64_oil_and_radio/verify.py --verify
python experiments/p64_oil_and_radio/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command uses the standard library and repository cipher code.
The optional PDF check uses PyMuPDF and Pillow to verify the PDF's byte
size and SHA-256 and the exact rendered pixels of all four crops.
[inputs.json](inputs.json) preserves every source row, the parenthetical
forms, glyph qualifications, chronology and prior credit.
[prior_candidates.json](prior_candidates.json) retains the earlier
screened bodies with the cache hash; temporary files are unnecessary
for replay.

A bounded check found no explicit separate Damascus/Aleppo body discussion
in the paper, dissertation text or cached 2017 comments. This absence
does not establish priority. The published Oct4–6 key and the oil body's
earlier authorship credit remain fully separate from this source audit.
