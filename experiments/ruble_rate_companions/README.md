# Companions to Norbert's p171 A1 ruble-rate reading

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The [case](../../cases/finance/ruble_rate_companions.md) adds source-reviewed
physical parts **A2 and A3 only**. Norbert's earlier A1 body, its published
repairs and Max Baertl's later editorial wording remain credited and unchanged.

A2 reports 140 marks for 100 Tsar rubles in Kiev, and a reported rate up to
190 marks in Warsaw. A3 recommends allowing more than par for `BONS` if
necessary. These are the telegram's statements; the edition does not verify
historical market prices or identify a particular financial instrument.

## The conditional geometry matters

A2 has **261 literal slots**, despite its printed `RICHI-252` label. The
working model excludes `---DD` and the visibly struck-through `G-VFA`, then
adds one unknown within the short `DVAX` group. The exclusions remove **ten
slots: six observed coordinates and four printed erasures**. Only `G-VFA`
is visibly cancelled; the other exclusion is a stated model hypothesis.

All five local insertion boundaries are evaluated. The full proposed text
has a six-substitution minimum at boundaries **202 and 203**, both giving
the same corrected ciphertext. A place/quantity-masked stencil has three
minima, **202–204**. Boundary 202 is a representative, not a unique historical
claim. The screen is conditional on the two fixed exclusions and an
already-seen readable candidate; it is not a blind control or global search.

A2 additionally needs three printed-erasure fills and one fill of the added
unknown. A3 uses its exact 152 source slots with two printed-erasure fills
and **zero observed-coordinate changes**. Its `PARI X PARI` duplication is
retained. Across both parts, the 413 literal slots become 404 working
coordinates; 196/202 raw fixed positions become 202/202 in the conditional
editions. The ten exclusions are additional to the six substitutions.

The published Nov7–9 key remains unchanged. The source image metadata,
prior unreviewed companion candidates, all five gap alternatives, full
source-index mappings and exact edit costs are preserved. Global witnesses
demonstrate consistency only.

```sh
python experiments/ruble_rate_companions/verify.py --verify
python experiments/ruble_rate_companions/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The optional PDF check independently regenerates and compares all crop pixels.
Only the two companion parts enter the proposed catalog; A1 is not recounted.
