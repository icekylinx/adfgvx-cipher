# p153: historical key construction and exact keyword searches

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

## Result

This investigation does **not** assign another p153 digit or plaintext letter.
It establishes why two tempting ways to complete its square are unsupported,
and makes the negative searches reproducible.

| Investigation | Coverage | Result |
| --- | --- | --- |
| A–J followed by digits | Both `A0…J9` and `A1…J0`; 16 square routes, with and without wrap | Neither convention fits any of the 21 historical/comparison squares or the p153 core. |
| One shared keyword for both key components | Every A–Z keyword equality pattern compatible with each numeric transposition; 16 routes; arbitrary digit placement allowed in a conservative relaxation | No historical/comparison key or either equivalent p153 representation survives. |
| Exact dictionary ranks | 724,720 normalized entries; relevant lengths 15–23 | No p153 match. The only match is the previously injected p217 implementation control. |
| Exact contiguous phrase ranks | Ten books, two umlaut normalizations, 8,720,768 letters; 26 key representations | No p153 match. `TRUPPENVERSCHIEBUNG` occurs twice in one independent book, in both normalizations. |

The historical/comparison group contains the fourteen period keys, the
13 November CHI key, the five July/August keys, and the undated NSA CHI
example. The entirely unknown square for `NSA-June1-CHI-21` supplies no
square-construction evidence and is skipped in those tests. The instructional
`VIKINGSCROWNHOTEL` key and the reported `TRUPPENVERSCHIEBUNG` key are kept
separate as positive controls. Full per-key results are in
[result.json](result.json) and [keyword_search.json](keyword_search.json).

## What the primary sources establish

The Childs collection prints the phrase `VIKINGS CROWN HOTEL`, its numeric
transposition, and its square on printed pages 11–12 (PDF pages 14–15).
Direct inspection confirms the square reproduced in the repository. Taking
the phrase's letters in first-occurrence order, appending unused letters
alphabetically, and inserting the digits `1…9,0` after `A…J` reproduces it
exactly. The earlier text introduces a set of messages submitted for study;
this worked construction is not evidence that every intercepted wartime key
used that procedure. [Childs collection, printed pp. 6, 11–12](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).

The reported p217 square similarly matches `TRUPPENVERSCHIEBUNG` with
`0…9` after `A…J`. Its recorded full square is used only as a construction
control. This does not independently resolve the ambiguous handwritten
digits or supply a missing parent-document provenance. See the
[p217 case](../../cases/p217.md) and the key's provenance in
[the key catalogue](../../data/keys.json).

