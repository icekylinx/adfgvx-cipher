# Post-publication source-recovery review

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

**Reviewed source inventory.** Work-period metadata and earlier snapshots are retained in `inputs.json`.

## Reviewed artifact refresh on 4 November 2026

Later source supplements changed five case-page prose sections and two generated
presentation artifacts. The [exact refresh audit](artifact_refresh_20261104.json)
records all seven before/after byte hashes, reversible changed-text spans,
unified diffs, review reasons and separately hashed source-package evidence.
The [original inputs](artifact_refresh_20261104_before_inputs.json) and
[original inventory](artifact_refresh_20261104_before_inventory.json) are
preserved byte-for-byte. Their catalogue snapshots, coverage counts, source
packages and timing metadata remain unchanged.

The refresh changes only those seven expected artifact hashes and adds four
review-evidence artifacts to the pin map. It does not exempt any original path
from hashing. All original fenced displays and headings in the five changed
case pages are unchanged. The reading-layer manifest retains every earlier
role, display and review-basis record; its updates are case-file hashes and the
separately reviewed p84 and p163 A16 pages. The live coverage dashboard adds
one conditional physical-source edition, p163 A16: 121 received coordinates
in a 286-slot frame with 165 hypothesized leading losses, 0 fixed raw labels
and a separately counted 59-label candidate. The verifier reverses this one
source contribution and the catalogue digest to recover the originally
pinned dashboard byte-for-byte. Its 679-body census denominator is unchanged.

The standard inventory verifier remains byte-identical. Run the additional
check with:

```sh
python experiments/post_push_review/verify_artifact_refresh.py
```

This check reconstructs each original pinned artifact from the reviewed current
text and exact inverse spans, verifies its original digest, checks the complete
old-to-new pin map, and proves that the preserved inventory changed only its
input digest and artifact count. It requires no historical checkout or network
access. New reading claims and their repair prices remain in the linked source
packages. The preserved inventory adds no source or raw plaintext count;
the independently recomputed live dashboard adds the one conditional A16
source edition and keeps its supplied labels outside the raw total.

## Current preserved inventory

This snapshot compares **195 → 631 other reviewed catalogue entries**, with all
22 challenge entries preserved. It adds **436 catalogue entries across 148 source
packages**, representing **435 newly catalogued physical sources** and one later
edition of an existing source. Across the challenge and other tables together,
there are **652 unique physical sources**; **630** are additional to
the challenge set. [p132_B is a later edition of challenge p132](../../docs/catalogue-source-overlaps.md),
with Thomas and Norbert's original reading credit retained. It adds a reviewed
entry but no new physical source. Interpretation and open-target method audits
also add no physical sources.

The source packages account for **89,654 literal source slots** and
**45,171 modeled plaintext positions**, of which
**43,349 have fixed raw labels** under their stated frames.
These are coverage counts, including repeated copies, prior body readings,
conditional frames, the later p132 edition and unresolved historical numerals.
They are not a count of first decipherments or independently authenticated
historical letters. All **902 observed-coordinate substitutions** remain separately priced.
Printed-mask fills, missing-slot fills, copied prefixes and source-layout
exclusions keep their distinct units in each package. In particular, the
copy-conditioned p157 A1 record contributes **0/95 fixed raw positions**;
its copied values are excluded from the fixed-raw total.

The p158 E1 parallel contributes **116 fixed raw positions** with the added
slot unassigned. Its independently witnessed A supplies **one additional
fixed position**, recorded separately as source-linked completion; the
package's displayed 117-position baseline remains unchanged. This one
position is excluded from the cumulative fixed-raw total.

The p162/p166 wire-report family contributes **205 directly fixed raw labels** across its three new source bodies. Its **157 additional source-linked fixed labels** are separate: 156 depend on the copied p166 prefix and one on an independently witnessed missing X. The six changed observed coordinates are charged once at their original source locations, including the three donor-prefix word repairs. These linked completions are excluded from the cumulative fixed-raw total.

