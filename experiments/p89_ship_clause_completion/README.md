# p89 A2: conditional completion of the ship-routing clause

**Source and arithmetic work: icekylinx and GPT-6 Astra Pro.**
The earlier body reading is credited to **Ayush Agarwal**, with review by
**D. Bourdeau**. This package prices a phrase already proposed in the reading
case; it does not claim first discovery of the ship-routing interpretation.

The conservative native source reads `?ELCHES?HI?FE`. The conditional
`WELCHESCHIFFE` completion supplies **three plaintext labels**, preserving
all **287 observed coordinates** in the original **290-slot** frame. The
source remains **142/145** fixed positions; the proposed layer is **145/145**.
There are **two printed-dash fills and one disputed-glyph fill**, with **zero
observed-coordinate substitutions, insertions, deletions or key changes**.

| Plaintext index | Raw pair | Domain | Proposed label | Source index | Proposed coordinate |
| ---: | --- | --- | --- | ---: | --- |
| 78 | `G?` | `58BDNW` | W | 176 | F |
| 85 | `?D` | `248CIM` | C | 70 | D |
| 88 | `?V` | `3BFKQS` | F | 177 | A |

Every index is zero-based. Source70 remains a D/E-like disputed glyph in the
conservative transcription. Its D fill reproduces the earlier published
candidate; it is not an upgraded visual observation. The remaining two
fills complete the proposed words at the printed dashes.

The native word `SCHIFFE` occurs in **p98 A2** under the same published
Nov1–3 key, in a notice about ships from Kospoli to Odessa/Nikolayev.
`WELCHES`, in `WELCHES KALIBER`, is native in **p86 A** under the
Oct28–31 key; it supports the same stem with a different grammatical ending. The verifier
reconstructs those words from their original coordinate rows and records
all 28 observed coordinate halves. These are vocabulary and subject-matter
witnesses, not a second received copy of the target sentence.

The three unknown halves admit **216** complete cryptographic alternatives.
The certificate retains every three-coordinate completion and its local
plaintext. One yields the proposed phrase, but the source arithmetic does
not make that phrase unique. The native and earlier published layers are
preserved, and all other labels, including `EZ`, remain unchanged.

## Reproduction

From the repository root:

```sh
python experiments/p89_ship_clause_completion/verify.py --verify
```

The standard-library verification uses two independent repository decoding
implementations, exhausts all 216 source-fill combinations, re-enciphers
the proposed layer exactly, and checks the original word witnesses.
Optional original-PDF verification regenerates three existing source crops:

```sh
python experiments/p89_ship_clause_completion/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The original PDF must match its frozen SHA-256. The source crops are reused
from the existing editions, without creating another physical record.
