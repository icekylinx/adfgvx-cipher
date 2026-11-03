# Flying-unit departure or retention inquiry

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Read the [complete p124 B edition](../../cases/military/nov4_flying_unit_inquiry.md).
A conditional short-group repair produces an ordinary-language body while
preserving the entire unresolved opening reference.

| Scope | Count |
| --- | ---: |
| Printed source slots | 183 |
| Valid observed coordinates | 158 |
| Conditional model slots | 184 |
| Plaintext positions | 92 |
| Fixed raw positions | 67 |
| Fixed edited positions | 83 |
| Observed-coordinate substitutions | 2 |
| Source-mask fills | 16 |
| Added-slot fills | 1 |
| Remaining unresolved positions | 9 |
| Deleted/reordered source slots | 0 |

Both local minimum gap positions (source boundaries 16 and 17) are retained.
Their raw outputs differ; their proposed ciphertext and partial edited
plaintext are identical. This comparison is scoped to the five insertions
inside or at the edges of the visibly short XFVV group.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## Reproduce

```sh
python experiments/nov4_flying_unit_inquiry/verify.py --verify
python experiments/nov4_flying_unit_inquiry/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier uses the unchanged complete Nov4–6 key, independently maps each
plaintext pair back to the source, checks all five local prices, preserves
the opening 17 positions, checks the live case displays, and constructs one
explicitly nonhistorical completion witness for full re-encryption. The
optional PDF check compares source-crop pixels using PyMuPDF and Pillow.

Earlier OCR, published key recovery and repository work retain separate
credit. This source restoration does not claim unique historical wording
or first-decipherment priority, and does not supply the missing intercept day.
