# Destroy written material and report by telephone

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p177 A orders destruction of written material, while retaining the
necessary cipher-key material, and asks for a telephone report of completion.
The source has an ordinary **186-coordinate** frame. Two observed-coordinate
substitutions give a readable 93-character body under the unchanged partial
`Nov10-12` key. No erased coordinate or unknown square cell is filled.

## Source and literal reading

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p177, PDF p180](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [source crop](../../experiments/november_radio_service/sources/childs_p177_A.png)
retains both the page heading and reception line:

```text
11th NOVEMBER, 1918.
A) MSX v MUA (11.50 a.m., November 10th)
1220
RIZI-186
```

The heading's November 11 and reception line's November 10 are preserved
without resolving the chronology. No historical identities are assigned to
MSX or MUA from the document-destruction wording alone.

All 186 source coordinates are valid. The conservative published square fixes
92 of 93 raw positions:

```text
ALLESCHRIFTSTUECKEBISAUFNOTWENDIGESSCHLUESSELMATERIALVERNICHTENXME?DUNGGESLHEHENENTELEFONISCH
```

The `?` comes from an **unassigned square cell**, not an unreadable source
coordinate. Its available labels are `56789` under the conservative partial
key. Assigning that cell the letter `L` would violate the existing published
anchors; this edition does not do so.

## Proposed reading and exact repairs

Two received-coordinate substitutions instead move the affected pairs to
already known letter cells:

```text
ALLESCHRIFTSTUECKEBISAUFNOTWENDIGESSCHLUESSELMATERIALVERNICHTENXMELDUNGGESCHEHENENTELEFONISCH
```

Readable German, with an unencoded grammatical word explicitly bracketed:

> Alle Schriftstücke bis auf notwendiges Schlüsselmaterial vernichten.
> Meldung [des] Geschehenen telefonisch.

The instruction is to destroy written material except the necessary key
material, and report by telephone that it has been done. The bracketed
`des` only smooths the telegram's grammar; it is not claimed as recovered
ciphertext. No reason for the order is supplied in the body.

| Source index, zero-based | Printed group / position, one-based | Change |
| ---: | --- | --- |
| 31 | 7 / 2 | `X` → `G` |
| 32 | 7 / 3 | `G` → `V` |

The [certificate](../../experiments/november_radio_service/certificates.json)
maps each change to its plaintext position and includes the full re-encrypted
witness. The source still has 186 slots; no coordinate is inserted, removed
or reordered, and the partial square remains unchanged.

## Why the initial odd-length lead was rejected

An earlier OCR extraction contained 185 slots and nominated this record
during a screen for before-transposition phase errors. Manual inspection
finds **186 slots, exactly matching `RIZI-186`**. The odd length was an OCR
transcription problem. This source edition therefore uses the ordinary
frame and does not count p177 A as evidence for the conditional mechanism
seen in [p126 A5](../military/armistice_transit_planning.md#a5-conditional-recovery-of-the-odd-frame)
or [p132 B](p132_radio_service.md#b-repeat-the-fourth-period-telegram-in-the-fifth).

The [inputs](../../experiments/november_radio_service/inputs.json) preserve
the manual rows, exact header, source crops and both published key records
used by the combined source package. The period key is credited to
**George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**,
[DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
and George Lasry's [2017-02-24 key comment](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
Earlier unreviewed OCR candidates existed. No explicit p177 A body example
was located in the bounded author-paper check; that absence does not establish
first-decipherment priority.

```sh
python experiments/november_radio_service/verify.py --verify
```
