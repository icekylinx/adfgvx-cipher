# Source retrieval across all 22 challenge entries

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

The [calibrated retrieval method](../source_similarity/README.md) is extended to
all **22 original challenge analysis layers**, producing **17,336 comparisons**
against the same 788 unverified OCR blocks. Six established relationship metrics
from the earlier run reproduce exactly. This adds coverage of sixteen challenge
entries beyond that run's six distinct target IDs; it does not add sixteen
decipherments.

## Results

| Target or group | Retrieval outcome |
| --- | --- |
| p152 | Its established p136 B1 parallel ranks first among other-page hits, local score 167. |
| p158 | The established p159/p168 component transmissions occupy the leading positions; scores reach 213. |
| p109 | Its known same-page section B relationship reproduces local score 303. Same-page results remain available separately. |
| p189 | Its independently established p185 near-parallel ranks first among other-page hits, score 85. This provides an additional retrieval control. |
| p132 | The strongest previously unreviewed other-page hit is p189 C, score 32 with an exact run of 11 coordinates. Image review yields a useful contextual instruction, but establishes no parallel. |
| Other targets | Leading other-page local scores are 19–28. No new source relationship or plaintext is accepted from those rankings. |

The script records the five leading other-page local and exact-run results,
their selected tracebacks, and **all same-page candidates**. It does not
silently label the best same-page block as the target: OCR can split a source,
and a different transmission on the same page can be useful, as p109 shows.
The [complete result](results.json) retains literal queries, source headers,
input hashes and all stated metrics.

## New source inspection: p189 C

The original p189 C image contains **124** legible coordinates, matching its
`RIZI-124` header. OCR omitted the final visible row `XFXX` and misread the
heading year as 1915. The earlier 120 coordinates match the image.

With the unchanged published `Nov13-15b` key, the full source gives:

```text
UNLOESBA?EHUNKSPRUECHENACHDEZEMBERSCHLUESSELENTZIFFERNXXIRRTUM
```

It fixes **61/62** raw positions. The most likely readable version is:

> Unloesba[r]e [F]unksprueche nach Dezemberschluessel entziffern. Irrtum.

That normalization needs exactly two substitutions of known source coordinates:
index **23 V→F** and **62 A→D**. All 122 others remain unchanged. The unknown
raw position cannot simply receive `R`: its domain is `234789QY`, and `R`
already occupies another square cell. No square is completed and no erased
coordinate is filled.

The [reader-facing case](../../cases/context/p189_C.md) and
[source inspection](source_inspection.json) retain the November/December
chronology tension, the closing `IRRTUM`, all position maps, and the three
unchanged-key comparisons. An independent column-offset implementation checks
the project decoder, and a separate candidate map checks the two substitutions.

The local resemblance to p132 remains score 32 after restoring the OCR row;
it contains 26 exact matches, one substitution and seven gap slots over a
31-coordinate query span. The full p132 query still has fitting cost 89.
The two decoded instructions concern radio traffic but differ in content and
key. **No retransmission or common plaintext is established.** The earlier
p132 readings and period-key recovery retain their attribution.

## Reproduce

The retrieval reuses the original C++17 alignment kernel. It needs Python and a
C++17 compiler, with no language model or network access:

```sh
python3 experiments/source_similarity_extension/retrieve.py --verify
```

This recomputes every pairwise comparison and the retained independent Python
tracebacks, then compares the full report. The six prior relationship metrics
are checked against the earlier frozen result. To regenerate the report, omit
`--verify`.

The compact source/decipherment/edit audit uses only the Python standard library:

```sh
python3 experiments/source_similarity_extension/check_source.py --verify
```

Supplying `--pdf /path/to/childs.pdf` additionally checks the inspected complete
scan's byte count and SHA-256. The repository includes the
[necessary source crop](../../sources/excerpts/childs_p189_C.png).

## Limits

Only the additional leading p132 candidate was newly transcribed from an image
in this extension. Other OCR candidates remain retrieval aids. Short matches
are common in a six-symbol alphabet; rank one does not establish a relationship.
An omitted, severely misread or differently encrypted parallel can escape this
search. No first-decipherment priority is claimed for the supplementary p189 C
reading, and it does not change the count or status of the 22 challenge entries.
