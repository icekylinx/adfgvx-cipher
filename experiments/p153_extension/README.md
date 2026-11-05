# p153: linked footer and conditional date constraints

**icekylinx and GPT-6 Astra Pro · ADFGVX Cipher · 2 November 2026**

The recovered shared key links an unresolved character in part 6 to the order
number in part 5. Keeping that link makes the best reading more informative
without assigning an unsupported digit or expanding an unidentified signature.

## Full reading of the surviving second part

With the [previously certified body reconstruction](../../cases/pages/153.md#edition-cases-p153b) and
the separately stated `AF=X` separator interpretation:

```text
MUNITIONSBESTAND DER NACHHUTARTILLERIE MELDEN
X <gamma> X G X R <u><v><w> B X A
```

The body means “Report the ammunition inventory of the rearguard artillery.”
The remaining letters are left as initials or text fragments. No unit,
signature, address, section number or padding convention is identified.

This conditional layer fixes **50 of 54 positions**, including four separator
positions. It uses the existing twelve erased-coordinate fills and two
`A`-to-`X` emendations; it introduces no additional source edit. The untouched
nineteen-letter square still fixes **33 of 54 positions**.

The footer's `<gamma>` is the same square cell `DV` as both outer characters of
the part-5 serial `NR <gamma><delta><gamma>`. This equality follows from the
received coordinates and shared square. It does not depend on treating the
characters as digits.

The three erased footer coordinates give `u=A?`, `v=?V`, and `w=A?`. Therefore:

- `u=v` is possible only when both letters are `G`.
- `v=w` is possible only when both letters are `G`.
- `u=w` is otherwise allowed.

These coupled restrictions are stronger than three independent lists of
possible letters. The [result](result.json) includes all twelve footer
coordinate mappings and exact source indices.

## Decimal-calendar constraints

<a id="what-a-decimal-calendar-interpretation-supplies"></a>

The first part contains the pattern:

```text
ANORDNUNGEN VOM <alpha>TEN <beta><beta>TEN NR <gamma><delta><gamma>
BEZIEHEN LASSEN SOWEIT NOCH NICHT GESCHEHEN
```

Suppose the day is one ordinary decimal character, the repeated two-character
field is a calendar month, and the serial contains three decimal characters.
Then the month is necessarily **11**, the only valid two-character month with
identical digits. The distinct cells for alpha, gamma and delta cannot also be
`1`. The recovered square alone does not establish these semantic assumptions.

| Additional assumptions | Possible day values | Date/serial assignments |
| --- | --- | ---: |
| Decimal fields only; leading zero in serial allowed | 2–9 | 448 |
| Referenced order is dated in 1918 no later than reception on 8 November; leading zero allowed | 2–8 | 392 |
| Decimal fields; serial has no leading zero | 2–9 | 392 |
| Both chronology and no-leading-zero assumptions | 2–8 | 343 |

The second row is a useful contextual reading. The no-leading-zero restriction
is kept separate because a three-character serial could be zero-padded. No day
or serial is selected or ranked.

Even after fixing one of these date/serial assignments and accepting the
existing body and separator hypotheses, there are **2,537 distinct remaining
footer triples**. With the nonfuture-date interpretation and leading zero
allowed, there are **994,504 distinct joint plaintext pairs**. This is an exact
ambiguity count within the stated model, not a likelihood estimate.

To see the count, the square has twelve unassigned cells and twelve unused
symbols after the four numeric assignments. Two cells matter to the three
footer erasures: `AA` and `VV`. They must have different unused symbols. The
two outer positions share a row containing five fixed symbols and `AA`; the
middle position uses a column containing five fixed symbols and `VV`. Hence

```text
25 * (5 + 12) + 11 * 12 * (5 + 11) = 2537.
```

The first term covers triples that use neither occurrence of the unknown row
cell. The second covers at least one occurrence of it. All assignments extend
to full bijective squares, so no hidden square-completion condition is omitted.

## Other recorded squares cannot supply the missing digits by relabeling

All **23 other nonempty recorded squares** disagree with the p153 core even
after arbitrary, independent permutations of their six rows and six columns,
with or without transposing the square. Each rejection has a short exact
witness: two established letters share a row or column in one square but do
not share the corresponding coordinate in the other. Coordinate permutations
preserve this relation. The witnesses are in [result.json](result.json).

The all-unknown `NSA-June1-CHI-21` square is excluded from this test because it
has no established cells. The result addresses only coordinate relabeling of
the recorded squares; it does not rule out another square, a related keyword,
an arbitrary permutation of the 36 cells, or additional source errors.

## Reproduce

Python 3.10 or later; standard library only:

```sh
python3 experiments/p153_extension/analyze.py --verify
```

The program reconstructs the transposition independently, checks the original
core decodes and all source-coordinate maps, enumerates every stated date
assignment, and roundtrips all 216 residual erasure fillings for each assignment.
It independently enumerates the footer union and compares the count with the
formula. Relabeled and transposed full-square controls check the invariant
test. The input evidence comes from the existing [p153
certificate](../../data/certificates/p153.json), [key
catalogue](../../data/keys.json), and [source
review](../../data/reviews/p153_source_review.json).
