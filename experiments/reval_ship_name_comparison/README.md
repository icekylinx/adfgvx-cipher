# Three vessel-name proposals in the Reval notice

**Source comparison and edition: icekylinx and GPT-6 Astra Pro.**

Contemporary shipping sources support reading three damaged fields in
[p213 A2](../../cases/naval/reval_steamer_notice.md#p213-a2) as **Peter Benoit,
Bjoern and Babylon**. Each proposal changes two observed coordinates after
the existing, independent **GD=J / DD=Y** interpretation is applied.
The source has 208 coordinates throughout; no new mask is filled.

## Primary spelling witnesses

| Proposed spelling | Primary source | Exact locator |
|---|---|---|
| **Peter Benoit** | *Lloyd's Register of Shipping, Steamers, 1917–18* | [PES–PET, P471](https://archive.org/details/HECROS1918ST/page/n798/mode/1up) · [entry crop](sources/peter_benoit_lloyds_1917_18.png) |
| **Björn** → cipher **BJOERN** | Same register | [BJE–BLA, B733–735](https://archive.org/details/HECROS1918ST/page/n136/mode/1up) · [three entries](sources/bjorn_lloyds_1917_18.png) |
| **Babylon** | *Hamburger Fremdenblatt*, no. 359 B, evening edition, 28 December 1915 | Printed p3, PDF p9, “Schiffs-Unfälle” · [issue](https://pdf.sub.uni-hamburg.de/kitodo/PPN1699277745_19151228AB.pdf) · [notice crop](sources/babylon_19151228_p9.png) |

The register's visible year is **1917–18**, although its archive identifier
uses 1918. It lists three distinct Björn entries. The first records capture
and removal to Cuxhaven; that note does not identify it as the vessel in
the Reval notice. The Babylon report concerns a Stockholm salvage claim in
1915. These witnesses establish contemporary spellings, with no independent
confirmation of the movements reported in November 1918. The telegram's
departure wording does not name a departure port.

## Exact source price

All indices are zero-based. The inherited word edition costs three observed
substitutions and one invalid-glyph fill.

| Field under the prior J/Y layer | Proposed field | Additional observed substitutions |
|---|---|---|
| `PETERXBENVIT` | `PETERXBENOIT` | Source **72 V→X**, **90 V→F** |
| `BJVERN` | `BJOERN` | Source **64 V→F**, **150 V→X** |
| `BACYLON` | `BABYLON` | Source **36 F→G**, **83 D→F** |

The proposals are independent and can be accepted separately. The combined
display accepts all three, for **nine observed substitutions and one mask
fill**. Re-encoding the same wording under the published square would cost
**13 substitutions and one fill**. The four-coordinate difference comes
from retaining the observed **GD=J** and **DD=Y** pairs under the prior
shared-name hypotheses; no new assignment is made here.

**Readable German — prior J/Y and the three historical name proposals:**

> Weitere Tonnage folgt baldigst. Ferner Rohstofftransport abging heute Peter Benoit. Folgt morgen Bjoern und Babylon.

All 104 positions already had labels in the baseline edition. This work
adds historical spelling candidates and their exact source prices; it does
not count them as newly recovered unknown positions, new physical messages
or uniquely identified voyages. The original names and source-coordinate
values remain in the earlier case and certificate.

## Reproduce

```sh
python experiments/reval_ship_name_comparison/verify.py --verify
python experiments/reval_ship_name_comparison/verify.py --verify --source-dir /path/to/downloaded-sources
```

The verifier reconstructs each proposed name independently, checks all
observed changes, preserves the earlier fill, and re-encrypts the individual
and combined editions. The current German quotation is checked character
by character. With the optional source directory, it regenerates all three
crops from the hash-pinned scan images and newspaper PDF and compares their
RGB pixels. Filenames and download URLs are in the inputs.

[Inputs and primary-source metadata](inputs.json) · [Coordinate certificate](certificate.json).
