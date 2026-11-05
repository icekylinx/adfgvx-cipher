# Baku personnel inquiry: a duplicated-block source reconstruction

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

[Read the source edition](../../pages/185.md#edition-cases-caucasus-baku-personnel-inquiry).

The p185 B body contains **279 source slots**, including one invalid glyph,
against the printed **268**. Its last row repeats `XFVVF DXXVG` exactly.
The primary conditional frame excludes one copy of that ten-coordinate
block and the final coordinate, giving **134 modeled positions** and
**125 fixed raw labels** under the unchanged published Nov13–15a key.

The proposed Baku personnel inquiry fixes **129/134 positions**, using
**10 observed-coordinate substitutions** and **1 source-mask fill** in
addition to **11 excluded observed coordinates**. All five remaining
reference positions stay unknown. The source header names General von
Kress in Tiflis; no unprinted personal identities or historical outcomes are
inferred from the inquiry.


**Reviewed source crops:** [p185_B_reviewed.png](sources/p185_B_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).

## Two unresolved reference patterns

<a id="why-two-reference-patterns-remain"></a>

Both duplicate-block locations and every remaining one-coordinate
exclusion are compared: **538 labelled source maps**. For the declared
letter pattern with unknown fields left as wildcards, the minimum cost is
10 substitutions at six maps. Those maps reduce to two distinct retained
ciphertexts. They display the same words and question marks, but the final
unknown reference cell is either the same as the third unknown or a fourth
distinct cell. The certificate preserves both and their individual source
maps. Unknown cells stay globally coupled and injective.

The comparison is candidate-conditioned and restricted to that two-stage
exclusion family. It is not a global historical uniqueness result. No
source-visible cancellation is asserted, and no deletion is counted as a
free OCR correction.

## Reproduce

```sh
python experiments/baku_personnel_inquiry/verify.py --verify
python experiments/baku_personnel_inquiry/verify.py --verify --pdf /path/to/childs.pdf
```

`inputs.json` preserves the full literal record, unchanged key, image
identity, exact assumptions and reading proposal. `certificates.json`
retains all source maps, candidate-conditioned costs, the native odd decode,
remaining reference relations and nonhistorical re-encryption witnesses.
`ocr_snapshot.json` and `prior_candidates.json` preserve the earlier
repository OCR and explicitly recomputed comparison. `catalog_proposal.json`
contains one new physical source record; alternative frames are not extra
records.

The optional original-PDF check compares the inspected crop pixel for pixel.
Published-key and earlier repository credit remain separate from the source
review and explicit editorial reconstruction by icekylinx and GPT-6 Astra Pro.
