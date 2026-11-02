# Sources, prior methods and implementation scope

## Historical material

The two target fragments are in Appendix B, printed page 153 of the Aegean Park
Press volume *General Solution of the ADFGVX Cipher System*. The inspected
[public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
records `FKR v CGH`,11.55p.m.,November 8, 1918, transmission 2250, parts 5 and 6,
with declared coordinate counts 132 and 108. The parent source audit supplies
the detailed edition/date distinctions and the source image. This suite
uses the source-audited transcription and never changes an observed coordinate.

The original 22-entry challenge is Klaus Schmeh's
[Unsolved ADFGVX messages from World War I](https://scienceblogs.de/klausis-krypto-kolumne/unsolved-adfxvx-messages-from-world-war-i/),
with material supplied by George Lasry. The
[2017 discussion](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1)
contains the known CHI solution and follow-up corrections in comments 50 and 53
by George Lasry and Norbert Biermann. The conservative 22-cell square used by
the optional anchor experiment is:

```
AROT?W
H??C??
SVU?I?
DXBP??
???NZE
LFK?G?
```

The legacy duplicated `X` is not a valid known-cell constraint. Unknown digits
and letters remain unknown. The CHI key is attested for a November 13 message;
its use as an anchor for November 8 is an explicit reuse hypothesis. The
[NSA historical report](https://www.nsa.gov/Portals/75/documents/news-features/declassified-documents/friedman-documents/publications/FOLDER_268/41784789082381.pdf)
describes Western CHI daily keys, so reuse must not be silently assumed.

## Algorithmic precedent

The principal modern precedent is George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker, *Deciphering ADFGVX messages from the Eastern Front of World War I*,
Cryptologia 41(2),101–136 (2017; online 2016),
[DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
A [public manuscript copy](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf)
is available. Pair and quadruplet coincidence statistics, heuristic
transposition search and column-pair methods are prior art. No novelty is
claimed for those underlying ideas.

The present implementation specializes length-class segmentation to the
joint 132/108-coordinate target; separates exact matching surrogates from
stochastic global pairing; uses independent short-text profile and language
models; and explicitly audits erasures, model failures and same-length
controls. It is not a verbatim reproduction of the 2017 search algorithm.
The exact-domain solver extends the parent investigation's single-message
implementation to multiple messages without cross-message language windows.

## Training data and earlier code

`models/provenance.json` lists all ten public-domain German books, source URLs,
byte hashes, weights and expected binary model hashes. Six general German
books train the short-text profile. The military language model additionally
uses Hindenburg's *Aus meinem Leben* and the three volumes of Helfferich's
*Der Weltkrieg*, at the disclosed domain weights. Source ID 6099, a French
book encountered in an earlier broad corpus list, is excluded entirely.

The source corpus and initial arithmetic checks were cross-checked against
the MIT-licensed [0wwafa/adfgvx-1918](https://github.com/0wwafa/adfgvx-1918)
baseline, commit`083921732d7c18e52424336ab4160fada5c61b4b`. The curated C engines
and portable Python helpers were written for this investigation; this package
does not contain the baseline's source files or its solution-trained model.

Authorship of this research implementation: **IceKylin and GPT-6 Astra**.
The parent repository's license applies. Synthetic control success is an
implementation/calibration result, not a new historical decipherment.
