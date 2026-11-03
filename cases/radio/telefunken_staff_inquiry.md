# Telefunken inquiry about returning personnel

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Status:** a complete unchanged-source reading of p112 B. The source has
188 valid coordinates; the old OCR had 189. The native frame yields all
94 positions without a substitution, fill, insertion or deletion.

The header is OSM v OUI, received at 2.45 p.m. on November 4, origin 1100.
Although the page's preceding heading says November 3, the unchanged
Nov4–6 key reads this body. The different date fields are preserved.

## p112 B

The source asks about the fate and expected return of personnel. Question punctuation belongs to the readable display. The literal source spelling RUECKEHR is rendered Rückehr, without silently adding the extra K in standard Rückkehr. No source wording or identity is added.

**Raw output — native source frame:**

```text
TELEFUNKENXKONSTANTINOPELXDRAHTETSCHICKSALUNSERESPERSONALSXISTRUECKEHRZUERWARTENUNDWANNXBREDOW
```

**Edited output — identical to raw output; no source changes:**

```text
TELEFUNKENXKONSTANTINOPELXDRAHTETSCHICKSALUNSERESPERSONALSXISTRUECKEHRZUERWARTENUNDWANNXBREDOW
```

**Readable German — based on the edited candidate above; the local qualifications remain in force:**

> Telefunken Konstantinopel drahtet: Schicksal unseres Personals? Ist Rückehr zu erwarten und wann? Bredow.

The candidate uses **0 observed-coordinate substitutions**, **0 source-mask fills** and **0 unprinted-coordinate fills**. These are literal square labels, without an additional historical numeral assignment.


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
