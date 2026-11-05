# Exact decoding from two damaged witnesses

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

## Exact joint decoding of p109 B and D

<a id="what-this-adds-to-p109"></a>

An exact decoder now combines the coordinate evidence of p109 B and the
previously repaired p109 D with independent German language tables. It
searches all permitted plaintexts under an explicit coordinate-error
budget, retaining the ten highest-scoring candidates for each budget.
It uses no plaintext crib and does not use the editorial candidate in
training or as a search constraint.

All **28 highest-ranked candidates**, across two scoring objectives, seven
error budgets, and full-message/body-only runs, contain the following
47-character interval at zero-based positions `67:114`:

```text
XIMMARSCHAUFBELGRADERKANNTXSONSTKEINEEREIGNISSE
```

Its readable part is:

> … im Marsch auf Belgrad erkannt. Sonst keine Ereignisse.

That means “… observed marching toward Belgrade. Otherwise no incidents.”
The preceding subject and unit abbreviation still require interpretation.
Within this interval, 33 positions are already unique in the minimum-cost
source domains; the model selects the other 14 from competing letters.
This is **not 47 newly source-fixed letters**. Agreement between the two
objectives is a sensitivity result: they share the same training corpus
and are not statistically independent witnesses.

The mixed four-/six-gram objective also selects `UEBERGANG` once two
extra coordinate substitutions are available. The full editorial reading
is not the optimum of either objective. The models still produce
`SAVM`, `LETZTERXALLE`, or `FDU`, and at larger budgets sometimes replace
the well-supported abbreviation `DIV` with `DIE`. Those failures remain
visible in the results. No digit, call sign, or ending is accepted from
a model optimum.

