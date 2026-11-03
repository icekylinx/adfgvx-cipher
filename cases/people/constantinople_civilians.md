# German civilians in Constantinople: an enquiry and a diplomatic appeal

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

A four-part enquiry asks whether German civilians, principally women and
children, have departed from Constantinople, where they have gone and what
is known of them. It asks for verification through the Swedish legation
and for reports on troop transports. It then says that the request to
permit German civilians to remain in Turkey has been put before the
Allies and the Supreme War Council in Paris, and that transport through
Ukraine is currently impossible.

The headcount is preserved as the published square's literal labels
**`0YY`**. No conventional numerical value is assigned. The source treats
the departure as a report requiring confirmation; its occurrence is not
established by this enquiry.

The primary source is J. Rives Childs, *General Solution of the ADFGVX
Cipher System*, printed p221 B, PDF p224. The page heading is November 25,
1918; the message header reads `XYZ v LP (06.14 a.m., November 26th)`,
`1300 (25/11)`, `4 TLE`. The
[literal edition](../../experiments/constantinople_civilians/inputs.json)
and [exact certificates](../../experiments/constantinople_civilians/certificates.json)
retain all glyphs, source mappings, frame alternatives and coordinate
repairs. The published `Nov25-28` square and transposition are unchanged.

## B1: reports of civilians leaving Constantinople

The first part advertises 298 coordinates but prints **297**. The source
has a four-letter `ADDG` group at positions 225–228. Inserting an erased
coordinate at boundary 227 gives this 149-position raw reading:

**Raw output — conditional insertion at source boundary 227 in the short group:**

```text
ANDEUTSCHENGESCHAEFTSTRAEGERKONSTANTINOPELXHIERVORLIEGENMELDUNGENWONACH0YYDEUTSCHEZI?ILPERSONENHAUPTSAECHLICHXRAUENKINDERVONDORTHIERHERABGEREISTSINDX
```

One observed-coordinate change, `XRAUEN` to `FRAUEN`, and filling the
missing coordinate for `ZIVILPERSONEN` give:

**Edited output — same conditional insertion model, with the stated repair and fill:**

```text
ANDEUTSCHENGESCHAEFTSTRAEGERKONSTANTINOPELXHIERVORLIEGENMELDUNGENWONACH0YYDEUTSCHEZIVILPERSONENHAUPTSAECHLICHFRAUENKINDERVONDORTHIERHERABGEREISTSINDX
```

Addressed to the German chargé d'affaires at Constantinople, the text
says that reports received at the sender's end describe German civilians,
mainly women and children, departing from there toward the sender. The
reported number has the raw labels `0YY`.

The geometry is not selected to obtain that quantity. The certificate
checks all **298 insertion boundaries**, masking all three headcount
positions. Boundary **227** uniquely minimizes ordinary-word changes at
one observed substitution; the next-best boundaries require two. All
three headcount characters then come from complete, unchanged observed
coordinate pairs:

| Plaintext position | Pair | Original source indices | Raw label |
| --- | --- | --- | --- |
| 71 | `AF` | 123, 251 | `0` |
| 72 | `DG` | 6, 200 | `Y` |
| 73 | `DG` | 226, 84 | `Y` |

The earlier OCR-based fit `0Y5` depended on a different missing-coordinate
placement. The source-supported ordinary-word optimum gives `0YY`, with
its repeated final pair made explicit. The source edition supplies those
pairs, not their conventional numerical interpretation.

## B2: verification through the Swedish legation

This part advertises 344 coordinates and prints **345 slots**. Its
six-letter group `AXDGXF` occupies source positions 130–135. Removing
source index 134, the second `X`, gives:

**Raw output — conditional deletion of the second X at source index 134:**

```text
BITTEDURCHVERMITTELUNGSCHWEDISCHERGESANDTSCHAFTDRAHTENOBMELDUNGZUTREFFENDWANNUNDWOHINABREISEERFOLGTXW6SUEBERVERBLEIBBEKANNTISTUNDUMWELCHEKA?EGORIENNUNPERSONENESSICHHANDELTX
```

The question mark comes from the printed dash in `A-FGA`, source index
207. Four observed-coordinate substitutions and one erased-coordinate
fill produce:

**Edited output — same conditional deletion model, with the stated substitutions and dash fill:**

```text
BITTEDURCHVERMITTELUNGSCHWEDISCHERGESANDTSCHAFTDRAHTENOBMELDUNGZUTREFFENDWANNUNDWOHINABREISEERFOLGTXWASUEBERVERBLEIBBEKANNTISTUNDUMWELCHEKATEGORIENVONPERSONENESSICHHANDELTX
```

The sender asks for a telegraphic report through the Swedish legation:
is the report correct, when and to where did the departure occur, what is
known of the people's whereabouts, and which categories of people are
involved?

All **345 possible single-coordinate deletions** are checked against the
same declared ordinary-word stencil. Source index **134** is the unique
minimum at four observed substitutions. The source erasure is priced
separately, and its removal is not used to conceal an extra coordinate.
The received `W6S` and `NUNPERSONEN` remain visible in the raw layer.

## B3: troop transports and the request to remain in Turkey

The third part has exactly **348 slots**. Its invalid `Y` in `DGADY`,
source index 319, remains an erasure. The raw reading is:

**Raw output:**

```text
BITTEFERNERDRAHTEN?EBERSTANDDERTRUPPENTRANSPORTEUNDALLGEMEINELZGEDERDEUTSCHENI8DERTUERKEIX0NSERERSUCHENUMBELASSUNGDERDEUTSCHENZIVILPERSONENINDERTUERKEIISTVONPRAESIDENTWILSONX
```