## Source packages

| Package | Reviewed source entries | Source slots | Modeled positions | Fixed raw labels | Observed substitutions |
|---|---:|---:|---:|---:|---:|
| [Crown airlift and an interrupted banknote instruction](../crown_airlift/README.md) | 3 | 371 | 195 | 175 | 1 |
| [Repeated ZITAG stop-order and contract cancellation](../zitag_purchase_orders/README.md) | 5 | 1068 | 534 | 531 | 14 |
| [Military meal allowances and a refused supplement](../military_allowances/README.md) | 4 | 1760 | 880 | 877 | 10 |
| [Six-part Orient intelligence report](../orient_intelligence/README.md) | 6 | 2020 | 1010 | 1009 | 4 |
| [Liman troop-report request, p222 A](../liman_troop_reports/README.md) | 2 | 414 | 207 | 207 | 1 |
| [Military-intendant addresses and responsibilities, p202 B](../military_intendant_remit/README.md) | 4 | 877 | 441 | 421 | 10 |
| [Neuhof demobilization instruction, p228 B](../neuhof_demobilization/README.md) | 3 | 696 | 348 | 298 | 10 |
| [Recall of the Turkish military mission](../turkish_mission_recall/README.md) | 4 | 1290 | 645 | 645 | 3 |
| [Hungary transport warning: a witnessed missing group](../hungary_transport_warning/README.md) | 6 | 877 | 441 | 405 | 2 |
| [September radio listening and acknowledgment procedure](../september_radio_procedure/README.md) | 3 | 556 | 278 | 275 | 3 |
| [Rail, motor and air transport on 30 November](../late_transport_dispatches/README.md) | 6 | 1442 | 721 | 677 | 14 |
| [Armistice transit and withdrawal planning, pp125-126](../armistice_transit_planning/README.md) | 7 | 1537 | 769 | 764 | 10 |
| [DEUTZITAG dispatch inquiries and an adjacent Tiflis order](../deutzitag_dispatch_inquiries/README.md) | 4 | 1018 | 509 | 509 | 1 |
| [Constanza naval-radio and telephone connections](../constanza_radio_connections/README.md) | 6 | 1308 | 654 | 654 | 5 |
| [Mackensen armistice appeal: six-part source edition](../mackensen_armistice_appeal/README.md) | 6 | 1352 | 681 | 667 | 24 |
| [Berlin newspapers via Orsova](../newspaper_dispatch/README.md) | 2 | 386 | 193 | 190 | 6 |
| [Companions to Norbert's p171 A1 ruble-rate reading](../ruble_rate_companions/README.md) | 2 | 413 | 202 | 196 | 6 |
| [Reconciling the Namur personnel-order witnesses](../namur_order_witnesses/README.md) | 2 | 494 | 252 | 237 | 11 |
| [Medical arrangements for transports returning from Turkey](../medical_return_transports/README.md) | 5 | 1437 | 721 | 712 | 24 |
| [Reval: steamers for troops, provisions and raw materials](../reval_steamer_notice/README.md) | 3 | 570 | 285 | 281 | 4 |
| [Mackensen withdrawal report: source edition and ninth-part assembly](../mackensen_withdrawal_report/README.md) | 12 | 2838 | 1451 | 1334 | 25 |
| [November radio service and document destruction](../november_radio_service/README.md) | 4 | 781 | 390 | 386 | 11 |
| [p212 A2 / p218 A2: a truncated copy across conflicting page dates](../p212_p218_crosscopy/README.md) | 1 | 160 | 142 | 30 | 1 |
| [Source editions of the p179 November instructions](../november_armistice_orders/README.md) | 5 | 1063 | 529 | 511 | 11 |
| [Radio-telegram priority: p128 A1 and A2](../radio_telegram_priority/README.md) | 2 | 508 | 254 | 247 | 6 |
| [Formation dissolution: Childs p83 B](../formation_dissolution/README.md) | 1 | 336 | 168 | 168 | 0 |
| [Odessa / Nikolaiev shipping instruction: Childs p98](../black_sea_disembarkation/README.md) | 3 | 782 | 391 | 391 | 7 |
| [Cash transport through Szolnok, Arad and Hermannstadt](../hermannstadt_cash_transport/README.md) | 2 | 391 | 196 | 193 | 5 |
| [Wallachia withdrawal preparations: p150 B1–B5](../wallachia_withdrawal_preparations/README.md) | 5 | 1012 | 506 | 466 | 9 |
| [Sale of communication apparatus: p157 B1–B2](../apparatus_sale_request/README.md) | 2 | 442 | 221 | 202 | 6 |
| [Radio contacts, key availability and neighboring source records](../radio_contacts_and_keys/README.md) | 7 | 1290 | 645 | 642 | 13 |
| [Hermannstadt radio setup and a request for armistice clarification](../hermannstadt_radio_report/README.md) | 4 | 932 | 465 | 464 | 12 |
| [Siegfried and Osthoff: later military-mission recall messages](../military_mission_recalls/README.md) | 4 | 802 | 401 | 394 | 6 |
| [Constantinople addresses, signatures and receipt instructions](../constantinople_address_parts/README.md) | 3 | 526 | 263 | 262 | 2 |
| [An instruction to decipher from opposite ends](../bidirectional_deciphering/README.md) | 1 | 105 | 52 | 51 | 2 |
| [Retrieved copies: banknote completion and armistice clauses](../retrieved_copy_editions/README.md) | 3 | 444 | 222 | 221 | 3 |
| [Palestine medical formations and p83 dissolution antecedent](../palestine_medical_dissolution/README.md) | 2 | 598 | 299 | 298 | 0 |
| [Second source witnesses of the newspaper-dispatch request](../newspaper_dispatch_witnesses/README.md) | 2 | 386 | 193 | 143 | 8 |
| [Inventory and medical-return source records](../inventory_and_medical_return/README.md) | 3 | 665 | 333 | 332 | 6 |
| [Surviving parts of an eight-part Transylvania situation report](../transylvania_situation_report/README.md) | 5 | 1057 | 550 | 499 | 6 |
| [Childs p188: conditional armistice request and native provisions fragments](../armistice_provisions_requests/README.md) | 3 | 669 | 334 | 319 | 29 |
| [Native p209 transport and disarmament traffic](../transport_and_disarmament_orders/README.md) | 5 | 1188 | 594 | 586 | 15 |
| [Source editions: equipment disposal and troop return on pp207–208](../repatriation_orders/README.md) | 7 | 1589 | 794 | 753 | 11 |
| [Delegation travel and Danube field reports, 10–11 November](../nov10_delegates_and_field_report/README.md) | 4 | 820 | 410 | 408 | 10 |
| [Upper p211: Oderberg fragment and troop-situation query](../prague_route_and_situation/README.md) | 2 | 244 | 122 | 122 | 3 |
| [Romanian ultimatum and Danube crossing: companions of p176a](../romanian_ultimatum_companions/README.md) | 3 | 588 | 294 | 284 | 6 |
| [November 3 radio, morning and pioneer reports](../nov3_radio_and_pioneer/README.md) | 3 | 828 | 414 | 412 | 10 |
| [p175 C3: withdrawal from the Danube and Sereth front](../p175_c3_gap_followup/README.md) | 1 | 217 | 111 | 102 | 4 |
| [p175 B2: payments and cheque acknowledgements](../hauptwechselamt_accounting/README.md) | 1 | 204 | 102 | 90 | 4 |
| [p64: the Nobel oil inquiry and the Damascus radio report](../p64_oil_and_radio/README.md) | 3 | 876 | 438 | 436 | 10 |
| [Late October radio service and Caucasus hide purchasing](../late_october_radio_and_materials/README.md) | 8 | 1612 | 796 | 765 | 11 |
| [November 3 medical, radio and withdrawal source editions](../nov3_medical_radio_withdrawal/README.md) | 5 | 921 | 458 | 455 | 3 |
| [September receipt and front-news inquiry](../september_receipt_and_front_inquiry/README.md) | 2 | 320 | 160 | 158 | 4 |
| [p97: wireless routing, repetition and supplies](../hungary_connection_and_supplies/README.md) | 3 | 638 | 319 | 319 | 6 |
| [Poti horse-delivery continuations](../poti_horse_delivery/README.md) | 2 | 450 | 225 | 188 | 20 |
| [Major Dunst: cancellation of the Turkey assignment](../dunst_assignment/README.md) | 2 | 747 | 373 | 373 | 4 |
| [Mecklenburg inquiry and Seeflugstation Ost personnel order](../mecklenburg_and_seaplane_personnel/README.md) | 3 | 1066 | 533 | 525 | 11 |
| [November 3 evening-report copies and November 4 radio notices](../nov3_evening_and_nov4_radio/README.md) | 7 | 1258 | 635 | 577 | 16 |
| [Turkish armistice report and shipping order](../turkish_armistice_shipping_order/README.md) | 3 | 918 | 459 | 459 | 11 |
| [Five-part Black Sea evacuation routing order](../black_sea_evacuation_routes/README.md) | 4 | 1314 | 707 | 609 | 8 |
| [Caucasus radio transmitters: typed and annotated source layers](../caucasus_radio_transmitters/README.md) | 2 | 306 | 153 | 151 | 3 |
| [November 1 contact times, service mail and the Sava evening report](../nov1_contact_mail_and_sava/README.md) | 5 | 643 | 322 | 279 | 3 |
| [End-of-October premium-payment order](../premium_payment_stop/README.md) | 2 | 410 | 205 | 205 | 0 |
| [Tiflis request for repetition of an encrypted telegram](../tiflis_repetition_request/README.md) | 1 | 314 | 157 | 157 | 2 |
| [November 8 radio-key instructions, apparatus prices and reports](../nov8_radio_keys_and_reports/README.md) | 7 | 1327 | 662 | 643 | 11 |
| [p108: naval inquiry and personnel-discharge order](../p108_naval_and_personnel/README.md) | 3 | 547 | 274 | 273 | 0 |
| [p107 railway instructions and dragoman-return inquiry](../p107_railway_and_dragoman/README.md) | 3 | 622 | 311 | 310 | 12 |
| [November 1 Mackensen and Orient reports](../nov1_mackensen_and_orient_reports/README.md) | 8 | 1395 | 695 | 659 | 19 |
| [p102 C/D: ammunition loading and leave arrangements](../nov1_ammunition_and_leave/README.md) | 2 | 520 | 260 | 260 | 0 |
| [Three-part report and request concerning Hungarian armistice negotiations](../hungarian_armistice_instructions/README.md) | 3 | 666 | 333 | 333 | 6 |
| [Sevastopol routing amendment with opaque numerical groups](../sevastopol_coded_routing/README.md) | 3 | 632 | 316 | 315 | 0 |
| [p162: map sheets, Tiraspol border fire and an embassy signature](../nov8_map_and_boundary/README.md) | 3 | 381 | 191 | 181 | 2 |
| [p151 fragments, annotated acknowledgment and Soldiers Council notice](../nov7_fragments_and_council/README.md) | 4 | 690 | 343 | 342 | 4 |
| [p161 B1: urgent Constantinople embassy address](../nov9_urgent_embassy_address/README.md) | 1 | 98 | 49 | 49 | 0 |
| [Romanian pacification consultation: p157 parts 2–5](../romanian_pacification_consultation/README.md) | 4 | 756 | 378 | 377 | 11 |
| [November 4: repetition, communications and a money acknowledgment](../nov4_repetition_and_connections/README.md) | 5 | 1030 | 515 | 514 | 7 |
| [November 2 acknowledgment copies and personnel orders](../nov2_acknowledgments_and_personnel/README.md) | 7 | 1175 | 588 | 584 | 3 |
| [Radio notices, Tiflis personnel and internment on p230](../nov30_radio_personnel/README.md) | 4 | 490 | 245 | 245 | 0 |
| [Radio reception instructions and a brief no-events report](../nov27_receiving_instructions/README.md) | 3 | 506 | 253 | 250 | 14 |
| [Armistice acknowledgments, personnel and Warsaw radio inquiries](../nov16_18_command_inquiries/README.md) | 7 | 1070 | 535 | 517 | 9 |
| [November 6 Ringbahn-key source witnesses](../nov6_ringbahn_key_witnesses/README.md) | 3 | 531 | 266 | 265 | 5 |
| [Warsaw station report: conditional recovery of a missing row](../warsaw_station_missing_row/README.md) | 1 | 242 | 141 | 101 | 0 |
| [Armistice-departure report: explicit p151/p157 copy reconstruction](../armistice_departure_copy/README.md) | 1 | 83 | 95 | 0 | 5 |
| [Wishing to travel home and uncertainty over Baltic transport](../home_departures_baltic_transport/README.md) | 2 | 424 | 212 | 209 | 0 |
| [Mackensen withdrawal report: separately received part 2](../mackensen_withdrawal_part2/README.md) | 1 | 377 | 189 | 188 | 13 |
| [Namur arrival, Cassel transport and armistice-information requests](../namur_cassel_armistice_requests/README.md) | 4 | 658 | 329 | 326 | 7 |
| [Eilvese, setup, boat-sale and director-departure source records](../nov4_radio_and_departure_queries/README.md) | 4 | 887 | 443 | 432 | 17 |
| [Gomel route derailment and station-train forwarding](../nov7_derailment_and_trains/README.md) | 2 | 540 | 270 | 260 | 3 |
| [Unreadable eighth part: source and shared-cell reconstruction](../nov7_eighth_part_repetition/README.md) | 2 | 323 | 161 | 155 | 0 |
| [Ober Ost troop movements: a conditional reading across two obliterations](../oberost_troop_movement_obliterations/README.md) | 1 | 308 | 154 | 150 | 1 |
| [Von Schorlemer: demobilization work inquiry and reply](../schorlemer_demobilization_inquiry/README.md) | 2 | 412 | 206 | 169 | 8 |
| [September radio instructions: Tiflis routing and key destruction](../september_radio_instructions/README.md) | 4 | 798 | 399 | 389 | 10 |
| [Siegfried assignment cancellation: conditional surplus coordinate](../siegfried_assignment_cancellation/README.md) | 1 | 401 | 200 | 196 | 7 |
| [State-bank accounting request and dispatched cheques](../staatsbank_accounting_cheques/README.md) | 2 | 401 | 201 | 192 | 5 |
| [November 6 resale and aerial reconnaissance](../nov6_resale_and_air_reconnaissance/README.md) | 2 | 412 | 206 | 196 | 6 |
| [Early radio and leave records](../early_radio_and_leave_records/README.md) | 4 | 812 | 406 | 391 | 3 |
| [Odessa consular routing and a Magdeburg wagon-sale instruction](../odessa_wagon_sale/README.md) | 2 | 490 | 245 | 241 | 1 |
| [Urgent shipping capacity and probable reliance on sea transport](../urgent_shipping_space/README.md) | 2 | 388 | 194 | 193 | 1 |
| [Benzol-pump inquiry with an explicit missing-coordinate model](../benzol_pump_query/README.md) | 1 | 101 | 51 | 47 | 6 |
| [An airfield and German troops: the surviving third part on p154](../airfield_german_troop_fragment/README.md) | 1 | 172 | 86 | 83 | 2 |
| [OKM availability through an incompletely identified radio route](../okm_radio_route/README.md) | 1 | 86 | 43 | 42 | 6 |
| [October 30 oil and supply records](../oct30_oil_and_supply_records/README.md) | 2 | 540 | 270 | 270 | 0 |
| [November 6 evening and embassy records](../nov6_evening_and_embassy_records/README.md) | 3 | 448 | 224 | 213 | 7 |
| [A regimental journey report with unresolved route and unit labels](../regimental_journey_report/README.md) | 2 | 466 | 233 | 228 | 10 |
| [Reduced provisioning strength and a separate evening report](../nov25_provisions_and_evening_report/README.md) | 3 | 630 | 315 | 315 | 6 |
| [An instruction to avoid fighting, with further orders to follow](../avoid_fighting_instruction/README.md) | 1 | 272 | 136 | 136 | 4 |
| [A radio-traffic transfer in a surviving second part](../radio_traffic_transfer_fragment/README.md) | 1 | 186 | 93 | 89 | 1 |
| [Oct31 armistice and followup](../oct31_armistice_and_followup/README.md) | 2 | 246 | 123 | 123 | 1 |
| [Nov1 nov2 native dispatches](../nov1_nov2_native_dispatches/README.md) | 4 | 730 | 365 | 365 | 3 |
| [Gokieloff return payment stop](../gokieloff_return_payment_stop/README.md) | 2 | 336 | 168 | 166 | 4 |
| [An accommodation-area report with unresolved army and place labels](../jaeger_accommodation_area/README.md) | 1 | 230 | 115 | 110 | 1 |
| [Short arrival, departure and car enquiries on November 12](../nov12_arrival_departure_and_car/README.md) | 4 | 220 | 110 | 103 | 1 |
| [Radio relay and march notice](../radio_relay_and_march_notice/README.md) | 3 | 536 | 268 | 266 | 16 |
| [An enquiry about an MMD command or representative](../mmd_command_whereabouts/README.md) | 1 | 126 | 63 | 59 | 1 |
| [A repeated negotiation assessment and a departure-order reference](../nov18_negotiation_repetition/README.md) | 2 | 484 | 242 | 228 | 5 |
| [Postponed departure, a supper query and a farewell](../nov14_15_departure_and_supper/README.md) | 3 | 368 | 184 | 181 | 7 |
| [Southern hungary positions part2](../southern_hungary_positions_part2/README.md) | 1 | 300 | 150 | 129 | 0 |
| [A parallel car enquiry with an explicit extra-coordinate model](../car_query_parallel_frame/README.md) | 1 | 37 | 18 | 18 | 1 |
| [Nov6 embassy 8956 annotation](../nov6_embassy_8956_annotation/README.md) | 1 | 130 | 65 | 65 | 5 |
| [An expected return and an attempt to obtain a vehicle](../return_time_and_vehicle_attempt/README.md) | 2 | 132 | 66 | 66 | 4 |
| [A second-part instruction on security measures at own discretion](../group_security_measures_fragment/README.md) | 1 | 202 | 101 | 96 | 6 |
| [A request to send money to BRASSO by another means](../brasso_money_alternative_route/README.md) | 1 | 244 | 122 | 113 | 0 |
| [Nov3 bucharest power source](../nov3_bucharest_power_source/README.md) | 2 | 390 | 195 | 195 | 4 |
| [Conditional November 13 congratulation](../nov13_congratulation_conditional_frame/README.md) | 1 | 75 | 37 | 36 | 1 |
| [Receipt request through Nikolajew: the other p105 telegram](../nov2_nikolajew_acknowledgment/README.md) | 1 | 300 | 150 | 150 | 0 |
| [Troop crossing in boats: a fragmentary November 6 report](../nov6_boat_crossing_fragment/README.md) | 1 | 192 | 96 | 93 | 5 |
| [Ringbahn instruction to the Caucasus delegation in Tiflis](../nov6_tiflis_ringbahn_instruction/README.md) | 2 | 365 | 184 | 175 | 1 |
| [Poti tobacco loading inquiry](../nov3_poti_tobacco_loading/README.md) | 1 | 212 | 106 | 106 | 1 |
| [Flying-unit departure or retention inquiry](../nov4_flying_unit_inquiry/README.md) | 1 | 183 | 92 | 67 | 2 |
| [Conditional November 6 marine-service notice](../nov6_marine_service_notice/README.md) | 1 | 286 | 143 | 136 | 3 |
| [Eilvese/OUI traffic schedule](../nov3_eilvese_traffic_schedule/README.md) | 1 | 362 | 176 | 176 | 3 |
| [November 22: reverse key use and an Aufbau date correction](../nov22_reverse_keys_and_date_correction/README.md) | 2 | 268 | 134 | 133 | 0 |
| [November 15: Warsaw radio personnel and a repeated key notice](../nov15_radio_personnel_and_key_notice/README.md) | 3 | 461 | 233 | 221 | 4 |
| [November 27: Helsingfors shipping and a vehicle-sale instruction](../nov27_ships_and_vehicle_sale/README.md) | 2 | 481 | 238 | 236 | 7 |
| [Baku personnel inquiry: a duplicated-block source reconstruction](../baku_personnel_inquiry/README.md) | 1 | 279 | 134 | 125 | 10 |
| [November 9: a crown airlift request and an urgent embassy address](../nov9_crown_airlift_and_embassy/README.md) | 4 | 624 | 312 | 311 | 1 |
| [November 7–8: embassy, legation and Etappe address parts](../nov7_8_embassy_address_parts/README.md) | 7 | 568 | 284 | 284 | 11 |
| [November 8: a separate Serbian-cavalry report witness](../nov8_serbian_cavalry_parallel/README.md) | 1 | 235 | 118 | 116 | 5 |
| [Arad provisions and strength report: conditional partial recovery](../arad_provisions_partial/README.md) | 1 | 271 | 136 | 124 | 6 |
| [November 7: Danube crossings and short message reports](../nov7_danube_and_message_reports/README.md) | 5 | 778 | 389 | 384 | 14 |
| [September 19: pigeons and Army Group East command arrangements](../september19_pigeons_and_command/README.md) | 3 | 542 | 271 | 268 | 1 |
| [November 11: Romanian mobilization and a crossing report](../nov11_romanian_mobilization_report/README.md) | 1 | 235 | 120 | 110 | 4 |
| [November 12: additional arrival and return enquiry witnesses](../nov12_seifert_additional_witnesses/README.md) | 2 | 104 | 61 | 35 | 2 |
| [Native restoration of the p151 E2 operations-map fragment](../nov9_operations_map_sheets/README.md) | 1 | 224 | 112 | 108 | 2 |
| [Poti first part: all minimum five-exclusion frames](../poti_first_part_conditional/README.md) | 1 | 225 | 110 | 103 | 5 |
| [Odessa courier report: a conditional loss before transposition](../odessa_courier_pretransposition/README.md) | 1 | 324 | 163 | 157 | 4 |
| [November 30: aviation march destinations](../nov30_aviation_march_destination/README.md) | 1 | 384 | 187 | 183 | 7 |
| [November 9 wire-return source family](../nov9_wire_return_source_family/README.md) | 3 | 528 | 362 | 205 | 6 |

## Additional interpretation and method audits

- [One conditional letter constraint for the Nov25–28 square](../nov25_letter_constraint/README.md)
- [Coordinate loss before transposition: source diagnostic and p198](../p198_pretransposition_loss/README.md)
- [Optional Nov22–24 interpretation: GD may stand for J](../nov22_nikolajew_constraint/README.md)
- [Literal-coordinate retrieval after publication](../post_push_copy_retrieval/README.md)
- [Bounded diagnostics of three unaccepted odd-length fragments](../odd_fragment_diagnostics/README.md)
- [Accounting copies: two recovered labels and a retained ending disagreement](../accounting_copy_reconciliation/README.md)
- [Optional address spelling in p132 A](../p132_optional_address/README.md)
- [An optional technical reading for the p63 inspector request](../p63_optional_technical_reading/README.md)
- [Optional staff vocabulary in the interference-damaged p137 A5](../p137_optional_staff_vocabulary/README.md)
- [Optional route vocabulary in the jammed p116 A13](../p116_optional_route_fragment/README.md)
- [An optional two-deletion reading of p105 B](../p105_optional_two_deletions/README.md)
- [A source glyph restores ZU DORT in the Gokieloff record](../p136_source_glyph_correction/README.md)
- [A literal duplicate-pair alternative for p109 D](../p109_optional_duplicate_pair/README.md)
- [Childs: all twelve numbered instructional examples](../childs_instructional_examples/README.md)

These packages retain their own calibration limits and conditional assumptions.
A source-compatible witness or an exact language optimum does not by itself
establish a historical plaintext or new key.

## Consistent reading presentation

The [reading conventions](../../docs/reading-conventions.md) define four
separate layers and precise source, frame and plaintext units. The first
mechanical pass preserves all 575 fenced blocks in 121 case pages; the
[manual review](../../docs/reading-conventions-manual-review.md) preserves
42 earlier blocks, 92 headings and 349 inline-code occurrences across 12
additional pages while clarifying their editorial symbols. The exact Tiflis
readable mapping retains 330 nonseparator labels. Both preservation checks
run in CI. A second layer-caption audit retains 637 fenced blocks in 138
overlapping cases, and the spacing audit retains 91 blocks in 25 cases.
The [complete presentation coverage](../../docs/reading-conventions-coverage.md)
classifies every current substantive case and protects each display's bytes
and local qualifier; new unreviewed pages fail its check. These overlapping
presentation counts are never added to source-record totals. A separate
[semantic display review](../../docs/reading-conventions-semantic-review.md)
retains exact unknown fields and exposes prose-only spellings in six cases. A follow-up shipping review preserves six earlier fences and maps all 414 nonseparator labels of three complete quotes, correcting an unmarked S relocation.
The p111/p112 package also checks every nonseparator label in seven complete
readable passages, preserving all five unresolved positions.

The [live readable-label audit](../../data/reviews/live_readable_mappings_20261103.json) checks 141 records in 81 case pages: 11,801 ordered nonseparator labels, 92 literal unresolved positions, and 3 explicitly declared display-only letters. It reads the actual Markdown quotations and their linked raw or edited streams, including protected internal separators and positional question marks. The [coverage guide](../../docs/reading-conventions-coverage.md) separately identifies later supplementary, table and continuation mappings without adding overlapping scopes together.

## Independent source-image binding

All **462 distinct delivered source images** have normalized PDF-page, rectangle, scale,
file-hash, RGB-hash and dimension metadata. The optional PDF verification
regenerates each crop from the pinned original and compares every RGB pixel.
This authenticates the crop location; it does not automate manual glyph
judgments or prove an editorial plaintext. Two of these images belong to the
unaccepted odd-fragment diagnostics and add no catalogue records or recovered
plaintext positions.

The original PDF SHA-256 is
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.

## Reproduce

```sh
python experiments/post_push_review/verify.py --verify
python experiments/post_push_review/verify.py --verify --pdf /path/to/childs.pdf
```

Default verification uses the standard library. PDF pixel checking needs
PyMuPDF and Pillow. Individual cryptographic and geometry verifiers remain
beside their packages and run in CI.

The review uses preserved start/end catalogues, so a later live catalogue
can grow without rewriting its historical count. The earlier
[87-to-195 review](../session_review/README.md) remains separate and unchanged.
The completion timestamp must satisfy the current requested continuation deadline.

For readable messages, use the [case guide](../../cases/README.md); for the
reorganized layout, use the [repository map](../../docs/repository-map.md).

### Published source crops

All **40 additional source crops** are now [available and independently verified](../../sources/reviewed-crops.md). The publication checker validates their exact PNG and RGB hashes against the existing source references; its optional PDF check reproduces every pixel from the authenticated original scan.
