# Exact digit symmetry with each candidate's loss pattern fixed

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

**A numerical class score cannot identify the names of unanchored digits.**
For each of the eight recorded `book_class` and `radio_class` candidates,
this package freezes its square, column ranks, five loss positions and
five coordinate fills. Permuting the unanchored digit labels jointly in
its square and plaintext produces exactly the same full ciphertext, the
same 165 received coordinates, and the same class score.

The exact family contains **k! distinct complete squares** and
**k! / (k−r)! distinct literal plaintexts**, where *k* is the number of digit
labels absent from the partial-square anchors and *r* is the number of
those labels that actually occur in the recorded candidate plaintext.
These are exact counts for this digit-permutation family, with the
candidate's letter placements fixed. They are not totals over all possible
completions of the partial square or over other loss patterns.

There is a second, separate limitation: **85/85 agreement after collapsing
digits does not imply that the literal truth belongs to this family.**
Two of the three perfect class matches have the wrong equality pattern
among their digits. Their truth-in-orbit booleans and explicit conflicts
are given below.

## Exact counts for the eight recorded candidates

“Literal” and “class” are agreement with the authored truth, each out of
85. “Truth in orbit” asks whether a permitted digit permutation can turn
this candidate's entire plaintext into that truth while keeping its
recorded loss pattern and coordinate fills fixed.

| Control key | Objective | k | r | Complete squares in this orbit | Distinct literal plaintexts | Literal | Class | Truth in orbit |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| CHI-Nov13 | book_class | 10 | 9 | 3,628,800 | 3,628,800 | 70 | 85 | **False** |
| CHI-Nov13 | radio_class | 10 | 9 | 3,628,800 | 3,628,800 | 70 | 85 | **False** |
| Nov13-15b | book_class | 6 | 4 | 720 | 360 | 80 | 85 | **True** |
| Nov13-15b | radio_class | 6 | 5 | 720 | 720 | 78 | 83 | False |
| Nov10-12 | book_class | 5 | 4 | 120 | 120 | 74 | 80 | False |
| Nov10-12 | radio_class | 5 | 4 | 120 | 120 | 77 | 81 | False |
| Nov7-9 | book_class | 2 | 2 | 2 | 2 | 82 | 84 | False |
| Nov7-9 | radio_class | 2 | 2 | 2 | 2 | 84 | 84 | False |

The unanchored digit sets are respectively `0123456789`, `234789`,
`56789` and `56`. Every other square label remains at the recorded
candidate's cell. This includes unanchored letters whose locations the
candidate selected: they are not moved by this audit. The Nov13-15b
control's conditional `Y` anchor is preserved exactly as it appears in
the frozen control input; this audit introduces no new anchor.

Do not add the table's orbit sizes as though they were disjoint sets.
They describe separate recorded optimization outcomes, and some families
can overlap. In particular, counts of verification operations are not
counts of unique squares across all rows.

## Why the counts and ciphertext invariance are exact

Let `S` be a complete substitution square extending the partial anchors,
`P` its candidate plaintext, and `U` the set of *k* unanchored digit labels.
Let `π` be any permutation of `U`, extended to fix every other symbol.
Define `S′ = π(S)` by replacing the labels in their existing cells, and
`P′ = π(P)` by the same replacements in the plaintext.

1. **Each plaintext symbol keeps its coordinate pair.** If a symbol `a`
   occupies cell `i` of `S`, then `π(a)` occupies cell `i` of `S′`.
   Equivalently, `S′⁻¹(π(a)) = S⁻¹(a)`. Fractionation therefore produces
   exactly the same coordinate stream for `(S,P)` and `(S′,P′)`.

2. **The remaining cipher operations are fixed.** Reading columns in the
   same rank order produces the same complete 170-coordinate ciphertext.
   Removing the same five positions yields the same 165-coordinate
   received string. The coordinate letters at those five positions also
   stay identical, so the recorded fills are unchanged. Known anchors
   remain valid because no anchored digit belongs to `U`.

3. **There are exactly k! distinct complete squares in this family.**
   Every label of `U` occurs once in the complete square. Two different
   permutations therefore differ at a square cell. The action on squares
   has no nonidentity stabilizer. Other possible letter placements are
   outside this family.

4. **There are exactly k! / (k−r)! distinct plaintexts.** Only the *r*
   digit labels appearing in `P` affect the resulting text. Their images
   must be distinct, giving `k × (k−1) × … × (k−r+1)` possibilities.
   Every such injection extends to `(k−r)!` full permutations on `U`.
   Equivalently, the permutations fixing `P` can freely permute only the
   *k−r* unused-in-plaintext labels. The quotient is the stated count.

This also covers the boundary cases: if `r=0`, the text is unchanged
under all `k!` square relabellings; if `r=k−1`, each visible mapping fixes
the last label, so the number of literal texts is still `k!`.

