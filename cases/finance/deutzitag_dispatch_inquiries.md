# DEUTZITAG: requesting details of purchase dispatches

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition: icekylinx and GPT-6 Astra Pro.** Childs p80 A and p81 A/C, printed heading 30 October 1918, received 31 October. Published `Oct28-31` key, unchanged. [Inputs](../../experiments/deutzitag_dispatch_inquiries/inputs.json), [exact certificates](../../experiments/deutzitag_dispatch_inquiries/certificates.json), [method](../../experiments/deutzitag_dispatch_inquiries/README.md).

The economic department of the Caucasus delegation is asked whether purchases have already been sent away, when and where further dispatches are expected, and how onward transport is intended. The request itself supplies no shipment answer.

## p80 A

[Source crop](../../experiments/deutzitag_dispatch_inquiries/sources/p80_A.png). Receipt `COS v LP (6.36 a.m., October 31st)`; origin `SS BERLIN 30/10 ... 1900`; addressee `KAUKASUS DELEGATION WIRTSCHAFTSABTEILUNG`. All 274 printed coordinates give this unedited 137-character body:

**Raw output:**

```text
DRAHTETOBVONEURENKAEUFENBEREITSABTRANSPORTEERFOLGTSINDEVENTUELLWANNUNDWOHINSOLCHEERFOLGENWERDENUNDWIEWEITERTRANSPORTGEDACHTISTXXDEUTZITAG
```

Reading: “Drahtet, ob von euren Käufen bereits Abtransporte erfolgt sind, eventuell wann und wohin solche erfolgen werden und wie Weitertransport gedacht ist. Deutzitag.”

## p81 A

[Source crop](../../experiments/deutzitag_dispatch_inquiries/sources/p81_A.png); [overprinted source glyph](../../experiments/deutzitag_dispatch_inquiries/sources/p81_A_overprint.png). Receipt `NKJ v LP (6.45 a.m., October 31st)`; origin `FUER COS SS BERLIN 30/10 B V K M KAUKASUS 1172`. All 338 coordinates are observed:

**Raw output:**

```text
FUERXSAULXWEINREICHXDOPPELPUNKTXDRAHTETJBVONEURENKAEUFENBEREITSABTRANSPORTEERFOLGTSINDEVENTUELLWANNUNDWOHINSOLCHEERFOLGENWERDENUNDWIEWEITERTRANSPORTGEDACHTISTXXDEUTZITAG
```

The received prefix is “Für Saul Weinreich:”. No independent personal identity is assigned. Source index 248 `G → F` changes the ordinary word `JB` to `OB`; the resulting suffix equals the complete p80 A and p81 C bodies at every coordinate pair. The corrected full candidate is:

**Edited output:**

```text
FUERXSAULXWEINREICHXDOPPELPUNKTXDRAHTETOBVONEURENKAEUFENBEREITSABTRANSPORTEERFOLGTSINDEVENTUELLWANNUNDWOHINSOLCHEERFOLGENWERDENUNDWIEWEITERTRANSPORTGEDACHTISTXXDEUTZITAG
```

This is one local ciphertext repair. The published J label is not changed globally.

## p81 C

[Source crop](../../experiments/deutzitag_dispatch_inquiries/sources/p81_C.png). Receipt `NKJ v LP (6.36 a.m., October 31st)`; origin `FUER COS SS BERLIN 30/10 1900`; addressee `KAUKASUS DELEGATION WIRTSCHAFTSABTEILUNG`. All 274 coordinates are **identical to p80 A**, and decrypt without repair:

**Raw output:**

```text
DRAHTETOBVONEURENKAEUFENBEREITSABTRANSPORTEERFOLGTSINDEVENTUELLWANNUNDWOHINSOLCHEERFOLGENWERDENUNDWIEWEITERTRANSPORTGEDACHTISTXXDEUTZITAG
```

## Attribution and scope

Earlier unreviewed OCR-derived repository candidates already contained all three bodies. This edition adds source checking, independent physical witnesses, exact position comparisons and a costed repair. It makes no claim of first historical decipherment. The [adjacent pioneer-detachment order](../caucasus/tiflis_pioneer_detachment.md) is a separate military message.
