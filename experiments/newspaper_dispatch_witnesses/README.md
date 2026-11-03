# Second source witnesses of the newspaper-dispatch request

Prepared by **icekylinx and GPT-6 Astra Pro**, using unchanged published period keys credited to Lasry, Niebel, Kopal and Wacker.

This package adds **2 physical source records, 386 native coordinate slots and 193 plaintext positions**. Raw fixed positions: 143; edited fixed positions: 192. Exact costs: 8 observed-coordinate substitutions and 50 source-mask fills. No coordinates are inserted, deleted or reordered; no baseline key or numeral assignment changes.

See [the complete case](../../cases/radio/newspaper_dispatch_witnesses.md). `inputs.json` preserves manual rows, original headers, invalid glyphs and all crop-rendering metadata. `prior_evidence.json` pins the earlier source package and credits the fixed copy-retrieval lead and unreviewed candidates. Existing source records and costs are unchanged.

```bash
python experiments/newspaper_dispatch_witnesses/verify.py --verify
python experiments/newspaper_dispatch_witnesses/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Default verification uses the standard library and existing independent cipher helpers. It checks source hashes, unchanged keys, exact repair costs, every stated witness comparison and raw/edited round trips. The optional PyMuPDF check verifies the pinned full scan hash and exact regenerated crop pixels. No search is launched.

## Specific scope limits

- Both p166 frames retain their exact native200/186 lengths. B1 has one literal Q-shaped noncoordinate glyph at174; B2 has49 printed dashes at137..185.
- The existing p171 editorial body is the stated target of this witness comparison. It is not a fresh blind plaintext prediction, and existing p171 repairs remain unchanged.
- B1 has all100 common coordinate pairs fully observed in at least one copy. B2 has88 such complete pairs,2 pairs assembled from observed halves, and3 still editorial pair choices.
- The B in SELBEM and R in VORZUGSWEISE are supported by mixed observed halves from the two copies, not whole pairs directly read in p166.
- The O in SOFORT, P in POST and D in DEUTSCHE still require unsupported source changes. Under fixed frame equality the candidate common stream costs14 total observed substitutions, above the coordinate-only minimum10. This is not a minimum-cost or unique-wording claim.
- The raw XA cell at priority position49 still has baseline domain56. Its missing p166 coordinate is copied from a directly observed p171 coordinate; this supplies a coordinate, not a digit assignment.
- The earlier optional753 historical interpretation remains separate and supplies no independent evidence in this comparison.
