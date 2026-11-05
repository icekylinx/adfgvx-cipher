# 27 November: Helsingfors shipping and a vehicle-sale instruction

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

[Read the source edition](../../pages/223.md#edition-cases-naval-nov27-ships-and-vehicle-sale).

Two physical source records on Childs p223 contain **481 printed slots** and
**479 accepted source coordinates**. The declared frames contain **476
coordinates**, **238 plaintext positions**, and **236 fixed raw labels**.
The complete proposals have **7 observed-coordinate substitutions**, **2
printed-mask fills**, and **5 excluded observed coordinates**. There are no
insertions, reorderings or key changes.


**Reviewed source crops:** [p223_reviewed.png](sources/p223_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).

## Source and frame distinctions

- **p223 B:** its native 246-slot source reports preparations and ships secured for Helsingfors. Seven word repairs are explicit; the earlier 239-character OCR is retained separately.
- **p223 C:** its 235-slot source carries a questioned `230?` length. A conditional exclusion of `GAFDG` at source indices 220–224 gives a 230-slot frame and a readable instruction to sell trucks and surplus material. The complete candidate fills two printed masks and changes no retained observed coordinate.

All **231** five-slot exclusion windows are priced against the exact stated
C candidate by two methods. Starts **220** and **221** are the only windows
with zero observed substitutions. They retain the same ciphertext but map
one surviving G to different original source positions. Both are preserved.
The native odd-length decode and its unpaired coordinate remain available;
the source exclusion is not claimed to be a visible cancellation or a free
OCR correction.

## Reproduce

```sh
python experiments/nov27_ships_and_vehicle_sale/verify.py --verify
python experiments/nov27_ships_and_vehicle_sale/verify.py --verify --pdf /path/to/childs.pdf
```

The optional PDF check compares every saved RGB pixel with the identified
source. `inputs.json` contains the literal transcriptions and exact
assumptions; `certificates.json` records all domains, prices, source maps and
re-encryption witnesses. `ocr_snapshot.json` and `prior_candidates.json`
retain the earlier machine text and explicitly recomputed comparison
outputs. `catalog_proposal.json` lists the two new physical records.

The frame comparison is conditioned on one candidate and one five-slot
exclusion family. It does not establish unique historical text or identify
the stage at which a surplus group arose. Reported shipping arrangements
and sale orders are not evidence that the corresponding transports or sales
were completed. Earlier published-key and repository credit is preserved.
