# November 6 Ringbahn-key source witnesses

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Three new physical records on Childs p145 preserve **531 typed source
coordinates**. Their declared frames have **532 coordinates** and **266
plaintext positions**, with **265 fixed raw positions**. Five observed
substitutions and one inserted-slot fill recover the full stated candidates.
The Nov4–6 key is unchanged.

The [edition](../../cases/radio/nov6_ringbahn_key_witnesses.md) reconstructs
the three-part key-reuse instruction already read in the p211 lower-B copy.
A printed four-coordinate XFVA group in p145 part 2 requires an explicit
one-slot frame hypothesis. Adding F at boundary 33 and changing three observed
coordinates reproduces the **unedited p211 part-2 ciphertext exactly**. All
five local gap locations are priced; the chosen one has the least observed
change cost within that family.

Every newly repaired plaintext position has direct fixed-raw support from
p211. In the reverse direction, p145 raw positions confirm four earlier
p211 word repairs, including the damaged DREISSIGSTER letter. Source-specific
reference labels and conflicting page/receipt dates remain unchanged.
No schedule compliance or historical numeral relabeling is asserted.

`inputs.json` preserves literal rows, headers, three crop bindings, the
unchanged key and a hash-pinned snapshot of the earlier p211 evidence.
`certificates.json` records independent transposition maps, raw coordinate
pairs, exact repairs, all local gap prices and both directions of source
support. Complete German quotes preserve every nonseparator label.
The earlier p211 body and p145 ending candidate retain their credits.

## Reproduce

```sh
python experiments/nov6_ringbahn_key_witnesses/verify.py --verify
python experiments/nov6_ringbahn_key_witnesses/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The optional PDF check regenerates all three new crops and the reused p211
crop and compares every pixel. It needs PyMuPDF and Pillow; the basic
verification uses only checked-in modules and the standard library.
