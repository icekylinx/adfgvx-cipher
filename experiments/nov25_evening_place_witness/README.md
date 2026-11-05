# Tiszaföldvár in two evening reports under different keys

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.** Published period keys
retain the Lasry–Niebel–Kopal–Wacker attribution.

The 25 November evening report on p220 B has `TISHAFOELDVAR` in a list
of places reached by leading elements. The separate 30 November report
on p229 A1 directly reads **`TISZAFOELDVAR`**, with all thirteen letters
supplied by **26 untouched original coordinates**. This provides a native
witness for a place spelling that otherwise would be an editorial guess
from geography.

Applying that spelling to p220 B costs **one observed-coordinate substitution**.
Its H at plaintext position 72 is `AA`, from original
source positions **6 and 150**. Change source **6 A→D** and preserve
source 150 A: the pair becomes `DA`, giving Z under the 25–28 November key.
The image clearly prints A. This is a proposed repair to the received
ciphertext, not a changed visual transcription.

| Source | Native place and range | Key | Treatment of the place |
| --- | --- | --- | --- |
| p220 B | `TISHAFOELDVAR`, [69,82) | Nov25–28 | One observed A→D substitution |
| p229 A1 | `TISZAFOELDVAR`, [41,54) | Nov28–Dec1 | No repair, fill or change of frame |

The donor's Z is pair `VX`, from original source **219 V and 148 X**.
The different keys encode the same proposed letter with different pairs;
the transfer concerns the plaintext spelling, not a reused coordinate pair.
All indices are zero based and the ranges are end-exclusive.

## Supported place names and unresolved unit fields

<a id="what-the-combined-place-reading-establishes"></a>

With the separately supported
[shared Y](../nov25_treaty_digits/README.md#the-shared-y-in-strzemieczny-and-nagymagocs),
p220 B's list contains the readable places **Tiszafoeldvar, Nagymagocs
and Kondoros**. The surrounding unit fields remain **`21?ID`, `PRD`
and `?21?`**. No unit identity, report date or new numeral assignment
is inferred from these place spellings.

**Conditional interpretation — the reached-place list, with the unit labels retained:**

> Es haben mit Anfaengen erreicht: 21?ID, Tiszafoeldvar. PRD, Nagymagocs. ?21?, Kondoros.

The 30 November donor reports an advance to Tiszaföldvár. It is a separate
report, under a different key and on another date, rather than a duplicate
reception of p220 B. Its native place spelling supports the earlier repair;
it does not independently prove the 25 November movement or its unit.

The existing `HABE7→HABEN` repair at source 157 remains separately priced.
Together, the recipient edition uses **two observed substitutions**, zero
mask fills and the original **220-coordinate frame**. Under the shared
partial square, it still fixes **103/110 positions**: H was already a fixed
received label, so replacing it with Z improves the word interpretation
without increasing the count of fixed positions.

## The provisioning report's army field

The same earlier source package also contains the two-part provisioning
message on p219 D1 and p220 A2. In D1, the existing shared **`FX=1`**
interpretation gives **`11XARMEE`** from received `JJXARMEE`.
The two original pairs are source **10 F + 83 X** and **53 F + 133 X**,
at plaintext positions 43 and 44. Neither is touched by the three earlier
ordinary-word repairs. The complete conditional body is:

**Conditional interpretation — existing shared square and three earlier word repairs:**

> Infolge verringerter Verpflegungsstaerke fuer 11. Armee keine Verpflegung mehr erforderlich.

The message says that the 11th Army's reduced provisioning strength makes
further provisions unnecessary. Its already readable continuation asks
for an immediate halt to further supplies. This is propagation of an
existing numeral interpretation to two untouched pairs, not a new
historical assignment from a guessed army identity. D1's three source
repairs remain separate from the two in the evening report p220 B.

## Source and cost checks

The verifier independently reconstructs both column geometries from literal
source rows, checks every original index in the thirteen-letter place spans,
and re-encrypts complete consistent witnesses. All **98 possible starts**
of the stated place spelling in p220 B's native frame are priced. Position
69 is the only one-substitution minimum. This bounded comparison concerns
one proposed spelling and one unchanged frame; it does not establish a
unique historical plaintext among arbitrary alternative words or models.

Both source packages and their original editions are retained:

- [25 November source and edition](../nov25_provisions_and_evening_report/README.md)
  · [p220 image](../nov25_provisions_and_evening_report/sources/p220_reviewed.png).
- [30 November source and edition](../late_transport_dispatches/README.md)
  · [p229 image](../late_transport_dispatches/sources/p229_A.png).

The [inputs](inputs.json) pin the earlier inputs, verifiers and certificates.
The [certificate](certificate.json) records both native place spans, all
98 costs, the single new change, the retained earlier repair, complete
streams and round-trip witnesses. Arbitrary unassigned square values in
those witnesses are consistency examples, not proposed historical digits.

```sh
python experiments/nov25_evening_place_witness/verify.py --verify
python experiments/nov25_evening_place_witness/verify.py --verify --pdf /path/to/childs.pdf
```

The optional PDF argument checks both reused source-image sets against the
pinned original scan. No new copy of those images is created.
