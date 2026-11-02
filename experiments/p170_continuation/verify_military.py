#!/usr/bin/env python3
"""Verify the p166/p167 prefix restoration and p170 B operational parallels.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
Reuses the independent column arithmetic in verify_seifert, not adfgvx.cipher.
"""
from pathlib import Path
import argparse
import itertools
import json
from verify_seifert import arithmetic, coordinate_map, encode, digest, ROOT, HERE, COORD, ALPHABET


def compare(source, target):
    assert len(source) == len(target)
    return {"known_coordinate_substitutions":[{"position_0based":i,"source_coordinate":a,"proposed_coordinate":b}
                                              for i,(a,b) in enumerate(zip(source,target)) if a != "?" and a != b],
            "erasure_fills":[{"position_0based":i,"proposed_coordinate":b}
                             for i,(a,b) in enumerate(zip(source,target)) if a == "?" and b != "?"]}


def verify(pdf=None):
    data = json.loads((HERE / "military_records.json").read_text())
    assert data["prepared_by"] == "icekylinx and GPT-6 Astra Pro"
    if pdf:
        assert digest(pdf) == data["source_pdf_sha256"]
    for crop in data["crops"]:
        assert digest(ROOT / crop["path"]) == crop["sha256"]
    key = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"] if k["id"] == "Nov7-9")
    ranks, square = key["column_rank_order"], key["square"]
    by_id = {r["id"]: r for r in data["records"]}
    assert len(by_id) == 6
    summaries = []
    complete_squares = []
    unknown = [i for i,c in enumerate(square) if c == "?"]
    assert len(unknown) == 2 and set(ALPHABET) - set(square) == set("56")
    for permutation in itertools.permutations("56"):
        full = list(square)
        for index, letter in zip(unknown, permutation):
            full[index] = letter
        complete_squares.append("".join(full))

    def check_witnesses(cipher):
        # Fill source erasures only for an arithmetic witness; no such fill enters the edition.
        concrete = cipher.replace("?", "A")
        for full in complete_squares:
            text, domains, _ = arithmetic(concrete, ranks, full)
            assert "?" not in text and all(len(d) == 1 for d in domains)
            assert encode(text, ranks, full) == concrete
            assert all(a == "?" or a == b for a,b in zip(cipher,concrete))

    def check_edition(source, edition):
        target = edition["ciphertext"]
        text, _, _ = arithmetic(target, ranks, square)
        assert text == edition["plaintext"]
        costs = compare(source, target)
        for name in costs:
            assert costs[name] == edition[name]
        if "plaintext_changes" in edition:
            before = arithmetic(source,ranks,square)[0]
            assert edition["plaintext_changes"] == [{"position_0based":i,"raw_plaintext":a,"proposed_plaintext":b}
                                                    for i,(a,b) in enumerate(zip(before,text)) if a != b]
        check_witnesses(target)
        return {"known_coordinate_substitutions":len(costs["known_coordinate_substitutions"]),
                "erasure_fills":len(costs["erasure_fills"])}

    for record in data["records"]:
        raw = "".join("".join(record["raw_source_rows"]).split())
        assert raw == record["raw_source_compact"]
        cipher = "".join(c if c in COORD else "?" for c in raw)
        assert cipher == record["analysis_ciphertext"]
        assert len(raw) == record["received_slots"]
        assert sum(c in COORD for c in raw) == record["valid_coordinates"]
        assert record["key_id"] == key["id"] and record["column_rank_order"] == ranks and record["partial_square"] == square
        text,domains,_ = arithmetic(cipher,ranks,square)
        assert text == record["raw_geometry_plaintext"] and domains == record["raw_domains"]
        assert record["fixed_plaintext_positions"] == sum(len(d)==1 for d in domains)
        check_witnesses(cipher)
        summary = {"id":record["id"],"source_slots":len(cipher),"raw_geometry_positions":len(domains),
                   "fixed_raw_geometry_positions":record["fixed_plaintext_positions"],"editions":[]}
        for edition in record["editions"]:
            summary["editions"].append(check_edition(cipher,edition))
        summaries.append(summary)
    a,b = by_id["p166_A3"]["analysis_ciphertext"],by_id["p167_A3"]["analysis_ciphertext"]
    recovery = data["prefix_recovery"]
    assert len(a)==184 and len(b)==204
    assert recovery["inserted_prefix"]==b[:20] and recovery["inserted_prefix_coordinates"]==20
    assert recovery["prefix_from_parallel_positions_0based"]==list(range(20))
    restored = b[:20]+a
    assert restored==recovery["restored_ciphertext"] and recovery["source_coordinates_unchanged"]==184
    text,domains,_=arithmetic(restored,ranks,square)
    assert text==recovery["plaintext"] and domains==recovery["plaintext_domains"]
    assert recovery["fixed_plaintext_positions"]==sum(len(d)==1 for d in domains)==101
    placements=[]
    for offset in range(21):
        pairs=list(zip(a,b[offset:offset+len(a)]));known=[(x,y)for x,y in pairs if x!="?" and y!="?"]
        placements.append({"offset_0based":offset,"known_matches":sum(x==y for x,y in known),
                           "known_disagreements":sum(x!=y for x,y in known),
                           "comparisons_with_erasure":sum(x=="?" or y=="?" for x,y in pairs)})
    assert placements==recovery["all_contiguous_placements"]
    ordered=sorted(placements,key=lambda row:row["known_disagreements"])
    assert ordered[0]=={"offset_0based":20,"known_matches":179,"known_disagreements":4,"comparisons_with_erasure":1}
    assert ordered[1]["known_disagreements"]==136
    assert recovery["best_offset"]==20 and recovery["source_disagreements"]==compare(b[20:],a)
    check_witnesses(restored)
    interim=[None]*204
    for source,destination in enumerate(coordinate_map(204,ranks)):
        interim[destination]=set((restored[source]+b[source]).replace("?",""))
    unused=set(ALPHABET)-set(square);shared_domains=[]
    for position in range(0,204,2):
        letters=set()
        for x,y in itertools.product(interim[position],interim[position+1]):
            letter=square[6*COORD.index(x)+COORD.index(y)]
            letters.update(unused if letter=="?"else letter)
        shared_domains.append("".join(sorted(letters)))
    composite=data["third_part_composite"]
    assert shared_domains==composite["source_only_domains"]
    assert "".join(d if len(d)==1 else "?"for d in shared_domains)==composite["source_only_domain_template"]
    assert sum(len(d)==1 for d in shared_domains)==composite["source_only_singleton_positions"]==97
    chosen=restored[:41]+b[41]+restored[42:]
    assert composite["chosen_parallel_positions_0based"]==[41] and chosen==composite["ciphertext"]
    assert arithmetic(chosen,ranks,square)[0]==composite["plaintext"]
    assert compare(a,chosen[20:])==composite["cost_against_p166_A3"]
    assert compare(b,chosen)==composite["cost_against_p167_A3"]
    normalized=composite["editorial_emendation"]
    normalized_cost=check_edition(chosen,normalized)
    assert normalized_cost=={"known_coordinate_substitutions":2,"erasure_fills":0}
    assert compare(a,normalized["ciphertext"][20:])==normalized["cost_against_p166_A3"]
    assert compare(b,normalized["ciphertext"])==normalized["cost_against_p167_A3"]
    assert len(normalized["cost_against_p166_A3"]["known_coordinate_substitutions"])==3
    assert len(normalized["cost_against_p167_A3"]["known_coordinate_substitutions"])==4
    assert len(normalized["cost_against_p167_A3"]["erasure_fills"])==1
    # All reserve-division question marks in the readable frames refer to one identical square cell.
    selected=[by_id["p166_A2"]["editions"][0]["ciphertext"],by_id["p170_B1"]["editions"][0]["ciphertext"],
              by_id["p170_B2"]["editions"][0]["ciphertext"],normalized["ciphertext"]]
    reserve_cells=[]
    for cipher in selected:
        text,domains,cells=arithmetic(cipher,ranks,square)
        questions=[i for i,c in enumerate(text)if c=="?"]
        assert len(questions)==1
        pos=questions[0];assert domains[pos]=="56" and len(cells[pos])==1
        reserve_cells.append(cells[pos][0])
    assert len(set(reserve_cells))==1
    return {"status":"passed","source_records":6,"source_slots":sum(len(r["analysis_ciphertext"])for r in data["records"]),
            "source_pdf_hash_checked":bool(pdf),"prefix_coordinates_recovered_from_parallel":20,
            "prefix_recovery_unchanged_source_coordinates":184,"restored_geometry_positions":102,
            "source_only_consensus_singletons":97,"reserve_digit_global_alternatives":[5,6],
            "reserve_cell_row_column":COORD[reserve_cells[0]//6]+COORD[reserve_cells[0]%6],
            "records":summaries,
            "scope":"Independent cipher arithmetic, source placement and edit checks. Readable word choices remain editorial; no full plaintext is claimed for p170 A."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf",type=Path)
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args();report=verify(args.pdf)
    print(json.dumps(report,indent=2)if args.json else "Operational parallels: 6 records, 1,248 source slots; 20-coordinate prefix and all edit checks verified.")

if __name__=="__main__":main()
