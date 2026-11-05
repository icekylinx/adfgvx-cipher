# p176a: exact source-retention bound

**icekylinx and GPT-6 Astra Pro.** This supplement fixes Norbert's earlier
112-position body, including `BEEURTEILT`, solely to price its compatibility
with the literal 214-slot source and unchanged Nov10–12 key.

[Case section](../../pages/176.md#edition-cases-p176a-source-retention-bound-for-the-earlier-proposal)
· [Inputs](inputs.json) · [Exact certificate](certificates.json).

All monotone source-retaining alignments into 224 slots require at least
**68 observed substitutions**, with exactly **252** optimal maps. Allowing
one printed mask to be excluded and eleven added slots gives a minimum of
**13**, attained only by excluding final mask **213**, with **two** optimal
maps. No observed coordinate can be deleted or moved. Masks and added fills
are counted separately. This is a conditional bound, not new historical wording.

The certificate records all optimal inserted-position vectors and full
attaining ledgers. A forward dynamic program and the separate
[independent suffix program](independent_check.py) agree on all eleven
families. The latter imports no repository arithmetic helper and constructs
its own column buckets. All 120 global digit completions produce the same
target ciphertext, since the target uses only assigned cells.

```sh
python experiments/p176a_source_retention_bound/verify.py --verify
python experiments/p176a_source_retention_bound/verify.py --verify --pdf /path/to/childs.pdf
python experiments/p176a_source_retention_bound/independent_check.py
```

The original case's fences and quotations are checked against a frozen
snapshot. External crop recipes reproduce the header and A4 source with the
optional original-PDF check; no new image file is packaged.

Norbert retains credit for the 2017 body, and Max Baertl for his separate
editorial completion. The period key remains credited to Lasry, Niebel,
Kopal and Wacker, and Lasry's 2017 list.
