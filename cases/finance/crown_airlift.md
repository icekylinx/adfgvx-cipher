# Crown airlift to Kronstadt and Hermannstadt

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source:** J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
printed p174, PDF p177, A1–A3. **Edition:** icekylinx and GPT-6 Astra Pro.
The source is a three-part message dated 10 November 1918, with header
`--- v ZO'N (07.24 p.m., November 10th); 17.50 3 TLE`.

The message describes an urgent shortage of crowns and requests daily
delivery of one million crowns by ordinary aircraft, alternately to
Kronstadt and Hermannstadt. An explicitly interrupted final part can be
read as requesting small-denomination notes. This is evidence of a
request, not proof of completed flights or receipt of cash.

The period square and transposition are unchanged. The source images,
literal rows, every coordinate-to-plaintext map and exact candidate
edits are in [the experiment](../../experiments/crown_airlift/README.md).

## p174 A1

The source advertises and prints **146 coordinates**. The raw 73-character
plaintext requires no repair:

**Raw output:**

```text
ANXOHLXOPXXKRONENBEDARFSEHRDRINGENDXBITTETAEGLICHMITGEWOEHNLICHEMFLUGZEUG
```

**Readable German — first-part wording; the final ellipsis marks continuation in A2:**

> An OHL, Op. Kronenbedarf sehr dringend. Bitte täglich mit gewöhnlichem Flugzeug …

## p174 A2

The source advertises and prints **146 slots**. One printed glyph is `C`,
outside the ADFGVX coordinate alphabet, and is retained as an erasure in
the model. The raw reading is:

**Raw output:**

```text
EINEMILLIONKRONENABWECHSWLNDNACHXKRONSTADTXUXHERMANNSTADTXFELDKR?EGSKASSE
```

The explicit ordinary-word candidate is:

**Edited output:**

```text
EINEMILLIONKRONENABWECHSELNDNACHXKRONSTADTXUXHERMANNSTADTXFELDKRIEGSKASSE
```

This changes observed source coordinate **103 from D to X**, repairing
`ABWECHSWLND`, and fills the invalid printed `C` at source index **80**
with **D**, producing the missing `I` in `FELDKRIEGSKASSE`. Indices are
zero-based. The candidate encrypts exactly to the certified repaired
ciphertext; no coordinate is inserted or removed in this part.

**Readable German — second-part wording; the ellipses mark its joins with A1 and A3:**

> … eine Million Kronen abwechselnd nach Kronstadt u. Hermannstadt. Feldkriegskasse …

The exact unpunctuated office word at the boundary with A3 is retained;
the edition does not invent a missing verb or office address.

## p174 A3

The source indicator is **RICHI-98**, but only **79 coordinates** are
printed, followed by **“Did not finish.”** The second line begins with a
complete `GAVGX` group that earlier OCR omitted. Appending 19 absent
coordinates gives the declared source model and raw 49-position reading:

**Raw output — conditional 98-slot frame; nineteen absent tail coordinates left unknown:**

```text
INM???LICHS???EINEN???EINEN???DENLX???1A4A1????OP
```

The first 33 positions admit the ordinary-word candidate:

**Edited output — same conditional 98-slot frame; proposed first 33 positions:**

```text
INMOEGLICHSTKLEINENSCHEINENSENDENLX???1A4A1????OP
```

With editorial spacing, its readable prefix is:

**Readable German — proposed body excerpt under the incomplete-tail model:**

> In möglichst kleinen Scheinen senden …

The candidate fills 12 absent coordinates and makes **zero substitutions
to the 79 observed coordinates**. Seven absent coordinates remain
unfilled. In particular, the observed `L` immediately after `SENDEN` is
not silently changed to a separator, and `1A4A1` is not converted into a
date or reference number.

Ordinary words alone leave a geometry ambiguity. Screening all 80
positions for one gap of 19 coordinates, while masking the last 16
plaintext positions, finds these three zero-substitution fits:

| Gap before source index | Raw reading |
|---:|---|
| 77 | `INM???LICHS???EINEN???EINEN????ENLXO???A4A1????OP` |
| 78 | `INM???LICHS???EINEN???EINEN???DENLX????A4A1????OP` |
| 79 | `INM???LICHS???EINEN???EINEN???DENLX???1A4A1????OP` |

All three support the same ordinary prefix without observed-coordinate
changes. The primary gap at 79 follows the source interruption, rather
than selecting a plausible-looking reference field. Every tied fit is
retained in the certificate. The absent letters remain an editorial
candidate, even when the candidate fits all observed pairs exactly.

## Attribution and reproducibility

The published Nov10–12 square and ranks supply the cryptographic key.
The first two bodies also predate this edition as unreviewed repository
OCR-derived screen results, now frozen with their original hashes.
This edition adds visual source correction, a documented reconstruction
of the interrupted third part and exact repair costs. Bounded checks of
the Lasry et al. paper, dissertation chapter and cached comment thread
did not locate an explicit discussion of this message; that does not
establish historical priority.

The three physical records contain **371 source slots**, of which **370**
are valid coordinates. Their declared models contain **195 plaintext
positions**, with **175 fixed raw positions** and **188 fixed positions**
after the explicit candidates. These are source-edition counts, not 188
newly discovered plaintext characters or new key assignments.

```bash
python experiments/crown_airlift/verify.py --verify
python experiments/crown_airlift/verify.py --verify --pdf /path/to/childs.pdf
```

## Later complete-copy witness

The [p195 A2 source edition](crown_banknote_completion.md) supplies the
nineteen missing tail coordinates of p174 A3. Eleven earlier conjectural
fills agree with the new source and one is contradicted. The literal copy
resolves the contiguous-gap location within the tested family, but `SENDEN`
still needs one observed-coordinate repair. The conflicting source dates
and part numbers remain explicit. This page and its original certificate
retain the earlier, more limited reconstruction for comparison.
