# Reconciling the Namur personnel-order witnesses

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The [case](../../cases/pages/171.md#edition-cases-people-namur-order-witnesses) presents a source-supported
126-position order to Hauptmann Staedt in Namur concerning contact with
`HPT V. WEIHER`, signed `MJR KROEGER`. Its `INSP1IN` anomaly is retained.

p171 C has 252 received slots, including four printed dashes. p172 E has 242
received coordinates and a jammed-opening marker. Under the explicitly
conditional same 252-coordinate-message model, E lacks ten leading coordinates.
At source offset 10, 227 of 238 jointly observed coordinates agree. This is
the unique best agreement fraction among 87 relative shifts having at least 200
jointly observed coordinates; the comparison uses no language score.

The two witnesses jointly cover every coordinate in the full frame. The
chosen common ciphertext restores E's prefix as `DGAAV FADFD`, using C's
observed values, and fills C's four printed dashes using E. The 11 remaining
observed conflicts require at least 11 substitutions in total. The chosen
body achieves this exactly: six changes in C and five in E. Every chosen
coordinate value is observed in one witness; 125 of 126 whole plaintext pairs
are directly observed in one copy, and one pair is assembled from the two
observed halves.

There are nevertheless **2,048 minimum-cost common coordinate streams**,
one choice at each conflict. The verifier enumerates them all, checks the
cost, and preserves an ordered digest and the selected choice bits. This
finite lower bound is conditional on the stated alignment and same-message
assumption. It does not prove unique original wording or length. The readable
choice is made after examining the witnesses; no blind-control claim is made.

The source accounting is 494 literal slots, 504 modeled working coordinates,
and two physical witnesses of one body. Raw fixed positions total 237/252;
both edited copies contain 126/126 fixed labels. Printed fills 4, modeled
leading fills 10, known substitutions 11, deletions 0, reordering 0, key changes 0.
The times 7.26pm and 7.21pm are retained without imposing a relay chronology.

The period key remains credited to Lasry, Niebel, Kopal and Wacker. The
earlier unreviewed C candidate is retained; the neighboring p172 C/p175 A
published body discussion is distinguished. No universal priority or new
biographical identification is claimed.

```sh
python experiments/namur_order_witnesses/verify.py --verify
python experiments/namur_order_witnesses/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The optional PDF check regenerates both crops and compares dimensions,
channels and pixels. Default verification is standard-library-only using
the existing independent column/domain/re-encryption helpers.
