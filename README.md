# ADFGVX Cipher

Readings, source criticism, and reproducible cryptanalysis of German radio traffic from 1918.

[![Research checks](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml/badge.svg)](https://github.com/icekylinx/adfgvx-cipher/actions/workflows/verify.yml) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**icekylinx and GPT-6 Astra Pro** · [Read the messages](cases/README.md) · [Research status](docs/research-status.md) · [Methods](docs/methods.md) · [Sources](sources/README.md) · [Citation](CITATION.cff)

A research edition of the **German radio cryptograms in Childs's 1918 collection**: the 22 Lasry–Schmeh challenge entries and a growing catalogue of other messages, with readable plaintexts, original source transcriptions, earlier credits and reproducible decryption evidence.

## Selected results

- **[October Caucasus traffic](cases/other/october_caucasus.md):** nine parts recover correspondence about personnel and funds for Kress, Westernhagen’s return, electrical equipment for Tiflis, Violetta’s cargo and radio timings. Printed strikeouts, duplicated groups, unresolved quantities and every editorial repair remain inspectable.
- **[Late key-sharing instructions](cases/other/late_november_cipher_instructions.md):** two complete parts explicitly agree on the BSL–UKS key, preserving all 320 coordinates. Related notices document missing December tables and a request for RICHI or plaintext after ITOCHI could not be read.
- **[Romanian withdrawal and headquarters movements](cases/other/p163_A.md):** six framed records with the [Temesvar station notice](cases/other/p164_B.md) add 608/730 fixed raw positions. The more damaged garrison continuation remains a separately costed reconstruction. [Later operational reports](experiments/operational_recovery/README.md) add eight parts on coal shortages, disarmament, troop positions and a headquarters move, with numerical interpretation kept separate.
- **[Additional source readings](experiments/corpus_recovery/README.md):** oil release and Black Sea shipping safety, the Dutch courier Vreede, Helsinki return transport for the Ostsee Division, Burkhardt's oil-company assignment, two Richter inquiries and the situation in Reval. Nine records fix 1,155/1,161 raw positions; all editorial repairs and unresolved numeral labels remain visible.
- **[p153a](cases/p153a.md) / [p153b](cases/p153b.md): new substantial partial decipherment.** A shared 18-column key recovers 60/66 first-part positions and 33/54 raw second-part positions. The ammunition-report reconstruction gives a 50/54-position conditional template, with every fill and emendation recorded.
- **Repeated and re-encrypted messages recover missing text.** The [Munich courier notice](cases/other/courier_munich.md) has a direct continuation and an explicitly qualified first part. A later key supplies [Kremp's departure request](cases/other/kremp.md) unchanged and independently quotes [the previously published Warsaw query](cases/other/mackensen_warsaw.md). [Osthoff](cases/other/osthoff.md), [Glatz](cases/other/glatz.md), [p152](cases/p152.md) and [p158](cases/p158.md) retain their complete source evidence.
- **Finance and naval administration:** [p205 A](cases/other/p205_A.md) requests thirty million kroner, initially five million; [p205 B](cases/other/p205_B.md) ends report submissions while requiring war diaries to continue. The six source parts fix 750/757 raw positions; four editorial substitutions and the remaining reference digits are explicit.
- **Politics, communications and station operations:** [Budapest telephone censorship](cases/other/p85_B.md), [Filittis family entry permission](cases/other/p96_B.md), [radio use for important messages](cases/other/p111_B.md), and [station-control / Seifert traffic](cases/other/seifert.md). Earlier Childs and Lasry-team readings keep their attribution.
- **Two assembled three-part notices:** [Feigenhaus and the changing political situation](cases/other/p120_p123.md), retaining its unusual vocabulary, and [Kress / Tiflis under the armistice](cases/other/p218_A.md), with Article XII independently identified and every source repair counted.
- **New source constraints:** an independent intercept supplies the [missing 20-coordinate operational-report prefix](cases/other/nov9_operational_reports.md); [p211](cases/other/p211_key_schedule.md) explicitly instructs December reuse of November keys. The [Monday date](cases/other/p204_A.md), [shared order reference](cases/other/p201_p206_orders.md) and military unit evidence support conditional digit assignments, kept separate from the published squares.
- **Challenge repairs remain visible:** the [p146 duplicate group](cases/p146.md), [p187b adjacent swap](cases/p187b.md), [p109 parallel report](cases/p109.md), [p189 conditional recovery](cases/p189.md), and [p215 Corps Kosch interpretation](cases/p215.md). The 2017 and September 2026 readings retain their original authorship.

Among the 22 challenge entries, three remain wholly open: **p73, p170, p198**. A source-linked recovery or contextual reading is not counted as an independently solved original ciphertext.

All current source reviews, arithmetic audits, and new editorial work are by **icekylinx and GPT-6 Astra Pro**. The tables credit the earlier public reading or the present recovery/review named in that row. Each case gives the most likely readable text, its meaning, and unresolved details.

<!-- READING-CATALOG:START -->
## The 22 challenge entries

These retain the original challenge identifiers. Page numbers alone do not identify a message: p198 is section D, while p198 B/C/E are separate records below.

| Ciphertext | Most likely content | Reading status | Reading or review credit |
|---|---|---|---|
| [p73](cases/p73.md) | Message routed to General von Kress | Open | — |
| [p100](cases/p100.md) | Enemy divisions approaching Belgrade | Prior body reading; source audit | Armin (2017) |
| [p105](cases/p105.md) | Naval telegram acknowledgments | Prior body reading; source audit | Norbert (2017) |
| [p109](cases/p109.md) | Evening report; likely Sava crossing | Prior body; new source parallel | Norbert (2017) |
| [p132](cases/p132.md) | Repeat-transmission instructions for Eilvese | Prior body reading; source audit | Thomas (fragment) and Norbert (body), 2017 |
| [p146](cases/p146.md) | Kerch radio call-sign instruction | Prior body; duplicate-group repair | Norbert (2017) |
| [p152](cases/p152.md) | Silk purchases and transport from the Caucasus | Source-linked body | icekylinx and GPT-6 Astra Pro (2026) |
| [p153a](cases/p153a.md) | Earlier orders; action still to be completed | New partial: 60/66 ordinary-letter positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p153b](cases/p153b.md) | Rearguard artillery ammunition report | New raw partial; conditional body and footer | icekylinx and GPT-6 Astra Pro (2026) |
| [p158](cases/p158.md) | Routing and army-key instructions | Composite sources identified | icekylinx and GPT-6 Astra Pro (2026) |
| [p164a](cases/p164a.md) | Temesvar / MIRCO contextual fragments | Prior partial; constraint audit | Norbert (2017) |
| [p164b](cases/p164b.md) | Height 828 and an uneventful situation report | Prior partial; constraint audit | Norbert (2017) |
| [p170](cases/p170.md) | Short intercept; original length uncertain | Open | — |
| [p171](cases/p171.md) | Ruble rates and expectations about Russia | Prior body reading; source audit | Norbert (2017) |
| [p176a](cases/p176a.md) | Breakthrough toward the north or northeast | Prior body reading; source audit | Norbert (2017) |
| [p176b](cases/p176b.md) | Army positions near Peterreve and Versecz | Prior contextual reading; constraint audit | Prinz and GPT-6 Astra (2026) |
| [p187](cases/p187.md) | Monitoring Russian and Polish army traffic | Prior body reading; source audit | George Lasry and Norbert (2017) |
| [p187b](cases/p187b.md) | Teleprinter failure and written reporting | Prior body; adjacent-swap explanation | George Lasry and Norbert (2017) |
| [p189](cases/p189.md) | Apparent vehicle request / await orders | Conditional partial | icekylinx and GPT-6 Astra Pro (2026) |
| [p198](cases/p198.md) | CHI intercept with a five-coordinate shortfall | Open | — |
| [p215](cases/p215.md) | Apparent Entente troop-transport report | Prior partial; Kosch interpretation and conditional ?1?6 reference | Norbert (2017) |
| [p217](cases/p217.md) | British cruiser and Allied squadron at Sevastopol | Prior body reading; correction verified | Prinz and GPT-6 Astra (2026); correction: Christian Horvat |

## Other ciphertexts — 133 reviewed records

Each row identifies a separate source record outside the 22-entry challenge. Multipart messages and repeated transmissions have separate rows even when one case page discusses them together. Direct readings, source-supported reconstructions and conjectural repairs retain their stated limits.

| Ciphertext | Most likely content | Reading status | Reading or review credit |
|---|---|---|---|
| [p69 B1](cases/other/october_caucasus.md#p69-b--violettas-cargo-from-braila-to-poti) | Violetta cargo from Braila for Poti | Conditional one-slot recovery; quantity fields retained | icekylinx and GPT-6 Astra Pro (2026) |
| [p69 B2](cases/other/october_caucasus.md#p69-b--violettas-cargo-from-braila-to-poti) | Additional wagons for the troops at Poti | Two minimum-cost short-group repairs; complete proposed continuation | icekylinx and GPT-6 Astra Pro (2026) |
| [p70 A1](cases/other/october_caucasus.md#p70-a--westernhagen-price-limits-and-an-urgent-return) | Westernhagen asked for the market report and price context | Two visible repeated groups removed conditionally; 156/161 raw positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p70 A2](cases/other/october_caucasus.md#p70-a--westernhagen-price-limits-and-an-urgent-return) | Urgent personal discussion and accelerated return | 121/123 raw positions at actual length 246; header says 256 | icekylinx and GPT-6 Astra Pro (2026) |
| [p71 A1](cases/other/october_caucasus.md#p71-a1--electrical-equipment-sent-to-tiflis) | Machine sets and converter dispatched to Tiflis | Source-preserving edition; 20-kW digit remains conditional | icekylinx and GPT-6 Astra Pro (2026) |
| [p72 A1](cases/other/october_caucasus.md#p72-a--reinforcements-administrative-personnel-and-money-for-kress) | OHL reinforcement order for the delegation to Kress | Printed 25-coordinate strikeout applied; 88/89 raw positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p72 A2](cases/other/october_caucasus.md#p72-a--reinforcements-administrative-personnel-and-money-for-kress) | Administrative personnel except garrison officials | Two 25-slot near-duplicate alternatives; 108/113 positions common | icekylinx and GPT-6 Astra Pro (2026) |
| [p72 A3](cases/other/october_caucasus.md#p72-a--reinforcements-administrative-personnel-and-money-for-kress) | Personnel will be supplied; necessary funds secured | 60/62 raw positions; explicit word repairs | icekylinx and GPT-6 Astra Pro (2026) |
| [p72 B](cases/other/october_caucasus.md#p72-b--radio-timings-and-reception) | Radio timings and reception at Poti | 136/137 raw positions; proposed time and wavelength repairs explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p77 B](cases/context/radio_instructions.md#p77-b--call-sign-instruction-for-konia) | Konia radio call sign and wavelengths | Direct reading; one word normalized | icekylinx and GPT-6 Astra Pro (2026) |
| [p84 A](cases/other/p84_AB.md) | Ask whether Izzet Pasha's order to release oil succeeded | 122/122 raw positions; unchanged source roundtrip | icekylinx and GPT-6 Astra Pro (2026) |
| [p84 B](cases/other/p84_AB.md) | Request daily Black Sea shipping-safety reports for the Caucasus command | 101/101 raw positions; unchanged source roundtrip | icekylinx and GPT-6 Astra Pro (2026) |
| [p85 B](cases/other/p85_B.md) | Telephone censorship through Budapest | 99/99 raw positions; two word repairs explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p89 A2](cases/supplementary/p89_A2.md) | Shipping and railway routing to Nikolayev | Earlier reading; one source glyph uncertain | Ayush Agarwal; review by D. Bourdeau (2026) |
| [p92 A](cases/other/p92_A.md) | Dutch courier Vreede to travel via Braila to Constantinople | 214/214 raw positions; one explicit word repair | icekylinx and GPT-6 Astra Pro (2026) |
| [p96 B](cases/other/p96_B.md) | Entry permission for Filittis and family | 180/181 raw positions; Copenhagen repair costed | icekylinx and GPT-6 Astra Pro (2026) |
| [p107 D](cases/supplementary/p107_D.md) | Acknowledgment of operational telegrams | Earlier reading; parenthesized glyphs retained | Ayush Agarwal; review by D. Bourdeau (2026) |
| [p109 B](cases/p109.md) | Evening enemy-division report toward Belgrade | Near-parallel supporting p 109; word alternatives remain | icekylinx and GPT-6 Astra Pro (2026) |
| [p111 B](cases/other/p111_B.md) | Use radio for important messages | 154/154 direct positions; no coordinate edits | icekylinx and GPT-6 Astra Pro (2026) |
| [p120 B1](cases/other/p120_p123.md) | Instruction to Feigenhaus; contact with Herkules | 197/197 raw positions; one word repair | icekylinx and GPT-6 Astra Pro (2026) |
| [p122 D suffix](cases/other/p120_p123.md) | Repeat of the Feigenhaus instruction, part 1 | Exact 164-coordinate suffix; not a separate complete message | icekylinx and GPT-6 Astra Pro (2026) |
| [p123 A2](cases/other/p120_p123.md) | Responsibility for further Notschreie declined | 97/116 raw positions; explicit conditional completion | icekylinx and GPT-6 Astra Pro (2026) |
| [p123 A3](cases/other/p120_p123.md) | Follow instructions; report plans after political change | One-coordinate deletion; two further substitutions | icekylinx and GPT-6 Astra Pro (2026) |
| [p131 B](cases/other/kremp.md) | Kremp asks for his departure date | 82/84 raw positions; later second-key body supports repairs | icekylinx and GPT-6 Astra Pro (2026) |
| [p134 B](cases/context/radio_instructions.md#p134-b--repeat-a-fourth-period-telegram-in-the-fifth) | Repeat a fourth-period telegram in the fifth | 50/51 raw positions; wording partly editorial | icekylinx and GPT-6 Astra Pro (2026) |
| [p136 B1](cases/p152.md#raw-p136-b1-parallel-plaintext) | Silk purchases in the Caucasus; first part | Full raw reading; supports the p 152 fragment | icekylinx and GPT-6 Astra Pro (2026) |
| [p136 B2](cases/p152.md#raw-continuation-witnesses) | Resell goods whose transport is not assured | Continuation; one coordinate supplied by a parallel | icekylinx and GPT-6 Astra Pro (2026) |
| [p138 A1](cases/other/osthoff.md) | Osthoff's Turkey posting cancelled, first witness | Missing group supplied by p148; all 121 candidate letters witnessed | icekylinx and GPT-6 Astra Pro (2026) |
| [p138 A2](cases/other/osthoff.md) | Osthoff reassigned to a railway replacement battalion | Shared source garbles; three proposed word repairs | icekylinx and GPT-6 Astra Pro (2026) |
| [p140 A1](cases/other/kiel_radio_control.md) | Take immediate officer control of all radio stations | 56/56 raw positions; separately costed word repairs | Prior body: Childs and Lasry et al.; source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p140 A2](cases/other/kiel_radio_control.md) | Prevent reception and distribution of Kiel messages | 65/67 raw positions; separately costed word repairs | Prior body: Childs and Lasry et al.; source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p140 A3](cases/other/kiel_radio_control.md) | Confiscate and destroy Kiel texts already received | 47/51 raw positions; separately costed word repairs | Prior body: Childs and Lasry et al.; source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p140 A4](cases/other/kiel_radio_control.md) | Urgent handling of the Kiel radio-control order | 45/49 raw positions; separately costed word repairs | Prior body: Childs and Lasry et al.; source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p140 B](cases/other/glatz.md) | Enquiry about Glatz's whereabouts | 167/168 letters witnessed; one damaged-glyph fill | icekylinx and GPT-6 Astra Pro (2026) |
| [p146 A](cases/other/kiel_radio_control.md) | Repeat order placing radio stations under officer control | 51/56 raw positions after explicit five-coordinate deletion | Prior body: Childs and Lasry et al.; source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p148 C1](cases/other/osthoff.md) | Osthoff's posting cancellation, clearer repeat | 120/121 raw positions; remaining letter supplied by p138 | icekylinx and GPT-6 Astra Pro (2026) |
| [p149 A2](cases/other/osthoff.md) | Repeated Osthoff reassignment and cabinet-order closing | 115/118 letters witnessed; three editorial changes | icekylinx and GPT-6 Astra Pro (2026) |
| [p149 B](cases/other/kremp.md) | Kremp reports recovery and asks for departure instructions | 84/84 raw positions with three garbles; later key supplies readable body | icekylinx and GPT-6 Astra Pro (2026) |
| [p149 C](cases/other/glatz.md) | Enquiry about Glatz's whereabouts | Parallel with four coordinate disagreements; raw errors retained | icekylinx and GPT-6 Astra Pro (2026) |
| [p151 D2](cases/other/courier_munich.md) | Notify the courier destination and report arrival | 67/68 raw positions; one garble supplied by a repeat | icekylinx and GPT-6 Astra Pro (2026) |
| [p152 E2](cases/p152.md#raw-continuation-witnesses) | Parallel continuation of the silk instruction | Direct raw reading with residual garbles | icekylinx and GPT-6 Astra Pro (2026) |
| [p153 D2](cases/other/courier_munich.md) | Notify the courier destination and report arrival | 67/68 raw positions; one garble supplied by a repeat | icekylinx and GPT-6 Astra Pro (2026) |
| [p153 E1](cases/other/courier_munich.md) | Munich couriers carrying radio operating documents | Conditional first-part reconstruction; all tied damage models retained | icekylinx and GPT-6 Astra Pro (2026) |
| [p155 A1](cases/context/p155.md) | Asgard arrival at Poti and troop pickup | 84/85 raw positions; source glyph remains erased | icekylinx and GPT-6 Astra Pro (2026) |
| [p155 A2](cases/context/p155.md) | Asgard/Tresivolus shipping continuation | Conditional single-coordinate loss repair | icekylinx and GPT-6 Astra Pro (2026) |
| [p158 C2](cases/other/courier_munich.md) | Notify GRUKONACH and telegraph the couriers arrival | 67/68 unchanged; 602 only under the separate historical key inference | icekylinx and GPT-6 Astra Pro (2026) |
| [p159 B](cases/p158.md#component-readings) | Munich routing and army-key instruction | Reconstruction from repeated transmissions | Childs (1918); review: icekylinx and GPT-6 Astra Pro |
| [p159 C](cases/p158.md#component-readings) | Munich–Innsbruck routing and army-key instruction | Source-supported one-coordinate deletion | icekylinx and GPT-6 Astra Pro (2026) |
| [p159 D](cases/other/kremp.md) | Kremp recovered and requests a departure date | 98/98 positions, 196/196 coordinates unchanged | icekylinx and GPT-6 Astra Pro (2026) |
| [p162 A1](cases/other/courier_munich.md) | Repeated Munich courier departure notice | Companion to p153 E1; 118/134 positions supported across both models | icekylinx and GPT-6 Astra Pro (2026) |
| [p163 A13](cases/other/p163_A.md) | Keep Crajova and Bucharest occupied until final evacuation | 126/134 raw positions; ten substitutions and six fills; opening unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p163 A14](cases/other/p163_A.md) | Final evacuation in one move; retain the Bucharest garrison | 121/122 raw positions; five substitutions and one fill | icekylinx and GPT-6 Astra Pro (2026) |
| [p163 A15](cases/other/p163_A.md) | Conditional garrison transfer to corps headquarters and Scholtz | 36/117 raw positions; 91-position prefix needs two substitutions and 63 fills | icekylinx and GPT-6 Astra Pro (2026) |
| [p163 A17](cases/other/p163_A.md) | Danube vessels and Scholtz headquarters movement to Calimanesti | 125/132 raw positions; sixteen substitutions and six fills | icekylinx and GPT-6 Astra Pro (2026) |
| [p163 A18](cases/other/p163_A.md) | Headquarters moves to Hermannstadt, Kronstadt and Sinaia | 131/155 raw positions; twenty-one substitutions and 24 fills | icekylinx and GPT-6 Astra Pro (2026) |
| [p164 A4](cases/context/p164_A4.md) | Dismounted cavalry west of an unidentified MIRCO | 87/99 raw positions; full proposal explicitly repaired | icekylinx and GPT-6 Astra Pro (2026) |
| [p164 B](cases/other/p164_B.md) | Dismantle the station and resume calls after reaching Temesvar | 69/70 raw positions; two substitutions; 0500 is a separate digit inference | icekylinx and GPT-6 Astra Pro (2026) |
| [p166 A1](cases/other/nov9_operational_reports.md) | Serbian cavalry in Peterwardein and Fehertemplom | 87/87 raw positions; three word/separator repairs explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p166 A2](cases/other/nov9_operational_reports.md) | Northward movement and Alpenkorps transport preparations | 105/106 raw positions; reserve division 5/6, context supports 6 | icekylinx and GPT-6 Astra Pro (2026) |
| [p166 A3](cases/other/nov9_operational_reports.md) | March toward Nagybeskerek and Werschetz; order footer | Missing 20-coordinate prefix supplied by p167; 184 received slots preserved | icekylinx and GPT-6 Astra Pro (2026) |
| [p167 A3](cases/other/nov9_operational_reports.md) | Complete-frame repeat of the operational-report ending | Supplies p166 prefix; conservative combined template 97/102 fixed | icekylinx and GPT-6 Astra Pro (2026) |
| [p168 A](cases/other/seifert.md) | Station under a soldiers' council; operation unchanged | 92/92 raw positions; spelling omission retained | Lasry, Niebel, Kopal and Wacker |
| [p168 B](cases/other/seifert.md) | Cologne soldiers' council plans to occupy a radio station | Two explicit coordinate repairs | Childs; Lasry, Niebel, Kopal and Wacker |
| [p168 C](cases/p158.md#earlier-historical-reading-of-a-component) | Repeated Munich routing order 11338 | Parallel witness to the p 159 B component | Childs (1918); review: icekylinx and GPT-6 Astra Pro |
| [p168 D](cases/p158.md#component-readings) | Repeated Munich–Innsbruck routing instruction | Parallel witness to the p 159 C component | icekylinx and GPT-6 Astra Pro (2026) |
| [p169 A](cases/other/seifert.md) | Repeated station-control report | Conditional one-coordinate deletion; clearer p168 witness | icekylinx and GPT-6 Astra Pro (2026) |
| [p170 B1](cases/other/nov9_operational_reports.md) | Parallel cavalry and northward-march report | Different from open p170 A; repairs and prose expansions explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p170 B2](cases/other/nov9_operational_reports.md) | Alpenkorps at Ujverbasz and the 9 November march | 117/119 raw positions; place fill and historical numeral separated | icekylinx and GPT-6 Astra Pro (2026) |
| [p172 A](cases/other/seifert.md) | Records destroyed; cipher keys still in personal custody | 67/68 positions; one supported erasure fill | icekylinx and GPT-6 Astra Pro (2026) |
| [p172 B](cases/other/seifert.md) | Immediate radio-listening instruction | Identical to p174 D; hundreds digit remains 5-9 | icekylinx and GPT-6 Astra Pro (2026) |
| [p174 B](cases/other/seifert.md) | Request notification when Seifert arrives | 36/37 raw positions; two glyph readings retained | icekylinx and GPT-6 Astra Pro (2026) |
| [p174 C](cases/other/seifert.md) | Query about Seifert's return | 24/24 positions; unchanged source roundtrip | icekylinx and GPT-6 Astra Pro (2026) |
| [p174 D](cases/other/seifert.md) | Repeated immediate listening instruction | Identical to p172 B; no digit inferred from repetition | icekylinx and GPT-6 Astra Pro (2026) |
| [p174 E](cases/other/seifert.md) | Seifert has departed | Two explicit coordinate repairs for the name | icekylinx and GPT-6 Astra Pro (2026) |
| [p180 A3](cases/other/p180_A.md) | Enemy follows withdrawal near Giurgiu; Braila and Focsani evacuated | 77/78 raw positions; nine substitutions and one fill | icekylinx and GPT-6 Astra Pro (2026) |
| [p181 A](cases/other/mackensen_warsaw.md) | Warsaw Soldiers Council asks about Mackensens advance | Prior query interpretation; later quote supplies one source erasure | Lasry, Niebel, Kopal and Wacker; source comparison: icekylinx and GPT-6 Astra Pro (2026) |
| [p185 C](cases/p189.md) | Vehicle provision impossible; await orders | Direct raw reading; source parallel for p 189 A | icekylinx and GPT-6 Astra Pro (2026) |
| [p185 D](cases/context/transport.md#p185-d-source-and-gap-model) | Movement via DHFN and readiness instruction | 91/99 positions under an unproved five-loss geometry | icekylinx and GPT-6 Astra Pro (2026) |
| [p186 A1](cases/context/p186.md#part-1--richi-170) | Monitor Russian and Polish army traffic | Earlier reading; three explicit erasure fills | Lasry team and Norbert (2017); review: icekylinx and GPT-6 Astra Pro |
| [p186 A2](cases/context/p186.md#part-2--richi-174) | Encrypted reporting and teleprinter failure | 80/87 conservative raw positions; ending unresolved | Lasry team and Norbert (2017); review: icekylinx and GPT-6 Astra Pro |
| [p187 C](cases/supplementary/p187_C.md) | Connection with Mackensen's army | Earlier reading; source correction checked | Ayush Agarwal; review by D. Bourdeau (2026) |
| [p189 C](cases/context/p189_C.md) | Instruction to use the December key; IRRTUM | 61/62 raw positions; two explicit substitutions | icekylinx and GPT-6 Astra Pro (2026) |
| [p189 E](cases/context/transport.md#independent-transport-context) | Pump, cars and trailers | Direct partial reading; counts unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p193 E](cases/context/transport.md#independent-transport-context) | Sprung cart for attachment; a car | Direct partial reading; one unknown cell | icekylinx and GPT-6 Astra Pro (2026) |
| [p194 A](cases/context/transport.md#independent-transport-context) | Arranged departure to Hanau via DHFN | Near-parallel; composite fixes 86/87 positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p196 B](cases/context/transport.md#independent-transport-context) | Repeated arranged departure to Hanau | Near-parallel; time digit remains unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p197 C](cases/context/transport_197_198.md) | Transport of radio equipment to Darmstadt | Missing-group hypothesis checked against p 198 B | icekylinx and GPT-6 Astra Pro (2026) |
| [p197 D](cases/context/transport_197_198.md) | Lorry, trailer and petrol-pump instruction | Partial witness; readable reconstruction costed | icekylinx and GPT-6 Astra Pro (2026) |
| [p197 E](cases/context/transport.md#independent-transport-context) | Lorry departure and men remaining until Sunday | Partial near-parallel; time and count unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p198 B](cases/context/transport_197_198.md) | Repeated equipment transport to Darmstadt | Clearer near-parallel; editorial changes explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p198 C](cases/context/transport.md#independent-transport-context) | Repeated lorry departure and Sunday stay | Direct partial reading; separate from challenge D | icekylinx and GPT-6 Astra Pro (2026) |
| [p198 E](cases/context/transport_197_198.md) | Repeated lorry, trailer and petrol-pump order | Literal duplicate-group deletion; partial reading | icekylinx and GPT-6 Astra Pro (2026) |
| [p201 B1](cases/other/p201_p206_orders.md) | Report positions reached and expected border crossings | 105/105 unchanged; clear source origin date 15 November | icekylinx and GPT-6 Astra Pro (2026) |
| [p201 B2](cases/other/p201_p206_orders.md) | Specify units and travel mode; acknowledge receipt | 86/89 raw positions; shared order reference with p206 | icekylinx and GPT-6 Astra Pro (2026) |
| [p203 C](cases/other/richter_aleppo.md) | Inquiry about Richter at the Aleppo radio park | 93/96 raw positions; postal digits remain coupled and unknown | icekylinx and GPT-6 Astra Pro (2026) |
| [p204 A](cases/other/p204_A.md) | Local radio station to be handed over to Poland | 69/70 raw positions; Monday 18 implies FD=8 conditionally | icekylinx and GPT-6 Astra Pro (2026) |
| [p205 A1](cases/other/p205_A.md) | Thirty-million-kroner request; shortage of banknotes | 118/118 raw positions; explicit word repairs | icekylinx and GPT-6 Astra Pro (2026) |
| [p205 A2](cases/other/p205_A.md) | Vienna bank transfer to Kronstadt for German administration | 152/152 raw positions; explicit word repairs | icekylinx and GPT-6 Astra Pro (2026) |
| [p205 A3](cases/other/p205_A.md) | Initial five million in mixed denominations; confirm sufficiency | 117/117 raw positions; unchanged source | icekylinx and GPT-6 Astra Pro (2026) |
| [p205 A4](cases/other/p205_A.md) | Further requests to the General War Treasury; reference digits | 94/99 raw positions; reference digits unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p205 B1](cases/other/p205_B.md) | End submissions to the dissolved Naval Warfare Command | 160/160 raw positions; unchanged source | icekylinx and GPT-6 Astra Pro (2026) |
| [p205 B2](cases/other/p205_B.md) | Continue keeping war diaries; naval reporting addressees | 109/111 raw positions; reference digits unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p206 A1](cases/other/p201_p206_orders.md) | Confirm receipt of earlier departure and reporting orders | 175/184 raw positions; complete source part reassembled | icekylinx and GPT-6 Astra Pro (2026) |
| [p206 A2](cases/other/p201_p206_orders.md) | References to disarmament, armistice and position-report orders | 179/200 raw positions; shared reference/date conditionally implies VA=5 | icekylinx and GPT-6 Astra Pro (2026) |
| [p206 A3](cases/other/p201_p206_orders.md) | Report division locations and acknowledge the present order | 115/124 raw positions; duplicated wording and unknown serial retained | icekylinx and GPT-6 Astra Pro (2026) |
| [p210 A1](cases/other/p210_A.md) | Helsinki: confirm return transport for the Ostsee Division | 93/93 raw positions; one adjacent-coordinate swap | icekylinx and GPT-6 Astra Pro (2026) |
| [p210 A2](cases/other/p210_A.md) | Ships may be sent; identify a suitable embarkation port | 115/115 raw positions; two explicit substitutions | icekylinx and GPT-6 Astra Pro (2026) |
| [p210 B](cases/other/p210_B.md) | End of Consul Burkhardt's oil-company assignment | 158/158 raw positions; five word repairs; date labels literal | icekylinx and GPT-6 Astra Pro (2026) |
| [p210 C](cases/other/richter_aleppo.md) | Fuller inquiry about NCO Kurt Richter in Aleppo | 201/204 raw positions; six substitutions and three fills | icekylinx and GPT-6 Astra Pro (2026) |
| [p210 D](cases/other/p210_D.md) | Request for a report on the situation in Reval | 58/58 raw positions; one explicit word repair | icekylinx and GPT-6 Astra Pro (2026) |
| [p211 B lower1](cases/other/p211_key_schedule.md) | Retain the November Ringbahn key | 107/107 raw positions; three spelling repairs explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p211 B lower2](cases/other/p211_key_schedule.md) | Use November keys for December traffic | 92/92 unchanged; first and last schedule dates stated | icekylinx and GPT-6 Astra Pro (2026) |
| [p211 B lower3](cases/other/p211_key_schedule.md) | Schedule endpoint and receipt acknowledgment | 66/67 raw positions; one invalid-glyph fill | icekylinx and GPT-6 Astra Pro (2026) |
| [p214 B](cases/other/mackensen_warsaw.md) | Forwarded quotation of the Warsaw query | 85/92 direct quote positions match p181 under a different key | icekylinx and GPT-6 Astra Pro (2026) |
| [p217 A1](cases/other/p217_A.md) | Scholtz divisions march into the assembly area | 114/114 baseline positions; unit-number interpretation separate | icekylinx and GPT-6 Astra Pro (2026) |
| [p217 A2](cases/other/p217_A.md) | Coal shortages stop transport; troop locations near Oroshaza | 120/120 baseline positions; unit-number interpretation separate | icekylinx and GPT-6 Astra Pro (2026) |
| [p217 A3](cases/other/p217_A.md) | Army headquarters at Szolnok; battalions apparently misdirected | 114/114 baseline positions; place and numerical fields unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p217 A4](cases/other/p217_A.md) | Czechs demand disarmament before troop transit | 98/98 raw positions; two word repairs | icekylinx and GPT-6 Astra Pro (2026) |
| [p217 A5](cases/other/p217_A.md) | Massow in Budapest asked to clarify transit and disarmament | 61/61 raw positions; two word repairs; reference unresolved | icekylinx and GPT-6 Astra Pro (2026) |
| [p218 A1](cases/other/p218_A.md) | Kress/Tiflis notice: armistice Article XII | 140/141 raw positions; article-number repair explicit | icekylinx and GPT-6 Astra Pro (2026) |
| [p218 A2](cases/other/p218_A.md) | Allied judgment governs withdrawal from former Russian territory | 141/142 raw positions; four substitutions and one fill | icekylinx and GPT-6 Astra Pro (2026) |
| [p218 A3](cases/other/p218_A.md) | No Allied demand yet to withdraw the Tiflis guard | 138/139 raw positions; two substitutions and one fill | icekylinx and GPT-6 Astra Pro (2026) |
| [p225 A](cases/other/late_november_cipher_instructions.md) | November key material retained because December tables are absent | 110/116 raw positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p226 B2](cases/other/late_november_cipher_instructions.md) | Numerical sequences read backward; missing first part | 104/104 raw positions; separately costed word repairs | icekylinx and GPT-6 Astra Pro (2026) |
| [p226 C1](cases/other/mackensen_internment.md) | Mackensen internment: Entente demands and withdrawal assurances | 172/172 raw positions; separately costed word repairs | Prior body: Lasry et al. (2016); source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p226 C2](cases/other/mackensen_internment.md) | Internment explained as a response to continued marching orders | 162/162 raw positions; separately costed word repairs | Prior body: Lasry et al. (2016); source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p226 C3](cases/other/mackensen_internment.md) | Promise of decent internment conditions and eventual return | 168/169 raw positions under local group-length repair | Prior body: Lasry et al. (2016); source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p227 A4](cases/other/mackensen_internment.md) | Preserve calm and order during Mackensen internment | 196/196 raw positions; separately costed word repairs | Prior body: Lasry et al. (2016); source edition: icekylinx and GPT-6 Astra Pro (2026) |
| [p227 B](cases/other/late_november_cipher_instructions.md) | Send telegrams for the army and subordinate formations directly | 76/76 raw positions; separately costed word repairs | icekylinx and GPT-6 Astra Pro (2026) |
| [p228 C1](cases/other/late_november_cipher_instructions.md) | December key agreement involving UKS, ZOEN and BSL | 88/88 raw positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p228 C2](cases/other/late_november_cipher_instructions.md) | Use the same key in BSL–UKS traffic; UKS agrees | 72/72 raw positions | icekylinx and GPT-6 Astra Pro (2026) |
| [p230 A3](cases/other/p230_A.md) | Division locations near Hermannstadt and Muehlbach | 116/116 baseline positions; seven substitutions; conditional unit labels | icekylinx and GPT-6 Astra Pro (2026) |
| [p230 A4](cases/other/p230_A.md) | Forces near Kronstadt and Fogaras; OKM headquarters moves | 115/115 baseline positions; one substitution; conditional unit labels | icekylinx and GPT-6 Astra Pro (2026) |

The catalogue covers source-reviewed records with published reading evidence; the wider OCR search pool contains additional unreviewed ciphertext candidates. Earlier authors retain their credits. Current source review and new research use **icekylinx and GPT-6 Astra Pro**; a review credit does not assert first-decipherment priority.
<!-- READING-CATALOG:END -->

## Review coverage

The [review ledger](data/review_ledger.json) currently records **104 claims and provenance checks**. It includes the 2017 comment history, earlier square completions, p217's published key images and naval corroboration, p176b's French documentary context, the newly checked October 2026 submissions, and the historical reading of p158's component.

A September 2026 mass-solution claim is retained with its [reproducibility assessment](data/reviews/unsupported_claim_checks.json) and **Jozef Krajcovic's earlier critique**. Its published constants and selected substrings do not provide a reproducible full reading; no target is marked solved on that basis.

## Verify

Python 3.10 or later; standard library only:

```sh
python3 -m adfgvx.verify
python3 -m adfgvx.verify --json
```

This checks the core source, cipher and reconstruction certificates, including 25 explicit repair variants of 14 earlier-readable entries and the three supplementary records. It reproduces source maps, retained-coordinate roundtrips, uncertainty domains and contradictory editorial completions. Odd-length ciphertext cannot silently lose a coordinate.

The [verification workflow](.github/workflows/verify.yml) also runs focused transport, p153 linked-field/key-structure, p215 interpretation, p109 ranking-summary and recorded open-target checks. Individual case and experiment pages provide their commands. Rebuilding corpus models or rerunning large searches is documented separately from checking the compact certificates.

## Search methods

The [experiment index](experiments/README.md) records completed search bounds, positive controls, scoring failures, and reproducible code. The p153 work enumerates column-length segmentations at widths 14, 16 and 18, then uses bounded pairing, order and square searches. The width-18 refinement produced the new partial reading. A separate exact post-discovery crib check, independently implemented twice, establishes its narrow key-equivalence and emendation constraints. Complete checks over every integer width from 14 through 26 leave only width 18 for the sixty-letter crib.

The [multi-witness decoder](experiments/parallel_decoder/README.md) adds exact language-ranked optimization under a declared source-edit budget. For p109, dynamic programming covers all `2^42` minimum-cost plaintexts without a beam or a plaintext crib. Its successes, model failures, 280 ranked candidates and word-level costs are retained together.

The [joint scattered-loss decoder](experiments/p198_joint_exact/README.md) exactly optimizes both missing positions and their values. For p198's five-loss hypothesis it covers 8,670,506,592,384 witnesses per fixed complete key, including aliases. Its four-gram controls expose wrong global optima even under true keys; those failures and all source-preserving witnesses are retained. The [p73 coordinate-count diagnostic](experiments/open_targets/P73_HISTOGRAM.md) provides a separate, transposition-independent way to prioritize key hypotheses.

The [six-gram extension](experiments/p198_joint_six/README.md) recovers one complete control, its exact loss positions and their values under two objectives. A second control still has a better-scoring wrong competitor. These calibrated successes and failures guide further attacks without changing the historical target statuses.

The [exact digit/Q/Y frontier](experiments/p198_category_frontier/README.md) supplies a language-model-free constraint on all 40,320 completions of one p198 partial key: an 85-character reading with just three digits must have at least thirteen Q/Y positions; a Q/Y-free reading needs at least ten digits. Two implementations recompute the full finite scope, and concrete witnesses attain every reported boundary point. This sharpens future proposal checks without declaring a plaintext or excluding the key.

## Contents

- `cases/`: Readings, qualifications, original credits, and source links
- `docs/research-status.md`: Current result boundaries and the next evidence or method that could reduce ambiguity
- `docs/methods.md`: A reader's guide to the cipher, evidence layers, exact searches and their limits
- `data/messages.json`: All 22 source records, legacy transcriptions, and conservative analysis layers
- `data/keys.json`: 25 historical, comparison, reported, or newly recovered partial keys; provenance and unknown cells retained
- `data/prior_readings.json`: 35 attributed earlier readings/fragments and 25 recomputed repair variants
- `data/supplementary_readings.json`: Three October 2026 readings and their primary-source corrections
- `data/review_ledger.json`: Claim-by-claim findings, earlier criticism, and exact attribution
- `data/certificates/`: Machine-readable source, edit, and plaintext evidence
- `adfgvx/`: Independent cipher and verification code
- `experiments/`: Portable attacks, bounded results, controls, and model provenance
- `sources/`: Bibliography and selected source excerpts

Identifiers use the printed page number. `p187` and `p187b` are the two parts listed separately in the original challenge. A question mark means unresolved evidence, never an arbitrary completed square cell. Original German text is preserved as data; editorial material is in English.

## Citation and reuse

icekylinx and GPT-6 Astra Pro. *ADFGVX Cipher* (2026). Cite the relevant case and commit using [CITATION.cff](CITATION.cff). Historical records, prior decipherments, key recovery, and later corrections retain their individual attribution. The [Apache-2.0 license](LICENSE) covers this project's code and editorial contributions; third-party materials retain their original status. See [NOTICE](NOTICE) and [Contributing](CONTRIBUTING.md).
