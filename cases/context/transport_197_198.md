# Equipment and lorry orders — p197/p198 parallels

[Case index](../README.md) · [Earlier transport traffic](transport.md) · [ADFGVX Cipher](../../README.md)

**Source linkage, reconstruction and review: icekylinx and GPT-6 Astra Pro.**
Four additional intercepts extend the transport conversation under the
previously published November 13–15b key. They concern equipment for Darmstadt
and a lorry, trailer and petrol pump. Their source disagreements and length
repairs remain explicit. The separate [p198 D challenge](../p198.md) is still open.

## Most likely readings

### Equipment for Darmstadt — p197 C / p198 B

> Nachr.-Chef. [EINHAFEN: unclear designation]. Zwei US-Geraete nach Darmstadt
> verladen. Station bleibt bis [16X0???] betr.-bereit. Seifert.

**Meaning:** Chief of signals; an unidentified designation follows. Load two
`US` apparatuses for Darmstadt. Keep the station operational until an unresolved
date/time. Signed Seifert. The abbreviations are read as *Nachrichtenchef* and
*betriebsbereit*; their full spellings were not transmitted.

The source-supported editorial template is:

```text
NACHRCHEFXEINHAFENXZWEIUSGERAETENACHDARMSTADTVERLADENX
STATIONBLEIBTBIS16X0???BETRBEREITXSEIFERT
```

Of its **92 specified characters out of 95**, 91 have a complete coordinate
pair in at least one aligned witness. The `E` in `VERLADEN` additionally needs
an erasure fill. Across both witnesses that choice also requires one known
coordinate change above the attainable minimum: **19 changes rather than 18**.
This is an edited composite of conflicting copies, not a clean full reading
already present in either copy.

**Terminology:** `US` plausibly refers to contemporary radio apparatus using
undamped waves. The manufacturer's *Telefunken-Zeitung*, no. 15 (May 1919),
shows an apparatus labelled `Tragbares U S Gerät 17` on printed page 15 and
records delivery of a `U-S-Gerät` on page 16, beside its discussion of
undamped-wave equipment. This supports the equipment interpretation; it does
not identify the specific model in the telegram. See the
[primary journal](https://www.radiomuseum.org/forumdata/users/5100/TZ_3Jg_Nr15_1v1_v10.pdf#page=16)
and [terminology review](../../data/reviews/transport_terminology.json).

`EINHAFEN` is retained without a place identification. The date/time is not
silently normalized to 16:00: the witnesses actually disagree in its final
positions.

### Lorry, trailer and petrol pump — p197 D / p198 E

> Es kommt ein [?]-Tonnen-Auto. Nur besten [Anhaenger] beladen.
> [Benzinpumpe] bereithalten.

**Meaning:** A lorry of unresolved tonnage is coming. Load only the best
trailer and have the petrol pump ready. The bracketed words include explicit
editorial changes; the tonnage is not a recovered digit.

```text
ESKOMMTEIN?TONNENAUTOXNURBESTENANHAENGERBELADENX
BENZINPUMPEBEREITHALTEN
```

Of **70 specified characters out of 71**, 66 have a complete observed pair,
one combines coordinate halves from the two witnesses, and three require
unattested coordinate changes. The preferred wording costs **13** known
coordinate changes across the two copies; their attainable minimum is **8**.
The extra changes affect `A`, `E` in `ANHAENGER` and `Z` in `BENZIN`.

## Linked number fields

The shared partial square links several unresolved characters across the
conversation. These identities help future recovery without choosing a digit:

| Field | Shared square cell |
|---|---|
| Lorry tonnage in p197 D / p198 E | `FV` |
| Hour digit in the planned `1?00` departure, p194 A / p196 B | `FV` |
| Hour digit in the reported `1?00` departure, p197 E / p198 C | `AF` |
| Hour digit in the apparent readiness time `0?05`, p197 C | `GA` |
| Men remaining, p197 E / p198 C | `GD` |

The planned and reported hour digits therefore **differ** under the common
bijective square. The tonnage equals the planned-hour digit. If all four
distinct fields are ordinary single decimal digits, they range over
`2, 3, 4, 7, 8, 9`, giving 360 joint assignments. Treating the reported departure
as same-day and no later than its `13.45` origin field narrows its time to
12:00 or 13:00. Further identifying the two movements and forbidding an early
departure would force the conditional scenario “planned 12:00, departed
13:00, a 2-ton lorry.” Those extra assumptions are unproved, so **the historical
key and the preferred plaintext retain their question marks**.

The [linked-field analysis](../../experiments/transport_followup/linked_fields.json)
records the exact source indices and all three scenario counts; its separate
enumeration checks every one of the square's 40,320 bijective completions.
An [independent review](../../data/reviews/transport_linked_fields_independent.json)
reconstructs the mappings by column offsets and confirms that every tied
source geometry gives the same field identities.

## What was repaired

| Source | Literal evidence | Stated reconstruction |
|---|---|---|
| p197 C | 185 slots against a `RIZI-190` label; six dashes and an invalid `C` | Insert five unknown coordinates. All 186 boundaries were checked; positions 64 and 65 tie and yield the same masked stream. |
| p198 B | 190 valid coordinates | Kept as printed; its disagreements with the proposed reading are recorded separately. |
| p197 D | 142 slots, including one dash at position 89 | A conditional relocation of that dash preserves the order of every known coordinate. Positions 74 and 75 tie among all 142 placements; both survive. |
| p198 E | 147 slots against a `RIZI-142` label; adjacent `XAXVV XAXVV` and an invalid `K` | Delete either identical five-coordinate group. Both deletions give the same 142-slot stream, preserving 141 valid coordinates. |

All positions above are zero-based. Minimum disagreement is an alignment
criterion; it does not establish that a proposed loss or misplaced dash
actually occurred. The two raw source readings, every tied geometry, and all
per-letter alternatives are available in the
[full experiment](../../experiments/transport_followup/README.md).

## Evidence and reproduction

- [Coordinate certificate](../../data/certificates/p197_p198_transport.json)
- [Independent arithmetic review](../../data/reviews/p197_p198_transport_independent.json)
- [p197 C/D source image](../../sources/excerpts/childs_p197_CD.png)
- [p198 B source image](../../sources/excerpts/childs_p198_B.png)
- [p198 E source image](../../sources/excerpts/childs_p198_E.png)

```sh
python3 experiments/transport_followup/verify_transport_families.py
python3 experiments/transport_followup/analyze_linked_fields.py --verify
```

The verifier independently reconstructs the transposition, checks every
source map and possible-letter domain, repeats every alignment comparison,
and verifies explicit ciphertexts attaining the stated edit totals.
