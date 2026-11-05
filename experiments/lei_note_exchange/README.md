# Lei-note redemption instructions

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

This source edition covers Childs p223 A1–A3, a three-part telegram about
redemption of stamped and unstamped lei notes. It asks for amounts,
denominations and details of stamping, proposes arrangements with
Austrian/Hungarian banks, and says negotiations remain in progress.
The full [case](../../pages/223.md#edition-cases-finance-lei-note-exchange) preserves all raw
and candidate readings, with their source limitations.

## Result

The three parts contain **999 printed slots**, including **994 valid
coordinates**. One missing coordinate in A1 gives the advertised total
of **1,000**, or **500 plaintext positions**. The selected raw models fix
494 positions; ordinary-word candidates fix 500 using 21 observed-coordinate
substitutions, five printed-erasure fills and one missing-coordinate fill.
All candidates re-encrypt exactly under the unchanged published key.

A1's `DDXF` group is short. A complete 342-boundary search uniquely selects
gap 176 under the declared ordinary-word stencil, with 14 observed-symbol
changes. All five physically local gaps 175–179 are retained, including
less favorable raw readings. Neighboring `VFAXX` and `VFFXF` are complete
five-letter groups. A3's `AFXGV` is also five letters; no deletion is needed.

The received `HEERESAZG` abbreviation and apparent `VORGENOMME` omission
remain explicit. The source heading is 27 November, the receipt header
28 November at 02.27 a.m., and the origin field `1.30 (11/27)`; none is
silently reconciled.

## Intact fields for later interpretation

The complete source pairs for these fields are observed and unchanged
by every ordinary-word repair:

- A2: `J1Y KRONEN FUER JYY LEI`.
- A3: `70 BZW 38 MARK`.
- A3 reference fields: `16Y8XJJXJ2B6` and `J447XJJXJ2`.

These are raw published-square labels, not assigned numerical values.
The certificate inventories every numeral and `J/Q/Y` occurrence: 28 in
the selected raw models, 27 in the candidates, plus all local alternatives.
The removed `Y` is the separately repaired ordinary-word garble
`EINLYESEN`; it is not concealed when considering numeric interpretations.
No assignment is inferred from plausible exchange rates alone.

The period key and earlier OCR corpus are credited. A2 was also already
an unreviewed p73 retrieval candidate. This edition does not claim first
computation of that body or universal historical priority.

## Reproduce

```bash
python experiments/lei_note_exchange/verify.py --verify
python experiments/lei_note_exchange/verify.py --verify --pdf /path/to/childs.pdf
```

`inputs.json` freezes literal source rows, key provenance and six crop
hashes. `certificates.json` records all positions, alternatives, repairs,
untouched field pairs and complete label inventories. The optional PDF
check verifies the full source hash and all crop pixels. The three-entry
`catalog_proposal.json` is provided for parent integration; no shared
catalog or key file is changed by this package.
