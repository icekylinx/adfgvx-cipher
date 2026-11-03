# One conditional letter constraint for the Nov25–28 square

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The unchanged coordinate pair `VD` has the published label `9` in the
Nov25–28 key. Two source-reviewed words, `MA9OR` in p224 C1 and `9EDE` in
p222 A1, suggest **`VD→J`** under the lexical readings *Major* and *jede*.
This package applies that one hypothesis to a frozen set of **23 reviewed
records, 3,176 plaintext positions**, retaining every inconvenient occurrence.
It adds no coordinate repair and authenticates no numeral assignment.

## All six observed raw `9` occurrences

Indices below are zero-based. Both coordinates are observed in every row.
The source positions and earlier repairs are independently recomputed in the
[certificate](certificates.json).

| Record | Plaintext index | Source-coordinate indices | Original word | Word under `VD→J` | Earlier source-edition decision |
|---|---:|---|---|---|---|
| p218 A1 | 1 | 60, 159 | `G9NERAL` | `GJNERAL` | `GENERAL`: one coordinate, `VD→FD` |
| p219 B | 123 | 349, 26 | `MOEGLICHK9IT` | `MOEGLICHKJIT` | `MOEGLICHKEIT`: one coordinate, `VD→FD` |
| p220 C4 | 59 | 142, 100 | `WNTERNI9RUNG` | `WNTERNIJRUNG` | `INTERNIERUNG`: this `9→E` repair costs one coordinate, `VD→FD`; the initial `W→I` is separately priced in its source edition |
| p222 A1 | 34 | 114, 189 | `9EDE` | `JEDE` | No source change; lexical anchor |
| p224 C1 | 9 | 125, 79 | `MA9OR` | `MAJOR` | No source change; lexical anchor |
| p224 C1 | 48 | 106, 218 | `GESCHAEFT9` | `GESCHAEFTJ` | `GESCHAEFTS`: two coordinates, `VD→GF` |

The first, second, third and sixth rows are inconvenient consequences in the raw
source view. Their separately recorded source repairs predate this hypothesis;
they are neither suppressed nor counted as new evidence for `J`. The two
anchors were used to propose the hypothesis, so they are **not held-out
controls**. This snapshot supplies **no additional clean held-out `VD`
occurrence**. The hypothesis is useful as a conditional reading, with these
limits; it does not prove an error-free substitution for every printed pair.

## A partial bijection, without a silent `J→9` swap

The published square and ranks are prior work by **Lasry, Niebel, Kopal and
Wacker**. Their late-period numerical labels require separate interpretation;
see the [existing late-key interpretation package](../late_key_interpretation/README.md)
and the source packages' attribution notes. No earlier plaintext, transcription
or source repair is claimed here as a new first decipherment.

This layer retains 23 ordinary-letter anchors and first releases all cells
whose baseline labels are `0123456789JQY`. It then assigns only `VD→J`:

```text
H???DK
ZAO?M?
BEIWT?
?PSCFL
VJ????
NGURX?
```

The old `J` cell, `FX`, remains unknown. The other 12 cells are one globally
bijective permutation of **`0123456789QY`**, giving **12! = 479,001,600** square
completions under the stated anchors. This count is an algebraic consequence
of the hypothesis, not a number of plausible historical keys. Repeated cells
must keep the same value across every message; the displayed marginal domains
cannot be chosen independently at each occurrence. The ordinary-letter anchors,
published ranks, earlier source geometry and word repairs retain their own
assumptions.

In particular, p224's `AOKJJ` becomes `AOK??`, not a guessed army number.
Money amounts, dates, references, rare letters and all other numeric fields
remain unassigned. This package changes neither the baseline key nor any
source-edition input or certificate.

## Complete propagation within a stated snapshot

The frozen reviewed set comprises:

- p218 A1–A3: [Kress/armistice source editions](../corpus_readings/README.md).
- p219 A1–A2 and B: [crown requests](../crown_cash_requests/README.md).
- p220 C1–C4 and p221 A5–A6: [Mackensen's appeal](../mackensen_armistice_appeal/README.md), retaining prior body credit to Childs and Lasry et al.
- p221 B1–B4: [Constantinople civilians](../constantinople_civilians/README.md).
- p222 A1–A2: [Liman troop-report request](../liman_troop_reports/README.md).
- p223 A1–A3: [lei-note exchange](../lei_note_exchange/README.md).
- p224 C1–C2: [Breslau staff transfer](../breslau_staff_transfer/README.md).

The input manifest records the selected catalog snapshot, every selected
record, and hashes of all fourteen source input/certificate files. It contains
**6,340 literal source slots**; the earlier selected insertion/deletion models
produce 6,352 working coordinates. This is complete for the declared reviewed
set, not for all surviving same-period traffic. The appeal's six records were
source-reviewed and awaiting catalog integration when this snapshot was frozen;
that distinction is recorded explicitly in the manifest.

Both raw and separately edited views are preserved. The inventory includes
all **111 definite raw** occurrences of digits or `J/Q/Y`, all **87 definite
edited** occurrences, and **27 raw erased pairs** whose baseline domain can
include such a label. Previous coordinate changes that remove, create or alter
an occurrence are shown explicitly. The 87 edited occurrences therefore must
not be mistaken for a count of original observed fields. Every raw and edited
record has its complete baseline text, conditional text, marginal domains and
source-index mapping.

## Reproduce

```sh
python experiments/nov25_letter_constraint/verify.py --verify
```

The standard-library verifier checks the dependency hashes and unchanged
published key, independently inverts each physical-column layout, compares
the resulting texts with the frozen source certificates, and recomputes every
inventory entry and previous coordinate change. It then constructs and
re-encrypts a globally consistent full-square/erasure witness for each of the
46 raw/edited views. These arbitrary witnesses demonstrate consistency only;
they are explicitly marked **not proposed original plaintexts**. They use the
same deterministic square completion across records.

This is a bounded propagation audit, not a search for additional digit values
or a claim that the two lexical readings are historically unique.
