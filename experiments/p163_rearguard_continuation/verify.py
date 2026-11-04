#!/usr/bin/env python3
"""Audit two linked p163 rearguard passages without completing the unknown key."""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains

CO = "ADFGVX"
AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def checked(ref):
    path = ROOT / ref["path"]
    assert sha(path) == ref["sha256"], ref["path"]
    return path


def read(wire, ranks, square):
    """Independent ragged-column offsets, marginal domains, and source origins."""
    n, width = len(wire), len(ranks)
    assert n % 2 == 0 and sorted(ranks) == list(range(1, width + 1))
    height, extra = divmod(n, width)
    lengths = [height + (col < extra) for col in range(width)]
    offsets = [sum(lengths[j] for j in range(width) if ranks[j] < ranks[col])
               for col in range(width)]
    origins = [offsets[i % width] + i // width for i in range(n)]
    assert sorted(origins) == list(range(n))
    unassigned = set(AL) - set(square)
    positions = []
    for i in range(n // 2):
        a, b = origins[2*i:2*i+2]
        pair = wire[a] + wire[b]
        rows = [CO.index(pair[0])] if pair[0] in CO else range(6)
        cols = [CO.index(pair[1])] if pair[1] in CO else range(6)
        values = set()
        for row in rows:
            for col in cols:
                c = square[6*row+col]
                values.update(unassigned if c == "?" else c)
        domain = "".join(sorted(values))
        positions.append(dict(plaintext_position_0based=i,
                              source_positions_0based=[a, b], pair=pair,
                              domain=domain, raw=domain if len(domain) == 1 else "?"))
    domains = [p["domain"] for p in positions]
    raw = "".join(p["raw"] for p in positions)
    assert raw == decrypt(wire, ranks, square)
    assert domains == plaintext_domains(wire, ranks, square)
    return dict(plaintext=raw, fixed_positions=sum(len(d) == 1 for d in domains),
                positions=positions)


def encode_pair(char, square):
    cell = square.index(char)
    return CO[cell // 6] + CO[cell % 6]


def ledger(before, after, original, reading):
    owner = {j: p["plaintext_position_0based"] for p in reading["positions"]
             for j in p["source_positions_0based"]}
    observed, fills = [], []
    for j, (a, b) in enumerate(zip(before, after)):
        if a == b:
            continue
        row = dict(source_position_0based=j, plaintext_position_0based=owner[j],
                   before=a, literal_source=original[j], proposed=b)
        (fills if a == "?" else observed).append(row)
    return dict(observed_substitutions=observed, printed_erasure_fills=fills,
                counts=dict(observed_substitutions=len(observed),
                            printed_erasure_fills=len(fills)))


def completions(square):
    cells = [i for i, c in enumerate(square) if c == "?"]
    missing = sorted(set(AL) - set(square))
    assert missing == ["5", "6"] and len(cells) == 2
    result = []
    for labels in permutations(missing):
        value = list(square)
        assignment = {}
        for cell, char in zip(cells, labels):
            value[cell] = char
            assignment[CO[cell//6] + CO[cell % 6]] = char
        result.append(("".join(value), assignment))
    return result


def variant(rec, start, text, ranks, square):
    original = rec["literal"]
    source = rec["source"]
    baseline = rec["baseline_wire"]
    raw = rec["raw"]
    result = list(baseline)
    evidence = []
    for i, char in enumerate(text, start):
        position = raw["positions"][i]
        pair = encode_pair(char, square)
        for j, value in zip(position["source_positions_0based"], pair):
            result[j] = value
        evidence.append(dict(**position, proposed=char, proposed_pair=pair,
                             observed_coordinate_count=sum(c in CO for c in position["pair"])))
    result = "".join(result)
    edited = read(result, ranks, square)
    assert edited["plaintext"][start:start+len(text)] == text
    new = [i for i, (a, b) in enumerate(zip(rec["baseline"]["positions"], edited["positions"]))
           if len(a["domain"]) > 1 and len(b["domain"]) == 1]
    witnesses = []
    if "?" not in result:
        for full_square, assignment in completions(square):
            plain = decrypt(result, ranks, full_square)
            assert "?" not in plain
            assert encrypt(plain, ranks, full_square) == result
            witnesses.append(dict(assignments=assignment, square=full_square,
                                  plaintext=plain, exact_roundtrip=True))
    return dict(start_plaintext_position_0based=start, proposed_span=text,
                ciphertext=result, plaintext=edited["plaintext"],
                fixed_positions=edited["fixed_positions"],
                newly_fixed_positions_0based=new,
                span_evidence=evidence,
                wholly_unobserved_new_positions_0based=[i for i in new
                    if all(c == "?" for c in raw["positions"][i]["pair"])],
                extension_cost=ledger(baseline, result, original, raw),
                total_cost=ledger(source, result, original, raw),
                remaining_source_erasures_0based=[j for j, c in enumerate(result) if c == "?"],
                global_digit_witnesses=witnesses)


def joint_repeat(records, square, specification):
    word = specification["word"]
    spans = specification["aligned_spans"]
    alignments = []
    for offset, char in enumerate(word):
        witnesses = []
        for span in spans:
            i = span["start"] + offset
            p = records[span["record"]]["raw"]["positions"][i]
            witnesses.append(dict(record=span["record"], **p))
        alignments.append(dict(word_position_0based=offset, proposed=char, witnesses=witnesses))
    assignment_results = []
    for full_square, assignments in completions(square):
        options = []
        minimum = 0
        for a in alignments:
            costs = {char: sum(observed in CO and observed != wanted
                              for witness in a["witnesses"]
                              for observed, wanted in zip(witness["pair"], encode_pair(char, full_square)))
                     for char in AL}
            best = min(costs.values())
            values = "".join(sorted(char for char, price in costs.items() if price == best))
            minimum += best
            options.append(dict(word_position_0based=a["word_position_0based"],
                                minimum_observed_substitutions=best, labels=values))
        words = ["".join(chars) for chars in product(*(p["labels"] for p in options))]
        assert word in words
        assignment_results.append(dict(assignments=assignments,
                                       minimum_observed_substitutions=minimum,
                                       minimum_options=options, tied_common_strings=words))
    assert assignment_results[0]["minimum_options"] == assignment_results[1]["minimum_options"]
    assert assignment_results[0]["tied_common_strings"] == assignment_results[1]["tied_common_strings"]
    options = assignment_results[0]["minimum_options"]
    assert assignment_results[0]["minimum_observed_substitutions"] == 4
    assert len(assignment_results[0]["tied_common_strings"]) == 96
    raw_support = []
    for a in alignments:
        first, second = a["witnesses"]
        if len(second["domain"]) > 1 and first["domain"] == a["proposed"]:
            raw_support.append(dict(word_position_0based=a["word_position_0based"],
                                    label=a["proposed"],
                                    a13_position_0based=first["plaintext_position_0based"],
                                    a15_position_0based=second["plaintext_position_0based"]))
    assert len(raw_support) == 7
    jointly_unobserved = [dict(word_position_0based=a["word_position_0based"], coordinate_half=h)
                          for a in alignments for h in range(2)
                          if all(w["pair"][h] == "?" for w in a["witnesses"])]
    assert jointly_unobserved == [dict(word_position_0based=7, coordinate_half=0)]
    return dict(assumption=specification["assumption"], alignments=alignments,
                forced_letters_at_minimum=sum(len(x["labels"]) == 1 for x in options),
                minimum_observed_substitutions=4, tied_common_strings_count=96,
                wholly_unobserved_shared_coordinate_halves=jointly_unobserved,
                a15_new_word_letters_with_unmodified_a13_singleton_support=raw_support,
                global_assignment_results=assignment_results)


def run():
    inputs = json.loads((HERE / "inputs.json").read_text())
    base = json.loads(checked(inputs["baseline_inputs"]).read_text())
    cert = json.loads(checked(inputs["baseline_certificates"]).read_text())
    checked(inputs["source_image"])
    checked(inputs["linked_opening"]["source_image"])
    key = base["key"]
    ranks, square = key["column_rank_order"], key["square"]
    published = next(k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]
                     if k["id"] == key["id"])
    assert (ranks, square) == (published["column_rank_order"], published["square"])
    records = {}
    for identifier in ["p163_A13", "p163_A15"]:
        source_record = next(r for r in base["records"] if r["id"] == identifier)
        existing = next(r for r in cert["records"] if r["id"] == identifier)
        literal = "".join("".join(source_record["source_rows"]).split())
        source = literal.replace("-", "?")
        raw = read(source, ranks, square)
        baseline_wire = existing["edition"]["ciphertext"]
        baseline = read(baseline_wire, ranks, square)
        assert source == existing["source_ciphertext"]
        assert raw["plaintext"] == existing["raw"]["plaintext"]
        assert [p["domain"] for p in raw["positions"]] == existing["raw"]["domains"]
        assert [p["source_positions_0based"] for p in raw["positions"]] == existing["raw"]["source_position_pairs_0based"]
        assert baseline["plaintext"] == existing["edition"]["reading"]["plaintext"]
        assert sha256(literal.encode()).hexdigest() == existing["source_sha256"]
        records[identifier] = dict(id=identifier, literal=literal, source=source,
                                   raw=raw, baseline_wire=baseline_wire, baseline=baseline,
                                   advertised_length=source_record["advertised_length"])
    assert len(records["p163_A13"]["source"]) == 268
    assert records["p163_A13"]["advertised_length"] == 278
    target = records["p163_A15"]
    assert len(target["source"]) == 234 and target["source"].count("?") == 81
    assert target["source"][140] == "X"
    primary = variant(target, inputs["proposal"]["start_plaintext_position_0based"],
                      inputs["proposal"]["text"], ranks, square)
    assert primary["extension_cost"]["counts"] == dict(observed_substitutions=1, printed_erasure_fills=18)
    assert primary["total_cost"]["counts"] == dict(observed_substitutions=3, printed_erasure_fills=81)
    assert primary["fixed_positions"] == 116 and len(primary["newly_fixed_positions_0based"]) == 18
    assert primary["wholly_unobserved_new_positions_0based"] == []
    assert all(p["observed_coordinate_count"] >= 1 for p in primary["span_evidence"])
    assert sum(p["observed_coordinate_count"] for p in primary["span_evidence"]) == 34
    for i, char in [(92, "7"), (100, "3")]:
        assert target["raw"]["positions"][i]["domain"] == char
        assert primary["plaintext"][i] == char
    comparisons = {p["id"]: variant(target, p["start"], p["text"], ranks, square)
                   for p in inputs["comparison_proposals"]}
    assert comparisons["after_only_three"]["extension_cost"]["counts"] == primary["extension_cost"]["counts"]
    assert comparisons["name_string"]["extension_cost"]["counts"] == primary["extension_cost"]["counts"]
    openings = {p["id"]: variant(records["p163_A13"], p["start"], p["text"], ranks, square)
                for p in inputs["linked_opening"]["variants"]}
    for identifier, observed in [("repeated_word", 3), ("separator", 4), ("aus_context", 6)]:
        assert openings[identifier]["extension_cost"]["counts"] == dict(observed_substitutions=observed, printed_erasure_fills=2)
        assert openings[identifier]["fixed_positions"] == 134
        assert len(openings[identifier]["newly_fixed_positions_0based"]) == 2
        assert openings[identifier]["plaintext"][3] == records["p163_A13"]["raw"]["plaintext"][3] == "3"
    witness = inputs["native_word_witness"]
    wi = json.loads(checked(witness["inputs"]).read_text())
    wc = json.loads(checked(witness["certificates"]).read_text())
    wr = next(r for r in wi["records"] if r["id"] == witness["record"])
    wcert = next(r for r in wc["records"] if r["id"] == witness["record"])
    source = "".join("".join(wr["source_rows"]).split())
    reading = read(source, wi["key"]["column_rank_order"], wi["key"]["square"])
    assert reading["plaintext"] == wcert["raw"]
    start = witness["start_plaintext_position_0based"]
    assert reading["plaintext"][start:start+len(witness["word"]) ] == witness["word"]
    native = dict(record=witness["record"], span=reading["positions"][start:start+len(witness["word"])],
                  observed_substitutions=0, erasure_fills=0)
    assert all(p["pair"].count("?") == 0 and len(p["domain"]) == 1 for p in native["span"])
    historical = inputs["historical_word_witness"]
    assert historical["attested_cipher_spelling"] in historical["short_quotation"].upper()
    summary = dict(physical_sources_added=0, raw_fixed_positions_added=0,
                   proposed_fixed_position_gain=20,
                   a15_raw_fixed=36, a15_prior_edited_fixed=98, a15_proposed_fixed=116,
                   a15_extension_observed_substitutions=1, a15_extension_printed_erasure_fills=18,
                   a13_prior_edited_fixed=132, a13_proposed_fixed=134,
                   a13_word_extension_observed_substitutions=3, a13_word_extension_printed_erasure_fills=2,
                   a13_separator_additional_observed_substitutions=1,
                   a13_aus_additional_observed_substitutions=2,
                   joint_repeat_minimum_observed_substitutions=4, joint_repeat_tied_common_strings=96)
    return dict(schema="adfgvx-p163-rearguard-certificate-v1", prepared_by=inputs["prepared_by"],
                inputs_sha256=sha(HERE / "inputs.json"), summary=summary,
                baselines={k: dict(source_sha256=sha256(r["literal"].encode()).hexdigest(),
                                   source_ciphertext=r["source"], raw=r["raw"],
                                   prior_edited_plaintext=r["baseline"]["plaintext"],
                                   prior_edited_fixed_positions=r["baseline"]["fixed_positions"])
                           for k, r in records.items()},
                a15_primary=primary, a15_comparisons=comparisons, a13_variants=openings,
                joint_repeat=joint_repeat(records, square, inputs["joint_repeat_model"]),
                native_word_witness=native, historical_word_witness=historical)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = run()
    path = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(dict(verified=args.verify, **result["summary"]), indent=2))
