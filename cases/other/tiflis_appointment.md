# A Polish representative in Tiflis — p192 parts 2 and 3

[Case index](../README.md) · [November 14 retransmissions](nov14_radio_retransmissions.md)

**Source edition, missing-group recovery and historical comparison: icekylinx and GPT-6 Astra Pro.**

The two unheaded parts at the top of printed page 192 describe an appointment
to represent the Polish government in the Caucasus. The first is directly
readable under the published November 13–15b key. The second becomes readable
after an explicitly certified missing five-coordinate group. Its courier
surname provides independent historical support for the conditional key
assignment **FX = Y**.

## Readable meaning

> Tiflis: You have been appointed the Polish government's trusted
> representative for the republics of Georgia, Armenia and Azerbaijan,
> with your seat in Tiflis. The appointment and instructions have already
> been sent to you through [Tydelski]. Ministry of Foreign Affairs. Bussche.

The bracketed surname uses the historical identification described below.
The preceding part and original message header have not been recovered.
Accordingly the addressee is not supplied from historical expectation.
The page is dated November 14, 1918; that is not independently established as
the appointment's original issue date.

### Part 2: the appointment and its geographic scope

All 230 source coordinates are valid. Their unmodified decryption is:

```text
TIFLISDOPPELPUNKTXSIESINDZUMVSRTRAUENSMANNDERPOLNISCHENREGIERUNGFUERDIEREPUBLIKENXGRUSIENXARMENIENXUNDXASERBEJNZANX
```

The ordinary-word candidate changes one source coordinate to give
`VERTRAUENSMANN`. The exact country spelling `ASERBEJNZAN` is retained in the
base reading. A separate same-length `ASERBEJDZAN` proposal costs one
additional coordinate change; neither spelling is silently expanded to
modern German. The interpretation as Azerbaijan follows the country list
and recognizable transmitted name, rather than a claim that every letter
is correct.

### Part 3: a missing group established without the surname

The source prints **227 valid coordinates** under a `RICHI-232` heading.
The certificate tests insertion of one five-coordinate gap at **all 228
possible boundaries**. Its ordinary-word stencil masks the entire eight-slot
courier name and the seven-slot signature. Neither `TYDELSKI` nor `BUSSCHE`
helps choose the gap.

The unique minimum is **source boundary 150**, before the printed group
`AAAFF`: exactly one observed coordinate must change to fit the surrounding
words. Four other boundaries require two changes. This is an exact result
for the stated single-group-loss model and displayed stencil, rather than a
proof of the historical copying error.

Under that geometry, before word repairs, the unchanged key gives:

```text
MITSITZINEIFLISERNANNTXXERNENNUNGUNDINST?UKTIONB?REITSDU?CHXT?DE?SKIXANS?EABGESANDTXXMINISTERIUMDESAEUSSERNXXBUSSCHE
```

Ordinary words supply four missing coordinates, and one observed-coordinate
change corrects `EIFLIS` to `TIFLIS`. The result fixes **114/116 positions**:

```text
MITSITZINTIFLISERNANNTXXERNENNUNGUNDINSTRUKTIONBEREITSDURCHXT?DE?SKIXANSIEABGESANDTXXMINISTERIUMDESAEUSSERNXXBUSSCHE
```

The unknown name letter at position 61 is a complete observed `FX` pair,
made from **original source indices 80 and 138**. Both coordinates precede
the gap and remain unchanged throughout every repair. The other unknown,
at position 64, has an observed F and one missing coordinate.

## The separate historical-name inference

Marek Mądzik's [archival study](https://bazhum.muzhp.pl/media/texts/rocznik-lubelski/1987-1988-tom-29-30/rocznik_lubelski-r1987_1988-t29_30-s77-87.pdf#page=3),
printed p78 note 3, names engineer Tadeusz Tydelski as chairman of the Polish
Caucasus council, citing CAW relacje 400.2500, appendix 2, p3. Pages 78–79
also connect him with Ostrowski's Baku office. The article and
[short name crop](../../experiments/tiflis_appointment/sources/madzik_p78_name.png)
were checked; the underlying manuscript was not. Identifying this courier
with that person remains a separate inference.

Under that identification, `T?DE?SKI` becomes `TYDELSKI`. It supplies the
missing L coordinate and sets **FX = Y** in the November 13–15b square.
The full candidate then reads:

```text
MITSITZINTIFLISERNANNTXXERNENNUNGUNDINSTRUKTIONBEREITSDURCHXTYDELSKIXANSIEABGESANDTXXMINISTERIUMDESAEUSSERNXXBUSSCHE
```

Its exact repair certificate has **one observed-coordinate substitution**
and **five inserted coordinates**, `GFGFA`, at the declared gap. Full
reencryption reproduces that repaired ciphertext exactly. The historical
key file remains unchanged.

This check alone does not prove Y: the same repaired ciphertext can encode
`T2DELSKI`, `T3DELSKI`, `T4DELSKI`, `T7DELSKI`, `T8DELSKI`, `T9DELSKI`,
`TQDELSKI` or `TYDELSKI` under the eight possible cell assignments. The
independent historical surname supplies the reason to select Y.

## Consequences for the pilot notices

Two inference layers are kept distinct:

| Layer | Assignment | Additional assumption | Complete-pair effects in these editions |
|---|---|---|---|
| Historical courier name | Nov13–15b FX = Y | The damaged courier name identifies Tydelski with correct spelling | p192 part 3 position 61; p190 A position 37 becomes FRYE |
| Cross-key pilot-name transfer | Nov13–15a DG = Y | The p190 A and p194 B FR?E fields contain the same correctly copied name | p194 B position 54 and interrupted p193 B position 54 |

Positions are zero-based. The first assignment does not depend on the pilot's
identity. The second remains conditional even if the Tydelski identification
is accepted. The machine-readable report includes every before/after raw
text and marginal-domain change across the two Tiflis records and all seven
[November 14 records](nov14_radio_retransmissions.md), including changes that
do not create another fixed letter.

## Evidence and reproduction

- [Literal source and historical-reference metadata](../../experiments/tiflis_appointment/inputs.json)
- [All 228 gap models, exact repairs and conditional key-layer effects](../../experiments/tiflis_appointment/certificates.json)
- [Part 2 source](../../experiments/tiflis_appointment/sources/p192_2.png)
- [Part 3 source](../../experiments/tiflis_appointment/sources/p192_3.png)
- [Verification instructions](../../experiments/tiflis_appointment/README.md)

The two records contain 457 printed coordinate letters. The declared
462-coordinate frame fixes 225/231 raw positions before repairs, 229/231
after the ordinary-word layer, and 231/231 under the historical-name layer.
Raw fixed positions include source garbles; these counts describe the
mathematical consequences of each explicitly stated layer.
