# Cash transport through Szolnok, Arad and Hermannstadt

Prepared by **icekylinx and GPT-6 Astra Pro**.

This source edition adds the two parts printed as section B on Childs p216. The page and origin heading say 24 November 1918; the receiving header says 01.30 a.m., 26 November. Those dates remain separate. The published Nov22–24 square and ranks are unchanged.

Part 1 requests that money be sent under special guard by train through Szolnok and Arad if the aircraft at Döberitz has not started. Part 2 continues with Hermannstadt, notification of arrival at the stations, and the literal phrase `KROGEHENHIERZUENDE`. The abbreviation `KRO` is not expanded to an asserted currency or denomination. This is a request, not evidence that the shipment occurred.

## Exact readings

The primary first-part raw reading is:

```text
FALLSFLUGZEUGDOEBERITZN2IHTGESTART2TXGELDUMGE?ENDUNTERBEMONDERERBEWSCHUNGMITXVXZ?GUEBERXSZOLNOKXARADX
```

The explicitly conditional ordinary-word candidate is:

```text
FALLSFLUGZEUGDOEBERITZNICHTGESTARTETXGELDUMGEHENDUNTERBESONDERERBEWACHUNGMITXVXZUGUEBERXSZOLNOKXARADX
```

Part 2 needs no coordinate substitutions or erasure fills:

```text
HERMANNSTADTXSENDENXANKUNFTAUFDEN8STATIONENOKM9EWEILSMITTEILENXKROGEHENHIERZUENDEXOKMXYAYY?18XX
```

Raw `8`, `9`, `YAYY?18`, the dates and all other numerical/reference labels remain as they decrypt. In particular, this edition does not replace `9EWEILS` with `JEWEILS`; that is a separately testable interpretation of the square label.

## Short group, exact costs and tied geometry

Part 1 advertises 202 coordinates but actually prints 201 slots. Its fourth group on the third line is `AAAV`, with four characters. It also prints a dash at zero-based source index 141. Both facts are preserved in `inputs.json` and the source crops.

The verifier evaluates all 202 possible positions for one inserted coordinate against the declared candidate. The minimum is five changes to observed coordinates. Two gap positions tie: 98 and 99, immediately before or after the final V of `AAAV`. Both require an inserted V and yield the same repaired ciphertext, because the repaired group is `AAAVV`. They give different mappings between model coordinates and the original paper, so both full mappings and raw readings are retained. The primary presentation uses gap 99, the end of the short group. This is conditional geometry based on an ordinary-word reading; it is not independent proof of the missing character's original position.

The five observed-coordinate substitutions are source indices 139 A→D, 140 A→F, 142 V→D, 143 D→X, and 194 V→F. They repair `NICHT`, `GESTARTET`, `BESONDERER` and `BEWACHUNG`. The printed dash at source 141 is filled V for `UMGEHEND`; the missing coordinate is also filled V. Part 2's final printed dash remains unresolved.

| Quantity | Two physical parts |
| --- | ---: |
| Printed source slots | 391 |
| Valid printed ADFGVX coordinates | 389 |
| Modeled coordinates | 392 |
| Plaintext positions | 196 |
| Fixed positions before the candidate | 193 |
| Fixed positions after the candidate | 195 |
| Observed-coordinate substitutions | 5 |
| Printed-erasure fills | 1 |
| Missing-coordinate fills | 1 |
| Printed erasures still unresolved | 1 |

## Independent lexical observation, without a key change

In part 2, zero-based plaintext position 46 is the pair `GD`, obtained from source indices 116=`G` and 185=`D`. Both are clearly printed and neither is repaired. The resulting baseline label is `9`, in `OKM9EWEILSMITTEILEN`.

Interpreting that one square cell as J would produce the ordinary German word `JEWEILS`. This is useful evidence outside the separate `NIKOLA9EW` medical-report family. It remains a lexical hypothesis: the ciphertext fixes `GD`, while language supplies the proposed letter. The source edition retains raw 9, and any partial-square propagation belongs in its own certificate.

## Prior work and reproducibility

The unreviewed repository screen already recognized part 2; its complete candidate and original cache hash are frozen in `inputs.json`. Part 1 is newly assembled from the exact printed layout, including the short group and final `FF`. Bounded text searches found no explicit Döberitz/Hermannstadt cash-transport body in the Lasry paper, dissertation or cached 55-comment discussion. This is not a claim that no earlier researcher ever read the message.

Run from the repository root:

```bash
python experiments/hermannstadt_cash_transport/verify.py --verify
python experiments/hermannstadt_cash_transport/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command uses the standard library and the repository cipher code. It independently reconstructs column offsets, all domains, source mappings, all gap costs, and exact repairs. The optional PDF check additionally requires PyMuPDF and Pillow; it checks the complete PDF hash and every crop's pixels. The full source PDF is not duplicated in this directory.

See [inputs.json](inputs.json), [certificates.json](certificates.json), [the proposed catalog records](catalog_proposal.json), and the [reading page](../../cases/pages/216.md#edition-cases-finance-hermannstadt-cash-transport).
