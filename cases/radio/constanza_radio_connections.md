# Constanza naval radio: telegram routing and exchange connections

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition: icekylinx and GPT-6 Astra Pro.** Childs p80 B1/B2 and p82 A1–A4, 30 October 1918; published `Oct28-31` key, unchanged. [Source inputs](../../experiments/constanza_radio_connections/inputs.json), [exact certificates](../../experiments/constanza_radio_connections/certificates.json), [method and limits](../../experiments/constanza_radio_connections/README.md).

The four-part message quotes the naval department at Constanza on telegram routing and telephone-exchange connections. Telegrams for foreign stations are said to travel over German lines to Bucharest or Braila. The naval radio station is described as directly connected to the local main exchange and also to the naval department's exchange, allowing communication with the main exchange and other telephone points.

The source describes these arrangements. It does not independently demonstrate that each link was operational. All original reference and date labels remain unchanged.

## p80 B1

[Source crop](../../experiments/constanza_radio_connections/sources/p80_B1.png). The source advertises and prints 242 coordinates. Raw, 121 positions:

**Raw output:**

```text
MARINEABTLGXCONSTANZAFUNKTUNTERNRX13558X13558X1XROEMX1VOM29X10XXAUFDORTXTELEGRXNRX351BRUCHSTRX18VOM25X10XXALLETELEGRXNAPH
```

Source index 94 `X → D`, independently witnessed by p82 A1, repairs the final `NAPH` to `NACH`. The raw reference `13558X13558X1XROEMX1` and the two date fields are retained, including the repeated number.

## p80 B2

[Source crop](../../experiments/constanza_radio_connections/sources/p80_B2.png). All 248 coordinates are observed. The **typed baseline** is:

**Raw output:**

```text
FR9MDLAENDISCHENSTATIONENWERDENUEBERDEUTSCHELEITGXPACHBUKARESTODERBRAILAABGESETZTXXDIEMARINEFUNKSTATXISTUNMITTELBARANHIESIGE
```

At source index 55, a visible supralinear F is printed above the typed G. Applying only that source annotation gives `FREMDLAENDISCHEN` and makes this ciphertext identical to the typed p82 A2 copy. The annotation's author and date are unknown.

Both copies still have `PACH`. A separate ordinary-word candidate, source index 142 `G → X`, produces the following reading:

**Edited output:**

```text
FREMDLAENDISCHENSTATIONENWERDENUEBERDEUTSCHELEITGXNACHBUKARESTODERBRAILAABGESETZTXXDIEMARINEFUNKSTATXISTUNMITTELBARANHIESIGE
```

## p82 A1

[Source crop](../../experiments/constanza_radio_connections/sources/p82_A1.png). The printed label is **RICHI-342**, but the source has **242 coordinates**. The independent p80 B1 copy advertises 242 and agrees at 241 coordinates. The edition uses the observed 242-coordinate frame, preserving the label discrepancy rather than inventing 100 missing coordinates. The raw text is already readable:

**Raw output:**

```text
MARINEABTLGXCONSTANZAFUNKTUNTERNRX13558X13558X1XROEMX1VOM29X10XXAUFDORTXTELEGRXNRX351BRUCHSTRX18VOM25X10XXALLETELEGRXNACH
```

## p82 A2

[Source crop](../../experiments/constanza_radio_connections/sources/p82_A2.png). All 248 source coordinates are observed:

**Raw output:**

```text
FREMDLAENDISCHENSTATIONENWERDENUEBERDEUTSCHELEITGXPACHBUKARESTODERBRAILAABGESETZTXXDIEMARINEFUNKSTATXISTUNMITTELBARANHIESIGE
```

Here `FREMD` is direct, while `PACH → NACH` requires the same separately priced one-coordinate repair as p80 B2, source index 142 `G → X`. The candidate equals the p80 B2 candidate above. The repetition of the error is explicitly preserved in both raw strings.

## p82 A3

[Source crop](../../experiments/constanza_radio_connections/sources/p82_A3.png). All 210 coordinates are observed. Raw, 105 positions:

**Raw output:**

```text
HAUPTVERMITTLGXUNDAUSSERDEMANVERMITTLGXDERMARXABTLGANG9SCHLOSSENUEBERDIESIEEBENFALLSMITDERHAUPTVERMITTLGX
```

Source index 64 `G → F` gives the ordinary-word candidate:

**Edited output:**

```text
HAUPTVERMITTLGXUNDAUSSERDEMANVERMITTLGXDERMARXABTLGANGESCHLOSSENUEBERDIESIEEBENFALLSMITDERHAUPTVERMITTLGX
```

The original 9 remains in the certificate; this local coordinate repair is not a global reassignment of that digit.

## p82 A4

[Source crop](../../experiments/constanza_radio_connections/sources/p82_A4.png). The 118 coordinates give 59 directly readable positions, without repair:

**Raw output:**

```text
UNDDARUEBERHINAUSMITALLENSPRECHSTELLENINVERKEHRTRETENKANNXX
```

## Assembly and attribution

The p82 source gives four explicitly numbered parts, and both page groups share origin `0730 (30) 4 TEILE`. p80 repeats the first two parts with one source-coordinate difference in each. The receipt times differ, `6.20 p.m.` on p80 and `6.10 p.m.` on p82; both are retained.

The complete four-part message has 409 plaintext positions. The p80 copies add 245 physically repeated positions to the edition. Correcting the earlier OCR boundary errors makes the first two parts readable; parts 3/4 already had substantially readable unreviewed candidates. This source edition provides exact provenance, comparisons and repairs, and makes no first historical decipherment claim.
