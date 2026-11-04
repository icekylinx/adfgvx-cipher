# Conditional Constantza station-shutdown notice

The message reports that the Constantza station has been taken out of operation. The transmitted shutdown time remains incomplete.

**Complete edition by printed page:** [p. 112](../pages/112.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


**Status:** a readable conditional edition of p112 C. The enlarged
[source](../../experiments/nov3_evening_and_nov4_radio/sources/p112_C_detail.png) · [Reading conventions](../../docs/reading-conventions.md)
clearly advertises 122 coordinates but contains only 110. Its two short
groups are `DVAX` and `AGFF`. A source-preserving 122-slot model adds twelve
unprinted coordinates; their values are not an observed continuation.

The selected frame adds ten coordinates before the visible stream, one
after DVAX and one inside AGFF. No printed marker independently proves
the missing prefix. All **161,025 parameter configurations** in the declared short-group
and two-five-block family are evaluated. They represent **155,400 distinct
source-origin layouts**, with 5,625 duplicate configurations where inserted
positions coalesce. Against the displayed candidate,
this is the only one-cost layout in that family. Allowing twelve arbitrary
missing coordinates gives **eight** equally cheap layouts, all retained.
A minimum for one chosen text does not prove unique wording or loss history.

## p112 C

The header is OUI v OSM, received at 5.59 p.m. on November 4, origin (4) 1700. The readable passage follows the priced edited stream, including its loss assumptions. The literal spelling CONSTANTZA and abbreviation NACHRCHEF are retained in the readable display.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 122-slot loss frame:**

```text
NAC?RCWE?XCO?STA?TZA?EITH?UTE?400AUSS?RB?TRI?B?ESETZTX?ILMISS
```

**Edited output — priced editorial candidate under the same stated frame:**

```text
NACHRCHEFXCONSTANTZASEITHEUTE?400AUSSERBETRIEBGESETZTXMILMISS
```

</details>

**Readable German — based on the edited candidate above; the local qualifications remain in force:**

> Nachrchef. Constantza seit heute ?400 außer Betrieb gesetzt. Milmiss.

The candidate uses **1 observed-coordinate substitution**, **0 source-mask fills** and **11 unprinted-coordinate fills**. Its remaining zero-based plaintext-position domains are `29: 0578CX`. These are literal square labels, without an additional historical numeral assignment.

The unknown position in `?400` has exact domain **0578CX**. Even under a
separate decimal-only assumption, it permits four values; no specific hour
is selected. The quoted time-like field keeps one question mark.

The [complete optional language screen](../../experiments/nov3_evening_and_nov4_radio/language_screen.json)
ranks every declared parameter configuration without a known plaintext. Its fresh synthetic
controls and failed 112-slot diagnostic frames remain separate from the
fixed-candidate cost proof. A high language rank is a lead, not an independent
source witness.


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
