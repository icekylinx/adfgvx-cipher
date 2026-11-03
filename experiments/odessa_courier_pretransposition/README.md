# Odessa courier report: a conditional loss before transposition

Research and source edition: **icekylinx and GPT-6 Astra Pro**.

[Read the complete source edition](../../cases/radio/odessa_courier_pretransposition.md).

p201 C has 324 native received coordinates and advertises 324. The unchanged
Nov 16–18 key directly fixes 153/162 labels. Independent visual audit corrected
the initial draft’s DDGAX to the printed GDGAX; BERLIN is already raw.
The exact transcription correction is retained separately from repairs. A separate loss-before-transposition
model first undoes the native 324-coordinate permutation, then restores two
fractionation coordinates. The reconstructed 326-coordinate stream has 163
plaintext positions and yields the address to the German representative in
Odessa, followed by KURIER ELSNER.

All 52,975 two-position loss descriptions are priced against retrospective
prefix words. Exactly [36,74] and [37,74] have zero observed conflicts; both
supply the same X/A fills. Omitting ODESSA leaves those same two minima;
address-only and courier-omitted scopes retain 522 and 32 alternatives. All
sets and exact price-distribution hashes remain in the certificate.

The unfilled model fixes 157/163 positions. Two fractionation fills fix 159;
four separately priced observed substitutions fix 160. Three reference
labels stay unresolved and globally distinct. All 40,320 full-square
assignments and 336 distinct reference triples are retained or checked.
No source coordinate is added, excluded or reordered in the received stream.

GXXDV contains two overstruck X-like glyphs. The primary readings remain
visually defensible but qualified. A conservative G??DV branch retains both
source masks and fixes 158/163 after the same loss and word repairs; selecting
both Xs in that branch would add two mask-fill costs. Neither is selected
through the deciphered words.

The verifier reproduces the precise forward process: fractionate 163 labels,
remove the two hypothesized coordinates, and transpose the remaining 324.
It never applies a 326-coordinate transposition. Independent native p201 A 1
supplies the recipient vocabulary only, retaining its earlier body credit.

```sh
python experiments/odessa_courier_pretransposition/verify.py --verify
python experiments/odessa_courier_pretransposition/verify.py --verify --pdf /path/to/childs.pdf
```

This package includes the source transcriptions, reviewed crops and pinned
PDF/crop/RGB metadata. The package verifier checks source pixels with
--pdf; the publication checker linked below also checks the delivered PNGs.
Core keys and messages remain unchanged. The model is conditional and does
not establish a unique historical loss mechanism or reference number.

**Reviewed source crops:** [p201_C_reviewed.png](sources/p201_C_reviewed.png) · [p201_C_overstrike.png](sources/p201_C_overstrike.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
