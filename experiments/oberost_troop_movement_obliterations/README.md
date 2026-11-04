# Ober Ost troop movements: a conditional reading across two obliterations

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Read the [complete source edition](../../cases/pages/186.md#edition-cases-military-oberost-troop-movement-obliterations). The p186 B1 body proposes troop movements within the Ober Ost territory. A disclosed layout model represents two obliterated group columns as five masks each, then conditionally excludes those ten masks to match the printed length 308. The original 318-position composite model and both odd 313-position controls remain available.

The result has 150/154 fixed conditional raw labels; one observed substitution and two source-mask fills give 152/154. Ten masked-layout-slot exclusions are counted separately, and no observed coordinate is excluded. Z0FORT and the opaque opening reference remain literal. The native second part is reviewed separately in [its companion case](../../cases/pages/186.md#edition-cases-military-home-departures-baltic-transport-p186-b2).

The ten group-width masks are modeled positions, not ten separately visible source glyphs. The certificate therefore distinguishes 308 individually transcribed positions from the 318-position composite layout. This geometry is a conditional analysis, not proof of historical cancellation.

## Reproduce

```sh
python experiments/oberost_troop_movement_obliterations/verify.py --verify
python experiments/oberost_troop_movement_obliterations/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Ordinary verification uses the standard library and repository helpers; the optional PDF check uses PyMuPDF and Pillow. Source hashes, source/model maps, all controls, individual coordinate changes, coupled unknowns and the nonhistorical roundtrip witness are replayed.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.
