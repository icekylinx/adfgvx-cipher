# Two completed Danube-report proposals

The new readings extend the existing p143 A and p144 C1 editions under the
published Nov4–6 key. They fill **three remaining plaintext positions** and
correct one additional letter, with no change to either source frame.

| Source | Previous proposal | Completed proposal | Additional source operations |
|---|---:|---:|---|
| [p143 A](../../cases/military/nov6_evening_danube_report.md#completed-reading) | 93/94 positions in the geographical proposal | 94/94 | One dash filled: source 33 → G, giving O in the address OKM. |
| [p144 C1](../../cases/military/nov6_horse_loading_reconnaissance.md#completed-reading) | 69/71 positions | 71/71 | Source 10 → F and 11 → A fill two dashes; source 104 V → A changes I to L in KLADOVO. |

The command reading selects O from the received half-pair's domain
`1EJORT`. Independent native messages attest both `OXKXM` (p124 A3,
Nov4–6 key) and `FUEROKM` (p226 A2, Nov28–Dec1 key). The verifier decodes
those phrases from observed coordinates, supporting the address formula.
In p144 the proposed O in KLADOVO fits `036OQY`; the preceding
separator X fits `0578CX`. These are interpreted completions of masked
pairs, with the rival source-compatible labels retained in the verifier's
output. The historical place has an independent attestation in the
[National Library of Serbia's 1893 General Staff map, K 2, Кладово](https://digitalna.nb.rs/view/URN:NB:RS:SD_571C5F8EA57C630BE1A06E28BA3ECF0E?virtuelne=NBS/Karte/srbija).
Its catalogue record supports the name, not the reported reconnaissance.

The full costs remain **four observed-coordinate substitutions and ten mask
fills** for p143, and **six substitutions and ten fills** for p144. Literal
`217I` and `M5` remain in the readings. The base certificates preserve the
raw outputs and earlier partial proposals.

```sh
python experiments/nov6_danube_completion/verify.py
```

The small verifier independently reconstructs the transposition, checks the
native readings, re-encrypts both complete proposals and reports every
additional and total source operation. It also checks the live German
quotations. [readings.json](readings.json) records the proposals and map
reference without duplicating the earlier source packages.

Source editions and completion: **icekylinx and GPT-6 Astra Pro**. The period
key and its provenance remain credited to the Lasry team in the base editions.
