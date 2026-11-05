# p167 C1: mission and Nachrichtenchef service address

**Partial recovery and edition: icekylinx and GPT-6 Astra Pro.**

The complete native first-part frame fixes **61/66 raw labels**. Explicit
ordinary-word proposals restore `MISSION`, `ABTLG` and `NACHRICHTENCHEF`,
giving **63/66 fixed candidate labels** with six observed substitutions
and two printed-mask fills. The labels `MILB`, `0RM` and `RELA` stay opaque.

[Read the edition](../../pages/167.md#edition-cases-radio-p167-mission-address)
· [Reviewed inputs](inputs.json)
· [Per-position certificate](certificates.json)
· [Original PDF, p170](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)

## Exact source and prices

The printed `RICHI-132` body contains 132 slots, including a dash at source
14 and the literal invalid `Z` at source 90. Both glyphs and all other source
coordinates were checked independently in the original scan. Its first-part
boundary precedes the separately headed section D; no second part is joined.
The Nov7–9 key and native source order and length stay unchanged.

The six observed changes are **20 D→X, 23 D→X, 83 V→D, 84 D→X, 114 V→X,
126 X→D**. The dash is filled as `G`; the invalid `Z` is filled as `X`.
Restoring B in `ABTLG` requires both a fill and an observed-coordinate change;
it is not counted as a pure erasure restoration.

An optional B→X separator reading in `MILB` requires two additional observed
changes, at 13 and 113. It costs eight substitutions in total and does not
replace the conservative primary reading.

## Global fields

The three remaining question marks come from two globally shared cells:
`XA=alpha` occurs after `ROEM` and at the last reference position; `VF=beta`
occurs at the other reference position. The fields are therefore
`ROEM alpha / KR 130 beta 1 alpha`, with alpha and beta distinct in `{5,6}`.

There are two complete-square witnesses: `5/6` gives reference `130615`,
and `6/5` gives `130516`. Both exactly re-encrypt to the same repaired
ciphertext. No numerical assignment or institution is selected.

## Reproduce

```sh
python experiments/p167_mission_address/verify.py --verify
python experiments/p167_mission_address/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks native lengths, the literal source, all repairs and
mask fills, both full injective square completions, exact re-encryption,
and the actual Markdown source, raw, edited and German displays. The PDF
option checks the original file and reproduces the reviewed crop pixels.
The source-image recipe is external; no new image file is required.

The earlier OCR block and published period key retain their provenance.
The source review, partial address reading and linked-field account are by
**icekylinx and GPT-6 Astra Pro**.
