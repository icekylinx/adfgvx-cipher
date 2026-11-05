# Military meal allowances and a refused supplement

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

This source edition assembles the four explicitly numbered parts of one
message: **p129 B1, p133 A2–A3 and p134 A4**. Every page repeats
`NKJ FUER COS v LP (7.18 a.m., November 6th)` and
`2400 (5/11) 4 TEILE`. The printed continuation notices and part numbers
support the assembly across nonconsecutive pages. It is not inferred
from thematic similarity or physical adjacency.

The message says local cash meal allowances are too high, including for
past periods, and rejects Swedish allowances as a governing standard.
It calls for lower rates based on the price of a field ration. Communal
purchasing and German dining facilities should support normal provision
of food in kind, leaving cash self-provisioning for unavoidable cases.
The final part refuses a requested cost-of-living supplement. The full
[case](../../pages/129.md#edition-cases-finance-military-allowances) preserves raw text,
explicit repairs and unexpanded reference fields.

## A complete direct reading of part three

Earlier OCR recorded 482 slots in p133 A3: it made the opening `VAGAG`
seven slots and omitted the intact final `GXFVD A`. The source contains
exactly the advertised **486 coordinates**. With the unchanged Nov4–6
key, these produce **243 fully readable letters**, without any source
substitution, erasure fill or missing-coordinate model:

```text
NATURALVERPFLEGUNGMUSSREGELBILDENXDIESEDURCHGEMEINSAMENEINKAUFXUMPREISENICHTUNNOETIGINHOEHEZUTREIBENUNDDURCHEINRICHTUNGDEUTSCHERSPEISEHAEUSERNACHMOEGLICHKEITFOERDERNSODASSSELBSTVERPFLEGUNGAUFTATSAECHLICHNICHTZUUMGEHENDEFAELLEBESCHRAENKTBLEIBTX
```

The verifier encrypts this direct reading back to the **unaltered source
ciphertext**. This is correction of the source transcription, not a
change to the published key or a guessed completion of missing source.

## Exact edition costs

| Part | Printed slots | Raw fixed positions | Candidate positions | Observed substitutions | Printed-erasure fills |
| --- | ---: | ---: | ---: | ---: | ---: |
| p129 B1 | 398 | 197/199 | 199 | 5 | 2 |
| p133 A2 | 452 | 225/226 | 226 | 4 | 1 |
| p133 A3 | 486 | 243/243 | 243 | 0 | 0 |
| p134 A4 | 424 | 212/212 | 212 | 1 | 0 |
| **Total** | **1,760** | **877/880** | **880** | **10** | **3** |

The three printed erasures are `-` and `C` in B1 and `L` in A2. Literal
invalid glyphs remain in the inputs. In A4 the only candidate change
repairs raw `0` between `ERBETEN` and `BEANTRAGTE` to a separator `X`.
It is separately priced and does not assign a global numerical mapping.

All reference fields remain unchanged, including initial
`X M X RM X 30 NR X 228`, final `PASCHE X RM X 2` and
`NR X 1235 X 18 X G X B X 1`. The edition does not expand `PASCHE` into a
particular book, author or regulation without independent evidence.
No actual Swedish rate or allowance amount is reconstructed.

## Prior work and limits

Parts one, two and four were already readable in earlier unreviewed
repository OCR screens. The old part-three output was unreadable under
its wrong 482-coordinate frame; all four prior candidate records are
frozen in `inputs.json`. The new contribution is visual source correction,
complete assembly, the direct third-part reading and reversible repairs.
Bounded checks did not locate an explicit body discussion in the paper,
dissertation chapter or cached comment thread. No first historical
decipherment claim is made.

The text records a requested policy and a refused supplement. It does
not establish that rates were subsequently reduced or that dining
facilities were actually created.

## Reproduce

```bash
python experiments/military_allowances/verify.py --verify
python experiments/military_allowances/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks the part sequence, header agreement, independent
coordinate mappings, plaintext domains, all repairs and exact
re-encryption. The optional PDF check verifies the source hash and crop
pixels. `catalog_proposal.json` proposes four source-record entries;
the shared catalog is not edited by this package.
