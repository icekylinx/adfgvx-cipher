# Siegfried and Osthoff: later military-mission recall messages

Prepared by **icekylinx and GPT-6 Astra Pro**; published keys credited to Lasry, Niebel, Kopal and Wacker, unchanged.

**4 physical records; 802 native coordinate slots; 401 plaintext positions.** The raw layer fixes 394 positions and the edition fixes 398, with 6 observed-coordinate substitutions and 4 fills. No geometry, key or numerical-label assignment changes.

See [the complete case](../../cases/people/military_mission_recalls.md). `inputs.json` records the source rows and crop provenance; `prior_candidates.json` retains earlier readings; `certificates.json` records exact costs, remaining domains and raw/edited round trips. The catalog proposal includes only the listed new physical records.

```bash
python experiments/military_mission_recalls/verify.py --verify
python experiments/military_mission_recalls/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Default verification uses the standard library and existing cipher helpers. The optional PyMuPDF check verifies the pinned full PDF and regenerated exact crop pixels. No search is run.

## Scope limits

- Siegfried is the literal surname in an Oberleutnant recall order. No additional biographical identity is established.
- MISZION and DESZEN are retained as received spellings. Four C1 coordinate substitutions repair ordinary text; two D1 substitutions repair KOMMRNDO and END.
- C1 has one unfilled printed erasure at date position19, domain1GIKNY. Two other question marks are observed XA/VF key cells with joint assignments56 or65, not independent arbitrary digits.
- No optional Nov7 numeric interpretation is applied; reference4??10 remains unresolved under the baseline key.
- D2 directly supplies the three letters D/A/T previously editorial in p149 A2. The later wording is abbreviated and has an extra literal1 after REGMTS; this is semantic/body corroboration, not one identical ciphertext stream.
- The older source editions and their repair costs remain unchanged. Only four p161 physical records are new catalog proposals.

`prior_osthoff_witness.json` freezes the selected existing p149 A2 record and its already proposed letters. The verifier pins its source files, independently decrypts that old source, and checks the three direct raw p161 D2 pairs under the other key. This is new corroboration of old source repairs, not a new reading of the old physical records.
