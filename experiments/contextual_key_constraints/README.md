# Consequences of the conditional November Y assignments

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The [Tiflis appointment edition](../../pages/192.md#edition-cases-caucasus-tiflis-appointment)
independently supports a conditional **Nov13–15b FX = Y** assignment through
the historically attested surname TYDELSKI. That edition also defines a
separate, stronger assumption: if the two pilot notices name the same person
with the same correct spelling, **Nov13–15a DG = Y** follows.

This experiment propagates those two assumptions. It does not change
`data/keys.json`, reinterpret a received coordinate, or treat the two
inferences as equally direct evidence.

## A stronger exact constraint on the p198 hypothesis

Under the Nov13–15b key hypothesis, fixing FX to Y reduces the compatible
square completions from **40,320 to 5,040**. The fixed 16-column transposition
and the model of exactly five lost coordinates remain additional assumptions
about p198. All 165 received coordinates stay unchanged and in their original
order, and all loss locations and fills remain available.

The resulting exact nondominated count pairs are:

| Digit positions | Q or Y positions | Other 24 letters |
| ---: | ---: | ---: |
| 4 | 6 | 75 |
| 5 | 5 | 75 |
| 6 | 4 | 75 |
| 7 | 3 | 75 |
| 8 | 2 | 75 |
| 10 | 1 | 74 |
| 13 | 0 | 72 |

Consequently, this conditional family requires **at least four digits**.
If a proposed reading has no Q or Y, it requires **at least thirteen digits**.
Without the name constraint, the corresponding minima were three and ten.
These are exact restrictions on proposals within a hypothesis, not evidence
that the historical message had a particular count. **p198 remains open.**

### Completeness of the restricted frontier

<a id="why-restriction-of-the-earlier-exact-result-is-sufficient"></a>

The [earlier frontier](../p198_category_frontier/README.md) exhausted all
28 choices of two unknown square cells holding Q/Y. Exactly seven of those
choices contain FX, square cell 17. Retaining them covers every completion
with FX=Y: the other Q/Y cell must hold Q, and the six remaining unknown cells
can receive the six unused digits in all **6! = 720** orders. Thus seven
classes cover all 5,040 allowed squares.

The count objective cannot distinguish Q from Y. Where an earlier
representative has FX=Q, swapping Q and Y throughout its complete square and
its plaintext gives a valid FX=Y representative with the same ciphertext and
the same counts. The certificate explicitly performs and verifies this
conversion for every retained witness. Filtering the seven exact frontiers
and taking their nondominated union gives the table above.

All seven memberships were also recomputed with the existing independent
adjacent-column-pair implementation: **15,504 column-loss allocations** per
membership, representing every one of the **1,115,034,284** five-position loss
choices and every six-valued fill. No language score or heuristic search is
used. A weaker condition that FX is either Q or Y covers 10,080 square
completions and gives the same category frontier.

Different frontier points may use different complete squares and different
loss geometries. Their witnesses are arithmetic examples, not plaintext
proposals, and cannot be combined into a single historical key.

## Propagation beyond the favorable name occurrences

The report inventories **29 physical source records in 51 declared source or
editorial variants**. It includes the three Tiflis parts, all seven 14 November
records, all four Warsaw/LP service records and their candidate variants, p185 C/D, all ten retained p189 alignments, six transport-context
records, four additional transport records and their repair aliases, the
previously read p187 C inquiry, and both p187 D gap aliases before and after
their existing explicit editorial repairs.

Every inventory entry retains its entire before/after raw text and every
changed marginal character domain. This includes reductions that create no
new fixed letter and variants that remain badly damaged. The scope is an
explicit list of reviewed frames, not a claim to all ciphertexts in Childs.

Only the same four complete-pair positions already reported in the Tiflis
edition become fixed: p192 part 3 position 61, p190 A position 37, and under
the additional cross-key assumption p194 B and p193 B position 54. The
other records gain domain restrictions without new fixed plaintext. This
inventory therefore does not count those four letters again as discoveries.

### The p187 D reference fields stay open

In the [aircraft-connection edition](../../pages/187.md#edition-cases-radio-p187-d), all twelve
unresolved reference positions use five distinct Nov13–15a cells. None is
DG. Assigning DG=Y removes Y from those cells' available labels, leaving
`0123456789Q`. It fixes **no reference digit**.

The five cells must have different labels within one global injective
square. Their possible coupled assignments therefore fall from
`12 × 11 × 10 × 9 × 8 = 95,040` to
`11 × 10 × 9 × 8 × 7 = 55,440`. Every such assignment can be extended to a
complete square by bijectively filling its remaining cells. No numerical-only
assumption is imposed, and both previously certified gap aliases have the
same result.

## Reproduction

```sh
python experiments/contextual_key_constraints/verify.py --verify
python experiments/contextual_key_constraints/verify.py --verify --recompute
python experiments/contextual_key_constraints/verify_independent.py --verify
```

The first command verifies dependency hashes, the complete inventory,
independent coordinate/domain arithmetic, all converted source-preserving
frontier witnesses, membership coverage and exact count aggregation. The
second additionally recomputes all seven retained frontiers with the
independent exact solver. A further independent reviewer enumerates all 40,320
original square completions, checks all 45 converted membership witnesses, and
constructs a full square extension for each of the 55,440 p187 D field assignments
in both aliases. Its script imports neither the primary verifier nor the project
cipher implementation. Standard-library Python is sufficient.

[certificate.json](certificate.json) contains all inputs by dependency hash,
the full variant inventory, separate historical assumptions, every retained
membership witness and the final frontier.
