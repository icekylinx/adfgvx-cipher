# Transports from Romania: warning against entry into Hungary

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition: icekylinx and GPT-6 Astra Pro.** Childs printed p184 (PDF p187), 13 November 1918; published `Nov13-15a` key, unchanged. [Inputs](../../experiments/hungary_transport_warning/inputs.json), [exact certificates](../../experiments/hungary_transport_warning/certificates.json), [method and limits](../../experiments/hungary_transport_warning/README.md).

Two three-part transmissions address the Mackensen command's mineral-oil department and warn that transports from Romania should not be allowed into Hungary because they would be lost there. This is what the message says; the edition supplies no independent evidence that this outcome happened.

Both origin headers give LP for UKS, `13.40 (13/11)`, three parts. The different receipt headers give `02.51 a.m.` and `02.15 a.m.` on the same date, an unresolved chronological inconsistency. The addresses and bodies differ in length. They are compared by explicit shared passages, not treated as identical whole messages.

## p184 B1

[Source crop](../../experiments/hungary_transport_warning/sources/p184_B1.png). All 146 printed coordinates give 73 fixed positions without repair:

**Raw output:**

```text
ANXOBERKOMMANDOXMACKENSENXWIRTSCHAFTSSTABXMINERALOELABTEILUNGXBUCKARESTXX
```

Reading: “An Oberkommando Mackensen, Wirtschaftsstab, Mineralölabteilung, Buckarest.” The received city spelling `BUCKAREST` is retained.

## p184 B2

[Source crop](../../experiments/hungary_transport_warning/sources/p184_B2.png). The source advertises 192 coordinates but prints 187. With five unknown coordinates inserted before source index 35, the 96-position raw text is:

**Raw output — conditional five-coordinate gap before source index 35:**

```text
TRANSPOR?EXVONXRUM?ENIENXNIC?TXNACHXUNGARNXHEREINLASSENXDAXSIEXINXUNGARNXRESTLO?XVERLOREN?SINDXX
```

The corresponding C2 text independently determines the missing group `DXDVA`. No observed B2 coordinate changes:

**Edited output — missing group supplied by the independently identified C2 witness:**

```text
TRANSPORTEXVONXRUMAENIENXNICHTXNACHXUNGARNXHEREINLASSENXDAXSIEXINXUNGARNXRESTLOSXVERLORENXSINDXX
```

Reading: “Transporte von Rumänien nicht nach Ungarn hereinlassen, da sie in Ungarn restlos verloren sind.” The gap is uniquely located among all 188 placements of one contiguous five-coordinate gap, using only 92 matching raw C2 positions. The certificate lists every gap score and the five individual witnesses. It does not assert uniqueness outside this recorded model.

## p184 B3

[Source crop](../../experiments/hungary_transport_warning/sources/p184_B3.png). All 110 coordinates are observed. The 55-position raw text retains 15 unknown reference positions:

**Raw output:**

```text
KRIEGSAMTXROEMX?X???STRICH????XKRAX???STRICH????XANCHXX
```

The office and reference syntax are readable; the number labels remain unassigned. No guessed reference number is supplied.

## p184 C1

[Source crop](../../experiments/hungary_transport_warning/sources/p184_C1.png). The shorter 136-coordinate address gives 68 fixed raw positions without repair:

**Raw output:**

```text
ANXOBERKOMMANDOXMKENSENXWIRTSCHAFTSSTABXMINERALOLABTEILUNGXBUMARESTX
```

The received forms `MKENSEN`, `MINERALOL` and `BUMAREST` remain explicit. Their likely relation to B1's address is clear from the message context, but the edition does not invent missing ciphertext to make the addresses identical.

## p184 C2

[Source crop](../../experiments/hungary_transport_warning/sources/p184_C2.png). All 190 coordinates are observed. The 95-position raw text is:

**Raw output:**

```text
TRANSTORTEXVONXRUMAENIENXNICHTXNACHXUNGARNXHE?REINLASSENXDAXSIEXINXUNGARNXRESTLOSVERLORENXTINDX
```

Two observed-coordinate substitutions, source index 75 `V → F` and index 86 `D → G`, yield:

**Edited output:**

```text
TRANSPORTEXVONXRUMAENIENXNICHTXNACHXUNGARNXHE?REINLASSENXDAXSIEXINXUNGARNXRESTLOSVERLORENXSINDX
```

Both corrected letters are witnessed by unchanged B2 positions that were excluded from the gap-selection mask. The extra position in `HE?REIN` remains unknown: plaintext index 45, pair `DX`, source indices 90 and 137, domain `0123456789QY`. The missing separator after `RESTLOS` and the shorter ending remain as received.

## p184 C3

[Source crop](../../experiments/hungary_transport_warning/sources/p184_C3.png); [enlargement of faint final-column groups](../../experiments/hungary_transport_warning/sources/p184_C3_faint.png). All 108 coordinates are retained:

**Raw output:**

```text
KRIEGSAMTXROEMX?X???STRICH????XKRAX???STRICH????XANCHX
```

Every one of these 54 positions has the same coordinate pair as the corresponding B3 position; B3 only adds a final X. All 15 unknown positions remain unknown in each copy. Exact pair agreement confirms the relationship and the preserved reference structure, but supplies no new digit assignment.

## Attribution and scope

Earlier unreviewed repository candidates already recognized much of the address, warning and footer. This edition adds source-checked coordinates and boundaries, an exact missing-group reconstruction, and explicit costed ordinary-word corrections. No claim of first historical decipherment is made. All fixed letters remain labels under the published key, and all unknown domains are available in the certificate.
