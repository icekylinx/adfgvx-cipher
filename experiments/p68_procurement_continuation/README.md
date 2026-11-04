# p68 A2: a procurement continuation with an unresolved verb

**icekylinx and GPT-6 Astra Pro** · [October Caucasus edition](../../cases/caucasus/october_caucasus.md#p68-a--provisional-procurement-text-carrying-chi-labels)

The second part of the p68 procurement exchange supports a further conditional
reading: `DONREGIERUNG`, `DORT EINGE?ANGEN`, `HGRU KIEW` and `ROSTOW`.
Above the earlier `UNDARTILLERIEMUNITION` opening, the common proposal adds
**15 fixed plaintext positions**, all retaining an observed coordinate half.
Its additional price is **one observed-coordinate substitution and 15 printed
mask fills**. No source coordinate is inserted, removed or moved.

The internal unknown in `EINGE?ANGEN` has **both coordinate halves missing**.
`EINGEGANGEN` and `EINGELANGEN` have exactly the same price and are displayed
as separate alternatives. Neither completion is included in the common layer.
The source therefore does not determine a unique complete sentence.

## Exact reading layers

All positions below are zero-based. The source has **186 literal slots**,
comprising 145 observed coordinates and 41 printed masks, for 93 plaintext
positions. The published October 4–6 square and 22-column rank are unchanged.

**Raw output — 56/93 positions fixed by the literal source:**

```text
??DARTILLER??T7QITJO?F??DO?RE?I????GD?RTEI?G??A??EOX??O????TA?SE?X??O?HGRUK?E??0X?OSTO?1??8XX
```

**Edited output — common conditional proposal, with both halves of position 45 still absent:**

```text
UNDARTILLERIEMUNITIONF??DONREGIERUNGDORTEINGE?ANGENX??O????TA?SE?X??O?HGRUKIEW?0XROSTOW1??8XX
```

**Conditional interpretation — readable German excerpts, preserving the literal unresolved fields:**

> […] und Artilleriemunition `F??` Donregierung dort `EINGE?ANGEN` […] `HGRU` Kiew `?0` […] Rostow `1??8` […]

The displayed spaces and case distinguish words for reading. They do not
replace missing source coordinates. `HGRU` remains an unexpanded raw
abbreviation. No date, quantity, sender or complete procurement event is
inferred from the damaged fields. In particular, the two absent letters after
the observed `F` at positions 21–23 remain `??`; a plausible `FUR` is not supplied.

| Layer | Fixed positions, including unchanged raw text | Observed substitutions | Printed-mask fills |
| --- | ---: | ---: | ---: |
| Literal source | 56/93 | 0 | 0 |
| Earlier opening, with other raw positions retained | 61/93 | 4 | 5 |
| Common new proposal, `EINGE?ANGEN` | 76/93 | 5 | 20 |
| Optional `EINGEGANGEN` completion | 77/93 | 5 | 22 |
| Optional `EINGELANGEN` completion | 77/93 | 5 | 22 |

The earlier edition asserted **21 opening positions**. That is not a count of
raw recovered positions: the literal source already fixes 56 positions across
the body. Applying the opening while retaining those other raw letters fixes
61 positions. The new common layer adds fifteen to that comparable baseline;
it leaves seventeen plaintext positions unassigned. Each complete verb
alternative adds one wholly unobserved position at the price of two further
mask fills.

The only new observed substitution is **source coordinate 48, F → A**, which
changes plaintext position 50 from raw `O` to proposed `N`. The original crop
confirms that the received character is F; it is an editorial repair, not a
corrected transcription. All four earlier observed substitutions remain
charged to the inherited opening.

## What the independent words support

| Proposed recipient word | Target start | New observed substitutions for that word | Independent raw word witness |
| --- | ---: | ---: | --- |
| `REGIERUNG` within `DONREGIERUNG` | 27 | 0 | p209 A1, positions 64–72 |
| `EINGEGANGEN` | 40 | 1 | p166 B1, positions 77–87 |
| `KIEW` | 74 | 0 | p66 A, positions 73–76 |
| `ROSTOW` | 81 | 0 | Book-lexicon candidate; no independent cipher copy asserted |

Each of the three cipher donor words is fully observed in its original
unchanged source frame. The verifier reconstructs those words from their own
source rows and independently checks every supporting coordinate pair. They
attest the individual vocabulary, **not a retransmission of this clause**.
`DON` combines observed `DO` with one compatible half-fill. `DORT` retains
observed `DRT` and supplies one compatible half. The word `KIEW` fills two
halves; `ROSTOW` retains four raw letters and fills two halves.

[`discovery.json`](discovery.json) records the raw-donor retrieval and the
separate 53,465-word book model. Its selected matches retain 13 observed halves
for `REGIERUNG`, 16 for `EINGEGANGEN`, six for `KIEW` and ten for `ROSTOW`.
`EINGELANGEN` is an equal-price letter alternative; this package does not
establish its grammatical suitability or claim that it came from the selected
book vocabulary. Only the G completion has the specified native word witness.
No calibrated
probability, exhaustive phrase uniqueness or complete historical sentence is
claimed for the word selection.

## Historical context and its limit

A German-language text by Leon Trotsky, published in 1922 as
[*Zwischen Imperialismus und Revolution*, “Strikteste Neutralität”](https://www.marxists.org/deutsch/archiv/trotzki/1922/georgien/02-neutral.html),
uses the name *Donregierung* and alleges a Georgian transfer of military
supplies to it in October 1918. This is a near-contemporary participant's
political account. It supports the name and broad setting as context; it
neither authenticates that allegation nor identifies this telegram as its
source. The coordinate-compatible `DON` proposal preceded this web check.
No missing letters are filled from the account.

[`context.json`](context.json) preserves that attribution and scope. The
heavily repaired first part of p68 A remains provisional, with its existing
24 observed substitutions. The new second-part vocabulary does not make the
whole exchange a directly recovered text or identify the two officers.

## Source and reproduction

The existing [original source crop](../october_caucasus/sources/childs_p68_A.png)
preserves both parts, their `CHI`/`RICHI` labels, all dashes and the exact
186-slot second body. The verifier independently constructs the inverse
column map, derives each raw letter domain, prices every layer, checks all
three native donor words and re-encrypts a complete arithmetic witness for
each layer. Arbitrary values used in those complete witnesses are excluded
from the displayed readings.

```sh
python experiments/p68_procurement_continuation/verify.py --verify
python experiments/p68_procurement_continuation/verify.py --verify --pdf /path/to/childs.pdf
```

The optional PDF check reproduces the existing crop pixel for pixel from the
pinned original document. The published key remains credited to George
Lasry, Ingo Niebel, Nils Kopal and Arno Wacker; the earlier source edition and
opening retain their existing attribution. This extension by **icekylinx and
GPT-6 Astra Pro** adds no physical ciphertext body to the catalogue.
