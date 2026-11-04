# The war's ending, in intercepted messages

[ADFGVX Cipher](../../README.md) · [Historical showcase](../historical-showcase.md) · [Reading catalogue](../../cases/README.md) · [Contributors](../../AUTHORS.md)

**This edition recovers the practical history inside the cipher:** an army seeking food for 80,000 men and 30,000 animals; headquarters asking for banknotes by aircraft; ships redirected from supplying an overseas force to collecting it; radio personnel arranging departures, asking after colleagues and preparing supper. The four studies below connect those individual messages into historical narratives. They place our new keys, restored copies and source editions beside independently preserved treaties, maps, diaries and diplomatic correspondence.

Research, source recovery and historical synthesis are by **icekylinx and GPT-6 Astra Pro**. Earlier decipherments are credited where they enter the story.

## Four ways into the collection

| Study | The historical question | Principal sources |
|---|---|---|
| **[An army trying to get home](an-army-trying-to-get-home.md)** | How did withdrawal become a problem of food, transit permission and internment? | Arad provisions and its recovered quantity; Hungarian negotiations; the Romanian ultimatum; Mackensen's appeal and the later letter to his soldiers' council. |
| **[The Black Sea network runs in reverse](black-sea-network.md)** | What happened to the shipping system that had sustained the German presence around the Black Sea and Caucasus? | The exact Sevastopol food dispatch; changed disembarkation ports; *Asgard* and Poti; the *Corcovado* sale; the Tiflis guard and Article XII. |
| **[What retreat cost](what-retreat-cost.md)** | What did it take to turn an order to return into actual movement? | Crown airlift requests, the recovered small-banknote instruction, a Vienna bank transfer, a blocked railway and the Breslau horseshoe dispatch. |
| **[Voices on the wireless](voices-on-the-wireless.md)** | What can official communications preserve of political upheaval and individual lives? | Kiel radio control; Seifert and the soldiers' council; arrival, car, supper and farewell messages; medical personnel and civilian return. |

Start with the [curated showcase](../historical-showcase.md) for a shorter route through the most revealing messages. The catalogue remains the route to every physical source, including fragments and unread bodies.

## What this edition contributes

Our central new cryptanalytic result is the **shared eighteen-column key and partial square for the two p153 CHI fragments**, recovered on 2 November 2026. It reads sixty of the first fragment's sixty-six positions without changing the source and supports the reconstructed instruction to report the rearguard artillery's ammunition stock in the second. The date, reference and closing fields remain partly unresolved. [The discovery and independent checks](../../experiments/p153_recovery/README.md) distinguish the original search from the later conditional proof.

For p153, **this is the first documented reconstruction identified in our review**. The [source and prior-work audit](../../data/reviews/p153_source_review.json) records the reviewed discussion, public solver pages, source material and phrase searches. Norbert's 17 September 2017 comment proposed analysing the two fragments together but supplied neither this key nor its text. Daniel Bourdeau's [September 2026 survey, preserved in its 24 September version](https://ciphers.jic.io/en/adfgvx.html), still lists both fragments as open. That is a specific, documented priority claim within the reviewed public record.

The broader contribution is an **interconnected source edition**. We identify repeat receptions, restore omitted printed groups, reconnect multipart messages and show which readings receive independent support. Several results materially change the historical information available:

- The [Arad witnesses](../../cases/military/danube_arad_witnesses.md) supply the eleven coordinates absent from the earlier reconstruction and fix its leading strength figure at **80000** from observed pairs.
- The [small-banknote witness](../../cases/finance/crown_banknote_completion.md) restores an interrupted nineteen-coordinate tail, resolves a local frame ambiguity and exposes one error in the earlier proposed completion.
- The [Palestine medical message](../../cases/military/palestine_medical_dissolution.md) identifies the formations to which an otherwise detached dissolution order referred.
- The [Seifert arrival enquiry](../../cases/radio/nov12_arrival_departure_and_car.md#p183-b) gains complete pair support from two complementary damaged copies.
- The [Mackensen appeal](../../cases/military/mackensen_armistice_appeal.md) gains a source-linked German edition that clarifies the distinction between acknowledging a note and accepting its demands.

These are claims about identifiable work and identifiable sources. Ordinary application of a previously published period key is credited as source edition or verification; a newly recovered key and an independently restored copy are stated as new results.

## The public literature behind the credits

The review combines the project's detailed source audits with public literature checked on **4 November 2026**. Its principal reference points are:

1. **J. Rives Childs and the wartime record.** Childs preserved the intercepted traffic and discussed the cipher in his historical technical reports. His collection is the source of the physical ciphertexts edited here. The [1935 report in the NSA archive](https://www.nsa.gov/Portals/75/documents/news-features/declassified-documents/friedman-documents/publications/FOLDER_268/41784789082381.pdf) and the [complete collection scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) have different functions: historical analysis and source corpus.
2. **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker.** Their [*Cryptologia* study](https://doi.org/10.1080/01611194.2016.1169461), published online in 2016 and in volume 41 in 2017, reports 618 deciphered cryptograms from the 668 it studied. Its historical section already presents the major Mackensen withdrawal, appeal and internment material and the Kiel/Seifert political messages. Those are earlier contributions, not discoveries reassigned to this project. [Author manuscript](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf).
3. **The 2017 challenge discussion.** Klaus Schmeh published Lasry's remaining challenge material. Armin, Norbert, Thomas, Max Baertl and Lasry contributed attacks, readings and corrections. The repository's [attribution audit](../../data/reviews/attribution_review_2017.json) checks **56 numbered comments** and uses their public display names. The p153 audit distinguishes that count from later indexes that inadvertently included sidebar comments. [Original discussion](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).
4. **The 2026 public work.** Bourdeau's [survey](https://dbourdeau.github.io/cyphersolver/adfgvx.html) consolidates earlier challenge results and reproduces known-key repairs. Prinz with GPT-6 Astra published the [p217 body](../../cases/p217.md) on 17 September; Christian Horvat supplied its later date correction. The current edition verifies and contextualizes that reading. Other contributors and applicable cases are listed in [Contributors](../../AUTHORS.md).

<details>
<summary>Review scope and source versions</summary>

The dated repository audits specify the earlier inspection of the original discussion and larger source files. The 4 November public review checked the research paper, the current survey and its September mirror, exact/component p153 phrase searches, and the contemporary documentary sources cited in the studies. The original ScienceBlogs page and some large external files were not consistently retrievable in that fresh review. The September mirror and the live author's page remain separate versions.

</details>

## How historical evidence is used

Each study starts from what a message actually says: an instruction, report, enquiry or proposal. A request for an airlift is evidence of the request; a diary or receipt is needed to establish a completed movement. A treaty can identify a damaged article reference, while the telegram's statement about the Tiflis guard remains its own report. A contemporary map can support a place name without proving an order's exact timetable.

German quotations use the linked edition's readable layer. Spacing and punctuation are editorial; retained abbreviations and unresolved fields remain visible. Local evidence notes identify substantive reconstruction where it matters. Full source transcriptions, raw readings and repair accounting stay with the cases, so the narrative can be read continuously and checked closely.
