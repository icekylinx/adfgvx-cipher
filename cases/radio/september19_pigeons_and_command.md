# September 19: pigeons and Army Group East command arrangements

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[Case index](../README.md) · [ADFGVX Cipher](../../README.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

These three native ciphertext bodies occupy the first page of Appendix B, printed p56 (PDF page 59). The earlier OCR retrieval pool began at p57 and omitted this entire page. The edition restores a pigeon-transfer record and the two printed parts about Army Group East and radio subordination.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## Source and accounting

[Original Childs PDF](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed page excerpt — source-PDF reference](../../experiments/september19_pigeons_and_command/inputs.json) · [Literal inputs](../../experiments/september19_pigeons_and_command/inputs.json) · [Exact certificates](../../experiments/september19_pigeons_and_command/certificates.json)

The unchanged published Sep19-21 key is used throughout. The page heading is September 19, 1918; the intercept headers are September 20. A fixed output label is not a historical numeral assignment. The header advertises 2 TLE for A, but only one section-A ciphertext body is printed; missing text is not counted as another source.

| Record | Native slots | Fixed raw labels | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p56_A](#p56-a) | 222 | 109 / 111 | 0 | 2 |
| [p56_B1](#p56-b1) | 168 | 83 / 84 | 1 | 1 |
| [p56_B2](#p56-b2) | 152 | 76 / 76 | 0 | 0 |

## p56 A

Literal header: `A) OSM v LP (02.00 p.m., September 20th); 1250 (19.9) FUER USK - UND - 1809 2 TLE; RICHI-222`.

**Source transcription — all printed slots in their original order:**

```text
DXFFX XGVDV DDFAA GAFFG XGXVX GFGFG AAGFV GGGGF
VGDDG FGFFF DXVFD AFDDX VDAFG AAGFA GAVGG GGFXA
FXGAV FGXFX XDDFF XDFXX XXAXX FGGVG AXGXA FAFDX
FXGFF GDDFA GVXFX FDFFF XXGGG XGXGV AXAVX GAXGG
XDXFF DFXDV XADFF XADDG DVVVX VFXGF XFDAF GADFG
AWTDF DFXDF FFXVD DVDDA XF
```

**Raw output — native frame and unchanged key:**

```text
AKONAC?22XZUDORTROEM3NR8S86VERSANDZIELANINACHDRAHTENDIE150AUSGESUCHTETAUBENUEBERWEISENWIRDXNACHRXCHE?RM4D84760X
```

**Edited output — 0 observed substitutions and 2 source-mask fills:**

```text
AKONACH22XZUDORTROEM3NR8S86VERSANDZIELANINACHDRAHTENDIE150AUSGESUCHTETAUBENUEBERWEISENWIRDXNACHRXCHEFRM4D84760X
```

**Readable German — spacing and punctuation of the same nonseparator labels:**

> AKONACH 22. Zu dort ROEM3 Nr. 8S86: Versandziel ANI nachdrahten. Die 150 ausgesuchte Tauben ueberweisen WIRD. Nachr. Chef RM4D84760.

**Meaning:** The record concerns a telegraphed dispatch destination and the transfer of pigeons. Its literal 150, ANI, ROEM3, 8S86 and final WIRD remain uninterpreted where the syntax or reference is uncertain; no omitted letter or historical number is silently supplied.

### Evidence limits

- The printed invalid symbols W and T in AWTDF are retained literally and masked independently for decoding. Their proposed V and F values complete AKONACH and CHEF at two source-mask fills, with no observed-coordinate substitution.
- ROEM3, 8S86, ANI, 150, WIRD and RM4D84760 remain exactly as decoded; their presence does not prove a historical numeral or repair the awkward pigeon-transfer syntax.
- The header advertises 2 TLE but only one section-A ciphertext body is printed on this page. No absent second body is invented or counted.

## p56 B1

Literal header: `B) OSM v LP (02.02 p.m., September 20th); 1800 (19.9) FUER OSM 2 TLE; 1 TL; RICHI-168`.

**Source transcription — all printed slots in their original order:**

```text
DAXFF DDGDD FFVGG ACXXV FFDDD AFFFF XGDXF XFXDV
XAFFF DXXXD DDXAA GVXDD XXDDG GADFD VADXF XVXAF
AFGFX GVXVF FFGGX XGGDF VXFXG GGGXG GGAFX DXAGX
AXFXA AGGGD GAFXA VGVVF VDGDX DFXXG GGDFX AFFGX
XXDAF VXG
```

**Raw output — native frame and unchanged key:**

```text
AKONA?H70XZURM1NR22750VX6X9X18XHGRXOSTWIRD6EMNAECHSTEIGENENDEUTSCHENAKONACHERHALTENX
```

**Edited output — 1 observed substitutions and 1 source-mask fills:**

```text
AKONACH70XZURM1NR22750VX6X9X18XHGRXOSTWIRDDEMNAECHSTEIGENENDEUTSCHENAKONACHERHALTENX
```

**Readable German — spacing and punctuation of the same nonseparator labels:**

> AKONACH 70. Zu RM1 Nr. 22750 V. 6.9.18. Hgr. Ost wird demnaechst eigenen deutschen AKONACH erhalten.

**Meaning:** Reports that Army Group East will shortly receive its own German AKONACH. The raw reference fields and abbreviation remain literal.

### Evidence limits

- The second glyph in group 4, ACXXV, is C-like and is retained as invalid C/masked. A faint or defective G cannot be ruled out, so the complete AGXXV source variant is retained separately. The word AKONACH does not determine the source glyph.
- Under the conservative C-like transcription, choosing G costs one source-mask fill. The distinct F-to-A change at source index 164 repairs 6EMNAECHST to DEMNAECHST at one observed-coordinate substitution.
- The closing AKONACH is unedited and supplies an internal vocabulary witness for the damaged opening.

## p56 B2

Literal header: `B) OSM v LP (02.02 p.m., September 20th); 1800 (19.9) FUER OSM 2 TLE; 2 TL; RICHI-152`.

**Source transcription — all printed slots in their original order:**

```text
XVXFF DDAGG GVDGG DGFGG AGAXG GFAXG DDAFF FVVDX
DFXGF FAGVG GDDAX XGFXF XAFFF VFXAG FGGXG XFFDX
FAFFX FGGGF DAVFD XXFDG GGAGG XXDXX DGFAV XFDDX
FXDGG GGFXX GVGFX XGVGX FXGFD DXDFD XX
```

**Raw output — native frame and unchanged key:**

```text
HIERAUFNEUREGELUNGDESUNTERSTELLUNGSVERHAELTNISSESFUNKA151XNACHRXCHEF1B16020X
```

**Edited output — 0 observed substitutions and 0 source-mask fills:**

```text
HIERAUFNEUREGELUNGDESUNTERSTELLUNGSVERHAELTNISSESFUNKA151XNACHRXCHEF1B16020X
```

**Readable German — spacing and punctuation of the same nonseparator labels:**

> Hierauf Neuregelung des Unterstellungsverhaeltnisses Funk A151. Nachr. Chef 1B16020.

**Meaning:** The second printed part announces a resulting reorganization of the radio unit or service named by the literal Funk A151 label. The certificate does not turn that label into a separately identified historical formation.

### Evidence limits

- The entire 152-slot body decodes without any mask, substitution, insertion, deletion or reordering.
- This is the explicitly printed second part of section B; the literal A151 and 1B16020 fields remain unassigned.

## Verification and credit

```sh
python experiments/september19_pigeons_and_command/verify.py --verify
python experiments/september19_pigeons_and_command/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier retains every native source slot, recomputes all coordinate pairs and repair costs, binds the complete readable displays, and checks re-encryption. The optional PDF check reproduces the exact crop pixels. The alternative G glyph is an evidence alternative, not another source record.

Historical Sep19-21 key: Childs, printed p236; published key and cryptanalytic work: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Source transcription, edition and explicit repair accounting: icekylinx and GPT-6 Astra Pro. This source edition makes no universal first-decipherment claim.
