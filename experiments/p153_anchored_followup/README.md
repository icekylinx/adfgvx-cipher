# Recovered-square reuse: final bounded supplement

Authors: **icekylinx and GPT-6 Astra Pro**.

Six searches fixed the nineteen ordinary-letter cells recovered from page 153,
while varying every column rank and all other square cells. Page 73 and page
170 were each searched at widths 18, 19 and 20. Every case completed 500
restarts of 100,000 proposal slots: 300 million historical slots in total.
No coherent additional reading was accepted.

An 89-letter synthetic control at width 19 used the same nineteen anchors and
two coordinate erasures. It completed 300 restarts of 60,000 slots. The search
failed to recover its key; its true masked objective is better than the retained
false maximum. Consequently this experiment has weak sensitivity calibration
and provides no exclusion of square reuse. The control wording was used earlier
for calibration but never language-model training. Its fresh key, source and
post-fit evaluation are retained.

The recovered cells are a reuse hypothesis, not a historical constraint on
these other messages. Page 73 has an 8 November reception header and a 26 October
origin/heading context; neither establishes shared keys. The model replaces
a half-erased digraph by a whole-cell wildcard and therefore omits the surviving
coordinate from its objective. Any accepted reading would require exact
coordinate-domain verification. No historical reading reached that stage.

## Reproduce

Build `../joint_search/src/anchored_joint.c` using the sibling Makefile. Generate
the military wildcard four-gram model using that package's deterministic model
builder. The required source and model SHA256 values are in `summary.json`.

```sh
python3 replay.py --solver ../joint_search/bin/anchored_joint --model /path/to/german_military37_quad_marginal.bin --output /tmp/p153-square-reuse
```

`--case p73_k18` selects one recorded case. The replay recreates the exact solver
input from the portable records; it does not supply evaluation plaintexts or
true keys. The canonical solver interface is described in the sibling package.
`verification.json` independently rechecks all seven final plaintexts and
objective values. `odd_width_scoped_review.json` separately records a read-only
review of the conditional post-discovery odd-width proof.

No executable, model or source book is included here. These results supplement
`../p153_followup/` and do not alter the accepted page-153 certificate.
