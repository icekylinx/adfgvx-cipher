# 22 November: reverse key use and an Aufbau date correction

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

[Read the source edition](../../cases/pages/214.md#edition-cases-radio-nov22-reverse-keys-and-date-correction).

Two native source records on Childs p214 contain **268 printed slots**,
**134 modeled plaintext positions** and **133 fixed raw labels** under the
unchanged published Nov22–24 key. The proposed complete reading fills one
invalid source glyph in p214 C. There are **zero observed-coordinate
substitutions**, frame insertions, exclusions or reorderings.

The full p214 A1 transcription restores a visible five-coordinate final
group omitted by OCR and a five-slot group incorrectly expanded to six in
OCR. Its directly read instruction is to retain keys and use them backwards
for December. The label `JJ`, the literal `SAEMTLICHES SCHLUESSEL`, and the
advertised but unprinted second part remain explicit. The short p214 C
reading preserves `J8`, `J7`, `J7`, `J3`, without turning them into calendar
dates. Its printed November 22d receipt corrects the OCR's November 23d.


**Reviewed source crops:** [p214_reviewed.png](sources/p214_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).

## Files and checks

- `inputs.json`: native source transcriptions, header distinctions, source image identity, unchanged key, readings and priced proposal.
- `certificates.json`: exact raw domains, source indices, one mask fill, a global square-completion witness and full re-encryption.
- `ocr_snapshot.json` and `prior_candidates.json`: frozen earlier OCR blocks and explicitly recomputed comparison outputs.
- `sources/p214_reviewed.png`: inspected source crop, bound by file and RGB-pixel hashes.
- `catalog_proposal.json`: the two physical-record entries for integration.

```sh
python experiments/nov22_reverse_keys_and_date_correction/verify.py --verify
python experiments/nov22_reverse_keys_and_date_correction/verify.py --verify --pdf /path/to/childs.pdf
```

The latter check reproduces the crop from the identified source PDF and
compares every RGB pixel. The source instruction does not prove subsequent
key use or a complete reversal schedule. Exact compatibility of the one
word proposal does not establish its unique historical wording.
