"""Source-cost and scoring-sensitivity analysis of the exact p109 results.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The phrase probes are post-hoc diagnostics; none constrains the decoder.
"""
from argparse import ArgumentParser
from collections import Counter
import json
from pathlib import Path

from compute import ALPHABET, HERE, candidate_record, square_pairs, symbol_cost


PROBES = [
    ("SAVA", 18), ("SAVE", 18), ("SAVM", 18), ("SAV4", 18),
    ("UEBERGANG", 23), ("UEBURGANG", 23), ("UMBURGANG", 23), ("UEB0RGANG", 23),
    ("TEILE", 39), ("XALLE", 39),
    ("1WEITERE", 52), ("HWEITERE", 52), ("ZWEITERE", 52),
    ("FDLXDIV", 60), ("FDUXDIV", 60), ("FDUXDIE", 60),
    ("ERKANNT", 86),
]


def completion_counts(data, start, stop, budget):
    counts = [1] + [0] * budget
    for row, minimum in zip(data["position_costs"][start:stop], data["position_minima"][start:stop]):
        multiplicities = Counter(cost - minimum for cost in row)
        counts = [sum(counts[old] * multiplicities[cost - old] for old in range(cost + 1))
                  for cost in range(budget + 1)]
    coordinate_types = Counter()
    for observed in data["intermediate_observations"][start:stop]:
        for first, second in zip(*observed):
            coordinate_types["one_observed" if "?" in (first, second)
                             else "two_agree" if first == second else "two_disagree"] += 1
    assert counts[0] == 2 ** coordinate_types["two_disagree"]
    return {"global_plaintext_span": [start, stop], "coordinate_types": dict(coordinate_types),
            "count_polynomial": "(1+5x^2)^two_agree * (2+4x)^two_disagree * (1+5x)^one_observed",
            "counts_by_exact_excess_budget": [str(count) for count in counts],
            "total_through_maximum_budget": str(sum(counts))}


def phrase_probe(data, word, position, runs):
    pairs = square_pairs(data["square"])
    stop = position + len(word)
    minimum = sum(data["position_minima"][position:stop])
    per_witness = {}
    for witness_number, name in enumerate(data["ciphertexts"]):
        per_witness[name] = sum(symbol_cost(pairs[symbol], [data["intermediate_observations"][i][witness_number]])
                                for i, symbol in enumerate(word, position))
    total = sum(per_witness.values())
    occurrences = []
    for run in runs:
        local = position - run["global_plaintext_span"][0]
        hits = [{"excess_budget": row["excess_budget"], "rank": candidate["rank"]}
                for row in run["by_exact_excess_budget"] for candidate in row["candidates"]
                if candidate["plaintext"][local:local + len(word)] == word]
        best = [{"excess_budget": row["excess_budget"]}
                for row in run["by_exact_excess_budget"]
                if row["candidates"][0]["plaintext"][local:local + len(word)] == word]
        occurrences.append({"scope": run["scope"], "objective": run["objective"],
                            "top_one_budgets": best, "reported_top_ten_occurrences": hits})
    return {"word": word, "global_plaintext_span": [position, stop],
            "minimum_cost_for_this_span_without_word_constraint": minimum,
            "word_coordinate_cost": total, "word_cost_by_witness": per_witness,
            "extra_coordinate_cost_needed": total - minimum,
            "minimum_full_message_cost_if_only_this_word_is_required": 42 + total - minimum,
            "reported_rankings": occurrences}


def stable_intervals(data, runs, minimum_length=4):
    # All top-one hypotheses, including both scopes and every exact budget,
    # are compared on the body shared by all four runs.
    texts = [(run["global_plaintext_span"][0], row["candidates"][0]["plaintext"])
             for run in runs for row in run["by_exact_excess_budget"]]
    intervals = []
    start = None
    for position in range(6, 115):
        values = {text[position - offset] for offset, text in texts} if position < 114 else set()
        if len(values) == 1:
            if start is None:
                start = position
        elif start is not None:
            if position - start >= minimum_length:
                text = texts[0][1][start - texts[0][0]:position - texts[0][0]]
                unique_minimum = sum(sum(value == minimum for value in row) == 1
                                     for row, minimum in zip(data["position_costs"][start:position],
                                                             data["position_minima"][start:position]))
                intervals.append({"global_plaintext_span": [start, position], "text": text,
                                  "length": len(text), "top_one_hypotheses_compared": len(texts),
                                  "positions_unique_in_minimum_cost_domains": unique_minimum,
                                  "positions_selected_from_multiple_minimum_cost_letters": len(text) - unique_minimum})
            start = None
    return sorted(intervals, key=lambda row: (-row["length"], row["global_plaintext_span"]))