The complete ranked results are in [p109_results.json](p109_results.json).
[p109_summary.json](p109_summary.json) contains exact counts, phrase costs,
agreement intervals, best-at-most-budget choices, and all reported
occurrences of the phrase probes.
For the historical reading, see [the p109 case](../../pages/109.md#edition-cases-p109).

## The source model

The input is the independently reviewed B transcription and the
`norbert18` variant of D, both under the recorded 1–3 November key.
The D input explicitly includes Norbert's published structural repair:
its original 258-coordinate transcript becomes a 248-coordinate witness.
The new algorithm does not silently replace that earlier hypothesis.
See [the source-parallel certificate](../../data/certificates/p109_parallel.json)
and [the prior-reading record](../../data/prior_readings.json).

The original timestamps and differing endings remain unresolved. A common
124-character plaintext is a model to test, not an established identity
of the two transmissions. Accordingly, the experiment also runs on the
body at positions `6:114`, excluding both the leading fields and the
different endings. That range is declared before optimization.

For a candidate plaintext symbol, its known square cell supplies two
coordinates. Each disagreement with an observed coordinate in either
witness costs one. A source erasure costs zero. The witnesses receive
equal weight; no undocumented preference for the cleaner-looking copy
is introduced. Every A–Z or digit symbol is allowed at every position,
subject only to the total cost budget.

| Scope | Plaintext positions | Coordinates compared per witness | Minimum combined cost | Exact budgets searched |
| --- | --- | ---: | ---: | --- |
| Full message | `0:124` | 248 | 42 | 42–48 |
| Body only | `6:114` | 216 | 39 | 39–45 |

All costs are measured **after the named earlier D repair**. They are not
edit counts against an untouched original D transcript.

The main lists are for **exact** costs: a candidate in the cost-46 list
spends exactly 46 substitutions. The summary also selects the best candidate
under each cost **ceiling**, using all preceding lists. In these recorded
runs, the best language score strictly improves at every excess budget,
so the same top-one strings remain selected under the ceiling interpretation.
Their larger-budget artifacts therefore cannot be explained solely by a
requirement to spend an otherwise unwanted extra error. No rerun is needed
to construct this envelope.

Every reported candidate is independently re-encrypted. The JSON lists
the received coordinate positions it would change in B and in the
conditioned D witness, plus its erasure fills. Their combined count is
checked against the dynamic program's source cost. The source files
themselves remain unchanged.

## Exact word costs and alternatives

These phrase probes are computed after the search. They expose the
source cost of editorial alternatives; they are not constraints used to
make the decoder print a desired phrase.

| Proposed text and position | Minimum extra cost for that text | B substitutions within the phrase | D substitutions within the phrase | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `SAVA`, `18:22` | 1 | 1 | 2 | A possible river-name completion; its final A is not fixed. |
| `SAVE`, `18:22` | 1 | 0 | 3 | An equal-total-cost alternative preserving every known B coordinate in the word. |
| `UEBERGANG`, `23:32` | 2 | 4 | 3 | Selected by mixed scoring at excess budget 2. |
| `TEILE`, `39:44` | 1 | 3 | 1 | Fits the proposed sentence, but is not selected in any reported top ten. |
| `1WEITERE`, `52:60` | 0 | 3 | 1 | Minimum-cost compatible; the model does not establish the numeral. |
| `FDLXDIV`, `60:67` | 0 | 0 | 2 | Preserves B's abbreviation; mixed scoring includes it among some alternatives. |
| `ERKANNT`, `86:93` | 0 | 0 | 3 | Preserves B exactly and appears throughout the model results. |

“Extra cost” means the cost above the sum of the positionwise minima for
that same span. The B/D substitution columns include the span's
irreducible disagreement cost, so their sum is larger than the extra
cost. The three disjoint requirements `SAVA` **or** `SAVE`, `UEBERGANG`,
and `TEILE` therefore require at least `1 + 2 + 1 = 4` additional
coordinates, or full-message cost **46**. This bound is achievable with
minimum-cost choices elsewhere; it is not a guarantee about the whole
sentence's historical wording.

The `SAVE` alternative deserves explicit retention. At position 21,
witness B reads the coordinate pattern `V?`, allowing `E` among its
literal possibilities while excluding `A`. `SAVA` and `SAVE` have the
same equal-weight total cost, but allocate the discrepancies differently
between the two witnesses. The Austrian State Archives catalogue uses
the spelling **Save** in its entry for a 26 October 1918 crossing order,
record `AT-OeStA/KA NL B/522.4.10`.
[Catalogue record](https://www.archivinformationssystem.at/detail.aspx?ID=7182872).
The document image was not inspected; this is nomenclature and context,
not a third copy of p109 or proof of its final river-name letter.

The ordinary four-gram model selects `SAVE` at excess budget 2 but
initially keeps the garble `UEBURGANG`. Mixed scoring resolves
`UEBERGANG` earlier and spends its remaining budget differently. In the
body-only mixed run at excess budget 6, `SAVE` is the first-ranked
alternative and `SAVA` appears at rank 8. Both variants must remain
qualified. The source-compatible spelling `ABENDMELUNG` is also
retained in the compact candidates; inserting the missing `D` of normal
German *Abendmeldung* would be a different geometry model.

## Candidate count at minimum coordinate cost

<a id="how-many-candidates-are-searched"></a>

At the full-message minimum, the two conditioned coordinate streams
contain 200 agreements, 42 disagreements, and six positions observed
only in D. Every disagreement admits either observed coordinate with
the same minimum cost. Because the 36-cell square is complete and
bijective, these coordinate choices correspond to distinct plaintexts.
There are exactly

\[
2^{42}=4,398,046,511,104
\]

full-message plaintexts at cost 42, and `2^39` body-only plaintexts at
cost 39. The reported minimum-cost body is the exact optimum among
those candidates, not the winner of a sampled beam.

The count at each excess budget is also exact. For two equal observations,
the agreed coordinate costs zero extra and each of five alternatives
costs two. For two different observations, either observed coordinate
costs zero extra and each of four alternatives costs one. With one
observation, five alternatives cost one. Therefore the full-message
count-generating polynomial is

\[
(1+5x^2)^{200}(2+4x)^{42}(1+5x)^6.
\]

The coefficient of `x^b` counts candidates at excess budget `b`. At
budget 6 alone there are **50,411,342,415,326,122,868,736** possible
full-message plaintexts. The body polynomial uses exponents 173, 39,
and 4 respectively. [The summary](p109_summary.json) records every
coefficient through budget 6 as an exact integer string.

## The dynamic program

The implementation is a general decoder for a fixed per-position symbol
cost matrix. It can be reused for other aligned witnesses with known
complete squares, or for other finite per-position domains. It does not
by itself solve globally coupled unknown square assignments or unknown
alignment/repair geometry.

At each position, a state contains:

- The last three letters for a four-gram objective, or the last five for
  a six-gram objective.
- The exact excess source cost already spent.
- The ten best prefixes reaching that state, ordered by integer score
  and then ordinary ASCII lexical order.

Appending a symbol adds its position cost and the completed language
gram. Prefixes reaching the same suffix and cost have identical future
options. A prefix below the best ten in that state cannot enter the
global best ten: the ten better prefixes can take the same continuation.
This dominance argument makes the retained state exact. No beam width,
score cutoff, or randomized search is used.

The largest run reached **710,816** suffix/cost states in one layer.
The state cap is a hard failure condition, not a pruning rule. None of
the recorded runs hit it.

### Deterministic scoring

The independently sourced military tables are the repository's existing
hash-pinned four-gram and six-gram models. Their provenance lists ten
German books and no challenge plaintexts.
[Model provenance](../joint_search/models/provenance.json).

Two additive objectives are tested:

1. Mean four-gram log frequency.
2. `0.3 × mean four-gram + 0.7 × mean six-gram` log frequency.

Every stored float32 log value is represented exactly at integer scale
`2^24`. For a message of length `n`, the mixture uses integer coefficients
`3(n−5)` and `7(n−3)` and divides only for display by
`10(n−3)(n−5)2^24`. This preserves the stated mean-score objective
without floating-point accumulation or tie drift. Six-gram hash lookups
and all final scores are cross-checked against the separately written
Python model reader used for p215.

The resulting scores are ranking functions, not posterior probabilities.
The corpus is independent of the target plaintext, but the two objectives
are built from that same corpus. Their shared errors illustrate why
agreement alone cannot settle historical readings.

## Validation and reproducibility

The recorded checks include:

- Independent exhaustive enumeration of 512 finite-domain completions
  for each Markov order, comparing every top-eight list at budgets 0–3.
- A 256-completion zero-score fixture verifying lexical tie order,
  including the distinction between digit and letter ordering.
- A 256-completion coordinate-cost fixture using different column
  permutations for the two witnesses, a source erasure, and an
  irreducible coordinate disagreement. Direct ciphertext mismatch
  counts agree with the positionwise cost sums.
- Independent re-encryption and Python objective checks for all 280
  reported p109 candidates.

With the existing model files available, reproduce all four runs:

```sh
python3 experiments/parallel_decoder/compute.py \
  --military-quad /tmp/adfgvx-models/german_military36_quad.bin \
  --military-six /tmp/adfgvx-models/german_military36_sixgram.bin \
  --work-dir /tmp/adfgvx-parallel-reproduce \
  --max-budget 6 \
  --top-k 10 \
  --verify

python3 experiments/parallel_decoder/summarize.py --verify
```

The first command recompiles the C++17 engine, validates the models,
runs the exhaustive controls, recomputes all rankings, and compares the
result with the stored JSON. Omit `--verify` to regenerate a result.
The summary command needs only Python and the recorded results.
Compiler outputs, cost files, and raw engine output stay in the selected
temporary working directory.

## Remaining source and language-model uncertainty

<a id="what-remains-uncertain"></a>

The two witnesses may differ in more than transmission errors, especially
in their endings. Other repairs of the original D transcript remain
possible. A character can have the best language score while being
wrong historically; abbreviated unit names, numbers, and call signs
are particularly poorly modeled by running-text n-grams.

The decoder strengthens the Belgrade/`ERKANNT` passage under the stated model,
quantifies the costs of the disputed words, and preserves `SAVE/SAVA`
and other alternatives with their limits. It does not turn a repaired
editorial interpretation into an untouched-ciphertext solution.
