# Arad provisions and strength report: conditional partial recovery

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

[Read the complete source edition](../../cases/pages/159.md#edition-cases-military-arad-provisions-partial).

p159 A has **271 native valid coordinates**, repeated `VDAGG` and `FFXDF`
groups, and a short `GDDA` group. The conditional model excludes **10 valid
coordinates**, adds **11 slots**, and retains the published Nov7–9 key.
The resulting 272-slot frame fixes 124/136 raw positions. The primary partial
proposal makes **six observed substitutions** and fills **10 of the 11
added slots**, leaving **134/136 positions** fixed.

The readable text concerns provisions, Arad, the Hungarian government and
fields containing MANN and TIERE. `14 TAGE U10 TAGE`, the repeated ARAD,
`STAEKE`, the first quantity and the footer remain qualified or unresolved.
No missing plaintext R is supplied to STAEKE, and no historical strength
number is selected.

All **173,580 canonical gap prices** are recomputed for one explicit partial
target. Four equivalent duplicate-instance choices give **694,320 labelled
source models**; the equality of their retained coordinate strings is
proved. **All 64 minimizing source maps** are kept. Their quantities form a
linked family: 48 maps retain P0000; 16 retain leading domain {3,4,5,6,8,P,V}.
The ties concern the six observed substitutions: the 48 P0000 maps fill
eleven added slots and fix 135/136 positions, while the 16 open-domain maps
fill ten and fix 134/136. Those counts are map multiplicities, not
likelihoods. If the leading label
uses XA=5/6, the footer at VF uses the other digit. **Twelve full global
witnesses** retain every source-compatible row coordinate and both digit
assignments.

```sh
python experiments/arad_provisions_partial/verify.py --verify
python experiments/arad_provisions_partial/verify.py --verify --pdf /path/to/childs.pdf
python experiments/arad_provisions_partial/explore.py --verify
```

The main verifier checks native/source layers, PDF hash and exact crop
pixels, structural prices, all tied source maps, numerical-label preservation,
the partial readable display and full re-encryption. `inputs.json` records
the complete family; `certificates.json` gives its audit. `explore.py` and
`exploration.json` preserve the earlier language-guided screen, explicitly
using a vocabulary adapted to the observed provisions lead. That screen
and the subsequent fixed-target optimization are not independent evidence
that the historical wording or geometry is unique.

`ocr_snapshot.json` and `prior_candidates.json` retain earlier repository
work. `catalog_proposal.json` proposes one conditional partial source
record, without counting alternative maps or key completions as additional
records. Published-key and prior-work credits remain intact.

**Reviewed source crops:** [p159_A_reviewed.png](sources/p159_A_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
