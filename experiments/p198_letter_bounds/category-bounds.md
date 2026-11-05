# Bounds for the 24 fixed ordinary letters

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

## Result

Across every completion of the recorded Nov13-15b partial square, every
five-coordinate deletion geometry and every filling of those coordinates,
p198 has at most **75 positions containing one of the 24 fixed ordinary
letters other than Q and Y**. Equivalently, this family satisfies

\[
n_{\mathrm{digits}}+n_Q+n_Y\geq10.
\]

The [separate ordinary-letter bound](README.md) also gives

\[
n_{\mathrm{digits}}\geq3.
\]

These conditions hold simultaneously, but they do not describe the entire
digit/Q/Y trade-off frontier. The historical counts are unknown, so neither
condition rejects or authenticates the key.

The first inequality is tight: an explicit source-compatible witness has
**75 target letters, no Q, no Y and exactly ten digits**. Therefore, within
the subset of this family containing no Q or Y, the attainable minimum
digit count is exactly ten. This conditional statement does not assume
that the historical plaintext lacked Q or Y.

## Category invariance across 40,320 square completions

<a id="why-one-category-assignment-covers-all-40320-square-completions"></a>

The target category is precisely:

```text
ABCDEFGHIJKLMNOPRSTUVWXZ
```

All 24 symbols already occupy known cells of the partial square. Its eight
unknown cells contain only `Q`, `Y`, `2`, `3`, `4`, `7`, `8`, `9`, which all
score zero for this objective. Thus every one of the `8! = 40,320` complete
squares assigns **the same category indicator to every cell**. No ranking
by letter frequency or assumption about digit meanings is involved.

One arbitrary representative completion therefore suffices to optimize
this category count over all complete-square extensions. Its particular
digit ordering has no effect on the bound. For the recorded witness the
representative is:

```text
HQYBMUF15PX0DJLR2347S6VONKZ8AWITEGC9
```

The maximizing witness inserts coordinates `AAFAA` at zero-based ciphertext
positions `63,71,101,105,114`. All 165 received coordinates remain unchanged
and in their original relative order. Its full text and ciphertext are in
[category_bounds.json](category_bounds.json), solely as a feasibility
witness. The count objective does not make this text plausible German,
and no historical plaintext is accepted.

## Exact optimization and controlled implementation change

The category indicator is additive across plaintext positions. The
reviewed [letter-count engine](exact_letter_bounds.cpp) therefore applies
with the same 15,504 column-loss allocations, exact local coordinate-fill
choices, canonical witness ties and maximum of 32 active states. Every
loss mask and coordinate filling remains covered.

[category_audit.py](category_audit.py) leaves the five frozen base-package
files unchanged. It checks the original C++ source's exact SHA-256, requires
each declared replacement to occur exactly once, and generates a separate
C++ file in the selected temporary directory. One replacement changes the
cell indicator from A–Z to A–Z excluding Q/Y; three rename output fields
to make the narrower category explicit. The report records all four
replacements and the generated source's hash. A changed base engine or
an unexpected replacement count aborts the audit instead of silently
adapting different code.

This is a count objective only. It uses no language model, corpus score,
probability, or numerical-frequency prior. The earlier ordinary-letter
search remains unchanged and supplies the separate minimum of three digits.

## Controls and verification

Three short controls contain explicit Q, Y and digit symbols and use widths
4, 6 and 16. Independent Python enumeration visits all **10,188** possible
loss/fill witnesses and checks both minimum and maximum category scores.
All six canonical count/mask/fill optima agree with the generated engine.
A full synthetic Nov13-15b control supplied with its true key attains
85 target letters, as its planted text permits.

The historical witness is independently decrypted, counted by category,
re-encrypted and reduced to the original received ciphertext. The category
invariance is checked directly from the partial square. A quick verification
checks these recorded facts and file hashes without rerunning the search:

```sh
python3 experiments/p198_letter_bounds/category_audit.py --verify-recorded
```

To regenerate the adapted engine, repeat all exhaustive controls, search
the complete geometry space and compare the report:

```sh
python3 experiments/p198_letter_bounds/category_audit.py \
  --work-dir /tmp/adfgvx-category-reproduce \
  --verify
```

Omit `--verify` to regenerate the report. The fast recorded-witness check
does not itself prove optimality; the full command reruns the exact search.
