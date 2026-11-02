# Independent validation of the page 153 candidate

Authors: **IceKylin and GPT-6 Astra**.

This package independently checks a candidate discovered by the joint search.
It adds no blind recovery claim. It separates the exact received text,
conditional readable cribs, two proposed source-coordinate repairs and the
unresolved key cells.

## Exhaustive conditional check

`historical_input.txt` supplies a 66-character first-part crib with six
unconstrained date/number positions, its 132 received coordinates, a 42-letter
second-part crib and that part's 108 source slots. The second part has 15 erased
slots. The readable first-part crib is:

```text
ANORDNUNGENVOM?TEN??TENNR???BEZIEHENLASSENSOWEITNOCHNICHTGESCHEHEN
```

`enumerate_independent.py` uses a separately implemented fixed-order depth-first
search. It enumerates every width-18 long-column segmentation and every
compatible ordered column pairing with a single injective substitution square.
It reproduces the root C enumerator: 18,564 segmentations, four locally feasible
segmentations, 28 recursive states and exactly two partial-key representations.
They differ by swapping both columns in every adjacent pair and transposing
the square. They express the same reading.

The second crib is used only after the first-part enumeration:

```text
MUNITIONSBESTANDDERNACHHUTARTILLERIEMELDEN
```

Both partial keys disagree with exactly two received coordinates: second-part
source indices 3 and 4, both literal `A`, would need to be `X`. All other known
coordinates touched by this crib agree. The two source glyphs were visually
confirmed as `A`, so these are proposed editorial repairs, not transcription
corrections. The enumeration supplies conditional necessity within this
geometry; it cannot establish why the historical source has those symbols.

```sh
python3 enumerate_independent.py --input historical_input.txt --output work_historical.json
```

The independent random-key positive control has two equivalent keys and zero
second-crib mismatches. Changing the first crib's initial `A` to `N` while
leaving its ciphertext unchanged produces zero keys. Both results agree with
the root C implementation. These small controls check the enumerator, not a
historical recovery rate. Their inputs, evaluation-only truth and outputs are
included. `algorithm_review.json` records the completeness argument and the
exact C source hash reviewed.

The completeness claim assumes width 18, ordinary row-major plaintext
coordinates followed by column readout, per-part resetting, and an unchanged
first-part source. Other widths, geometries, edits or cribs are outside it.
The supplied first crib was chosen after discovering the candidate; this is
validation conditioned on that discovery.

## Nineteen cells versus twenty

The 60 specified first-part letters constrain 19 distinct square cells:

```text
?T?UGI???????WO?CMB??SZ??NDH?VEA??LR
```

There are still 17! = 355,687,428,096,000 complete injective squares extending
those assignments. The displayed solver's rare letters and numerals are not
therefore recovered historical values. In particular, the four distinct cells
in the first-part pattern are:

```text
VOM<alpha>TEN<beta><beta>TENNR<gamma><delta><gamma>
```

The equality and inequality relationships are retained; the four values are
not assigned. Interpreting the repeated month cell as `11` would forbid the
other distinct cell gamma from also being `1`.

Reading the second-part footer's separator-looking cell `AF` as `X` adds an
optional twentieth assignment:

```text
?TXUGI???????WO?CMB??SZ??NDH?VEA??LR
```

That interpretation is absent from the first-part crib and is not used in the
exact enumeration. It leaves 16! = 20,922,789,888,000 possible complete squares.
Neither mask is an independently attested historical key.

## Bounded keyword check

`check_dictionary.py` checks both equivalent rank representations against all
18-letter entries of the normalized German wordlist pinned by the fixed-search
suite. The 724,720-entry list contains 18,651 words of length 18, representing
17,729 distinct stable rank permutations. Neither recovered representation has
an exact match. Repeated keyword letters are ordered from left to right.

```sh
python3 check_dictionary.py --wordlist NORMALIZED_WORDLIST --output work_dictionary.json
```

The exact normalization and rebuild provenance are in
`experiments/fixed_search/tools/dictionary_pipeline.py` and its data files.
This check does not exclude a phrase, an unlisted word, another spelling,
a different ranking convention or a generated transposition. It does not
identify the historical keyword.
