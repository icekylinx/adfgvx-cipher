# An archival counterpart to the Mackensen internment letter

**Document comparison: icekylinx and GPT-6 Astra Pro.**

Document 96 in Gerhard Engel, Bärbel Holtz and Ingo Materna, eds.,
*Groß-Berliner Arbeiter- und Soldatenräte in der Revolution 1918/19*
(Akademie Verlag, 1993), pp461–462, preserves a typescript carbon copy
of the letter transmitted in Childs's p226 C / p227 A. Its address,
internment argument, reassurance and closing council match the four-part
radio message. The edition gives a **28 November** dateline and records
**29 November** dispatch; Childs's originating line is `2200 (11/29)`.
[Publisher and DOI](https://doi.org/10.1515/9783050068831.400) ·
[Consulted transcription](https://dokumen.pub/gro-berliner-arbeiter-und-soldatenrte-in-der-revolution-1918-19-dokumente-der-vollversammlungen-und-des-vollzugsrates-vom-ausbruch-der-revolution-bis-zum-1-reichsrtekongre-reprint-2014nbsped-9783050068831-9783050022475.html).

## Archival signatures and parallel wording

<a id="what-the-second-witness-establishes"></a>

The copy signs **Molkenbuhr** and **Richard Müller**. This provides independent
documentary support for the previously proposed `SOLKENBUHR→MOLKENBUHR`
and `MNELLER→MUELLER` repairs. Each costs one observed coordinate in the
392-slot fourth part. Richard is supplied by the archival witness; the
ciphertext carries only the surname.

| Passage | Childs decryption / earlier edition | Archival counterpart |
| --- | --- | --- |
| First part's damaged noun | `SMUTIONEN`, 9 positions; earlier publication `SITUATIONEN`, 11 | `Faktoren`, 8 letters |
| Armistice term | Edited `WAFFENSTILLSTANDES` | `Waffenstillstandsvertrages` |
| Closing hope | Edited `EUCH ALLERECHTBALD` | The copy omits the extra *recht* |
| Signatures | Raw `SOLKENBUHR / MNELLER` | `Molkenbuhr / Richard Müller` |

The witnesses therefore preserve related versions. The archived noun does
not fit the nine received positions, and the existing two-coordinate
`STATIONEN` proposal remains a cipher-side alternative. No body word or
source length is changed to match the copy. The new contribution is the
independent signature support and the documented differences; the earlier
13-substitution full edition already existed.

The accessed source is the edition's transcription. The original carbon
copy and the images of these two printed pages have not been inspected.
Its OCR shelfmark is retained in the input notes without normalization.

## Reproduce the source comparison

```sh
python experiments/mackensen_archival_comparison/verify.py --verify
```

The verifier re-decrypts the native fourth part, reconstructs its column
positions independently, prices the two surname changes, and checks the
existing 12- and 13-substitution editions. It also audits the three noun
lengths and the case's signature table. Source images and earlier
certificates are reused.