def budget_envelopes(runs):
    envelopes = []
    for run in runs:
        available = []
        rows = []
        for exact in run["by_exact_excess_budget"]:
            available.extend(exact["candidates"])
            # Prefer lower source cost when language scores are identical;
            # the remaining tie is ordinary ASCII lexical order.
            best = min(available, key=lambda row: (-row["integer_objective"],
                                                   row["excess_coordinate_substitutions"], row["plaintext"]))
            rows.append({"maximum_allowed_excess_budget": exact["excess_budget"],
                         "selected_exact_excess_budget": best["excess_coordinate_substitutions"],
                         "integer_objective": best["integer_objective"],
                         "plaintext": best["plaintext"]})
        envelopes.append({"scope": run["scope"], "objective": run["objective"],
                          "tie_order": "Higher language score, then lower coordinate cost, then ASCII lexical text",
                          "every_exact_budget_improves_the_best_at_most_score": all(
                              row["maximum_allowed_excess_budget"] == row["selected_exact_excess_budget"] for row in rows),
                          "best_with_at_most_budget": rows})
    return envelopes


def summarize(result):
    data, runs = result["input"], result["runs"]
    budget = max(run["maximum_excess_budget"] for run in runs)
    counts = [completion_counts(data, *span, budget) for span in ((0, 124), (6, 114))]
    probes = [phrase_probe(data, word, position, runs) for word, position in PROBES]
    stable = stable_intervals(data, runs)
    assert stable[0]["global_plaintext_span"] == [67, 114]
    zero_budget_bodies = []
    for run in runs:
        text = run["by_exact_excess_budget"][0]["candidates"][0]["plaintext"]
        offset = run["global_plaintext_span"][0]
        zero_budget_bodies.append(text[6 - offset:114 - offset])
    assert len(set(zero_budget_bodies)) == 1
    return {
        "schema": "adfgvx-parallel-decoder-summary-v1", "project": "ADFGVX Cipher",
        "authors": "icekylinx and GPT-6 Astra Pro", "case": "p109",
        "status": "Exact model rankings and source costs, with no accepted new historical letters",
        "minimum_cost_common_body_top_one": zero_budget_bodies[0],
        "all_four_runs_agree_at_their_minimum_coordinate_cost": True,
        "completion_counts": counts,
        "shared_top_one_body_intervals": stable,
        "at_most_budget_envelopes": budget_envelopes(runs),
        "post_hoc_phrase_probes": probes,
        "joint_editorial_phrase_cost": {
            "phrases": ["SAVA or SAVE at18", "UEBERGANG at23", "TEILE at39"],
            "minimum_excess_for_these_disjoint_constraints": 4,
            "minimum_full_coordinate_cost": 46,
            "scope": "Exact source-cost arithmetic; does not say the resulting full sentence is a model optimum or historical truth.",
        },
        "source_nomenclature_context": {
            "url": "https://www.archivinformationssystem.at/detail.aspx?ID=7182872",
            "repository": "Austrian State Archives",
            "record": "AT-OeStA/KA NL B/522.4.10",
            "document_date": "1918-10-26",
            "catalogue_title": "Durchschlag eines Befehls an Ludwig Kralik zum Übergang über Save und Donau",
            "scope": "The archive catalogue uses Save for the river in a contemporary crossing-order record. The original document image was not inspected, and this is not a parallel plaintext witness.",
        },
        "limits": [
            "Both scoring objectives use the same independently sourced corpus. Agreement is sensitivity evidence, not statistically independent evidence.",
            "The model rankings do not endorse SAVM, UEBURGANG, LETZTERXALLE, HWEITERE, FDU, or DIEX as historical readings.",
            "No signature, call sign, digit, or ending is assigned from a language-model optimum.",
            "Absence from a reported top-ten list is not an impossibility proof or a global rank calculation.",
            "The42-cost minimum and2^42 count assume one common full plaintext and the fixed earlier repair of D; different endings may have been sent.",
        ],
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "p109_results.json")
    parser.add_argument("--output", type=Path, default=HERE / "p109_summary.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    summary = summarize(json.loads(args.input.read_text()))
    if args.verify:
        assert json.loads(args.output.read_text()) == summary
        print("Parallel-decoder counts, cost probes, and agreement intervals verified")
    else:
        args.output.write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps({"stable_interval": summary["shared_top_one_body_intervals"][0],
                          "word_costs": [{key: row[key] for key in ("word", "extra_coordinate_cost_needed", "word_cost_by_witness")}
                                         for row in summary["post_hoc_phrase_probes"]]}, indent=2))


if __name__ == "__main__":
    main()
