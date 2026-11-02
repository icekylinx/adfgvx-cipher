# Alternative p153 rectangle geometries

Both experiments preserve the 225 valid coordinates and 15 erasures of the two source parts. Neither produces an accepted reading.

| Model | Completed scope | Unsearched alternatives |
|---|---|---|
| Concatenate the parts into one complete 240-coordinate rectangle | Both part orders and all 24 reported keys: 48 cases | Arbitrary unknown squares or transpositions; a longer original rectangle with parts 1–4 absent |
| Continue the writing-column phase into part 6 | Both signs of the 132-coordinate phase shift and all 24 keys: 48 cases, 45 distinct effective-key combinations | Arbitrary unknown squares or transpositions |

The source labels identify parts 5 and 6 and give separate lengths 132 and 108. These alternate geometries are explicitly exploratory. Stored controls check arithmetic under the planted model; they do not validate historical plaintext ranking. The all-unknown June 1 square provides no direct reading.

From this directory:

```sh
python3 p153_concatenated_screen.py --repository ../.. --output /tmp/p153_concat.json
python3 p153_continuation_phase_screen.py --repository ../.. --output /tmp/p153_phase.json
```

An optional `--model` argument accepts the independent 36-symbol quadgram table rebuilt by [the joint-search model builder](../joint_search/README.md). The checked-in JSON files record the original model hash and source snapshot; later catalog metadata changes do not alter the ciphertexts.
