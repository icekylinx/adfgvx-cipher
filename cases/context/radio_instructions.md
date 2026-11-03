# Radio instructions: p77 B and p134 B

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[Case index](../README.md) · [ADFGVX Cipher](../../README.md)

**Status:** Two source-checked contextual records, outside the 22-target challenge. The established period keys are credited to the earlier corpus researchers. Source transcription, comparison, and verification: **icekylinx and GPT-6 Astra Pro**. No first decipherment priority is claimed for these wider-corpus messages.

## p77 B — call-sign instruction for Konia

**Most likely reading:**

> Nachrichtenchef drahtet mit 4 B 49338: Funkerabtlg. Osmanie. Zu dort 2032: [Funkerabtlg.] Konia erhaelt Rufnamen Nathan Otto Karl. Wellen von dort festlegen. Admiralstab 17830 D 2.

**Meaning:** The signals chief reports that the radio detachment at Konia receives the call sign spelled Nathan–Otto–Karl. The recipient is to determine the wavelengths. Administrative references and the Admiralty Staff signature are retained.

All **350 received coordinates** give **175 plaintext characters** and re-encrypt exactly under `Oct28-31`. The raw `FUNKERABT3G` is normalized in brackets; no source coordinate is silently changed. The directly decoded formula `ERHAELT RUFNAMEN` followed by spelling words independently supports the revised interpretation of [p146](../p146.md). This October message concerns Konia and does not establish Kerch's November date.

Source: [Childs p77 B](../../sources/excerpts/childs_p77_B.png), PDF page 80; header `OSM v LP (6.47 a.m., October 30th); SS BERLIN 29/10 1922; RICHI-350`. Under the source's header convention, LP is the sender and OSM the recipient.

## p134 B — repeat a fourth-period telegram in the fifth

**Most likely reading:**

> [Eilvese]. [Telegr.] [der] 4. [Periode] in 5. wiederholen. OSM.

**Meaning:** A message apparently directed to Eilvese asks for a fourth-period telegram to be repeated in the fifth period.

The **102 source slots** yield **50 of 51 fixed characters** under `Nov4-6`:

```text
EGLV2SSEXT?LEGRXDE8X4XPORIODEINX5XWIEDERHOLENXOSMXX
```

The malformed final glyph of group 16, source index 79, remains unknown. The place name and other corrected words are editorial. The repeated instruction independently supports the corresponding vocabulary in [p132](../p132.md); it is not an identical copy, does not establish `VORHER`, and does not explain what the numbered periods denote.

Source: [Childs p134 B](../../sources/excerpts/childs_p134_B.png), PDF page 137; header `LP v NKJ (4.02 a.m., November 6th); 0530 (6); RIZI-102`.

## Evidence and verification

The [source records](../../experiments/source_followup/source_context.json) preserve the full grouped ciphertexts, literal raw plaintexts, per-position domains, and coordinate maps. The [review](../../experiments/source_followup/README.md) records the retrieval scope and attribution.

```sh
python3 experiments/source_followup/verify_context.py --verify
python3 -m adfgvx.verify
```
