# Odessa / Nikolaiev shipping instruction: Childs p98

Prepared by **icekylinx and GPT-6 Astra Pro** with the unchanged published Nov1–3 square and ranks of Lasry, Niebel, Kopal and Wacker.

Three source records total **782 literal coordinates and391 fixed plaintext positions**, with **seven observed-coordinate substitutions** in the edited readings. A1 changes the disembarkation destination of Siegfried troops to Odessa. A2 and its next-day B witness direct shipping from KOSPOLI to Odessa or Nikolaiev. Their132/133-character bodies overlap extensively;391 is a physical-record total, not a distinct-message character count.

All four A2/B repairs have direct coordinate-pair witnesses in the other received copy. The three A1 repairs are separate language proposals. `NUMEHR`, `NIKILJEW`/`NIKOLAJEW`, `FECH`, reference digits and both lengths remain explicit. There are no source erasures, fills, insertions, deletions, reorders, baseline key changes or new numeral assignments.

An earlier unreviewed A1 candidate already read the body and was included in frozen p73 retrieval inputs. Earlier A2/B candidates lacked the first printed rows and did not read coherently; all prior candidates and bounded attribution checks are retained. The new contribution is the complete source edition, A2/B readings and exact witness/repair accounting, without a universal priority claim.

See [the readable case](../../cases/military/black_sea_disembarkation.md), `inputs.json`, `prior_candidates.json`, `certificates.json` and `catalog_proposal.json`. The three crops include full PDF page/rectangle/scale/hash provenance.

From the repository root:

```bash
python experiments/black_sea_disembarkation/verify.py --verify
python experiments/black_sea_disembarkation/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Default verification uses only the standard library and existing project cipher helpers. It independently derives readings, checks all seven exact repair costs, verifies four cross-copy coordinate-pair witnesses, retains every raw digit/J/Q/Y occurrence and re-encrypts the raw and edited bodies. The optional PDF check requires PyMuPDF and authenticates both the pinned PDF hash and exact regenerated crop pixels. No search is launched.
