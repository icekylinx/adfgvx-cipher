# Retrieved copies: banknote completion and armistice clauses

Prepared by **icekylinx and GPT-6 Astra Pro**.

The frozen [literal-coordinate retrieval](../post_push_copy_retrieval/README.md)
identified these three strong cross-page candidates. Manual source inspection
now supplies three new physical records, 444 fully observed coordinates and
222 plaintext positions. There are 221 raw fixed labels, 222 in the edited
readings, and three explicitly priced observed-coordinate substitutions.

- [p195 A2](../../pages/195.md#edition-cases-finance-crown-banknote-completion) preserves the
  nineteen coordinates missing from p174 A3. Eleven of twelve earlier
  conjectural fills agree with the new source; one is contradicted. All eighty
  contiguous-gap placements are costed. One new observed-coordinate change
  is still needed for `SENDEN`; the raw domain is digits `56789`, not S.
- [p137 B4 and C](../../pages/137.md#edition-cases-military-armistice-clause-witnesses) provide
  the exact armistice clause and receipt fragments. The first witnesses a
  previously masked X. The second repeats both earlier corrupt words and
  therefore does not independently certify their two repairs.

All source rows, prior-package hashes, full coordinate origins, complete
gap costs, header conflicts and arbitrary consistency witnesses are retained.
The three earlier records are contextual evidence and are not counted again.

```sh
python experiments/retrieved_copy_editions/verify.py --verify
python experiments/retrieved_copy_editions/verify.py --verify --pdf /path/to/childs.pdf
```

Default verification is standard-library only. Optional PDF verification
regenerates both page images, with the recorded clean renderer-cache policy,
and compares every pixel. The baseline keys, source lengths and ordering
are unchanged.
