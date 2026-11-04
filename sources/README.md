# Sources

[Reviewed source crops](reviewed-crops.md) · [Evidence verification](../docs/source-evidence-modes.md)

| Source | Use |
|---|---|
| [Childs full scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view), located through [Richard Bean's catalogue](https://richardbean.id.au/misc/kryptos/aegean-park-press.html) | Original intercepts and historical key tables. For the intercept log and key appendix, printed page *p* is PDF page *p + 3*. |
| [Lasry–Schmeh challenge](https://scienceblogs.de/klausis-krypto-kolumne/unsolved-adfxvx-messages-from-world-war-i/) | The 22 target records. |
| [2017 discussion](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1) | Original public readings, key recovery, and corrections; individual comments are cited per message. |
| [Lasry et al., Cryptologia](https://doi.org/10.1080/01611194.2016.1169461) | Modern recovery methods and period keys. |
| [Lasry dissertation](https://www.uni-kassel.de/upress/online/OpenAccess/978-3-7376-0458-1.OpenAccess.pdf) | Independent corroboration of partial key squares. |
| [Bourdeau's review](https://dbourdeau.github.io/cyphersolver/adfgvx.html) | Reviewed status and plaintext-constraint checks; inspected 2 November 2026. |
| [0wwafa/adfgvx-1918](https://github.com/0wwafa/adfgvx-1918) | Prior reproducible re-attack and proposed readings; independently reviewed here. |
| [Prinz, 17 September 2026](https://www.prinzai.com/p/gpt-6-astra-solves-a-wwi-german-radio) | p217 keyword and reading. |
| [Prinz, 19 September 2026](https://www.prinzai.com/p/another-wwi-german-radio-cipher-falls) | p176b partial reading; Christian Horvat's 21 September comment corrects p217. |

The included excerpts preserve original intercept pages and the contemporary material needed to inspect specific historical claims. Each source retains its institutional provenance. The complete Childs book and modern editorial material are not redistributed. Original German, French, and ciphertext are quoted as research data; repository discussion is in English.

## p152 terminology

`STRUSEN` is a genuine silk-trade term, not an error requiring normalization. [Guérin-Mèneville's 1853 report in the Polytechnisches Journal](https://dingler.bbaw.de/articles/ar128114.html), volume 128, p. 451, identifies it with the outer cocoon layer. This independently supports the commodity context of the raw decipherment.


## Bibliographic distinctions

The Aegean volume's 2000 edition date is supported by Lasry's bibliography; the inspected imprint is undated. Its opening technical paper matches *General Solution for the ADFGVX Cipher System*, Register 129, whose separate government title page states 1934. That publication date is distinct from the date of Childs's wartime records and from the composition date of the earlier manuscript.

*German Military Ciphers from February to November 1918* is a different report, published in 1935 with Friedman's foreword dated 25 June 1934. The foreword dates Childs's underlying report to about December 1918 and identifies later added notes. Exact source identifiers and evidence are in [the registry](registry.json).

## Header direction

`X v Y` means **radio recipient X, radio sender Y**. The explicit routes and adjacent headers on [printed p. 9 of the 1935 report](excerpts/nsa_header_convention_p9.png) establish the convention: `NKJ v LP` accompanies a message from LP through NKJ, and `OSM v COS` accompanies a message from COS to OSM. Thus `CM v CZ` is CZ to CM; `-- v CM` has an unknown recipient and a known sender CM. A relay call sign need not identify the ultimate author or addressee.

## Historical and technical context

These sources support specific interpretations or delimit a search. They do not
replace a missing ciphertext witness or assign an unknown key cell.

| Source | Use and limit |
|---|---|
| [Paquet, Groener and Hopman records, edited by Winfried Baumgart in 1971](https://digitale-sammlungen.de/en/details/bsb00042051) | Contemporary shipping and Crimea command context for p155 and the conditional p215 Kosch reading. Diary/document text is distinguished from the modern editor's notes. |
| [Telefunken-Zeitung, 1919, no. 15](https://www.radiomuseum.org/forumdata/users/5100/TZ_3Jg_Nr15_1v1_v10.pdf) | The manufacturer's contemporary terminology supports the undamped-wave radio-apparatus interpretation of `US GERAETE` in the p197/p198 equipment traffic. No particular model is established. |
| [Australian War Memorial, Allied-fleet memorandum of 24 November 1918](https://transcribe.awm.gov.au/transcription/item/rcdig0000179-4) | Independent Black Sea departure-order context for p217. It does not verify p215's reported troops or explain its nationalities. |
| [Kress, *Meine Mission im Kaukasus*, 2001 edition](https://de.scribd.com/document/46043064/General-Der-Artillerie-a-D-Friedrich-Freiherr-Kress-von-Kressenstein-MEINE-MISSION-IM-KAUKASUS) | A retrospective memoir accompanying a 1943 covering letter. The bounded late-period inspection finds no matching p73 radiogram; an apparent calendar-date match belongs to the editor's 1917 discussion. |
| [Lepsius, *Deutschland und Armenien 1914–1918*, 1919](https://www.gutenberg.org/files/58144/58144-h/58144-h.htm) | Documents 439–444 were checked. Document 442 is Kress's outgoing 30 October report, not the sought incoming p73 message. |
| [Central-Volksblatt, 14 November 1918, front page](https://www.werl.de/fileadmin/user_upload/Stadtarchiv/Titelseiten_aus_dem_Central-Volksblatt/14._November_1918.pdf) | A WTB dispatch dated 12 November reports six evacuation trains daily for each of AOK 11 and Mackensen's army. Original article and issue date were visually checked; the report establishes an announced allocation, not completed train movements. [Crops and provenance](../data/reviews/mackensen_railway_press.json). |
| [Lloyd’s Register of Shipping, 1919–20, Volume II—Steamers](https://archive.org/details/HECROS1920ST/page/n1294/mode/1up) | The Sueh entry and its explicit supplement cross-reference identify Corcovado under a French flag and French Government ownership in the inspected register copy. This supplies later context, without dating the transfer or establishing completion or currency of the intercepted ten-million proposal. [Page locators and review](../data/reviews/lloyds_corcovado_context.json). |
| [Béla Barkóczy-Klopsch, Mackensen's army in Hungary, 1923](https://real-eod.mtak.hu/8911/1/MTA_AKisAkademiaKonyvtara_043.pdf) | The formation list and transport chronology support conditional late-November numeral assignments. [Inspected pages and cipher consequences](../experiments/late_november_calendar_and_units/README.md). |
| [Der Gebirgsbote, no. 129, 13 November 1918](https://bibliotekacyfrowa.pl/Content/60534/PDF/directory.pdf) | A decree dated 11 November places the VI Army Corps deputy general command in Breslau. [Masthead, decree and personnel-message comparison](../experiments/nov25_treaty_digits/README.md#a-separate-breslau-unit-interpretation). |
| [Engel, Holtz and Materna, Berlin workers' and soldiers' council documents, document 96](https://doi.org/10.1515/9783050068831.400) | The published archival transcription gives a counterpart to the p226–227 letter, its dispatch date and signatures. [Textual variants and exact surname-repair costs](../experiments/mackensen_archival_comparison/README.md). |

Exact page/image locators, inspected scopes and limitations are retained in
[the registry](registry.json) and the linked case and review records. The
[two held-out books](../experiments/open_targets/heldout_sources.json) used for
statistical calibration have separate source and byte-hash provenance; their
prose is not treated as a source for any historical telegram's wording.