Collapsing every digit to `#` leaves the entire class string unchanged.
Consequently every objective that is a function of that class string is
constant on the orbit. These two recorded objectives have word weight
zero, and their quadgram tables depend only on the 27 classes A–Z and
`#`. No assertion of digit-permutation invariance is made for the separate
36-symbol `book` and `radio` objectives, or for a numerical prior.

## Perfect class agreement can still have a wrong equality pattern

The authored truth in control 0 begins:

```text
NRX274XDERTRANSPORTMIT36WAGEN...
```

The two candidates with 85/85 class agreement begin:

```text
book_class:  NRX980XDERTRANSPORTMIT28WAGEN...
radio_class: NRX653XDERTRANSPORTMIT15WAGEN...
```

At **zero-based positions 4 and 23**, the book candidate repeats digit
`8`, and the radio candidate repeats digit `5`. The truth has `7` at
position 4 and `6` at position 23. A permutation cannot send one digit
to both `7` and `6`. Thus the literal truth is outside both recorded
candidates' digit orbits despite their exact class texts and class scores.
Their loss positions/fills differ from the truth's loss witness. This
shows that a perfect class score can hide a remaining loss/equality
ambiguity as well as unknown labels; merely renaming digits cannot
repair these particular candidates.

Control 1's `book_class` candidate gives the complementary example:

```text
candidate: AX6XSX3718X...SEIT13NOVEMBER...ZAHLUNG450000MARK...
truth:     AX6XSX2814X...SEIT12NOVEMBER...ZAHLUNG350000MARK...
```

The required mappings are `3→2`, `7→8`, `8→4`, and `4→3`. They are
consistent and injective, while anchored digits `0,1,5,6` stay fixed.
The two unused-in-plaintext source labels `2,9` can map to the remaining
target labels `7,9` in either order. Exactly **two complete squares in
this orbit** therefore produce the literal truth, with the original
candidate's ranks, loss positions and fills. The certificate includes
one explicit full permutation and its complete square.

That representative square need not equal the original truth-generation
square: the latter can place unobserved letters differently. The boolean
above is deliberately about **literal plaintext membership** in this
candidate's fixed digit orbit, not equality with the originally generated
full key.

## What was enumerated, and what was proved by counting

The standard-library verifier exhausts all digit permutations for the
six rows with `k≤6`: **1,684 permutation evaluations** in total. It checks
the unchanged full ciphertext, all received coordinates, fills, anchors
and class text for every permutation, and independently counts distinct
squares and literal texts. A deterministic hash records each enumeration
stream in the certificate.

For the two `k=10` rows, **10! was not enumerated**. The exact count follows
from the proof above. The verifier explicitly checks the nine adjacent
digit swaps `0↔1, 1↔2, …, 8↔9`, a generating set of the full permutation
group. It checks the analogous generators for the smaller rows as well:
**38 generator witnesses** across all eight rows. Every generator's
complete square and plaintext are retained.

An additional binary-table audit checks **all 36⁴ = 1,679,616 entries
per table**, or **3,359,232 entries across both tables**. Every float32
entry is bit-for-bit identical to the representative obtained by replacing
all digit indices with the same numeric-class index. The audit also
recomputes the recorded candidate/truth scores and verifies exact score
equality for all 38 generator witnesses. This is a full lookup-table
invariance check, not a full enumeration of the 10! key orbits.

## Frozen evidence and reproduction

- [`inputs.json`](inputs.json) preserves the eight original result rows
  and four authored controls without changing their squares, ranks,
  loss positions, fills, model hashes or truths. It binds the upstream
  dataset, results, class builder and model provenance by SHA-256.
- [`certificate.json`](certificate.json) contains the counts, all generator
  witnesses, small-orbit enumeration hashes, and prominent
  `truth_in_fixed_candidate_plaintext_orbit` booleans with their proof
  witnesses or conflicts.
- [`binary_table_check.json`](binary_table_check.json) preserves the
  optional complete adapter check and exact objective values.
- [`verify.py`](verify.py) uses only Python's standard library. Its cipher
  implementation is independent of the search engine and project cipher
  module.

Run the mathematical and source-binding verification from the repository:

```bash
python experiments/radio_domain_model/digit_symmetry/verify.py
```

To also repeat the complete binary-table check:

```bash
python experiments/radio_domain_model/digit_symmetry/verify.py \
  --models /path/to/unchanged/radio-model-tables
```

The local audit used `/tmp/adfgvx-radio-model`. The optional `--write`
flag regenerates only this directory's derived certificate and binary
check; the usual commands verify the existing frozen files.

These are fresh authored controls, not historical telegrams. The result
is an exact identifiability limit for the declared objective and recorded
candidate geometries. It supplies no historical digit assignment and
changes no model, baseline key or existing experiment ledger.
