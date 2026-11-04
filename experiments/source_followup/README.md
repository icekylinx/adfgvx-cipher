# Source and attribution follow-up

**icekylinx and GPT-6 Astra Pro · 2 November 2026**

Primary-source checks supporting the readable case edition. Historical period keys and previously published readings retain their original credit. The two contextual messages below are not added to the 22-target challenge total.

## Findings

| Record | Checked result | Scope |
| --- | --- | --- |
| [p109 B transcription](p109_B_review.json) | Independent visual transcription agrees with the first review: 248 slots, 242 valid coordinates, six erased positions. | Supports the separately certified p109 B/D source relationship. No source glyph was changed to improve the German. |
| [p132 attribution](attribution_followup.json) | Norbert explicitly proposed **GEBET VORHER** on 12 March 2017, comment 40. | The wording is prior art. The present work contributes review, clear presentation and the complete coordinate audit. |
| [p77 B contextual reading](source_context.json) | All 350 received coordinates yield 175 letters and re-encrypt exactly. The message directly contains **ERHAELT RUFNAMEN NATHAN OTTO KARL**. | Independent evidence for the call-sign instruction formula used in the p146 interpretation; it concerns Konia, not Kerch. |
| [p134 B contextual reading](source_context.json) | 102 slots yield 50 fixed letters out of 51, with one malformed source glyph retained as unknown. | Independent support for the fourth-period/fifth-period repeat instruction in p132; not an identical copy or proof of its VORHER clause. |
| [p186 suffix and glyph review](p186_source_and_suffix_delta.json) | Conservative treatment of two questionable glyphs; no injective square completion can make the p186 and p187b suffixes identical by deleting just one p186 character. | Refines the existing p186 record and explains why its numeral 1 cannot simply be transferred into p187b. No new digit is assigned. |

## Two contextual readings

### p77 B: call-sign instruction

```text
NACHRICHTENCHEFXDRAHTETXMITX4XBX49338XXFUNKERABTLGXOSMANIEXXZUXDORTX2032XFUNKERABT3GXKONIAXERHAELTXRUFNAMENXNATHANXOTTOXKARLXWELLENXVONXDORTXFESTLEGENXXADMIRALSTABX17830XDX2XX
```

The signals chief reports that the radio detachment at Konia receives the call sign spelled Nathan–Otto–Karl; the recipient is to determine the wavelengths. `FUNKERABT3G` remains a literal garble. The `4 B` administrative reference is also useful context for the ending of p146. This October message does not establish the Kerch instruction's date.

### p134 B: repeat transmission

```text
EGLV2SSEXT?LEGRXDE8X4XPORIODEINX5XWIEDERHOLENXOSMXX
```

The likely sense is “[Eilvese]: repeat the telegram of the fourth period in the fifth. OSM.” The exact malformed words remain visible. The last glyph in group 16 is overstruck or malformed and is not treated as a known ADFGVX coordinate. The source does not explain what the numbered periods denote.

## p186: the ending cannot be copied unchanged

Norbert identified the p186/p187 body relationship in [comment 53, 3 May 2017](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1#comment-878079), and explicitly said p186 had already been deciphered by the Lasry team. The original repository record is [retained separately](../../data/reviews/p186_chi_parallel.json).

After `NACHCHEF`, the p186 suffix has nine positions and p187b has eight. Consider every possible deletion of one p186 suffix character, while preserving all other source constraints and both injective partial squares. All nine possibilities fail:

- Deleting position 0 or 1 places the known numeral `1` against the known separator `X`.
- Deleting position 2 makes the two occurrences of p187b cell `VA` equal the distinct known characters `1` and `X`.
- Deleting any position 3 through 8 forces p186 cell `FV` to encode `1`; its square already assigns `1` to the different cell `DD`.

This proves only the stated suffix-alignment obstruction. The messages may have different references, additional errors or another relationship. The body correspondence still independently supports the readable `RUSSISCHEN` and `NICHT ARBEITET` interpretations.

The new glyph review masks source indices 20 and 29 of p186 A2, where the scan shows an M-like/overstruck glyph and a Y-like glyph. The existing `V` interpretations remain plausible hypotheses; they should not be confused with an unambiguous literal transcription.

## Reproduce

Python 3, standard library only:

```sh
python3 experiments/source_followup/verify_context.py --verify
python3 experiments/source_followup/audit_p186.py --verify
```

The arithmetic independently reconstructs the transposition map, each plaintext domain, every known letter's coordinate pair and the coordinate re-encryption. p77 B additionally has a complete ordinary plaintext re-encryption. The suffix check has both a positive identity control and a negative fixed-digit conflict control, as well as the short argument above.

The [retrieval script](scan_companions.py) scans the existing 788 unverified OCR blocks under 24 nonempty published/recovered squares, at most four declared group-layout models and zero through four trailing erasures. It evaluated **165,216 models**. [The retained results](retrieval_results.json) include exact model choices, source hashes and search terms.

```sh
python3 experiments/source_followup/scan_companions.py
```

Retrieval scores are keyword-ranking aids, not confidence estimates. The raw p146 target does not emerge from these unedited source models because its established transmission repairs lie outside the scan. Negative findings therefore exclude neither companion messages nor other source-error models. Only the visually checked, explicitly recorded p77 and p134 source layers are promoted from this retrieval into contextual readings.
