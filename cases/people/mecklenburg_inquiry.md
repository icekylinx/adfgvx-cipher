# Mecklenburg inquiry about a letter to Herzog Karl Michael

The Mecklenburg legation requests prompt answers through Kapitänleutnant Wagner and the Tiflis consulate. The two parts retain their separate addressees and reference fields.

**Complete edition by printed page:** [p. 141](../pages/141.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p141 A, PDF p144, contains two parts received under
`ASO v LP (08.12 p.m., November 6th)`, with `FUER ASO (6/11) 2 TLE`.
The Mecklenburg legation requests quick answers through
Kapitänleutnant Wagner and the Tiflis consulate. The second part asks about a
July letter to Herzog Karl Michael and his opportunity to respond. The
wording is awkward in one place and is preserved below.

## p141 A1

The [first-part crop](../../experiments/mecklenburg_and_seaplane_personnel/sources/p141_A1.png)
has **304 slots**, matching `1 TL RICHI-304`. There is one printed dash
and one unreadable visible glyph. The unchanged published **Nov4–6** key
fixes **150 / 152 positions** before editing.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 304-coordinate frame:**

```text
BXMXKXSEWASTOPOLX?ECKLENBURGISCHEGESZNDTSCHAFTBITTETDRINZENDBEIKAPITAENLEUTNANTXWAGNERXUNDKONSULATXTIFLISXSCHNELLEBEANTWORTUNGFOLGEN?ERFRAGENZUERWIRKENX
```

**Edited output — three observed-coordinate substitutions, one printed-dash fill and one unreadable-glyph fill:**

```text
BXMXKXSEWASTOPOLXMECKLENBURGISCHEGESANDTSCHAFTBITTETDRINGENDBEIKAPITAENLEUTNANTXWAGNERXUNDKONSULATXTIFLISXSCHNELLEBEANTWORTUNGFOLGENDERFRAGENZUERWIRKENX
```

</details>

**Readable German — spacing and punctuation:**

> B. M. K., Sewastopol. Mecklenburgische Gesandtschaft bittet dringend,
> bei Kapitänleutnant Wagner und Konsulat Tiflis schnelle Beantwortung
> folgender Fragen zu erwirken.

The `?` inside the ciphertext transcription's group `XAX?F` is a
placeholder for an indeterminate visible mark at source **68**, not a
printed question mark or an omitted source slot. The candidate supplies F,
yielding the D in `FOLGENDER`. The printed dash at source **109** is filled
with X, yielding the M in `MECKLENBURGISCHE`.

## p141 A2

The [second-part crop](../../experiments/mecklenburg_and_seaplane_personnel/sources/p141_A2.png)
contains **422 slots**, including six printed dashes, exactly matching
`2 TL RICHI-422`. Its raw reading fixes **205 / 211 positions**.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 422-coordinate frame:**

```text
1XST?PXISTBEKANNTXOBDASIMJULIANXHERZOGXKARLXMICHAELXABGESANDTHANDSCHREIBENDESGROSSHERZOGSABGESANDTWOODENISTX2XSTOPXISTBEKANNTXOBHERZOGGE?EGENHWIT?UEINERR?ECKAEUSS?RUNGGEH?BTHATXBESTAETIGUNGXAUMIRALSTABX32982XBX2
```

**Edited output — five observed-coordinate substitutions and six printed-dash fills:**

```text
1XSTOPXISTBEKANNTXOBDASIMJULIANXHERZOGXKARLXMICHAELXABGESANDTHANDSCHREIBENDESGROSSHERZOGSABGESANDTWORDENISTX2XSTOPXISTBEKANNTXOBHERZOGGELEGENHEITZUEINERRUECKAEUSSERUNGGEHABTHATXBESTAETIGUNGXADMIRALSTABX32982XBX2
```

</details>

**Readable German — spacing and punctuation; one grammatical spelling expansion is bracketed:**

> 1. Stop. Ist bekannt, ob das im Juli an Herzog Karl Michael
> abgesandt[e] Handschreiben des Grossherzogs abgesandt worden ist?
> 2. Stop. Ist bekannt, ob Herzog Gelegenheit zu einer Rückäusserung
> gehabt hat? Bestätigung. Admiralstab. 32982. B. 2.

The first **ABGESANDT** is directly adjacent to **HANDSCHREIBEN** in the
edited stream. The bracketed E makes that adjective readable in normal
German but is **not** an encoded plaintext position. The later repeated
**ABGESANDT** is also literal. This edition does not silently replace
either occurrence with “delivered,” “received,” or another smoother verb.

## Conditional interpretation and source limits

The primary editions accept a faded G at A1 source **161** and a faint A
at A2 source **279**. The
[detail crop](../../experiments/mecklenburg_and_seaplane_personnel/sources/p141_A1_glyphs.png)
shows the first glyph, and the
[faint group ending](../../experiments/mecklenburg_and_seaplane_personnel/sources/p141_A2_faint_end.png)
shows the second. Their masked alternatives remain in the certificate:

- Masking A1 source 161 changes the initial **B** of `BXMXK` to domain
  **8ABGIR**. The variant leaves that code character unresolved.
- Masking A2 source 279 changes the **E** of the first `ABGESANDT` to
  domain **9EKVXZ**. That variant also leaves its position unresolved.

Each alternative retains all six exact re-encryption witnesses. No newly
masked glyph is filled simply to preserve the primary reading. The
variants do not add physical records or enter the primary counts.

The names, titles and questions are what the telegram says. This source
edition does not independently identify the grand duke, confirm a letter's
dispatch or reply, or expand the `B.M.K.` address and `32982 B2` reference.
The two primary candidates together contain **363 positions**, use **eight
observed substitutions and eight source fills**, and re-encrypt exactly.
There is no frame or key change.

Both bodies were already partly readable in earlier repository screens.
Their prior credit and the published key are retained. The
[inputs](../../experiments/mecklenburg_and_seaplane_personnel/inputs.json),
[certificates](../../experiments/mecklenburg_and_seaplane_personnel/certificates.json)
and [reproduction instructions](../../experiments/mecklenburg_and_seaplane_personnel/README.md)
provide the complete source and editing ledger.

</details>
<!-- CASE-EDITION:END -->
