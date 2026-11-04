# Oil stocks and production: the Nobel and Hagelin message

The Nobel oil inquiry requests stock and production figures for the different grades of naphtha at the firm and other companies, quantities already delivered, and corresponding information for Novorossisk. The message bears the name Hagelin; the body and its interpretation were published by Lasry and collaborators.

**Complete edition by printed page:** [p. 64](../pages/064.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


**Prior body and interpretation:** George Lasry, Ingo Niebel, Nils Kopal
and Arno Wacker, *Deciphering ADFGVX messages from the Eastern Front of
World War I* (2016), **§6.6 and Table 5**, author PDF pp25–26,
[DOI](https://doi.org/10.1080/01611194.2016.1169461). · [Reading conventions](../../docs/reading-conventions.md)

**Current source edition and exact repair audit: icekylinx and GPT-6 Astra Pro.**

The paper already publishes this complete two-part oil inquiry and
discusses the Hagelin name. This case supplies its literal source frames,
quantified repairs and qualification of marked or faded characters.
It is not a first-decipherment or new personal-identification claim.

Childs printed p64 A, PDF p67, is headed
`--- v NKJ (3.23 a.m., October 5th)` and **Beginning lost**. Its first
surviving body has length 346 and no printed part number; this edition
calls it A1. The following body explicitly says `2 TL / RICHI-354`.
Both native lengths agree with their headers and use the unchanged
published **Oct4–6** key.

## p64 A1

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 346-coordinate frame:**

```text
HP?MXBENEDIKTXVERTRETERKUKAOKXINATORXATOMXXERSUCHEDRINGENEZUSTELLUNGFOLGENDENTELEGRXUXVERANLASSUNGDASSANTWXTELEGRXANHERUEBYRMITTELTWIRDXXGEBRSEDERNOBELXATOMXXDRAHTETVOURAETE
```

**Edited output — four observed-coordinate substitutions and one
printed-dash fill:**

```text
HPTMXBENEDIKTXVERTRETERKUKAOKXINATOMXATOMXXERSUCHEDRINGENEZUSTELLUNGFOLGENDENTELEGRXUXVERANLASSUNGDASSANTWXTELEGRXANHERUEBERMITTELTWIRDXXGEBRUEDERNOBELXATOMXXDRAHTETVORRAETE
```

</details>

**Readable German — spacing, punctuation and the two bracketed
editorial expansions noted below:**

> [Hauptmann] Benedikt, Vertreter k.u.k. A.O.K. in Atom. Atom. Ersuche
> [dringende] Zustellung folgenden Telegr. u. Veranlassung, dass Antw.
> telegr. anher übermittelt wird. Gebrüder Nobel, Atom: Drahtet Vorräte …

`HPTM` is expanded in brackets. The bracketed **dringende** is a
grammatical normalization of the exact stream's **DRINGENE**; the
additional D is not claimed as a recovered encoded character. The
ellipsis means that the source message continues in A2 below. The
repeated `ATOM` remains visible and is not replaced with another place.

The [source crop](../../experiments/p64_oil_and_radio/sources/p64_A1.png)
has one printed dash. Three faded right-edge glyphs have primary readings
V, X and F, documented in an enlarged crop. A separate variant masks
those three readings and quantifies the resulting uncertainty. It does
not change the accepted transcript or conceal a length adjustment.

## p64 A2

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 354-coordinate frame, including both parenthesized
X coordinates:**

```text
NAPHTAXPRODUKTIONSAEMTLICHERSORTENBEIUNSUND6NDERENFIRMENATOMXFERNERWIEVIELBISJETZTGELIEFERTXDIEUELBENDATEQBETREFFENNQVOROSSISKFALLSSOLCHEIHNENBEKANNTXHAGELINXXXLSTARMEEOXQU12059
```

**Edited output — five observed-coordinate substitutions:**

```text
NAPHTAXPRODUKTIONSAEMTLICHERSORTENBEIUNSUNDANDERENFIRMENATOMXFERNERWIEVIELBISJETZTGELIEFERTXDIESELBENDATENBETREFFENNOVOROSSISKFALLSSOLCHEIHNENBEKANNTXHAGELINXXXOSTARMEEOXQU12059
```

</details>

**Readable German — spacing and punctuation of that candidate:**

> Naphta-Produktion sämtlicher Sorten bei uns und anderen Firmen Atom.
> Ferner, wieviel bis jetzt geliefert. Dieselben Daten betreffen
> Novorossisk, falls solche Ihnen bekannt. Hagelin. Ostarmee O. Qu. 12059.

The native word **BETREFFEN** remains. The paper's table prints
**BETREFFEND**; its extra D is not inserted into this exact stream.
The inquiry seeks oil-related figures rather than reporting actual
stock or delivery amounts. The reference number is qualified below.

The name **HAGELIN** is directly present in the raw reading. Lasry and
colleagues propose Karl Wilhelm Hagelin and also note uncertainty about
the name's role in the message. This edition does not independently
identify the person or determine who authored the quoted request.

## Parentheses and the reference number

The [source](../../experiments/p64_oil_and_radio/sources/p64_A2.png)
prints **`(X)XVVG`** and **`GFD(X)`**. Those marked X values occupy
source coordinates **90** and **353**. They count as one coordinate
each; the qualification punctuation is retained in the literal rows.

The primary edition accepts both printed X values. Its word repair
changes source 90 from X to A. If this marked coordinate is instead
treated as unknown, that same change is a mask fill and the remaining
observed-substitution count is four. Both prices are recorded.

**Conditional interpretation — the final reference:** The `5` in
`12059` depends on the parenthesized X at source 353. Masking it leaves
the field **`120?9`**, whose unknown has domain **57DSTU**. Requiring a
decimal reference would leave **12059 or 12079**. That field-type
assumption does not choose one, and the sensitivity edition does not
silently retain the primary 5. Every complete coordinate alternative
has an exact re-encryption witness.

## Exact scope

The two parts have **700 source slots**, **699 valid coordinates**, and
**350 plaintext positions**. The primary raw readings fix **349 / 350**
positions; the edited candidates fix **350 / 350**, with **nine
observed-coordinate substitutions and one printed-dash fill**. There
is no insertion, deletion, group movement or key change. The source
qualification variants are not additional physical records.

[Inputs](../../experiments/p64_oil_and_radio/inputs.json),
[certificates](../../experiments/p64_oil_and_radio/certificates.json)
and [verification instructions](../../experiments/p64_oil_and_radio/README.md)
preserve every printed row, coordinate price, alternative domain and
prior attribution.

</details>
<!-- CASE-EDITION:END -->
