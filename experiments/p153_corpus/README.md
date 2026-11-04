# Fixed p153 CHI key: source-corpus retrieval experiment

Prepared by icekylinx and GPT-6 Astra Pro on 2 November 2026.

## Result

The recovered p153 column rank was applied to **788 extracted OCR ciphertext blocks**, covering printed pages 57–230 of the Childs collection. The program evaluated **10,896 fixed-key layout/square models**, including repeated geometries. The two p153 blocks were the only coherent matches identified. No additional companion was accepted.

This is a **retrieval experiment, not an exclusion proof**. The OCR can omit, merge, split or misread blocks. The partial square, uncertain message lengths and limited layout models leave other same-key messages possible.

## Reproduce

Python 3 and its standard library are sufficient. No network, full book, external repository or language-model installation is required.

```sh
python run_screen.py --verify
```

The check reproduces the supplied summary and the SHA-256 digest of every evaluated model result. To inspect all results:

```sh
python run_screen.py --all-output all_results.jsonl --output reproduced_summary.json
```

The included verification passes with 788 blocks and 10,896 models. The all-model digest is `34ae75827f4989f25fc5b48bd9168e142a63e13ab42ccb11593a5fcbb85ddb21`.

## Inputs and models

- `inputs.json` contains only extracted ciphertext groups and their printed-page, PDF-page and OCR-line locators. The groups are explicitly unverified. Full-page OCR and scanned books are not included.
- `config.json` records the 18-column rank, 19-cell partial square and two visually checked p153 controls. A second model adds `AF=X` as a separate separator hypothesis. No date, order-number or unit-number digits are assigned.
- `ranking_weights.json` preserves the numerical quadgram weights used in the initial screen. They derive from the public baseline repository's military vocabulary; its URL, source hash and formula are included.
- `expected_summary.json` records the controls, highest-ranked candidates and all ranked candidates from nearby printed pages 146–170.

The raw OCR geometry is tried first. Explicit alternatives align short or long OCR groups to five slots, and enumerate one-character insertion/deletion possibilities when at most three nonfinal groups contain four or six characters. These are hypotheses about OCR layout, not corrections to the historical source. Arbitrary missing whole groups and general transmission errors are outside this scan.

For odd-length hypotheses, the final unpaired coordinate is retained in the result record and is not scored as a plaintext letter. Such a result is not a complete decryption.

## Interpretation limits

The ranking averages only fully observed quadgrams and can reward chance fragments. For example, an incoherent p178 OCR candidate ranks marginally above p153 part 5 on only five observed quadgrams. Numerical rank is therefore not evidence of a decipherment. The accepted p153 result depends on its separate exact-coordinate certificate and source review.

The primary source labels p153 as parts 5 and 6, dated 8 November. Earlier or later companion parts were not located. Printed p168 D also carries a `CHI` label but is already readable under the RICHI 7–9 November key, so a label alone does not establish geography or key family. See the adjacent `p153_source_review.json` for the original header, source crops, direction convention and prior-art boundaries.
