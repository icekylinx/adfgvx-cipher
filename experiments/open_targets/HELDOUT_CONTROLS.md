# Held-out language-model checks for two planted controls

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro (2026)**

The wrong Nov13b control candidate outranks the planted truth under two independently sourced German war books, even with six-grams. The CHI13 wrong candidate loses under both held-out mixed models. This post-hoc comparison shows both the usefulness and the limits of changing the language model; it does not optimize any historical case or establish a plaintext acceptance threshold.

## Frozen texts and source-preserving witnesses

Both synthetic controls encode the same newly written 85-character body:

```text
DERSTABMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBITTEWEITEREBEFEHLEUEBERMITTELN
```

It reads approximately: “The staff reports that the bridge by the village is now usable again. Please transmit further orders.” The continuous telegram-style spelling deliberately supplies no spaces or punctuation.

The exact joint-quad decoder under the true fixed CHI13 square selects this different source-preserving text:

```text
DERSTABGELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBITTEREITEREBEFEHLESEKERMITTELN
```

Under the true fixed Nov13b square, the corresponding wrong candidate is:

```text
DERSTARMELDETDIEBRUECKEBEIDEMDORFNUNWIEDERBENUTZBARISTBETTEWEITEREBEFEHLEUEBERMITTELN
```

The second changes only two characters, but `DERSTARMELDET` and `ISTBETTE` are not the planted message. [Frozen inputs](joint_control_inputs.json) retain both true squares, rank orders, original 165-coordinate received strings, planted full ciphertexts, and each candidate's five missing positions and inserted values. Every candidate re-encrypts exactly after that stated insertion and preserves all 165 received coordinates.

The compared candidates came from the [exact joint-loss decoder](../p198_joint_exact/README.md), before either held-out model was built. The new source models never choose a new key, loss geometry, or letter filling in this diagnostic.

## Independent books and scoring

The source books are Paul Emil von Lettow-Vorbeck's [*Meine Erinnerungen aus Ostafrika*](https://www.gutenberg.org/ebooks/71877), 1920, and Walter Flex's [*Der Wanderer zwischen beiden Welten*](https://www.gutenberg.org/ebooks/52118), the 1918 edition. Neither appears among the original repository model's training books. The [source manifest](heldout_sources.json) pins their exact downloaded bytes.

For each book separately, remove the Gutenberg wrapper, expand umlauts, uppercase the text, and retain A–Z and digits. Build quadgram and six-gram counts for joined text, sentence-boundary `X`, and word-boundary `X`. Report each convention separately and also a **5:3:1 count mixture**, matching the original model's normalization weights. The different conventions reuse one book and are not independent replications.

An observed n-gram receives `count / total`; an unseen n-gram receives `0.01 / total`. Convert each probability to a base-10 logarithm and round it to float32 before averaging all complete-text windows. The mixed score is 30% of the quadgram mean plus 70% of the six-gram mean. All candidates have 85 characters, so each comparison contains 82 quadgrams and 80 six-grams.

## Results

Values are **wrong-candidate score minus planted score**. Positive values favor the wrong candidate. They are score differences, not probabilities or likelihood ratios for independent messages.

| Model | Wrong candidate | Quad difference | Six difference | 30/70 mixed difference |
| --- | --- | ---: | ---: | ---: |
| Original ten-book model | CHI13 | +0.063606 | −0.222219 | −0.136471 |
| Original ten-book model | Nov13b | +0.116412 | +0.107354 | +0.110072 |
| Held-out Lettow-Vorbeck, 5:3:1 | CHI13 | −0.000782 | −0.331378 | −0.232200 |
| Held-out Lettow-Vorbeck, 5:3:1 | Nov13b | +0.119492 | +0.099481 | +0.105484 |
| Held-out Flex, 5:3:1 | CHI13 | −0.060307 | −0.232859 | −0.181093 |
| Held-out Flex, 5:3:1 | Nov13b | +0.074846 | +0.045334 | +0.054188 |

The Nov13b wrong candidate also wins with **each convention taken separately**, under both books and both n-gram lengths. CHI13 loses under all six-gram and mixed comparisons. Its quadgram sign changes with the convention: both books' plain and sentence-boundary models reject it, while both word-boundary models favor it.

The original-model comparisons were independently rescored from the fixed complete texts using the existing pinned binary quad/six models. The frozen input file retains those numbers. The held-out score file retains all 16 source-specific n-gram tables' totals, unseen floors, hashes of complete count dictionaries, and the counts of every n-gram needed for these three compared texts. That is enough to check the reported held-out scores without downloading books or loading binary models.

## What follows, and what does not

These comparisons support diagnosing the Nov13b result as a language-objective problem that persists beyond the original training corpus. They do not prove that every better model will fail, that the original optimum remains globally optimal under a new model, or that a historical message with the same score is wrong. Only the frozen candidates are compared here.

A grammatical or word-based model may distinguish errors such as `STARMELDET` and `ISTBETTE`, but it must be calibrated against additional fresh controls and actual historical conventions before its preference is promoted to evidence. Source parallels, original images, coordinate-preserving repairs, and key reuse remain more direct constraints than a small n-gram score margin.

## Reproduce

```sh
python experiments/open_targets/heldout_rescore.py \
  --cache /path/to/heldout-books --download \
  --output /path/to/rebuilt_heldout_control_scores.json

python experiments/open_targets/heldout_rescore.py \
  --cache /path/to/heldout-books \
  --verify experiments/open_targets/heldout_control_scores.json \
  --output /path/to/reproduced_heldout_control_scores.json

python experiments/open_targets/verify_light.py
```

The full rebuild verifies both source hashes, retrains every documented source-specific table, checks all complete-count hashes, and reproduces the score file. The lightweight command independently decrypts the candidate witnesses and recomputes their held-out scores from published relevant counts; it does not rebuild the entire books' count dictionaries.
