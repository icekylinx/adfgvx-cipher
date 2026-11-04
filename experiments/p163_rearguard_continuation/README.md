# The third rearguard position in two parts of the withdrawal order

**Source reconstruction and review: icekylinx and GPT-6 Astra Pro.**
The published period key retains its Lasry-team attribution.

Two damaged passages in [p163 A](../../cases/pages/163.md#edition-cases-military-p163-a) support the
same military compound, **NACHHUTSTELLUNG**. The proposed part-15 continuation
is **`X7XAUSDER3XNACHHUTSTELLUNG`**: “7. Aus der 3. Nachhutstellung …”. Its
26 positions preserve **33 of 34 observed coordinates**, require **one observed
substitution and 18 printed-erasure fills**, and lead into the still-unread
part 16. The action that follows is not supplied.

Part 13 independently preserves much of the same word at its opening. Its
15-letter word proposal costs **three observed substitutions and two fills**.
Together, these extensions add **20 proposed fixed positions** to the existing
editions, without adding a physical source or changing any raw source count.
They remain explicitly priced editorial readings.

## Part 15: a complete proposed tail, with the unknown square retained

**Raw output — unchanged last 26 positions, at 91–116:**

```text
?7???S???3?N???H???B?L???G
```

**Edited output — one known-coordinate substitution and 18 printed-mask fills:**

```text
X7XAUSDER3XNACHHUTSTELLUNG
```

**Readable German — editorial punctuation and spacing:**

> 7. Aus der 3. Nachhutstellung …

This is a beginning, not a complete instruction. It specifies a point of
departure in the withdrawal order; neither its ensuing action nor the
geographical location of this third position is recovered.

The raw **7** at plaintext position **92** and raw **3** at position **100**
remain unchanged. Interpreting them as a numbered heading and an ordinal,
and supplying the surrounding `X` separators, are editorial decisions.
The nearby part-17 heading `9` supports the numbered-order context.

The one known-coordinate change is **source position 140, X→V**, which changes
raw plaintext **B→T at position 110**. The
[original source crop](../withdrawal_recovery/sources/childs_p163_A15_A16.png)
clearly prints `X` as the first character of `XDDFV`, the fifth group in the
fourth row. This is a proposed historical error repair, not a revised
transcription of an ambiguous glyph.

The tail's 18 other unknown positions each retain **one observed
half-coordinate**. No newly supplied tail letter is wholly unobserved.
The compatible span `AUSDER3XNACHHUT` requires **no observed-coordinate change**
and eleven fills; `X7X` requires two further fills. All of the new observed
repair cost lies in the final `STELLUNG` sequence.

Joined to the separately published prefix, the proposed part reads:

**Edited output — inherited prefix plus the proposed tail; the shared square digit remains unknown:**

```text
VONBUKARESTGENERALKOMMANDO?3XUNTERSTELLTUNDWIRDNACHANKUNFTINKRONSTADTOXKXSCHOLTZZUGEFUEHRTXX7XAUSDER3XNACHHUTSTELLUNG
```

The published partial square still yields **116/117 fixed positions**. The
remaining `?` is the linked `5`/`6` corps digit. The verifier retains **both**
global injective square assignments and their complete re-encrypting witnesses;
it does not select a new digit assignment. The earlier historical argument for
corps 63 remains a separate layer.

The full part-15 price is **three observed substitutions and 81 printed-erasure
fills**, including the earlier prefix's two substitutions and 63 fills. That
prefix already contains one wholly unobserved letter, at plaintext position
18; this supplement does not relabel that inherited choice as source-forced.
The new tail raises the earlier edition from **98/117 to 116/117** fixed
positions under the published partial square.

## Part 13: separate the repeated word, separator, and opening preposition

**Raw output — unchanged first 20 positions:**

```text
ALS3QIA2HHUB?TE?LUNG
```

The following existing edited words are `ZUERFOLGEN`. Three levels are retained:

| Layer | Proposed first 20 positions | Additional observed substitutions | Additional printed-mask fills |
|---|---|---:|---:|
| Repeated word only | `ALS3QNACHHUTSTELLUNG` | 3 | 2 |
| Also propose the separator | `ALS3XNACHHUTSTELLUNG` | 4 | 2 |
| Further grammatical proposal | `AUS3XNACHHUTSTELLUNG` | 6 | 2 |

The least expansive layer leaves raw **ALS3Q** in place. The separator costs
source **95 F→V**. Reading **AUS** instead of raw **ALS** costs two further
observed substitutions, **81 D→A** and **188 D→V**. The resulting phrase
“aus 3. Nachhutstellung zu erfolgen” fits the part-15 continuation, but the
preceding part is unavailable; `AUS` is not forced by the surviving syntax.
The preceding printed page 162 contains separate short messages, not part 12
of this order. The lower-cost `ALS` reading is therefore retained explicitly.

Within the word alone, the recorded repairs are **27 G→X**, **14 G→F**, and
**189 X→V**; printed masks **1** and **28** are filled with `D`. These replace
raw `I`, `2`, and `B` by proposed `N`, `C`, and `T`, respectively. In particular,
the original numeral `2` is visibly accounted for as a repair; it is not
silently normalized. The preceding raw **3** remains unchanged.

All three word-bearing versions fix the remaining two source erasures and
raise the existing part-13 edition from **132/134 to 134/134** fixed positions.
Their full-part prices are respectively **13**, **14**, and **16** observed
substitutions, each with **eight** printed-mask fills. Every version retains
the **268 visible slots**, despite the printed **RICHI-278** header. No
unproved ten-coordinate restoration is introduced.

## Exact joint support and the alternatives it leaves

The joint check makes one explicit assumption: the aligned 15-position spans
in parts 13 and 15 represent **one shared word**. It then minimizes observed
coordinate substitutions over all 36 alphabet labels, under both global
assignments of the partial square's two unknown cells. Masked coordinates have
no mismatch cost.

| Word position, zero-based | Part-13 original pair | Part-15 original pair | Labels at the joint minimum | Proposed label |
|---:|---|---|---|---|
| 0 | `GG` | `XG` | `IN` | N |
| 1 | `XD` | `?D` | `A` | A |
| 2 | `GD` | `F?` | `2C` | C |
| 3 | `VX` | `V?` | `H` | H |
| 4 | `VX` | `VX` | `H` | H |
| 5 | `AV` | `A?` | `U` | U |
| 6 | `GX` | `?V` | `BT` | T |
| 7 | `?X` | `?X` | `BFHOSW` | S |
| 8 | `GV` | `GX` | `BT` | T |
| 9 | `DV` | `D?` | `E` | E |
| 10 | `?D` | `DD` | `L` | L |
| 11 | `DD` | `?D` | `L` | L |
| 12 | `AV` | `A?` | `U` | U |
| 13 | `XG` | `X?` | `N` | N |
| 14 | `DG` | `DG` | `G` | G |

The minimum is **four observed substitutions across the two word spans**,
attained by **96 common strings**. Ten letters are forced at that minimum;
four disagreements give two-way choices, and the shared erased first half
at word position 7 permits six letters. Both global digit assignments produce
the same result. Every tied string is retained in
[`certificates.json`](certificates.json).

`NACHHUTSTELLUNG` is one of those minima, not a uniquely forced cipher answer.
The withdrawal context and independent attestation of the complete military
compound support its lexical selection. Seven of part 15's ten newly fixed
letters inside that compound also have unchanged, fully observed part-13
witnesses. Part 15 in turn directly supports the `L` supplied at part-13
position 15. The `S` half-coordinate erased in both copies remains a lexical
choice.

The full-tail alternatives also remain visible. `X7XAUSNUR3XNACHHUTSTELLUNG`
has the same **one-substitution / eighteen-fill** cost: `DER` versus `NUR`
cannot be decided by coordinate agreement alone, and the unread next part
could matter to the grammar. The coordinate-compatible string
`X7XAUSDER3XNACHHUTHBELLING` has that same price, but no person or coherent
sentence is identified from it. Both are retained as compatibility rivals,
not silently discarded by a language score.

The earlier exploratory `NACHHERSTELLUNG` is also priced separately: its
15-letter span requires **three** observed changes and ten fills, compared
with **one** and ten for `NACHHUTSTELLUNG`. Its two extra substitutions are
not made in the selected proposal.

## Independent vocabulary witnesses

The unchanged raw stream of [p176 B2](../nov10_delegates_and_field_report/README.md)
contains `NEUESTELLUNGENDONAUKNIE` under a different period key. The verifier
rebuilds the eight-letter `STELLUNG` witness directly from its original source
coordinates, with no substitutions or fills. This attests the letter sequence
in military vocabulary, not the entire part-15 sentence.

More specifically, a reproduced **26 August 1915** AOK 11 situation assessment,
Ia no. 6480, uses **“eine feindliche Nachhutstellung”**. It appears in the
“Gorlice” chapter of Hans von Seeckt's *Aus meinem Leben. 1866–1917* (1938),
[available in the public Projekt Gutenberg text](https://projekt-gutenberg.org/authors/hans-von-seeckt/books/aus-meinem-leben-1866-1917/chapter/7/).
This establishes historical use of the compound. It is not a parallel copy of
the November 1918 order and does not attest this third position or the proposed
full clause. The package records the public text witness and its scope without
claiming to possess a hash-verified original scan of that report.

## Reproduce

```sh
python3 experiments/p163_rearguard_continuation/verify.py --verify
```

The standard-library verifier checks the existing input/certificate and source
image hashes, independently reconstructs ragged-column offsets, compares every
raw domain with the project reader, and records every proposed substitution
and fill. It recomputes all three part-13 layers, the full part-15 continuation,
the retained rivals, all 96 joint minimum strings, the independent native
vocabulary witness, and exact re-encryption under both complete digit
assignments. It adds no source records, changes no key, and assigns no frame or
plaintext to the jammed fragment between parts 15 and 17.
