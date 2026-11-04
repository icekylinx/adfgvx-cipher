# An optional technical reading for the p63 inspector request

[Reading conventions](../../docs/reading-conventions.md)

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The [existing p63 A edition](../../cases/caucasus/october_requests.md#p63-a--a-partially-readable-inspector-request)
leaves the 21-character span `VASCHIWNENMECH8ISCHEN` unassigned. A more
specific **optional** reading is now available: `MASCHINENTECHNISCHEN`,
conditional on treating one raw `W` as surplus and making three additional
observed-coordinate substitutions. It does not replace the primary partial
edition or add a newly recovered physical record.

The proposal is equivalent to excluding the two coordinates `DD` at
untransposed indices **86–87** from plaintext pairing. They remain in the
complete transmitted witness. Including the already stated repairs outside
the technical span, the full optional candidate costs **15 observed-coordinate
substitutions, two printed-dash fills and two surplus interim coordinates**.
The primary edition continues to cost 12 substitutions and two dash fills,
with the technical span unassigned.

## The source and the two reading frames

The [already published source crop](../october_requests/sources/childs_p63_A.png)
shows 54 groups of five, or **270 literal slots**. The header remains
`RICHI-54`, not `RICHI-270`; it contains the printed spelling
`FEZDEIRENBAHNCHEF`. Nothing is cancelled in the printed body. The unchanged
published `Oct4-6` square and rank order apply.

**Raw output — complete unchanged native 270-slot source; 133/135 fixed positions:**

```text
E?BITTEUEBER?EID5OGJEEINESBESRIEBSUNDVASCHIWNENMECH8ISCHENKONTROLLEWRSGENERALVSNKRESSEINVERSTAODENDEUTSCHEDELXKASKXABTXZXNRX474DG1MOOLX
```

The original partial template preserves its 21 unassigned positions:

**Edited output — existing primary partial edition, unchanged:**

```text
ERBITTEUEBERSENDUNGJEEINESBETRIEBSUND?????????????????????KONTROLLEURSGENERALVONKRESSEINVERSTANDENDEUTSCHEDELXKAUKXABTXZXNRX474DGEMOLLX
```

For the optional model, first undo the original 270-slot transposition.
The extra `W` at native plaintext index 43 corresponds exactly to the pair
`DD` at interim indices 86–87. Treating that pair as surplus gives 268
pairing coordinates and the following 134-position stream. No received
coordinate is removed before reversing the original transposition.

**Raw output — conditional pairing after excluding interim DD, before word repairs; 132/134 fixed positions:**

```text
E?BITTEUEBER?EID5OGJEEINESBESRIEBSUNDVASCHINENMECH8ISCHENKONTROLLEWRSGENERALVSNKRESSEINVERSTAODENDEUTSCHEDELXKASKXABTXZXNRX474DG1MOOLX
```

The technical substring is now `VASCHINENMECH8ISCHEN`. Three explicitly
priced single-coordinate substitutions give `MASCHINENTECHNISCHEN`:

**Edited output — optional 134-position candidate under the surplus-DD model:**

```text
ERBITTEUEBERSENDUNGJEEINESBETRIEBSUNDMASCHINENTECHNISCHENKONTROLLEURSGENERALVONKRESSEINVERSTANDENDEUTSCHEDELXKAUKXABTXZXNRX474DGEMOLLX
```

**Readable German — complete optional edited stream:**

> Erbitte Übersendung je eines Betriebs- und maschinentechnischen Kontrolleurs.
> General von Kress einverstanden. Deutsche Del. Kauk. Abt. Z. Nr 474D. Gemoll.

The optional wording requests an inspector for operations and a technical
inspector for machinery. That description depends on the proposed deletion
and repairs. The source does not itself demonstrate that either person was
sent, or identify them. The existing `GEMOLL` name repair retains its
separate clear-header support on p69; no new identity claim is added here.

## Every additional operation

Indices are zero-based except the printed group/character column.

| Operation | Original source index | Printed group / character | Native plaintext index | Conditional plaintext index | Effect |
| --- | ---: | --- | ---: | ---: | --- |
| Keep `D` as surplus interim coordinate 86 | 261 | 53 / 2 (`GDDFF`) | 43 | — | First coordinate of raw extra `W`; restored before forward transposition |
| Keep `D` as surplus interim coordinate 87 | 16 | 4 / 2 (`XDVXX`) | 43 | — | Second coordinate of the same raw `W`; restored before forward transposition |
| `X` → `V` | 54 | 11 / 5 (`FVGGX`) | 37 | 37 | `V` → `M` at the start of the technical word |
| `F` → `G` | 177 | 36 / 3 (`GGFVG`) | 47 | 46 | `M` → `T` in the technical word |
| `F` → `D` | 238 | 48 / 4 (`XFVFF`) | 51 | 50 | Raw numeral label `8` → `N` inside the proposed word |

The 12 substitutions and two dash fills outside this word are exactly the
same original-source changes as in the primary edition. The certificate
compares their complete ledger. The added `8` → `N` proposal is a local word
repair; the substitution square remains unchanged and `474D` is retained.
The two surplus `D` coordinates are neither a dash fill nor a deletion from
the recorded ciphertext.

To reproduce the 270-slot received witness, encode the 134-character optional
text, reinsert the original `DD` at interim boundary 86, and transpose the
result with the original rank order. This reproduces every source coordinate
after precisely the 15 substitutions and two printed-mask fills. Directly
transposing only 268 coordinates would be a different model and is not the
operation used here.

## Exhaustive comparison within the declared family

For this fixed 134-character target, the verifier compares all **36,315**
ways to exclude two distinct coordinates from the original 270-coordinate
intermediate stream. The pair **[86, 87]** is the sole minimum at **15
observed-coordinate substitutions and two mask fills**. The subset of **269
adjacent-pair exclusions** has the same unique minimum. Every cost, not just
the winning pair, is retained in the certificate.

This is a retrospective fixed-target comparison. It does not prove the
historical mechanism or exclude another wording. A spurious plaintext `W`
before encipherment and an extra fractionated `DD` before transposition are
indistinguishable under this model. The printed source gives no cancellation
mark at either original coordinate, and the two source locations are far
apart. These limitations are why the result remains a separate optional
interpretation.

The old 21-letter proposal `MASCHINENMECHANISCHEN` remains an unaccepted
same-length conjecture at 28 observed substitutions. The new model costs
fewer substitutions while adding a different explicit operation, so these
are different error hypotheses rather than interchangeable cost totals.

## Independent period vocabulary, with a narrow evidential role

A directly inspected primary text, [“Eingesandt,” *Dinglers Polytechnisches
Journal*, volume 315 (1900), p52](https://dingler.bbaw.de/articles/mi315mi03_3.html),
uses the phrase **“maschinentechnischer Eisenbahnsekretär”** in a notice about
railway technical careers. The BBAW digital edition supplies a period
railway attestation of the adjective. It does **not** attest this particular
telegram, the exact *Kontrolleur* title, or the surplus-coordinate model.
The candidate remains an inference from the damaged cipher text and word
structure. Only the short lexical phrase is reproduced; the digital text
is attributed to the BBAW Dingler edition under its CC BY-SA 4.0 notice.

## Reproduce

[Inputs](inputs.json) preserve the existing source record and key without
altering either. [The certificate](certificates.json) binds the two frames,
every coordinate origin, all extra operations, numeral repairs, the exact
270-slot forward witness and the complete two-removal cost grid. It also
checks that every heading, fenced display and quoted display of the
existing primary case remains unchanged.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
[printed p63, PDF p66](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The unchanged period key retains the existing attribution to J. Rives
Childs, George Lasry, and **George Lasry, Ingo Niebel, Nils Kopal and Arno
Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
No first historical body-decipherment claim is made.

```sh
python experiments/p63_optional_technical_reading/verify.py --verify
python experiments/p63_optional_technical_reading/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```
