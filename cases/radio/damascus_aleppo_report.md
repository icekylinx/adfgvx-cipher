# Damascus radio station and a smaller transmitter at Aleppo

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs printed p64 B, PDF p67, preserves a short report addressed to
the communications chief. It says that the Damascus radio station
was blown up and mentions a smaller transmitter at Aleppo. The
receiving header is `LP v OSM (12.49 a.m., October 4th)`, followed by
`(4) 1130`. Those two header times remain unchanged; this fragment
does not establish a consistent sending and receiving chronology.

## p64 B

The [source crop](../../experiments/p64_oil_and_radio/sources/p64_B.png)
has **176 slots**, including one printed dash, matching `RICHI-176`.
It uses the unchanged published **Oct4–6** key.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 176-coordinate frame:**

```text
NACHRCHEFXRADIODAMASKUSAM1X10X?600UHRGESPRENBTXKLEINERSENDERINALEPPOXAKONACH70XNRX30056X
```

**Edited output — one observed-coordinate substitution, with the printed
dash still unfilled:**

```text
NACHRCHEFXRADIODAMASKUSAM1X10X?600UHRGESPRENGTXKLEINERSENDERINALEPPOXAKONACH70XNRX30056X
```

</details>

**Readable German — spacing and punctuation of that candidate:**

> Nachr. Chef: Radio Damaskus am 1.10. ?600 Uhr gesprengt. Kleiner Sender
> in Aleppo. Ako Nach 70. Nr. 30056.

The single word repair changes source coordinate **28 G→X**, producing
`GESPRENGT`. The code-like `AKONACH70` and reference `30056` are retained,
without a new office or unit identification. The events are statements
in this historical report, not independently verified findings.

## Conditional interpretation of the hour

The unknown in **`?600UHR`** is plaintext position **30**. It is pair
**F?**, using observed source coordinate **82** and the printed dash
at source **162**. Under the published square, its full domain is
**1EKLOS**. All six coordinate completions are preserved and re-encrypt
exactly with the one stated word repair.

**If the unknown is required to be a decimal digit**, the domain contains
only **1**, producing **1600UHR**. This is an explicit field-type
interpretation and requires one additional source-mask fill. It is
kept separate from the raw and edited streams above and from their
counts. The baseline still fixes **87 / 88** plaintext positions.

## Source and attribution limits

This one physical record has **176 source slots**, **175 valid
coordinates**, and **88 plaintext positions**. Its price is one
observed-coordinate substitution, with no source-mask fill, insertion,
deletion or key change in the main edition.

The body already appeared in an earlier unreviewed repository screen.
A bounded search found no explicit separate Damascus/Aleppo discussion
in the paper, thesis or cached 2017 comments; that absence does not
establish historical priority. The published period key remains credited
to the earlier key recoverers, and the adjacent oil inquiry has its
own explicit prior publication.

[Inputs](../../experiments/p64_oil_and_radio/inputs.json),
[certificates](../../experiments/p64_oil_and_radio/certificates.json)
and [reproduction instructions](../../experiments/p64_oil_and_radio/README.md)
retain the source rows, exact inverse, domains and all six hour witnesses.
