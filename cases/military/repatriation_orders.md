# Equipment disposal, Alpenkorps return, and Finland evacuation orders

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Seven source-reviewed physical records on Childs pp207–208 are now readable.** The clearest gain is the complete two-part Alpenkorps order: its first part was missing an entire row in the earlier OCR extraction, while its second part supplies a printed witness for five erased coordinates and one differing coordinate on p207. Two neighboring messages concern equipment and horses that cannot reach Germany, and the German force in Finland.

Prepared by **icekylinx and GPT-6 Astra Pro**. The published Nov16–18 key and the earlier OCR-derived candidates retain their separate prior credit. These are source editions under that published key; no claim of first historical decipherment is made.

## Evidence and costs

The page headings both say **18 November 1918**. All counts below use the manually transcribed printed rows. A fixed label means a letter or numeral fixed by the conservative published square. Its eight unfilled cells still have the domain `03456789`; no numeral assignment has been added.

| Printed record | Source slots | Raw fixed labels in the working frame | Editorial fixed labels | Explicit cost |
|---|---:|---:|---:|---|
| p207 A1 | 318, including 12 dashes | 146/159 | 159/159 | 7 coordinate substitutions; 12 dash fills |
| p207 A2 | **221**, heading 220 | 102/110, conditional | 102/110 | Exclude the final printed X before untransposition; no substitutions |
| p207 B | 228, including 5 dashes | 105/114 | 109/114 | 1 substitution and 5 fills, supplied by the p208 A2 witness |
| p207 C1 | 208 | 101/104 | 101/104 | 1 substitution |
| p207 C2 | 140 | 67/70 | 68/70 | 2 substitutions; the doubled A remains |
| p208 A1 | 246 | 123/123 | 123/123 | None |
| p208 A2 | 228 | 109/114 | 109/114 | None |

The complete diplomatic rows, raw readings, per-position domains, coordinate origins and repair ledgers are in the [inputs](../../experiments/repatriation_orders/inputs.json) and [certificates](../../experiments/repatriation_orders/certificates.json). Every printed coordinate, including the excluded final X of p207 A2, remains in those records.

## Alpenkorps return: p208 A1–A2 and the p207 B witness

The p208 header reads `ZO'N v LP (20.59 p.m., November 18th)`, `07.10 (18/11) 2 TLE`. Part 1 gives this unaltered 123-label reading:

**Raw output:**

```text
ANOBERKDOMACKENSENXXWENNVERHAELTNISSEESGESTATTENISTALPENKORPSSOANZUSETZENDASSPREUSSISCHEVERBAENDENACHSCHLESIENZURVERFUEGUNG
```

Part 2 continues, also without coordinate repairs:

**Raw output:**

```text
PREUSSXKMSXXBAYRXVERBAENDENACHBAYERNZURVERFUEGGDESBAYRXKMZUGEFUEHRTWERDENXXEMPFANGBESTAETIGENXXOHLXRM1AXX1?????OPX
```

With word spacing, the instruction is addressed to Oberkommando Mackensen. If conditions permit, the Alpenkorps is to be directed so that Prussian formations are sent to Silesia for the Prussian `K.M.`, and Bavarian formations to Bavaria for the Bavarian `K.M.`. Receipt is to be acknowledged. The abbreviation `VERFUEGG`, the office labels and the unresolved numerical reference are retained as deciphered.

The p207 B header instead reads `ZO'N v LP (20.10 p.m., November 18th)`, followed by a blank message-time field and `2 TLE`. Its single printed body has no explicit part number. It corresponds to p208 A2, rather than to the unrelated p207 A message above it.

Of p207 B's **223 observed coordinates, 222 agree** with the later printed witness. At source index 127, p207 has G and p208 has F; that distinction produces the raw `...WERDENXM...` versus `...WERDENXX...`. The five dashes at indices 165–169 are supplied as `ADAGX`. One of those fills restores a coordinate in an unresolved numeral cell: it does **not** assign that cell a digit. After these separately recorded changes, the entire 228-coordinate working witness is identical to the literal p208 A2 source. The agreement establishes a strong printed-copy relationship; it does not establish independent transmissions or intercepts.

## Equipment and horses: p207 A1–A2

The header reads `ZO'N v LP`, an unspecified reception time on November 18, and `13.00 (18/11) 2 TLE`. The first part's editorial reading is:

