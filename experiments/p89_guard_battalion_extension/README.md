# p89 A3: the guard-battalion destination fragment

**icekylinx and GPT-6 Astra Pro** · [Evacuation-order edition](../../cases/pages/089.md#edition-cases-military-black-sea-evacuation-routes-p89-a3)

The previously unread tail of p89 A3 admits the twenty-character phrase
`ERSXBATLX2XGARDEREGT`, independently present in the p104 D order to
Lieutenant Meier. The phrase fits **all 27 observed recipient coordinate
halves**, without changing a received coordinate. It fills 13 explicitly
lost coordinates and adds **12 fixed plaintext positions**. A separate
`BERLIN` proposal at the end adds three further half-supported positions.

Together with the prior prefix, this gives **166/179 positions**, up from
151/179. The increase is 15 proposed positions, with **zero additional
observed substitutions** and 16 additional fills in the source-declared
lost block. One of the new positions, the T in `BATL`, is wholly absent;
the other fourteen retain an observed coordinate half.

## Exact reading layers

**Raw output — the printed 100-coordinate loss retained at its stated location; 81/179 fixed positions:**

```text
???ITE??NA???BR?I?A???HTN??HT???O??H?N???ERL??SB???ND?I?H???MPF??AB???HE?X?D???TEN??WE???RL?I?U???NGE??HL???EN?N?U???NXZ???F???MI?I?D???STE???N???SX?A?L???GAR???E???XZ?F?SZ??ERL??
```

**Edited output — prior prefix plus the guard-battalion and separate Berlin proposals; 166/179 positions:**

```text
ZWEITENSNACHXBRAILAXGEHTNICHTSXDORTHINUNTERWEGSBEFINDLICHEDAMPFERABDREHENXXDRITTENSXWEITERLEITUNGINGESCHLOSSENENZUEGENXZIELFUERMI?I?D???STE???N?ERSXBATLX2XGARDEREGT?XZ?F?SZ?BERLIN
```

**Readable German — excerpt of the two newly proposed spans; the omissions remain unread:**

> […] ERS BATL 2 GARDEREGT […] Berlin.

The independent donor uses `ERS BATL 2 GARDEREGT` after `BEIM` and before
`MELDEN`, supporting an abbreviation for a replacement battalion. The
recipient's immediately preceding position 143 remains unresolved, so
the exact word boundary before `ERS` is not fixed. In particular, the
alternative continuation `PERS` is not excluded. No complete destination
sentence, additional unit designation or journey is asserted.

| Layer | Fixed positions | Observed substitutions | Printed-mask fills | Lost-coordinate fills |
| --- | ---: | ---: | ---: | ---: |
| Prior prefix | 151/179 | 1 | 1 | 69 |
| Prior prefix + twenty-character phrase | 163/179 | 1 | 1 | 82 |
| Above + separate `BERLIN` proposal | 166/179 | 1 | 1 | 85 |

The remaining fifteen coordinate masks permit exactly **6^15** complete
plaintexts under the final layer. Thirteen plaintext positions remain
unresolved, including two pairs with both halves missing. The constructed
full round-trip witness assigns arbitrary A coordinates only to check the
cipher arithmetic; those values are excluded from every reading above.

## Independent observed-word witness

The [p104 D source](../nov2_acknowledgments_and_personnel/sources/p104_D.png)
has 149 received coordinates against its RICHI-150 header. Its existing
edition inserts one unknown inside the visibly short `ADAG` group. This
geometry remains conditional. Crucially, the entire guard-battalion phrase
at donor positions 40–59 uses **40 original observed halves** and survives
unchanged at **all five** local insertion boundaries 100–104. No donor
word repair or invented coordinate supplies that phrase.

The donor's `BERLIN` at positions 21–26 is fully observed in the primary
frame and at boundaries 100–102. Boundary 104 instead leaves its final N
unresolved. The shorter recipient `BERLIN` proposal therefore has its own
scope: its observed `ERL`, three surviving halves and the independent
place word support the completion, without making it an all-frame invariant.

The recipient's T at position 150 has two absent halves. The numeral 2 at
153 has one observed half and one explicitly filled half; its presence in
this candidate is not an independently authenticated historical unit number.
Positions 143, 164, 167 and 172 remain `?`. No extra separator, genitive S,
`ZU FUSZ` expansion or interpretation of the earlier `MI?I?D...` field is
silently added.

## Source, retrieval and checks

The [p89 A3 crop](../black_sea_evacuation_routes/sources/p89_A3.png) prints
`(missed 20 groups)` exactly after the first 200 coordinates. The original
258 slots, including its single dash, therefore produce the stated
358-coordinate frame with 100 lost slots at that boundary. This extension
does not optimize or move that gap. The key remains the published Nov1–3
square and 19-column rank.

The frozen retrieval searches the previously unread tail, positions
127–178, against **484 distinct raw streams / 51,327 characters**, with
all entries from the same evacuation-message edition excluded, including
the p90 A5 entry also referenced through a later snapshot. An alias cannot
retain a sibling message part. At a minimum
length of twelve, its highest-supported zero-substitution hit is precisely
the twenty-character phrase at position 144. The donor manifest is reused
by reference and every raw-text digest is checked.

All **500 deterministic coordinate shuffles** preserve the target's mask
positions and observed histogram; none gives a twelve-character match in
this declared search. Four independent planted-word controls recover the
planted word at its correct offset; some top matches include compatible
neighboring characters. These controls validate retrieval behavior, not
historical uniqueness or a probability that the reading is correct.

The verifier independently rebuilds both source frames, all five donor
gap alternatives, every coordinate map and edit, and each complete
arithmetic witness. The optional PDF check regenerates both existing
source crops pixel for pixel. No additional binary image copy is needed.

```sh
python experiments/p89_guard_battalion_extension/verify.py --verify
python experiments/p89_guard_battalion_extension/verify.py --verify --pdf /path/to/childs.pdf
python experiments/p89_guard_battalion_extension/replay_search.py
```

The existing p89 A2 reading remains credited to Ayush Agarwal and is not
counted as new work. Earlier source editions, including the p104 D gap
reconstruction, retain their credit. Published keys remain credited to
George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. This extension is by
**icekylinx and GPT-6 Astra Pro** and adds no new physical ciphertext body.
