# October Caucasus traffic — Kress, Westernhagen and a shipment for Poti

[All readings](../README.md) · [ADFGVX Cipher](../../README.md) · [Source and verification](../../experiments/october_caucasus/README.md)

**Source edition and repair analysis:** icekylinx and GPT-6 Astra Pro. **Earlier key:** the published October 4–6 square and 22-column transposition, credited to Childs and George Lasry / Lasry, Niebel, Kopal and Wacker in the [key catalogue](../../data/keys.json).

Nine source-reviewed parts recover five exchanges about the Caucasus: personnel and money for Kress's delegation, price instructions to Westernhagen, electrical equipment sent to Tiflis, a cargo leaving Braila for Poti, and radio timings. An interrupted continuation is retained separately without an accepted reading. The German readings below use explicit editorial repairs. Every received coordinate, surviving garble, ambiguous layout and repair cost is retained in the [certificate](../../experiments/october_caucasus/certificates.json). This is a new reproducible edition in this repository, without a first-historical-decipherment claim.

## p72 A — Reinforcements, administrative personnel and money for Kress

**Source:** printed p. 72 / PDF p. 75, section A, three parts. `COS v OSM (--------, October 9th); NR 294 KRESS (6) 2040 3 TLE`. The heading is **6 October 1918**. The clear route is OSM to COS, with Kress named in the header; it does not make Kress the sender.

### Most likely readable German

> Zu Tel. 30.9. [NATEKS] Nr. 8557. 1. Verstärkung der Deleg. von O.H.L. ohne Beteiligung [… K.M.] angeordnet. 2. Mit Bericht vom 8.[?], [4A] Nr. 553 angeford. Verw.-Pers. wird mit Ausnahme der Garnison-Verw.-Beamten — vergl. Tel. 26.[?], [unresolved reference] — zur Verfügung gestellt werden. 3. Notwendiges Geld ist sichergestellt.

**Meaning:** Reinforcement of the delegation has been ordered by Supreme Army Command, without the participation of an office whose abbreviation is damaged. Requested administrative personnel will be made available, except for garrison-administration officials. Necessary money has been secured.

`Deleg.`, `O.H.L.`, `Verw.-Pers.` and `Garnison-Verw.-Beamten` are expanded only in the explanation. The reference text `NATEKS`, the raw `?SKXM` office abbreviation, and several dates and numbers remain unresolved. The edition does not identify a particular ministry or assign the damaged reference digits.

### What the three source parts preserve

| Part | Literal / interpreted coordinates | Fixed raw positions | Source issue | Additional editorial cost |
|---|---:|---:|---|---:|
| A1 | 203 / 178 | 88/89 | The second copy of an identical 25-coordinate run is visibly struck out. | 1 known-coordinate substitution; no asserted fill |
| A2 | 251 / 226 | 108/113 common to both models; 109/113 in one model | An unmarked 25-slot near-repeat; two deletion alternatives remain. | 6 substitutions; 1 or 2 asserted fills |
| A3 | 124 / 124 | 60/62 | Two invalid/missing source coordinates; unchanged geometry | 4 substitutions; 2 fills |

The A1 strikeout is a source instruction. The A2 deletion is a reconstruction hypothesis: its adjacent copies differ only by a printed `X` versus a non-coordinate `S`. Removing either copy gives the same raw text except for `GARNISON` versus `G?RNISON`. Both are kept; the latter does not become an independently witnessed `A`.

The raw core is already recognizable as `VERSTAER1UNGDERDELEGXVONOXHXLXOHNEBETEILIGUNG...ANGEORDNET`, and A3 directly contains `ZURVERFUEGUN...GESTELLT...` and most of `NOTWENDIGESGELDISTSICHERGESTELLT`. The stated costs account for making those words readable; the uncorrected strings remain in the certificate.

## p70 A — Westernhagen, price limits and an urgent return

**Source:** printed p. 70 / PDF p. 73, section A, two parts. `POT, COS v NKJ (3.10 a.m., October 7th); FUR COS DEUTSCHE DELEGATO WIRTCHI ABTLG 2305 (6) 2 TLE`.

