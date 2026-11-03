# Radio contact, operating times and an unavailable key

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

These four independent records describe a broken wire connection, timed
radio calls, an embassy receiving station and the local absence of an
`OSKACHI` key. They use unchanged previously published keys and complete
source frames. They are grouped by subject, not asserted to be one exchange.

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [collected intercepts](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [inputs](../../experiments/radio_contacts_and_keys/inputs.json) and
[certificates](../../experiments/radio_contacts_and_keys/certificates.json)
retain exact source rows, headers, key provenance, image hashes, raw readings
and all local repairs. Printed page numbers are three less than PDF page numbers.

## p100 C: direct contact while the wire is broken

The [source](../../experiments/radio_contacts_and_keys/sources/childs_p100_C.png)
is under a November 1 heading, with this November 2 reception line:

```text
C) UKS v ZÖN (2.03 a.m., November 2nd)
2235 (1) AN LP
RIZI-158
```

All 158 coordinates give 79 fixed plaintext labels under `Nov1-3`, without
any repair:

```text
WANNISTUNMITTELBARERVERKEHRMITEUCHXMUENCHENODERBRSLAUMEGLICHXDRAHTUNTERBROCHENX
```

The sender asks when direct communication with the recipient, Munich or
the place written `BRSLAU` will be possible, and says the wire connection
is interrupted. `BRSLAU` is naturally read as Breslau and `MEGLICH` as a
damaged spelling of *möglich*, but **both remain literal in the certificate**.
No missing plaintext letters are inserted. The separately printed
[p100 B](../military/budapest_wire_break.md) gives a longer wire-break report;
this does not by itself prove a single transmission or a specific route.

This is distinct from the [p100 challenge](../p100.md), whose earlier
Belgrade body remains credited to Armin.

## p137 D: the OSKACHI key is no longer here

The [source](../../experiments/radio_contacts_and_keys/sources/childs_p137_D.png)
has `RIZI-102`. Its upper sender initial is overprinted, so the header is
conservatively retained as:

```text
D) ?CO V OSM (1.55 November 5th,)
RIZI-102
NF NRO V OSM
```

The page heading is November 6. Neither it nor the footer is used to resolve
the unclear upper callsign or the time's missing a.m./p.m. designation.
The two dots after the final cipher group `AX` are punctuation; the footer
is outside the 102-coordinate body.

All 51 raw plaintext positions are fixed under `Nov4-6`:

```text
POTSAGENDA3SSCHLUESSELOSKACHIHIERNICHTMEHRVORHANDEN
```

One observed-coordinate substitution, source **79: G→X**, changes the `3`
inside `DA3S` to `S`:

```text
POTSAGENDASSSCHLUESSELOSKACHIHIERNICHTMEHRVORHANDEN
```

Readable German:

> POT sagen, dass Schlüssel OSKACHI hier nicht mehr vorhanden.

It asks that POT be told the `OSKACHI` key is no longer available here.
The key name itself is unchanged. The message does **not** say why it is
unavailable, identify a specific square or rank order, give its operating
period, or connect it to a separate challenge ciphertext. Its presence
inside a telegram decoded with `Nov4-6` does not make `OSKACHI` another name
for that transport key.

The raw numeral `3` remains visible in the original reading and numerical
ledger. Its local word repair does not reassign the square's digit `3`.

## p142 A: 0430 calling signal, then listen again at 0645

The [source](../../experiments/radio_contacts_and_keys/sources/childs_p142_A.png)
is headed November 6:

```text
A) NKJ ZÖN v LP (08.25 p.m., November 6th)
FUER ZÖN 1900 (6/11)
RIZI-128
```

All 128 coordinates and 64 plaintext labels are fixed under `Nov4-6`, with
no substitutions or fills:

```text
GEBENSIEX0430X10XMINXVVVXDANNIHREFKSPRUNDHOERENSIEUNSWIEDERX0645
```

The instruction is to send **10 minutes of `VVV` at 0430**, then the
recipient's radiograms (`FKSPR`), and listen again at **0645**. All three
numerical fields are literal published-square readings. No extra day or
time zone is inferred from the evening reception time.

## p150 A2: receiving station in the embassy

The [source](../../experiments/radio_contacts_and_keys/sources/childs_p150_A2.png)
explicitly labels this **part 2**. Its first part has not been attached or
reconstructed in this edition:

```text
A) LP v NKJ (8.55 p.m., November 7th)
PERA OSMAINE 6/11
FUER EILKESE ZU SS D (5) 2200
2 TL RICHI-180
UMGEHEND WEITERGEBEN
```

The page heading is November 6. The literal `OSMAINE` and `EILKESE` spellings
and the November 7 reception remain unchanged. The instruction separator
before `UMGEHEND WEITERGEBEN` is outside the ciphertext.

The 180-slot source contains one dash and gives 89 fixed labels out of 90
under `Nov4-6`:

```text
JEDOCHHOERTEMPEGSSTMTXINBOTSCHAFTAUFEUCHXNAMEXQZXXADT?SSENCHIFFRITENXINMLLENPERIDENANRUFEN
```

Six known-coordinate substitutions and one dash fill give:

```text
JEDOCHHOERTEMPFGSSTATXINBOTSCHAFTAUFEUCHXNAMEXQZXXADRESSENCHIFFRIRENXINALLENPERIDENANRUFEN
```

The receiving station (`EMPFGSSTAT`) in the embassy listens for the
recipient. The message supplies the literal name/separator field
`NAMEXQZXX`, asks for addresses to be enciphered, and says to call in every
period. **The precise name boundary within `QZXX` is left unresolved.**
`CHIFFRIREN` and `PERIDEN` remain literal spellings; no extra plaintext
letters are claimed. The opening `JEDOCH` is retained rather than inventing
the missing preceding clause.

Known-coordinate changes, all at zero-based source indices:
**23 X→V, 80 X→V, 86 F→A, 92 X→V, 150 A→V, 167 X→V**.
The separate printed-dash fill is **112 ?→A**. Two of those substitutions
jointly change one raw `E` to `F` in `EMPFGSSTAT`; the certificate does not
collapse their cost into a single coordinate repair.

## Verify and prior credit

```sh
python experiments/radio_contacts_and_keys/verify.py --verify
```

The independent standard-library verifier rebuilds every source witness,
checks raw domains and numerical fields, and prices substitutions separately
from source-dash fills. No source coordinate is inserted or removed and no
published square is changed. Re-encryption confirms this stated arithmetic,
not the unique history of a damaged word or the identities of station names.

The keys are prior work by **George Lasry, Ingo Niebel, Nils Kopal and Arno
Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also published in George Lasry's [2017-02-24 comment 4](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
Earlier unreviewed OCR-derived candidates existed. The bounded author-paper
check found no explicit examples of these bodies; it does not establish
universal first-decipherment priority.
