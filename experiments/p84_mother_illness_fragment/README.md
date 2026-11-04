# p84 C: a conditional illness clause

This package extends the separately preserved
[German field-post fragment](../p84_field_post_fragment/README.md) with
`MUTTERSCHWERKRANKBITTEKOMMX` at plaintext positions 68–94. The
[case](../../cases/pages/084.md#edition-cases-radio-p84-mother-illness-extension) keeps the equally
compatible `MITTELSCHWERKRANKBITTEKOMMX` counterexample.

The unchanged 28–31 October key fixes 14/122 raw positions. The two word
fragments together propose 52/122. All five prior short-group frames remain
priced: frames 77–79 require no observed substitution, and frames 78–79 tie
at five printed-mask fills plus 42 added-slot fills. The representative is
frame 78. This preference is conditional on the words.

## Verification

From the repository root:

```bash
python experiments/p84_mother_illness_fragment/verify.py --verify
python experiments/p84_mother_illness_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

The second command requires PyMuPDF and the original PDF with SHA-256
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
It verifies PDF page 87 and the pinned crop's RGB hash. The ordinary check
requires the Python standard library and repository modules.

`inputs.json` pins the source, published key, candidate words and expected
frame prices. `verify.py` directly assigns a grid and checks its order against
the core arithmetic. It rebuilds both candidate ledgers, every position's
source ownership and complete re-encryption witnesses. No arbitrary witness
completion is promoted to a reading.

## Lexical provenance

The words were found by matching a dictionary to half-coordinate domains and
then composing a coherent clause. This is a lexical hypothesis. There is no
claimed native copy or authenticated retransmission of the new clause.

The dictionary is the existing ten-book, 53,465-word model with SHA-256
`6ea36fc166dd884a3a46f99aa7fd9ab03ae237d5a79c1a30f059e983d5f0d9ef`.
Its source URLs and hashes are in
[the frozen provenance](../p198_word_search/lexicon_provenance.json).
Rebuild it without adding attacked ciphertext or the new candidate:

```bash
python experiments/p198_word_search/build_lexicon.py --cache /path/to/book-cache --output /tmp/p84-lexicon
python experiments/p84_mother_illness_fragment/replay_words.py --lexicon /tmp/p84-lexicon/lexicon.txt
```

The second command checks the frozen dictionary entries and enumerates all
compatible dictionary words at the five selected starts, for every retained
frame. It does not claim to reconstruct the human composition of the clause.
`search_provenance.json` records the discovery sequence and its selection
limits. The earlier field-post phrase's shuffle controls apply only to that
earlier search.

**icekylinx and GPT-6 Astra Pro**, 4 November 2026. Apache-2.0.