### Most likely readable German

> An Westernhagen. Bestätigen Telegr. 28.9. Euer früheres Telegr. nicht erhalten. Da von euch ohne Bericht und Kenntnis dortiger Marktlage gelassen, können Preisgrenzen nicht aufgeben. Mdl. Rücksprache sofort erforderlich. Bitten Rückkehr beschleunigen. Drahten Gleiches über ASTO Constanza. Bestätigt Empfang. Deutkauf.

**Meaning:** A telegram of 28 September is acknowledged, but an earlier one was not received. Without the requested report or knowledge of local market conditions, the sender cannot give price limits. An immediate personal discussion is needed; Westernhagen is asked to hasten his return. The same instruction is being telegraphed via `ASTO Constanza`, and receipt is to be acknowledged.

The source names only **Westernhagen**. `MDL` is interpreted as *mündliche*; `ASTO` and the signature `DEUTKAUF` are retained without an institutional expansion. The encrypted spelling is `RUECKEHR` with one `K`; ordinary German spelling in the displayed reading supplies the second `k` as a prose normalization. The unusual but directly decoded `AUFGEBEN` remains; the edition does not silently substitute a more idiomatic verb.

| Part | Literal / interpreted coordinates | Fixed raw positions | Source issue | Additional editorial cost |
|---|---:|---:|---|---:|
| A1 | 332 / 322 | 156/161 | Two separate identical five-coordinate pairs: `AAAAA AAAAA` and `DAAGG DAAGG` | 7 substitutions; 5 fills |
| A2 | 246 / 246 | 121/123 | Header says `RICHI-256`; the printed 246-slot body decodes at its actual length | 4 substitutions; 2 fills |

Removing one copy of each repeated A1 group gives four source-index aliases and **one identical 322-coordinate stream**. Those deletions are conditional, despite the visible repetition. A2 is not padded by ten invented coordinates to force its length to match the header: its raw reading already begins `MDLXRUECKSPRACHEDOFORTERFORDERLICH...` and ends `...EMPFANGXDEUTKAUF` at 246 slots.

## p71 A1 — Electrical equipment sent to Tiflis

**Source:** printed p. 71 / PDF p. 74, section A, first of two parts. `POT v OSM (01.17 a.m., October 8th); FUR COS (6) 1230 2 TEILE; 1 TL RICHI-170`. The page heading is **6 October 1918**.

### Most likely readable German

> Nach Tiflis abgegangen 28.9., mit 2 Begleiter: 2 Stück 16-kW-Maschinensätze und 1 20-kW-Umformer.

**Meaning:** Two machine sets rated at 16 kW and one converter, provisionally read as rated at 20 kW, were dispatched to Tiflis on 28 September with two accompanying people. The directly decoded telegraphic form is `BEGLEITER`; no grammatical final `N` is inserted into the cipher edition.

The literal **170 slots** have unchanged geometry and fix **72/85 raw positions**. Twelve printed dashes and one damaged `C`-shaped glyph in row one's last group are treated as erasures. That glyph may be an incomplete `G`, but the raw letter domain remains open. The proposed reading fills all **13 erasures** and changes **one known coordinate**, source slot 40 from `G` to `X`, to repair the raw `GEGA?BEN` fragment to `GEGANGEN`. All slot and plaintext positions in the certificate are zero-based.

The two equipment counts, the **16-kW** rating, and the date digits `28` and `9` survive directly. The **2** in the proposed **20-kW** rating is an erasure fill, so the exact second rating is conditional. The raw ending is `...UND1??0KX?XUMFORMER`, not a fully recovered numerical specification.

Part A2 advertises **192 coordinates** but stops after **85**, followed by the printed note `(interference)`. Under the simple hypothesis that the lost suffix supplies the remaining 107 slots, no complete plaintext letter is fixed: each surviving symbol supplies only one side of a coordinate pair. Its literal fragment and conditional letter domains are preserved separately. It contributes neither a new accepted reading nor inferred equipment details.

