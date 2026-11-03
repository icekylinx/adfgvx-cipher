# The Caucasus K.M. representative is to remain

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

This p142 B telegram replies to an earlier message and says the `BEV K.M.`
representative in the Caucasus, at Tiflis, is to remain. The closing names
the `KRIEGSAMT KRIEGSROHSTOFFABTLG`. The abbreviated office `K.M.` is left
unexpanded; the closing alone is not used to assign it a different title.

## Source and reading

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p142, PDF p145](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [B crop](../../experiments/radio_contacts_and_keys/sources/childs_p142_B.png)
is under a November 6 heading:

**Source transcription — clear header and/or literal source record:**

```text
B) NKJ v LP (08.30 p.m., November 6th)
FUER COS EINMAL 1250 (6/11)
RICHI-286
```

All **286 coordinates** are visible and valid, matching the printed length.
The earlier 280-slot OCR extraction omitted source content and is not the
analysis frame. The unchanged published `Nov4-6` key fixes all 143 raw labels:

**Raw output:**

```text
FUERXBEVXKMXKAUKASUCXT9FLISXZU4TELEGRAMMVOMX29X10X18XPOTX44XNRX2331XBEVXKXMXSOLLBLEIBENXKRIEGSAMTKRIEGSROHSTOFFABTLGXNRXZXROEMX1XAX23X11X18XKRA
```

Three observed-coordinate substitutions give:

**Edited output:**

```text
FUERXBEVXKMXKAUKASUSXTIFLISXZUMTELEGRAMMVOMX29X10X18XPOTX44XNRX2331XBEVXKXMXSOLLBLEIBENXKRIEGSAMTKRIEGSROHSTOFFABTLGXNRXZXROEMX1XAX23X11X18XKRA
```

Readable core:

**Readable German:**

> Für Bev. K.M. Kaukasus, Tiflis. Zum Telegramm vom 29.10.18,
> POT 44, Nr. 2331. Bev. K.M. soll bleiben.

The source uses `BEVXKMX` in the address and `BEVXKXM` later; both exact
separator patterns remain in the encoded edition. The following reference
is retained verbatim and **not silently interpreted as a November date**:

**Raw output — unchanged reference-field excerpt:**

```text
KRIEGSAMTKRIEGSROHSTOFFABTLGXNRXZXROEMX1XAX23X11X18XKRA
```

| Source index, zero-based | Printed group / position, one-based | Change | Effect |
| ---: | --- | --- | --- |
| 52 | 11 / 3 | `F` → `V` | `T9FLIS` → `TIFLIS` |
| 53 | 11 / 4 | `V` → `F` | `ZU4TELEGRAMM` → `ZUMTELEGRAMM` |
| 171 | 35 / 2 | `D` → `G` | `KAUKASUC` → `KAUKASUS` |

The raw `9` and `4` within words are separately preserved in the numerical
ledger. Their local repairs do not reassign square digits. All actual date,
number and reference fields remain unchanged. There are no erasure fills,
coordinate insertions, deletions or square changes.

## Reproduce and prior credit

The [source inputs](../../experiments/radio_contacts_and_keys/inputs.json)
and [certificate](../../experiments/radio_contacts_and_keys/certificates.json)
retain raw domains, changes and the complete forward witness.

```sh
python experiments/radio_contacts_and_keys/verify.py --verify
```

The published key is credited to **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
Earlier unreviewed OCR-derived candidates existed. No universal first-reading
priority is asserted. The exact repaired witness establishes its stated
three-coordinate cost, not the identity of the representative or proof that
the instruction was carried out.
