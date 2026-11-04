# Turkish armistice and the Dardanelles–Bosporus notice

The message reports that the Turkish armistice has opened the Dardanelles and Bosporus to the Entente. Its closing routing fields remain damaged.

**Complete edition by printed page:** [p. 112](../pages/112.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Status:** a native 230-slot source edition of p112 D, with six observed
coordinate substitutions, one printed-dash fill and one unresolved final
position. It describes the straits opening to the Entente after a Turkish
armistice. The raw closing fields are not turned into a guessed sender.

The source header reads POT v NKJ, received at 1.12 a.m. on November 5,
with routing `VE FÜR M G KDEUR OSMAN HRGR OST` and origin `1655 (4)`.
The existing Nov4–6 key is unchanged. The readable display adds spacing and punctuation but no extra grammatical
letters; its character mapping is checked against the priced edited stream.

## p112 D

The date-like 31X10 is a literal source label. The original grammatical form WAFFENSTILLSTAND has no added genitive ending. BVN, BEIBVG and 7OSPOLI remain as received, and the final unknown has domain 9EKVXZ.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native source frame:**

```text
INFOLGE31X10XABGESCHLOSSENENWAFF?NSTILLSTANDXTUERAEIXDARDANE9LXNXBOS6ORFSXDERENTENTE4EOEFFNETXXBVNXBEIBVGX7OSPOLIX?
```

**Edited output — priced editorial candidate under the same stated frame:**

```text
INFOLGE31X10XABGESCHLOSSENENWAFFENSTILLSTANDXTUERKEIXDARDANELLENXBOSPORUSXDERENTENTEGEOEFFNETXXBVNXBEIBVGX7OSPOLIX?
```

</details>

**Readable German — based on the edited candidate above; the local qualifications remain in force:**

> Infolge 31.10. abgeschlossenen Waffenstillstand Türkei, Dardanellen, Bosporus der Entente geöffnet. BVN BEIBVG 7OSPOLI ?.

The candidate uses **6 observed-coordinate substitutions**, **1 source-mask fill** and **0 unprinted-coordinate fills**. Its remaining zero-based plaintext-position domains are `114: 9EKVXZ`. These are literal square labels, without an additional historical numeral assignment.


## Evidence and reproduction

The [source package](../../experiments/nov3_evening_and_nov4_radio/README.md),
[literal inputs](../../experiments/nov3_evening_and_nov4_radio/inputs.json) and
[coordinate certificate](../../experiments/nov3_evening_and_nov4_radio/certificates.json)
retain source crops, exact domains, every operation and complete forward witnesses.
The published keys retain their Lasry–Niebel–Kopal–Wacker attribution. Earlier
OCR candidates are archived separately; no first historical decipherment is claimed.

```sh
python experiments/nov3_evening_and_nov4_radio/verify.py --verify
```

</details>
<!-- CASE-EDITION:END -->
