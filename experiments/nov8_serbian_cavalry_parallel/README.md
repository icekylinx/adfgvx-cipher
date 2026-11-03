# November 8: a separate Serbian-cavalry report witness

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

[Read the source edition](../../cases/military/nov8_serbian_cavalry_parallel.md).

p158 E1 is a new physical witness to the previously edited p170 B1 report.
It has **235 native source coordinates**, including a four-character
`XDGV` group. The independently printed p170 `AXDGV` supplies one A and
restores a **236-coordinate / 118-position** analysis frame, fixing **117
positions** under the unchanged published Nov7–9 key.

All **236 one-coordinate alignments** are compared directly between the
printed sources. Boundaries **82–85** minimize disagreements at **three**,
with **232 agreements**; all yield the same filled ciphertext. Their
unfilled outputs and mappings remain separate. Boundary 85 is the primary
view because it respects the visibly short group. No language target enters
this source comparison.

The primary readable proposal costs **five observed substitutions**: three
have raw p170 support and two are shared ordinary-word repairs. The
source-linked A is separately counted as **one added coordinate**. The
literal `ANENMELDUNG`, `PETERWADEIN`, `FEINBERUEHRUNG` and label 217 remain in
the exact reading. An optional earlier `ABENMELDUNG` proposal is priced at
seven substitutions. Both global assignments of the unresolved VF/XA
labels 5/6 are checked and retained.

```sh
python experiments/nov8_serbian_cavalry_parallel/verify.py --verify
python experiments/nov8_serbian_cavalry_parallel/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks source hashes and optional exact crop RGB pixels,
unaltered keys, native odd diagnostics, the source alignment, every repair,
raw-copy support, conservative union domains, readable-label preservation
and exact full re-encryption under both global completions. `inputs.json`
and `certificates.json` contain the full record; `ocr_snapshot.json` and
`prior_candidates.json` retain older OCR and prior body credit.
`catalog_proposal.json` proposes one new physical record. The existing
p170 body is credited rather than counted again. Different reception dates
remain literal and no specific copying mechanism is inferred.

**Reviewed source crops:** [p158_E_reviewed.png](sources/p158_E_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