Lasry, Niebel, Kopal, and Wacker analyze the substitution key as an arbitrary
36-cell permutation in §2.2. More decisively, §5.4 separates algorithmic key
recovery from exact digit identification: the latter requires traffic context
and outside intelligence, such as recognizing unit numbers. The paper does
not supply a universal digit-placement rule that would fill p153's missing
cells. [Author copy of the research paper, §§2.2, 5.4](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf),
[DOI](https://doi.org/10.1080/01611194.2016.1169461).

The contemporary survey distinguishes western `CHI` from eastern `RICHI`
in the preamble and key schedules. Its description does not establish the
above keyword constructions as the general generator of either traffic
system. Its discussions of dummy letters in other systems cannot be
transferred to p153's ADFGVX footer without separate evidence.
[German Military Ciphers from February to November 1918, printed pp. 13–16](https://www.nsa.gov/Portals/75/documents/news-features/declassified-documents/friedman-documents/publications/FOLDER_268/41784789082381.pdf).

These are bounded source findings. They do not prove that the original
German key-generation instructions never existed, that all keys were
randomly generated, or that independent square and transposition keywords
were impossible.

## Calibration before inference

The two controls are reconstructed by forward encryption-key generation,
before any negative result is interpreted:

| Control | Normalized keyword length | Digits after A–J | Square and numeric transposition reproduced? |
| --- | --- | --- | --- |
| Worked `VIKINGSCROWNHOTEL` | 17 | `1234567890` | Yes |
| Reported `TRUPPENVERSCHIEBUNG` | 19 | `0123456789` | Yes |

Each passes only the normal row-major route in the shared-keyword test.
For its matching digit convention, each passes normal row-major with
linear or cyclic interpretation. Neither digit convention passes any of
the 21 historical/comparison keys. Consequently a generator that works
on these two examples has failed its broader calibration; it cannot
justify assigning p153's date or serial digits.

The digit test allows either axis direction and serpentine traversal.
It treats every `(letter, digit)` pair as a two-cell placement and checks
that all ten pairs can coexist without occupying the same cell. It
honors observed letters and digits; remaining question marks may be
completed only injectively. Arbitrary row and column relabeling is
outside this bounded test.

## Exact exclusion of the shared-keyword family

The second test is stronger than trying a dictionary. It covers **every**
A–Z string whose stable alphabetical ranks equal the recorded transposition.
Equal letters are ranked from left to right, as in the two controls.

Let `q` list physical column positions in increasing-rank order. At an
adjacent descent, `q[i] > q[i+1]`, the keyword letters must be different:
equal letters would have received the opposite tie order. At an ascent,
they may be equal or different. Choosing those optional equality
boundaries enumerates all possible repeated-letter patterns. The actual
letters have not yet been selected.

For p153's main representation there are **1,024** such patterns. For
each one, reading the equality classes in physical column order and
keeping their first occurrences determines the order of the deduplicated
keyword prefix. The proposed square generator then appends letters absent
from that keyword in alphabetical order.

Now take just the known letters of the observed square along a chosen
route. Ignore all digits, all unknown cells, and exact spacing. Any
successful construction must split that known-letter sequence into:

1. An initial subsequence embedded in the keyword prefix.
2. A strictly increasing suffix consisting of letters absent from the
   keyword.

The checker tries every allowable split and prefix embedding. It enforces
the relative order of assigned alphabet values and checks that enough
unused alphabet values remain between them for the unassigned classes.
Allowing arbitrary digit placement and ignoring cell spacing makes this
a **relaxation**: a genuine generated square must pass, while a relaxed
pass need not yield a genuine square.

No pattern passes for p153. The same result holds when every adjacent pair
of physical columns is exchanged and the square is transposed, the
equivalent representation that reverses the coordinate pairs. All 21
historical/comparison keys also fail. Both construction controls pass.

As a separate check on false exclusions, 128 seeded A–Z words of lengths
15–23 were generated independently. Their squares use deduplicated
keyword prefixes, alphabetic tails, arbitrary digit insertion, randomly
selected routes, and partial observations. Every actual construction
passes the necessary-condition checker.

**Scope:** the exclusion applies to one shared keyword and the stated
routes/alphabet. It does not exclude separate keywords, different alphabet
orders, additional permutations, unrelated generators, or a different
underlying source transcription. It yields no new plaintext by itself.

## Dictionary and phrase results

The dictionary is the existing normalized `enz/german-wordlist` input,
pinned to SHA-256
`3573b3957d004f1b3dc8b84f24bd944234e52c75fe596a8381e1dcf9de0a0495`.
It contains both umlaut expansions and unaccented variants, plus the
previous experiment's explicitly documented context words and injected
`TRUPPENVERSCHIEBUNG` control. See its
[provenance](../fixed_search/data/wordlist_provenance.json). Of particular
relevance, **18,651** candidates have p153's 18-column width; neither
equivalent rank sequence matches any of them.

The phrase search goes beyond whole-word lookup. It examines every
contiguous letter window in the ten hash-pinned books already used as
independent corpus sources. Each book is uppercased, normalized once with
`AE/OE/UE` and once with `A/O/U`, and stripped of characters outside A–Z.
Windows may therefore span words or punctuation. Complete source files,
including Gutenberg headers and footers, are included; windows never
cross file boundaries. This normalization is intentionally distinct from
the statistical-model training pipeline.

There are **8,720,428 windows per 18-column key representation**. Neither
p153 representation matches. Of all 26 tested key representations, only
the reported p217 key matches the book corpus. Its keyword appears twice
in Karl Helfferich's *Der Weltkrieg*, volume III (1919), Gutenberg 52159.
Both normalizations preserve those two occurrences, giving four recorded
hits. These naturally occurring hits are independent of the dictionary's
injected control. They establish a successful retrieval control, not that
Helfferich's book was the historical source of the key.
[Source book](https://www.gutenberg.org/ebooks/52159).

The C scanner's rank comparisons are independently checked against Python
sorting for every window of a 3,382-character fixture. The fixture includes
one constructed witness for every numeric target, both named control
keywords, and seeded random letters. Both implementations produce the
same 28 matches and cover all 26 target representations.

## Reproduce

The structural analysis uses only Python's standard library and the
repository's existing key catalogue:

```sh
python3 experiments/p153_key_structure/analyze.py --verify
```

For the searches, prepare the existing normalized wordlist and the ten
source books using the repository's documented
[dictionary pipeline](../fixed_search/README.md) and
[model-source workflow](../joint_search/README.md). The search verifies
every source hash before proceeding. A C11 compiler is required.

```sh
python3 experiments/p153_key_structure/search_keywords.py \
  --wordlist /tmp/adfgvx-key-structure/normalized-words.txt \
  --corpus-dir /tmp/adfgvx-corpus \
  --work-dir /tmp/adfgvx-key-structure/reproduce \
  --verify
```

Omit `--verify` to regenerate the corresponding result file. The compiled
scanner, normalized book streams, original books, and dictionary remain
in the requested temporary directory. Only code, hashes, counts, and
small result records belong in this experiment.

## Consequence for the case

The most likely p153 body readings remain those in
[p153a](../../cases/p153a.md) and [p153b](../../cases/p153b.md). The exact
date/serial/footer ambiguity is documented in the
[extension analysis](../p153_extension/README.md). A justified further
completion needs new traffic evidence, a recovered companion part, or
independent historical key material. A convention selected only because
it produces a readable date would not supply that evidence.
