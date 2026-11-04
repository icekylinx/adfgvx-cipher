# p176 A6: a conditional repeated-place reading

**Research and source audit: icekylinx and GPT-6 Astra Pro.**

This supplement proposes `XKLAUSENBURGX` at plaintext positions 28–40
of the native p176 A6 frame. The earlier
[coal-train fragment](../p176_coal_train_fragment/README.md) already proposes
`KLAUSENBURG` at 17–27. Reading the new span as a repetition gives a
plausible continuation, with **no observed-coordinate substitution and
15 additional printed-mask fills**. It raises the conditional edited output
from **48/80 to 59/80 fixed positions**.

Both copies are partly supplied. The first copy is an earlier contextual
proposal, not a fully observed donor word. The new reading depends on that
proposal and a separate repeated-word hypothesis. The equal-price
`XBLANKENBURGX` alternative demonstrates that the observed coordinates do
not determine the second place. Four newly supplied plaintext positions
have neither coordinate observed.

[Inputs](inputs.json) · [Exact certificates](certificates.json) ·
[Verifier](verify.py) · [Earlier edition](../../cases/military/p176_coal_train_fragment.md)

## Raw and conditional edited output

**Raw output — unchanged native 160-slot frame and published partial key;
14/80 fixed positions:**

```text
??H????U??E????E??L????N??R????A???????G???????N???????N???????X???????1???????X
```

**Earlier edited output — the coal-train and predicate proposal;
zero observed substitutions and 44 printed-mask fills; 48/80 fixed:**

```text
KOHLENZUEGENUEBERKLAUSENBURG???A???????G?GERECHNETWERDEN???????X???????1???????X
```

**Edited output — conditional repeated-place proposal; zero observed
substitutions and 59 printed-mask fills in total; 59/80 fixed:**

```text
KOHLENZUEGENUEBERKLAUSENBURGXKLAUSENBURGXGERECHNETWERDEN???????X???????1???????X
```

**Readable German — conditional interpretation; the repetition annotation
and punctuation are editorial:**

> … Kohlenzuegen ueber Klausenburg [Wiederholung: Klausenburg] gerechnet werden […]

The proposed word and separators are priced separately. Every displayed
candidate retains the last 24 positions exactly, including literal `X`,
`1`, and all unresolved positions. No footer, number, date, office or
signature is supplied.

| Added span | Plaintext positions | New fixed positions | Additional observed substitutions | Additional mask fills |
|---|---:|---:|---:|---:|
| `KLAUSENBURG` only | 29–39 | 9 | 0 | 12 |
| Left `X` only | 28 | 1 | 0 | 1 |
| Right `X` only | 40 | 1 | 0 | 2 |
| `XKLAUSENBURGX` | 28–40 | 11 | 0 | 15 |
| Rival `XBLANKENBURGX` | 28–40 | 11 | 0 | 15 |

The new full span has 26 coordinate positions: **11 observed coordinates
are retained and 15 printed masks are filled**. Plaintext 31 `A` and 39 `G`
were already fixed in the native output. The new positions 29 `K`, 32 `U`,
37 `U`, and 40 `X` are wholly unobserved; their two source coordinates are
both printed masks. Positions 28, 30, 33–36 and 38 each preserve one observed
coordinate and supply the other. These distinctions are listed individually
in the certificate.

## What assuming a repeated word actually determines

The following table compares the two **native**, unfilled spans at 17–27
and 29–39. It does not use either proposed word to construct the domains.
Assuming only that the eleven letters repeat, a letter must belong to the
intersection of the two native domains.

| Word position | First native pair | Second native pair | Shared letters under the partial square | Proposed letter |
|---:|---|---|---|---|
| 0 | `D?` | `??` | `FIKNOS` | K |
| 1 | `GA` | `G?` | **L** | L |
| 2 | `?D` | `AD` | **A** | A |
| 3 | `?G` | `??` | `56789JQSUZ` | U |
| 4 | `??` | `D?` | `FIKNOS` | S |
| 5 | `V?` | `V?` | `2CEHQW` | E |
| 6 | `DX` | `?X` | **N** | N |
| 7 | `??` | `?F` | `056789BFHR` | B |
| 8 | `A?` | `??` | `14ARTU` | U |
| 9 | `AF` | `A?` | **R** | R |
| 10 | `?D` | `XD` | **G** | G |

Only **L, A, N, R, G** are forced by the source after making the repeated-word
assumption. In particular, the first copy supplies native `L`, `N` and `R`
to constrain the second; the second copy supplies native `A` and `G` to
constrain the first. The six other letter positions remain variable.

The five missing square cells remain globally distinct over digits 5–9.
The displayed partial-square domains are unions over these assignments,
so their sizes must not be multiplied as though the digit choices were
independent. The verifier instead checks **all 120 complete squares**.
Each permits **46,656 zero-error common strings** under the repeated-word
assumption: six positions each admit six letters. `KLAUSENBURG` is one
such string in every completion; this count does not establish its
historical uniqueness.

There is limited repetition context in the same six-part message:
p175 C1 has the literal native string `24X24` at 84–88. All ten coordinate
halves of this string are observed, and the verifier rebuilds it from the
source without substitutions or fills. This shows one repeated number in
the assembled message. It does not establish that the sender repeated this
place name or that `X` necessarily marks such a repetition.

## Alternatives and limits

`XBLANKENBURGX` fits the new span with the same 15 mask fills and no
observed change. It does not repeat the earlier proposed `KLAUSENBURG`.
This rival is retained as a compatibility witness; no geographical or
historical route identification is asserted for it. Many other strings
also fit. The repeated-place hypothesis is preferred here only as a
contextual reading linked to the earlier proposal.

The inherited `N`/`X` choice at plaintext 11 remains equal in price. An `X`
instead of `N` changes the proposed fill at source 151 from `D` to `G` and
keeps all counts unchanged. The A5 syntax motivates the existing dative
`KOHLENZUEGEN`; this supplement supplies no new decision on that choice.

The native source still has **160 slots, 74 observed coordinates and
86 printed dashes**. The full new candidate fills 59 masks and leaves
27 masks unresolved. No source coordinate, frame boundary, transposition
rank or square label is changed. This is an extension of an existing
partial reading, not a new physical record or eleven new raw letters.

## Reproduce and inspect the source

```sh
python experiments/p176_repeated_place/verify.py --verify
python experiments/p176_repeated_place/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier pins the baseline inputs and certificate, the companion source
assembly, and the [existing A6 crop](../romanian_ultimatum_companions/sources/p176_A6.png).
It independently constructs column offsets and plaintext domains, checks
the exact incremental fill ledger, identifies wholly unobserved letters,
rebuilds the native repetition witness, and checks every candidate under
all 120 injective square completions. An independent column encoder also
checks every full round trip.

Full round-trip witnesses fill remaining masks arbitrarily with coordinate
`A`; these witness-only fills never enter the partial edited output.
The optional PDF check uses the pinned original and existing recipe:
PDF page 179, printed p176, rectangle `[70,359,527,406]`, render scale 4.
Without the PDF, the verifier checks the existing crop's file hash and
explicitly reports that no fresh source-pixel comparison was performed.
The crop was visually inspected: its observed 74-coordinate prefix is
followed by printed dashes, and `RICHI-160` remains literal.

The published period key retains the credit to George Lasry, Ingo Niebel,
Nils Kopal and Arno Wacker. Earlier part-4 work remains separately credited
to Norbert and Max Baertl in the linked edition. The present conditional
extension and source audit are by **icekylinx and GPT-6 Astra Pro**.
