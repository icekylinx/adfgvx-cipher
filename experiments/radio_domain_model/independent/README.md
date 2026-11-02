# Independent word and radio objective audit

Prepared by **icekylinx and GPT-6 Astra Pro**. This audit checks the completed
word-search archive, the word objective's two implementations, and every entry
of the frozen radio and numeric-class model tables. It does not run an attack,
accept a historical plaintext, or count a pending search as complete.

The first audit preserves the exact
[30-case word-record snapshot](word_records_30_snapshot.json) and its
[report](audit_30.json). It checked **923,755,000 completed mutation proposals**;
the 19 declared pending cases are outside that report. Later audits can use
the live word archive without overwriting this initial snapshot.

The [final 49-case audit](audit_49.json) covers **all 49 original completed
logs**, **2,055,765,000 measured mutation proposals**, and **zero pending
jobs**. Its records hash matches the final collector and verification gate.
The initial 30-case snapshot and report remain unchanged.

## What is independently checked

The reference word scorer uses hash lookup of each bounded substring and a
backwards memoized recurrence over the preceding word identifier. It does not
use the search engine's trie or the verifier's forward table. A compiled
[harness](word_score_harness.cpp) calls the archived C++ scoring function without
invoking its optimizer. The initial comparison includes 82 distinct archived
truths, candidates, seed texts, digit runs, separator cases and deterministic
random strings. Both the C++ scorer and the forward Python scorer agree with
the backwards reference within **7.11 × 10⁻¹⁵**. This finite comparison supports
implementation consistency; it does not establish that the language objective
prefers correct historical wording.

The final audit expands that comparison to **101 distinct texts**. The maximum
absolute difference remains **7.11 × 10⁻¹⁵** for both implementations, and all
six independently reconstructed model tables still match byte for byte.

A separate [builder replay](lexicon_rebuild_check.json) regenerated the word
lexicon from the ten cached, hash-pinned books using the retained portable
builder. The complete lexicon and every provenance field match the frozen
artifacts: 1,091,203 weighted word occurrences, 53,465 distinct words and
176,836 retained word pairs. This check changes neither training data nor the
model used by the archived attacks.

When the original-log directory is provided, the audit checks each completed
log's hash, best and final events, monotone counters, completion marker and
input-file agreement with its manifest. It sums the final proposal counters,
not the best-candidate discovery counters. Neither the initial 30-case snapshot
nor the final 49-case archive has a warm control seed equal to the entire control
truth. Reused earlier optimizer
states remain reused observations, not fresh independent controls.

The model reconstruction counts training quadgrams independently with a
`Counter`, extracts coordinate indices from flattened radix-36 integers, and
rebuilds both normalized probability mixtures and class lookup adapters. All
six 36/37-index output tables match the recorded binary files **byte for byte**,
including every wildcard marginal. The two dataset splits have disjoint
declared families and no exact 32-character overlap across their training and
validation layers. This tests the recorded family map, not every possible
historical relationship between messages.

The sole initial finding was a latent exclusion-key typo, `Nov25-27` in place
of catalog key `Nov25-28`. It was corrected before this portable audit was
frozen. No selected training record used that period; the frozen dataset and
model bytes are unchanged. The report marks the issue **resolved**.

## Run the audit

NumPy and a C++17 compiler are required. The frozen table bytes were produced
with NumPy 2.3.5; use that recorded version when checking byte-for-byte model
reconstruction. The compiled harness lives in a temporary directory. Apart
from the explicitly requested report, the audit does not write repository
files or change a model.

```sh
python experiments/radio_domain_model/independent/audit.py \
  --quad /path/to/german_military36_quad.bin \
  --lexicon /path/to/lexicon.txt \
  --models /path/to/radio-models \
  --original-log-root /path/to/original-word-search \
  --records experiments/radio_domain_model/independent/word_records_30_snapshot.json \
  --output /tmp/independent-audit-30.json
```

Omit `--records` to audit the live `p198_word_search/records.json`. Omit
`--original-log-root` when the transient original logs are unavailable; the
report explicitly records that original-log checks were skipped. The model
and word-objective comparisons still run. The log root must retain the four
original manifest locations, with each input, `.jsonl` and `.result.json` file
alongside its corresponding manifest; absolute paths recorded by the original
run are resolved by basename for portability. It must also retain the original
`word_loss` executable at the log root so its archived binary hash can be checked.
A locally rebuilt executable can reproduce the scoring code but need not have
the same binary hash; keep that rebuild separate from the original audit artifact.

The source edition assumptions and earlier key/body credits remain in the
parent packages. This implementation audit is separate from the validity of
those historical interpretations and from the optimizer's search coverage.