Three observed-coordinate changes and the erased-coordinate fill give:

**Edited output:**

```text
BITTEFERNERDRAHTENUEBERSTANDDERTRUPPENTRANSPORTEUNDALLGEMEINELAGEDERDEUTSCHENINDERTUERKEIXUNSERERSUCHENUMBELASSUNGDERDEUTSCHENZIVILPERSONENINDERTUERKEIISTVONPRAESIDENTWILSONX
```

The sender also requests the status of troop transports and the general
situation of Germans in Turkey. Its request for German civilians to be
allowed to remain there has, it says, been acted on by President Wilson;
the sentence continues in the next part. The raw `LZGE`, `I8` and `0NSER`
are repaired at explicit source coordinates. They are not silently
relabelled as global square values.

## B4: referral to the Allies and the route through Ukraine

The last part advertises 266 coordinates but prints **265 valid
coordinates**. The visibly deficient group is `XDXG`, source positions
190–193. Constraining the missing coordinate to that group gives its best
fit at boundary **190**. This primary, source-local model reads:

**Raw output — conditional missing-slot placement at source boundary 190:**

```text
DENALLWEERTENUNDDEMOBERKRWEGSR6TINPARISVORQELEGTWORDE?XBEFOERDERUNGDERZIVILPERSONENDURCHXUKRAINEXZURZELTUNMYEGLICHXXYUSWAERTIGBERLINX
```

Nine observed-coordinate changes and one missing-coordinate fill support:

**Edited output — same conditional missing-slot frame, with the stated repairs and fill:**

```text
DENALLIIERTENUNDDEMOBERKRIEGSRATINPARISVORGELEGTWORDENXBEFOERDERUNGDERZIVILPERSONENDURCHXUKRAINEXZURZEITUNMOEGLICHXXAUSWAERTIGBERLINX
```

The request has been submitted to the Allies and the Supreme War Council
in Paris. Transport of civilians through Ukraine is currently impossible.
The signature is the Foreign Office in Berlin.

This source-local frame is not presented as the only possible original.
A broader screen masks **PARIS**, **UKRAINE** and the whole signature
before comparing all 266 insertion boundaries. It gives **six tied
body-only minima at 181–186**, just before the visibly short group. These
all need five observed-coordinate changes in the unmasked body. Their
full-text repair costs are:

| Inserted-coordinate boundary | Body-only cost | Full proposed-text cost |
| --- | ---: | ---: |
| 181 | 5 | 8 |
| 182 | 5 | 7 |
| 183 | 5 | 7 |
| 184 | 5 | 6 |
| 185 | 5 | 6 |
| 186 | 5 | 6 |
| 190, primary source-local fit | 8 | 9 |

The fully specified target therefore has three cheaper broad minima at
184–186. The edition retains **all six** masked-body ties, their raw
readings and separate source maps, as well as the primary source-local
frame. Every retained frame can be repaired to the same proposed
plaintext and exactly the same corrected ciphertext; the required source
changes differ. The cheaper word fit does not erase the competing
physical-group evidence, and the historical context below is not used to
choose a boundary.

## Independent contemporary corroboration

After transcribing the source and running the geometry screens, two
contemporary diplomatic texts were located in the official U.S.
*Foreign Relations* edition. They corroborate the subject and routing of
B3–B4 independently of the ciphertext:

- [Lansing to the Swiss Minister, November 15, 1918](https://history.state.gov/historicaldocuments/frus1919Parisv02/d4),
  no. 290, archival reference `763.72119/2800a`, printed pp. 17–18,
  acknowledges German radio appeals concerning the armistices and states
  that they will be communicated to the associated governments and the
  Supreme War Council in Paris.
- [Lansing to House, November 16, 1918, noon](https://history.state.gov/historicaldocuments/frus1919Parisv02/d5),
  telegram 38, archival reference `763.72119/9126a`, printed pp. 18–20,
  transmits Solf's November 15 wireless request that German civilians be
  permitted to remain in Turkey for consideration by that council.

These official editions reproduce contemporary documents; the underlying
manuscripts were not inspected. The German intercept credits President
Wilson, while the corroborating texts record Lansing's official actions.
They do not establish a separate personal act by Wilson, the `0YY`
headcount, the claimed departure, or any source-coordinate geometry.
The precise source note is retained in
[`historical_context.json`](../../experiments/constantinople_civilians/historical_context.json).

## Attribution and exact scope

Lasry and colleagues explicitly discuss the neighboring **p221 A**
Mackensen message. This source edition covers **B1–B4** only. Its bounded
prior-work check located no explicit discussion of this B body in the
checked paper, dissertation chapter or cached 55 ScienceBlogs comments;
that is not a universal historical-priority claim. The period key's prior
authorship remains credited in the inputs.

The four parts contain **1,255 printed slots**, **1,253 valid coordinates**
and **1,256 modeled coordinates**, producing **628 plaintext positions**.
The primary raw models fix **624** positions. Seventeen observed-coordinate
substitutions, two source-erasure fills and two missing-coordinate fills,
along with B2's one explicitly identified surplus-coordinate removal,
give a full **628-position candidate under the published raw labels**.
Its numerical headcount is still semantically unresolved.

```bash
python experiments/constantinople_civilians/verify.py --verify
python experiments/constantinople_civilians/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier reconstructs each transposition independently, checks every
raw domain and repair, reruns the exhaustive frame comparisons, and
exactly reencrypts all full candidates. The PDF option checks the complete
primary scan hash and every crop pixel. No substitution-square label is
changed by this edition.