**Edited output:**

```text
ANXOKMXGERAETUNDPFERDEDIEWEDERDURCHMARSCHNOCHDURCHBAHNDEUTSCHLANDERREICHENKOENNENXFREIHAENDIGVERKAUFENXMOEGLICHSTVERHINDERNXDASSEIGENETRUPPEGANZENTBLOESSTWIRDX
```

This directs `OKM` to sell equipment and horses that can reach Germany neither by marching nor by rail, while preventing the German troops from being left entirely without them. The raw wording is already substantially legible, but this complete reading requires **seven observed-coordinate changes and twelve dash fills**. It is an explicitly repaired source edition.

The seven substitutions, at zero-based source indices, are `18 V→F`, `43 V→F`, `51 V→F`, `61 G→D`, `106 D→X`, `124 X→D` and `192 X→D`. The certificate lists each affected plaintext label and each independently priced dash fill.

The printed second part contains 44 complete five-coordinate groups followed by one extra X: **221 source slots against RICHI-220**. Excluding only that final X before untransposition yields:

**Raw output — conditional exclusion of the final observed X at source index 220:**

```text
GLEICHESERGEHTANXETRAXSUEDOSTXFECHXGRXHXQUXUNDKRIWEISOKMXNRX??1?X11X1?XANCHXKMXALLGMXKRDPXNRX2???X1?XGEHXANCHX
```

The opening says that the same instruction goes to the listed addressees. `ETRA SUEDOST`, `FECH`, `KRIWEISOKM`, `KRDP`, the `ANCH` tokens and all partly known references remain literal. In particular, `FECH` has not been silently reordered into a more familiar word.

The verifier prices all **221 possible single-coordinate exclusions** against this retrospective known-letter template, allowing the marked numeral positions to remain in any of the eight unfilled square cells. Excluding index 220 is the sole zero-substitution placement in that bounded comparison. That is conditional template evidence, not proof that the final X was historical padding or that all other damage mechanisms are impossible. The unmodified 221-slot reading and its unpaired coordinate are preserved alongside the conditional reading.

## Finland: p207 C1–C2

The header reads `KOW v LP (04.04 p.m., November 18th)`, `17.00 (18/11) FUER - H 2 TLE`. The message and reception time fields are retained without imposing a chronology.

Part 1, after the single substitution `32 F→G`, reads:

**Edited output:**

```text
ANDEUTSCHENGENERALINFINNLANDXXDORTIGEXNRXBXCX212XUNDXRMX1AXNRX???XBEURTEILENLAGEVERSCHIEDENXOHLXNIMMTANX
```

Part 2, after `66 V→A` and `67 G→A`, reads:

**Edited output:**

```text
BALDIGERABTRAANSPORTFUERNOETIGGEHALTENWIRDXOHLXRMX1AXNOX11?1?XGEHXOPXX
```

The German general in Finland is told that two cited reports assess the situation differently. OHL assumes that early removal or transport of the force is considered necessary. The body contains the literal doubled A in `ABTRAANSPORT`; it has not been deleted. The references `B.C.212`, `RM.1A`, `11?1?`, and the other partly known number remain unexpanded.

The raw beginning of part 2 is `BALDIGLRABTRAAN?PORT`. The unknown label inside the word has the numeral domain `03456789` under the published square. Producing S requires the stated observed-coordinate substitution into the existing S cell. It is a word repair, **not** a newly inferred square assignment. The two unresolved numeral labels later in the reference remain unknown.

## Reproduction and credit

Run the [standalone verifier](../../experiments/repatriation_orders/verify.py):

```bash
python experiments/repatriation_orders/verify.py --verify
python experiments/repatriation_orders/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The default check needs only the Python standard library. The optional PDF check uses PyMuPDF to verify the exact scan hash and all nine saved source-image pixel hashes. The [experiment README](../../experiments/repatriation_orders/README.md) gives the finite scope and provenance. The seven earlier OCR candidates are retained in [prior evidence](../../experiments/repatriation_orders/prior_evidence.json), including their omitted rows, damaged group lengths and partial earlier readings. George Lasry's published key, Childs's source, and the research of Lasry, Niebel, Kopal and Wacker remain credited separately from this source-edition work.
