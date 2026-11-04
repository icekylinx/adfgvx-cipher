# Three-part report and request concerning Hungarian armistice negotiations

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Childs p124 A1/A2/A3, PDF p127, have consecutive source labels and native
lengths **352 / 266 / 48**. Their message line is `1715 (4/11) 3 TLE`;
the receiving header is November 5 at 7.17 p.m. All three parts use the
unchanged published **Nov4–6** key. The separate damaged p124 B is excluded.

The [reading case](../../cases/pages/124.md#edition-cases-military-hungarian-armistice-instructions)
reports negotiations for Hungarian troops, the requested departure of
German troops from Hungarian and South-Slav territory, an assignment to
send two staff officers and a request for instructions. These are the
message's statements and requests, not proof that the actions occurred.

## Correcting the source transcript and keeping source repairs separate

A1 was already readable in an earlier unreviewed repository candidate.
A2/A3 were obscured because the OCR lost the source-defined boundary,
merging A2 with the first 40 coordinates of A3. It also introduced two
extra symbols in overlong groups and omitted A3's final **VDFFA FAA** row.
The visible source, its headings and its group boundaries resolve these
OCR problems without any historical source insertion or deletion.

`ocr_snapshot.json` freezes the four earlier OCR blocks and origin hash.
The verifier independently reconstructs the following exact differences:

- A1's masked source **194** is visibly F.
- In the concatenated old A2/A3 OCR stream, delete the extra A at old index
  **67** from `FXAXFF`, giving source **FXXFF**, and the extra `?` at old
  index **211** from `?AVGVX`, giving source **AVGVX**.
- Resolve old masks **114** and **160** as source-visible V glyphs.
- Split the corrected 306-coordinate prefix at **266**, following the
  source's `2 TL` and `3 TL` labels.
- Restore the visible final eight A3 coordinates **VDFFAFAA**, completing
  its advertised 48-coordinate frame.

The two obsolete indices above refer to the old merged OCR, not to a
historical source-deletion proposal. The shared corpus remains unchanged.
After source transcription and separation, the editorial candidates cost
**3 / 3 / 0 observed-coordinate substitutions**. Those six changes are
listed separately in the certificate and are not disguised as OCR edits.

## Conservative strings and counts

A1 keeps the exact **KOOVES** name string and its final **0** label.
A2 keeps **GENERLSTABSOFFIZIERE**, which lacks the A of the normal spelling.
Only the readable German layer shows **Gener[a]lstabsoffiziere**; the
bracketed letter is not in the decoded streams or fixed-position count.
All numbers and command references remain literal.

There are **three physical records**, **666 valid source coordinates**
and **333 / 333 fixed plaintext positions**, before and after the six
local coordinate substitutions. There are no fills, historical source
insertions/deletions, length hypotheses or key changes. Every complete
edited stream re-encrypts exactly. The proposal counts the three source
parts once each, and excludes obsolete OCR merges and separate p124 B.

Earlier A1 body credit, earlier A2/A3 OCR candidates, published key
provenance and bounded prior-publication checks are preserved in
`prior_candidates.json`. This edition makes no historical first-solution
claim. Exact re-encryption is a compatibility certificate, not proof of
historical uniqueness.

## Reproduce

From the repository root:

```sh
python experiments/hungarian_armistice_instructions/verify.py --verify
```

The primary verifier uses the standard library and checked-in cipher
module. Original-PDF pixel verification additionally requires PyMuPDF and
Pillow:

```sh
python experiments/hungarian_armistice_instructions/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier checks the PDF's frozen byte count and SHA-256 before
regenerating all three crops and comparing their pixels. Scratch caches
are not runtime dependencies.

**Cross-key withdrawal phrase.** The unchanged p117 C3 source under Nov1–3
independently supports two existing p124 A1 word repairs under Nov4–6.
Their 59-letter tail agrees at 57 raw positions; p117 supplies U and H for
`UNGARISCHEN` and `SUEDSLAVISCHEN`. The original `WERDEN`/`SOLLEN`
difference and different headers remain explicit. The separate
`FDER`→`FUER` repair gains no new support from this comparison.
[The paired-source certificate](withdrawal_parallel.json) adds source
evidence, with no new fixed-position or physical-message count.
Run `python experiments/hungarian_armistice_instructions/verify_parallel.py --verify`;
adding `--pdf /path/to/childs.pdf` checks both original crop pixels.
