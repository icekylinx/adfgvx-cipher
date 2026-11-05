# A staff officer assigned to the Breslau corps command

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

Two parts of Childs p224 C describe a staff officer's transfer to special
employment with a corps command at Breslau. The received name is
`STRZEMIECZNQ`, the rank token is `MA9OR`, and several formation/reference
labels remain in their published-square form. This package provides a
visually checked source edition of bodies already present as unreviewed
OCR-derived retrieval candidates; it does not claim the first computation
of those candidates.

The full [case](../../pages/224.md#edition-cases-people-breslau-staff-transfer) preserves both
raw and ordinary-word candidate readings. All **558 coordinates** are
valid and the advertised lengths match exactly: **260 + 298**. There are
**279 raw-label plaintext positions**, all fixed under the published
`Nov25-28` square. The ordinary-word candidates make three observed
coordinate changes in C1 and six in C2. No coordinates are added, removed,
reordered or filled, and no key label is reassigned.

## Interpretation fields left untouched

| Field | Record / plaintext index | Pair | Original source coordinates |
| --- | --- | --- | --- |
| `MA9OR` rank label `9` | C1 / 9 | `VD` | 125, 79 |
| `STRZEMIECZNQ` final `Q` | C1 / 90 | `AD` | 86, 210 |
| `7 A K BRESLAU` number `7` | C2 / 14 | `GA` | 247, 1 |

All indices are zero-based. These pairs are unchanged by the ordinary-word
repairs. `certificates.json` also inventories **every** occurrence of
`0123456789JQY` in both raw texts and both candidates: 16 source occurrences
and 14 candidate occurrences. The two removed source occurrences are the
ordinary-word garbles `0ER` and `GESCHAEFT9`, not new key assignments.

The already located [Breslau context](../boots_request/breslau_context/source.json)
contains a visually checked decree of the VI Army Corps deputy general
command dated 6 July 1917, printed in *Waldenburger Wochenblatt*, no. 165,
**18 July 1917**. Its unit-location association may support interpreting
raw `7` as `6` if the same institutional recipient is assumed. The decree
is sixteen months earlier, and the p224 abbreviation omits `stellvertretend`;
neither continuity nor the officer's identity follows automatically.
This package applies no such relabelling.

A separate 1913 *Deutscher Reichsanzeiger* OCR entry attests the spelling
`v. Strzemieczny`. The scan image was unavailable and no independent link
to the officer in p224 was found. It is retained only as a spelling lead,
with no applied `Q→Y` assignment.

The optional [follow-up leads](followup_leads.json) record the bounded
independent-source search and its access limits. They add no certified
individual identification, surname image, or key assignment.

## Source and credit

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed p224, PDF page 227. It gives receipt as 28 November at
00.13 a.m., with `2230` as an undated origin time, below a 26 November
subheading. All are preserved. The cleartext fragment beginning
`VON LP AN CO` after C2 is outside its 298 coordinates and is not counted
as another ciphertext.

The period key is prior published work. Lasry and colleagues cite the
neighboring p224 A message; no explicit discussion of C was located in
the bounded paper/dissertation/comment check. The earlier repository
OCR candidates are explicitly credited in `inputs.json`.

## Reproduce

```bash
python experiments/breslau_staff_transfer/verify.py --verify
python experiments/breslau_staff_transfer/verify.py --verify \
  --pdf /path/to/childs.pdf --historical-pdf /path/to/waldenburg_1917.pdf
```

The verifier independently reconstructs the column mapping, checks every
raw position and coordinate repair, reencrypts both full candidates,
checks the complete raw-label inventory and verifies the unchanged
interpretive fields. The PDF options additionally check both complete
source hashes and all retained crop pixels. The enlarged Childs crops
make the source `G` glyphs reviewable without treating them as invalid `C`.