## p69 B — Violetta's cargo from Braila to Poti

**Source:** printed p. 69 / PDF p. 72, section B, two parts. `COS v NKJ (---- October 11th); NR 298 FUR COS HPTM GEMOLL (6) 2330 2 TLE`. The page heading says **5 October**, while the individual clear header says `(6)`; both are preserved.

### Most likely readable German

> Ab Braila 4.10. mit D. Violetta: 10 000 Eierhandgranaten, 3 Wagen Masch.-Gew., [04WLI] russ. Gew., 9 Wag. Mun., [94TS6] Lebensmittel, 16 Faß Benzin, 2 Kisten Kuriergepäck, 10 Wag. Mun. für Mun.-Dep. Poti und mehrere Wag. für dort. Truppen.

**Meaning:** A cargo sent from Braila aboard the vessel *Violetta* includes hand grenades, machine guns, Russian rifles, ammunition, food, petrol and courier luggage. Poti's ammunition depot and troops there are named as destinations. Two damaged quantity fields are unresolved. The proposed **10 000** hand grenades is also conditional: the common raw reading is `100?0`, and the fourth digit depends on the declared alignment and an erased-coordinate fill. It is not an independently established exact quantity.

The displayed **4.10.** date and several words are editorial repairs. `04WLI` and `94TS6` are raw garbles, not accepted quantities; no numerical expansion is supplied for them. `D.`, `Masch.-Gew.`, `russ. Gew.`, `Wag.` and `Mun.-Dep.` are interpreted in their cargo context. The text does not independently establish the ship's registry or the nature of the wagons carried.

| Part | Literal / interpreted coordinates | Raw positions fixed across every tested placement | Source issue | Minimum additional editorial cost |
|---|---:|---:|---|---:|
| B1 | 329 / 330 | 159/165 | Four-letter group `VXFX`; insert one erased slot at any of its five boundaries | 9 substitutions; 2 fills |
| B2 | 65 / 66 | 28/33 | Four-letter group `(X)FFF`; insert one erased slot at any of its five boundaries | 1 substitution; 1 fill |

These models supply a slot because a printed group is short and the header is one longer. They do not prove that the historical loss occurred there. In B1 the editorial template has two tied minimum-cost placements. In B2, the proposed complete continuation is

```text
UNDMEHREREWAGXFUERDORTXTRUPPENXXX
```

It replaces the short printed `XFFF` by `GDFFF`: either insert `G` before the printed `X` and change that `X` to `D`, or change `X` to `G` and insert `D` after it. Both have exactly one known-coordinate substitution and one missing-coordinate fill. All five within-group placements, including the more expensive ones, remain in the certificate.

## p72 B — Radio timings and reception

**Source:** printed p. 72 / PDF p. 75, section B. `POT v OSM (---------, October 9th); FUR POT (6) 0830; RIZI-274`. The source prints `RIZI`; that label is not silently rewritten as `RICHI`.

### Most likely readable German

> Zu dort Nr. 479: 20.00, 20.30 für OSM ungeeignet. Sind Sie mit RICHI [M98], 30.9., mitgeteilten Zeiten einverstanden? Wie ist dort Empfang OSM, Welle 2800 und 3500? Schlee.

**Meaning:** The proposed times are unsuitable for OSM. The recipient is asked whether the previously notified times are acceptable and how OSM is received at two wavelengths.

The unchanged 274-coordinate geometry fixes **136/137 raw positions**. The displayed `NR`, `2000`, `SIE` and `3500` require **four known-coordinate substitutions**, with one additional erased-coordinate fill for `ZU`. The first time and second wavelength are plausible editorial values, not independently recovered numerical facts. `2030`, `2800` and `SCHLEE` are directly decoded; the damaged reference `RICHIM98` is left unresolved.

## Relation to the open p73 challenge

These messages add readable traffic from the Kress/Caucasus route, with explicit October origin and later interception dates. They supply neither p73's key nor a matching plaintext passage. **p73 remains open**; the source-level repairs here do not decide between its conflicting 26 October and 8 November date layers.
