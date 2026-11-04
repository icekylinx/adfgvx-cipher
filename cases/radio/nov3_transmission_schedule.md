# November 3 radio transmission schedule: surviving second part

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Prepared by **icekylinx and GPT-6 Astra Pro**.

Childs p110 A explicitly labels this as part 2 of a two-part message:
OSM v LP, received at 3.52 p.m. on November 3, origin `1605 (3/11)`.
Only this second part is identified here. The first part is not supplied.
The published Nov1–3 square and column order are unchanged.

## Source reading

### p110 A2

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
1000BIS1200X1545BIS1645X2100BIS2230XXOSMXSENDET0200BIS0330X0430BCS0530X0900BIS0X45X1900BIS0025X2230BIS2300XXRINGBAHNVERKERAENDERTSICHNICHPXX
```

**Edited output:**

```text
1000BIS1200X1545BIS1645X2100BIS2230XXOSMXSENDET0200BIS0330X0430BIS0530X0900BIS0X45X1900BIS0025X2230BIS2300XXRINGBAHNVERKERAENDERTSICHNICHTXX
```

</details>

Cost: **2 observed-coordinate substitutions** and **0 source-mask fills**. Source length and transposition are unchanged.

The fragment lists transmission intervals, then says that the Ringbahn
traffic does not change. Only `BCS`→`BIS` and `NICHP`→`NICHT` are repaired.
The awkward raw `VERKER` is retained; the missing letters needed for the
modern spelling `VERKEHR` are not inserted.

All time-like fields remain as received, including `0900BIS0X45` and
`1900BIS0025`. The X in the first field is a decoded symbol, not an unknown
placeholder. No replacement hour, date rollover or time zone is inferred.
The earlier OCR screen already gave a largely readable schedule; this is
an exact source edition and repair ledger, not a first-decipherment claim.

## Notation and evidence

The fixed-width strings preserve every plaintext position. `?` means one
unresolved position, `X` is a literal decoded symbol that may serve as a
separator, and digits retain the published square's labels. Word spacing,
calendar values and numerical identities are not silently inferred. A source
mask fill is separate from a change to an observed ADFGVX coordinate.

[Source rows and image metadata](../../experiments/nov3_radio_and_pioneer/inputs.json),
[coordinate and domain certificate](../../experiments/nov3_radio_and_pioneer/certificates.json),
and [method, prior credit and reproduction](../../experiments/nov3_radio_and_pioneer/README.md).
