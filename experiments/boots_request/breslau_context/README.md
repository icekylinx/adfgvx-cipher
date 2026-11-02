# Breslau: a separate contextual emendation, not a recovered key cell

**icekylinx and GPT-6 Astra Pro.**

The boots request's primary edition retains `SELLVXGENXKOMX?XAXKXBRESLAU`.
The unknown unit character is the complete received pair **GD**, from original
source coordinates 27 and 162. Its unchanged-square domain is **234789QY**.
It cannot be assigned `6`: the published Nov13b square already assigns `6`
to **GG**, and a substitution square must remain injective.

An independent contemporary decree supplies a qualified contextual lead.
The *Waldenburger Wochenblatt*, no. 165, **18 July 1917**, PDF page 8, prints a
decree headed **VI. Armee-Korps / Stellv. General-Kommando**, dated
**Breslau, 6 July 1917**, and signed by the deputy commanding general von
Heinemann. The [source metadata](source.json), title crop and complete decree
crop record a visually inspected primary scan from the
[Lower Silesian digital library](https://jbc.jelenia-gora.pl/Content/51388/52552_waldenburger_wochenblatt_1917-165.pdf).
This source precedes the telegram by sixteen months; it does not itself
authenticate the telegram or establish institutional continuity to its date.

If the telegram addresses that same VI Army Corps command, a **single extra
received-coordinate repair D→G at source index162** changes GD to GG and
reads `6` under the unchanged square. This is an optional source emendation,
not a square fill. It would take the two-part edition from **196/200 to
197/200 fixed positions**, with **five** received-coordinate substitutions
instead of four, and the same twelve erasure fills. The quantity and full
connective domain remain unresolved.

The primary boots inputs and certificate are unchanged. The separate
[certificate](certificate.json) gives the complete source map, partial
reading and joint square witnesses for every retained connective value.
Those arbitrary completions are feasibility witnesses, not selected numbers.

```sh
python experiments/boots_request/breslau_context/verify.py --verify
python experiments/boots_request/breslau_context/verify.py --verify \
  --pdf /path/to/52552_waldenburger_wochenblatt_1917-165.pdf
```

The optional PDF check compares the original file hash and every crop pixel.
No visually inspected 1918 decree is claimed.
