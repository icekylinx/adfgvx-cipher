# Constantinople addresses, signatures and receipt instructions

Prepared by **icekylinx and GPT-6 Astra Pro**; published keys credited to Lasry, Niebel, Kopal and Wacker, unchanged.

**3 physical records; 526 native coordinate slots; 263 plaintext positions.** The raw layer fixes 262 positions and the edition fixes 262, with 2 observed-coordinate substitutions and 0 fills. No geometry, key or numerical-label assignment changes.

See [the complete case](../../cases/radio/constantinople_address_parts.md). `inputs.json` records the source rows and crop provenance; `prior_candidates.json` retains earlier readings; `certificates.json` records exact costs, remaining domains and raw/edited round trips. The catalog proposal includes only the listed new physical records.

```bash
python experiments/constantinople_address_parts/verify.py --verify
python experiments/constantinople_address_parts/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Default verification uses the standard library and existing cipher helpers. The optional PyMuPDF check verifies the pinned full PDF and regenerated exact crop pixels. No search is run.

## Scope limits

- These are visible first parts containing addresses, signatures and receipt instructions. Header claims of2 or3 parts do not make the unprinted/unlinked remaining parts recovered.
- p147 C1 names STUMM and p156 C1 retains raw BUSSCHS; no corrected spelling, expanded personal name or message body is supplied.
- p148 B1 retains one L-shaped noncoordinate glyph as a mask. Its F-to-X above-line annotation is applied as one observed-coordinate substitution, not zero-cost source normalization.
- The other p148 B1 substitution changes BEIUETLE to BEIDETLE. Reference labels and the remaining domain9EKVXZ stay unresolved.
- No continuation payload, new numerical interpretation, key change or unique original wording is asserted.
