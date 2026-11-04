# Delegates directed through Spa toward Berlin

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition: icekylinx and GPT-6 Astra Pro.**

**Prior body and historical discussion:** George Lasry, Ingo Niebel,
Nils Kopal and Arno Wacker, *Deciphering ADFGVX messages from the Eastern
Front of World War I* (2016), §6.4, author PDF p24,
[DOI](https://doi.org/10.1080/01611194.2016.1169461). That discussion
explicitly cites p175 A together with p172 C. This edition adds a
source-exact transcript and quantified repairs; it does not claim the
travel message as a new historical decipherment.

Childs printed p175 A, PDF p178, contains two parts under
`ZM v SY (10.57 p.m., November 10th); VE (10) 2 TLE`.
The text directs delegates by train or car to Spa, with onward travel
toward Berlin on the following date-like field. Its time remains
partly unknown. The two parts have native lengths **192** and **104**
coordinates and use the unchanged published **Nov10–12** key.

## p175 A1

The [source crop](../../experiments/nov10_delegates_and_field_report/sources/p175_A1.png)
directly decrypts to:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
HPTMXMANNITAED1XNAMUTXZUGLEICHFUERHPTMXVXWEIHERXEXIX2XXABGEORDNETEMITZUGODETAUTOSONACHSPALEITENX
```

</details>

Four observed-coordinate repairs give this readable candidate:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
HPTMXMANNSTAEDTXNAMURXZUGLEICHFUERHPTMXVXWEIHERXEXIX2XXABGEORDNETEMITZUGODERAUTOSONACHSPALEITENX
```

</details>

It addresses the officer named by the candidate `MANNSTAEDT` at Namur,
also for Captain von Weiher, and directs delegates by train or car to
Spa. The exact address field `EXIX2` is retained. This edition does not
independently identify either officer, expand the unit field or identify
the delegates as particular historical people.

The separate [Namur order witnesses](namur_order_witnesses.md) have
`HPTMANNSTAEDT` without this part's separator after `HPTM`. That string
can instead be segmented as a title followed by `STAEDT`. Their related
wording supports comparison, but does not establish a shared person
or make these messages exact retransmissions. The earlier source
reconciliation remains unchanged.

## p175 A2

The [second-part crop](../../experiments/nov10_delegates_and_field_report/sources/p175_A2.png)
directly reads:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DASSWEITERFAHRTNACHBERLINAM11X11X?X03XNACWMXOHLRM4BX
```

</details>

One observed-coordinate repair changes `NACWM` to `NACHM`:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
DASSWEITERFAHRTNACHBERLINAM11X11X?X03XNACHMXOHLRM4BX
```

</details>

The continuation gives onward travel to Berlin on `11X11` at
`?X03 NACHM`, followed by `OHLRM4B`. All these labels remain literal.
The unknown time digit has domain **56789** under the published partial
square. It is not a missing coordinate. Enumerating all **120** full
square completions gives five compatible literal time digits, each in
24 completions, with the exact same candidate ciphertext.

The earlier paper describes a Berlin arrival at 15:00. That historical
narrative is credited separately; the present source edition does not
borrow its time or change `03`, and the wording here concerns onward
travel rather than an independently verified arrival.

## Exact cost and evidence

The two parts contain **296 observed coordinates**, **148 plaintext
positions**, **147 fixed raw labels**, and the same 147 fixed labels
after repairs. They require **five observed-coordinate substitutions**,
with no fill, gap, deletion or key change. The unknown time remains
unknown; no increase in the fixed-label count is claimed for this pair.

[Inputs](../../experiments/nov10_delegates_and_field_report/inputs.json),
[certificates](../../experiments/nov10_delegates_and_field_report/certificates.json)
and the [reproduction instructions](../../experiments/nov10_delegates_and_field_report/README.md)
retain every literal row, source position, plaintext domain and edit.
Earlier unreviewed repository candidates are frozen separately.
