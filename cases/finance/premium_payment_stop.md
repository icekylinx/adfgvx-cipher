# Order to stop premium payments and inform subordinate offices

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p78 A1/A2, PDF p81, are one source-labeled two-part message:
`NKJ FUER OSM v LP (12.54 p.m., October 31st)`;
`SSD BERLIN M GST 29/10 AN BVS BEIM BVG KOSPOLI`; `0940 2 TLE`.
The native lengths match every visible coordinate, and both parts decode
without repair under the unchanged published **Oct28–31** key.

## p78 A1

The [first part](../../experiments/premium_payment_stop/sources/p78_A1.png)
contains **240 valid coordinates** and **120 / 120 fixed plaintext positions**.

**Raw output — native 240-coordinate frame:**

```text
GEMAESSXFECHXROEMISCHXNEUNX52021STRICH2949XSINDMITABLAUFOKTOBER18SAEMTLICHEPRAEMIENZAHLUNGENAUSLANDESMITTELNEINZUSTELLEN
```

**Edited output — unchanged, with zero substitutions or fills:**

```text
GEMAESSXFECHXROEMISCHXNEUNX52021STRICH2949XSINDMITABLAUFOKTOBER18SAEMTLICHEPRAEMIENZAHLUNGENAUSLANDESMITTELNEINZUSTELLEN
```

**Readable German — spacing, punctuation and umlauts:**

> Gemäß FECH, römisch neun, 52021 Strich 2949, sind mit Ablauf Oktober 18
> sämtliche Prämienzahlungen aus Landesmitteln einzustellen.

The continuous sequence **AUSLANDESMITTELN** supports the displayed word
boundary “aus Landesmitteln.” It is not changed to “Auslandsmitteln.”
The display retains **Oktober 18** and the full reference as written;
no missing date digit or numerical label is supplied.

## p78 A2

The [second part](../../experiments/premium_payment_stop/sources/p78_A2.png)
contains **170 valid coordinates** and **85 / 85 fixed plaintext positions**.

**Raw output — native 170-coordinate frame:**

```text
ALLEDORTUNTERSTELLTENDIENSTSTELLENSOFORTBENACHRICHTIGENXXSCHIFFAHRTXROEMX4XAXNRX14380
```

**Edited output — unchanged, with zero substitutions or fills:**

```text
ALLEDORTUNTERSTELLTENDIENSTSTELLENSOFORTBENACHRICHTIGENXXSCHIFFAHRTXROEMX4XAXNRX14380
```

**Readable German — spacing and punctuation:**

> Alle dort unterstellten Dienststellen sofort benachrichtigen.
> Schiffahrt. Röm. 4. A. Nr. 14380.

“Schiffahrt” retains the decoded historical spelling. The closing
abbreviations and the label **4** remain literal.

## Conditional interpretation and scope

The two-part header and consecutive part labels establish this assembly.
Across both records, **410 visible coordinates** give **205 / 205 fixed
plaintext positions**. Both unchanged outputs re-encrypt exactly, with
zero source repairs or frame changes. The message gives instructions to
stop payments and notify offices; it does not show that either step was
carried out.

Both exact bodies were already present in earlier unreviewed repository
screens. The present contribution is visual source verification,
source-defined assembly and independent reproducibility, with published
key credit retained. It makes no historical first-solution claim. See
[inputs](../../experiments/premium_payment_stop/inputs.json),
[certificates](../../experiments/premium_payment_stop/certificates.json)
and [reproduction instructions](../../experiments/premium_payment_stop/README.md).
