# Eilvese/OUI: transmission arrangements and provisional traffic times

The telegram sets out sending and receiving arrangements for Eilvese/OUI and provisional transmitting windows. It uses the technical terms *ungedaempft* and *toenend*. The stated numerical fields and windows are reported as transmitted labels; the edition does not independently authenticate their numerical assignments, add a wavelength unit or a time zone, or establish that the schedule was implemented.

**Complete edition by printed page:** [p. 113](../pages/113.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p113 section D, part 1, gives transmission and reception arrangements
for **Eilvese/OUI**, followed by provisional transmitting windows. A repeated
source group and its adjacent damaged group create a length conflict:
**362 printed slots** appear under **RIZI-352**. An explicitly conditional
exclusion of ten slots produces a complete **176-position raw reading**
under the unchanged published **Nov1–3** key.

Two ordinary-word repairs, **UNGEDAENPFT→UNGEDAEMPFT** and **BIX→BIS**, cost
**3 observed-coordinate substitutions**. The primary frame needs **no
coordinate fills**. It excludes **7 observed coordinates and 3 printed
dashes**, counted separately from those three word-repair substitutions.
All equally priced frame alternatives are retained. Numerical labels,
including the unusual **3X13**, remain literal.


**Reviewed source crops:** [p113_D1_reviewed.png](../../experiments/nov3_eilvese_traffic_schedule/sources/p113_D1_reviewed.png) · [p113_D1_repetition_detail.png](../../experiments/nov3_eilvese_traffic_schedule/sources/p113_D1_repetition_detail.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## p113 D1

[Complete reviewed source — source-PDF reference](../../experiments/nov3_eilvese_traffic_schedule/inputs.json)
and [repeated-group detail — source-PDF reference](../../experiments/nov3_eilvese_traffic_schedule/inputs.json).

<details>
<summary>Literal source transcription</summary>

**Source transcription — header:**

```text
Page heading: 3rd NOVEMBER, 1918.
D) NKJ (UKS) v LP (3 p.m., November 3rd)
0605 (3/11) 2 TLE
1 TL RIZI-352
```

</details>

The page announces two parts. This edition recovers only the printed first
part and does not attach an unrelated nearby telegram as its continuation.
The cipher field is literally **RIZI**, retained as printed.

### Native source, before any exclusion

The [literal transcription](../../experiments/nov3_eilvese_traffic_schedule/inputs.json)
has **362 slots**, of which **359 are valid coordinates** and three are
printed dashes. In row 5, the source prints **FAGVD DG--- FAGVD**, at indices
175–189. All three groups remain in the source record, along with the final
`AV` that the earlier OCR omitted.

<details>
<summary>Raw decoded text</summary>

**Raw output — native 362-slot frame; 178/181 fixed positions:**

```text
5DDVOQH855BS4KMW9LP08MP5BF6ENJA2P9S070OXIVGAU1O028PQVI8987C8X5RKBG57QU7H3RDPJFRS1EC57E3PBOFG8WNP1Q1IA?WLNBBCC2R?EZDJARQN?JK65TI83R2VX240D9VD9OM9N9LNYWJE2ODX6I3MPJOH1ARTS7XVC0OAM2UPM
```

</details>

The native output is retained as evidence of the frame conflict; it is not
the readable message below. The printed length difference motivates a
bounded ten-slot comparison, but does not by itself prove a deletion.

### Declared 352-slot frame

The primary frame excludes **source indices 175–184 inclusive**: the first
`FAGVD` and the adjacent `DG---`. It retains the second `FAGVD`, all other
source positions and their order. The scan has no cancellation mark through
the excluded groups, so this remains an editorial frame hypothesis.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional ten-slot exclusion; 176/176 fixed positions:**

```text
EILVESEXOUIXSENDETABX3X13X12XNACHTSXUNGEDAENPFTANSIEMITWELLE9500XOUIEMPFAENGTSIEWELLEX4250XTOENENDXXVORLAUFIGEVERKEHRSZEITENXXOUIXSENDET12NACHTSBIX0100X0330BIS0345X0530BIS0600X
```

**Edited output — the same conditional frame; 3 observed-coordinate substitutions and no fills; 176/176 fixed positions:**

```text
EILVESEXOUIXSENDETABX3X13X12XNACHTSXUNGEDAEMPFTANSIEMITWELLE9500XOUIEMPFAENGTSIEWELLEX4250XTOENENDXXVORLAUFIGEVERKEHRSZEITENXXOUIXSENDET12NACHTSBIS0100X0330BIS0345X0530BIS0600X
```

</details>

**Readable German — complete conditional edited stream, with literal labels and spelling retained:**

> Eilvese. OUI sendet ab 3X13, 12 nachts, ungedaempft an Sie mit Welle 9500. OUI empfaengt Sie Welle 4250, toenend. Vorlaufige Verkehrszeiten: OUI sendet 12 nachts bis 0100, 0330 bis 0345, 0530 bis 0600.

**Meaning:** The telegram sets out sending and receiving arrangements for
Eilvese/OUI and provisional transmitting windows. It uses the technical
terms *ungedaempft* and *toenend*. The stated numerical fields and windows
are reported as transmitted labels; the edition does not independently
authenticate their numerical assignments, add a wavelength unit or a time
zone, or establish that the schedule was implemented.

The field **3X13** is not converted into a plausible date. **Vorlaufige**
keeps the source's encoded spelling without silently adding E or changing
it into an umlauted form. All values **9500**, **4250**, **12**, **0100**,
**0330**, **0345**, **0530** and **0600** remain unchanged.

## Coordinate costs and complete frame alternatives

The word repairs affect two plaintext positions but three observed
coordinates:

| Original source index | Model index after exclusion | Observed-coordinate change |
| ---: | ---: | --- |
| 4 | 4 | G→D |
| 321 | 311 | X→V |
| 348 | 338 | G→V |

The certificate maps each changed pair to its raw and proposed plaintext
letter. It fully re-encrypts the complete 176-position candidate. This
checks the explicit proposal and its source price; it does not turn the
exclusion hypothesis into a visible historical correction.

### Every consecutive ten-slot exclusion

All **353** possible consecutive ten-slot exclusions are compared against
the fixed complete candidate. The minimum is **3 observed-coordinate
substitutions**, attained by starts **172–185 inclusive**. These frames
have different additional source-mask-fill and exclusion costs:

| Exclusion start | Retained source masks that must be filled | Observed coordinates excluded |
| --- | ---: | ---: |
| 172 or 185 | 3 | 10 |
| 173 or 184 | 2 | 9 |
| 174 or 183 | 1 | 8 |
| Any start from 175 through 182 | 0 | 7 |

All rows exclude ten source slots and require the same minimum observed
substitution count. The **eight no-fill starts 175–182** produce exactly
the same retained ciphertext and raw plaintext. Their source-to-model
mappings differ, so every alias remains in the certificate. The displayed
start 175 is the natural whole-group choice, not a uniquely determined
historical location.

### Every pair of complete five-slot groups

The verifier also compares all **2,556** ways to exclude two of the 72
complete five-slot groups, retaining the final two-character `AV` group.
Three pairs attain the same three-substitution minimum:

| Group starts in original source | Source-mask fills | Observed coordinates excluded |
| --- | ---: | ---: |
| 175 and 180 | 0 | 7 |
| 180 and 185 | 0 | 7 |
| 185 and 190 | 3 | 10 |

The first two remove `DG---` and one of the two copies of `FAGVD`; they
produce the same complete raw stream. The third remains a recorded minimum
of the observed-substitution objective, but retains all three dashes and
requires their values to be supplied. It is not silently discarded from
the comparison.

These are **fixed-candidate comparisons** within two stated families.
Arbitrary ten-position subsets and all other possible plaintexts have not
been exhausted. The repeated group, advertised length and strong body
reading support this reconstruction, while the absence of an explicit
cancellation keeps the frame conditional.

## Source restoration, attribution and reproduction

Earlier repository OCR supplied **355 slots**, omitting the visible
`DG---` group and final `AV` and masking several printed coordinates.
The reviewed 362-slot transcription restores those marks first; the later
ten-slot exclusion is a separate operation. The frozen old input and its
recomputed unchanged-key output remain available in
[prior candidates](../../experiments/nov3_eilvese_traffic_schedule/prior_candidates.json).

J. Rives Childs's scan is the historical source. Published period-key
recovery by George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker, Lasry's
2017 key list, and earlier repository work retain their credit. The current
work supplies a source edition, bounded frame comparisons and explicitly
priced word repairs. It asserts **no first-decipherment priority**.

[Inputs](../../experiments/nov3_eilvese_traffic_schedule/inputs.json),
[certificates](../../experiments/nov3_eilvese_traffic_schedule/certificates.json),
and [reproduction instructions](../../experiments/nov3_eilvese_traffic_schedule/README.md)
preserve the native reading, exact crops, every retained and excluded source
position, all minimum-frame aliases and full candidate re-encryption.

</details>
<!-- CASE-EDITION:END -->
