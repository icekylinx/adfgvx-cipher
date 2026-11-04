# Caucasus radio transmitters: typed and annotated source layers

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Childs p88 A1/A2, PDF p91, preserve one two-part message under the unchanged
published **Nov1–3** key. Its receipt is dated November 2; its message line
is `1330 (1.11)`. The native lengths are 172 and 134 coordinates. The
adjacent **RIZI-204** message B is separate and is not included.

The [reading case](../../cases/pages/088.md#edition-cases-caucasus-caucasus-radio-transmitters)
keeps a mostly readable first part without forcing its malformed verb.
The second part yields a compact readable notice about General von Kress
and a 1500-watt tube transmitter after three observed-coordinate changes
and one invalid-glyph fill. Both bodies were already present in earlier
unreviewed repository screens; this package contributes a source edition,
annotation audit, exact arithmetic and explicit limits, not a claim of
historical priority.

## Evidence and counts

- `inputs.json` freezes the literal rows, source headers, published key and
  source crops. The Q in A1 and y-like mark in A2 each occupy one visible
  source slot. They are masked, not deleted.
- `certificates.json` contains every raw position, coordinate-domain,
  original source index, proposed change and re-encryption check.
- `prior_candidates.json` retains the earlier repository candidates and a
  bounded prior-paper, thesis and 2017-comment keyword check.
- `catalog_proposal.json` proposes only A1 and A2 as two physical records.

There are **306 visible slots**, **304 valid coordinates**, and **153
plaintext positions**. The typed layer fixes **151 / 153** positions; the
conservative edited layer fixes **152 / 153**. Its total cost is **three
observed-coordinate substitutions and one invalid-glyph fill**. A1's Q
remains unknown, with all six exact compatibility witnesses retained.
There is no frame, length, rank, square or numeral-label change.

A1's tempting `ERBITTETRANSPORT` normalization would require **20 observed
substitutions plus one fill**, despite the rest of the message being
readable. Its exact certificate is included as a **rejected, uncounted
editorial alternative**. The primary stream retains `ER?TTE` and
`TRANSPORRT` instead.

## All four source annotations

The second part has four glyphs aligned above existing typed slots. Their
origin and intention are not known. The verifier enumerates **all 16
subsets**, retaining each raw output and its cost to the same conservative
edited candidate. This is complete enumeration of the four replacement
choices, not a reconstruction of the annotator's intent.

Only source 107 V→X is used in the primary edited candidate, where it gives
`WATT`. The other three proposed aligned replacements give `SEN0`,
`0?NERAL`, or reference `M9523` when applied separately. Those results
remain visible; the annotation layer is not silently presented as a
corrected transcription. These are variants of A2, not additional
physical records.

## Reproduce

From the repository root, using Python 3 and the checked-in cipher module:

```sh
python experiments/caucasus_radio_transmitters/verify.py --verify
```

This standard-library path reproduces all certificates, annotation
combinations, costs and complete compatibility witnesses. Optional source
pixel verification requires PyMuPDF and Pillow and the original Childs PDF:

```sh
python experiments/caucasus_radio_transmitters/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The PDF is matched by its frozen byte count and SHA-256 before the five
crops are regenerated and compared pixel for pixel. Scratch caches are
not runtime dependencies. Exact re-encryption establishes compatibility
with the chosen frame and unchanged key; it does not establish that an
editorial reading is historically unique.
