# An enquiry about an MMD command or representative

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

A complete native short message asks whether a command or representative is present. MMD and the final reference remain literal. The proposed A in KOMMANDO costs an observed-coordinate change; the separate Y-like source glyph stays masked and unresolved.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p190 excerpt](../../experiments/mmd_command_whereabouts/sources/p190_reviewed.png) · [Inputs](../../experiments/mmd_command_whereabouts/inputs.json) · [Position and change certificates](../../experiments/mmd_command_whereabouts/certificates.json) · [Reading conventions](../../docs/reading-conventions.md)

The published `Nov13-15b` key is unchanged. [Original OCR records](../../experiments/mmd_command_whereabouts/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/mmd_command_whereabouts/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p190 C](#p190-c) | 126 | 59 / 63 | 1 | 0 |

## p190 C

**Source transcription — header:** `C) --- v --- (06.05 p.m., November 14th); FUER ASO RAT 13.41; RICHI-126`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
BEFINDETSICHDORTKOMM?NDOXXMMDXXODERVERTRETERXADMIRALSTAB15?6?D?
```

**Edited output — 1 observed-coordinate substitution and 0 source-mask fills; no insertion, deletion or reordering:**

```text
BEFINDETSICHDORTKOMMANDOXXMMDXXODERVERTRETERXADMIRALSTAB15?6?D?
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> Befindet sich dort Kommando MMD oder Vertreter. Admiralstab 15?6?D?.

**Meaning:** The message asks whether the command labeled MMD, or a representative, is present at the destination. It closes with Admiralstab and the unresolved reference 15?6?D?. The source does not expand MMD or identify the destination.

**Editorial limits.**

- The native source contains126 slots, including the final AAGFF G. The first-row fifth group has a Y-like or Y/V-uncertain third glyph, conservatively retained as FVYAG and masked at source 22.
- The raw KOMM?NDO unknown comes from the fully observed VG square cell, not from the Y-like source glyph. Its domain is {2,3,4,7,8,9,Q,Y}; proposing A therefore costs an observed G→V substitution at source 112. No unknown key cell is silently assigned A.
- The final reference has two fully observed unknown square cells GD and AD, and a final source-mask pair ?G. Their domains remain explicit; they are not forced into a numerical date or serial number.
- The single source mask remains unresolved. The final character domain is {2,3,4,6,7,8,9,B,G,P,Q,R,Y}, while the earlier two unknown cells range over {2,3,4,7,8,9,Q,Y}.
- The question is punctuated with a period in the exact reading so that ? continues to denote an unresolved plaintext position.

The final three unresolved labels also obey a joint constraint. GD and AD are distinct square cells. The source-mask pair ?G can select known B, P, R, 6 or G, or an unused label through VG; it cannot select GD or AD. Thus the three final labels must be mutually different, even though their marginal domains overlap.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/mmd_command_whereabouts/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
