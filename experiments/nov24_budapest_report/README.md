# 24 November: report sent by teleprinter via Budapest

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The original p217 B2 source gives a complete native **176-coordinate / 88-label**
stream. Its intact 51-label sentence reads:

> Meldung geht ausserdem durch Fernschreiber ueber Budapest.

It says the report is additionally being sent by teleprinter through Budapest.
The source requires **zero coordinate edits or fills**. The prefix and compact
fields remain literal: `OLFENINIUS`, `ARADJZ`, `EY`, `AOKYY`.

[Read the edition](../../cases/pages/217.md#edition-cases-military-nov24-budapest-report) ·
[Original source PDF, p220](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) ·
[Certificate](certificates.json)

## Source and attribution

Childs, *General Solution of the ADFGVX Cipher System*, printed p217 / PDF page 220,
section B, under `24th NOVEMBER, 1918.` The header is `UKS v ZON`, received
at `07.15 p.m., November 24th`, followed by `(missed beginning) 2 TLE`.
B1 is labeled `RICHI-204`; B2 is `RICHI-176`.

The unchanged Nov22–24 key comes from the Lasry–Niebel–Kopal–Wacker work and
Lasry's published key list. An earlier unreviewed repository OCR candidate
already recognized this sentence. This edition checks every printed coordinate,
restores the native source transcription, and supplies the complete exact raw
stream and per-position source ledger. The preserved
[earlier candidate](prior_candidates.json) records that lineage.

## First part

All **204 printed slots** of B1 were also checked. The duplicated `FXXXF`
groups at source indices 45 and 50 are genuinely printed. Its native output
remains in this package as the earlier diagnostic. The new
[conditional B1 edition](../nov24_train_report/README.md) recovers the
train-report wording through an explicitly priced repeated-group frame.

## Reproduce

```sh
python experiments/nov24_budapest_report/verify.py --verify
python experiments/nov24_budapest_report/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks source lengths,
unchanged published key, all 88 raw positions, full re-encryption and the exact
51-position quoted span. With the original PDF it reproduces the reviewed crop and checks its dimensions and RGB-pixel hash.
