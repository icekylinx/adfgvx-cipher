#!/usr/bin/env python3
"""Check the shared J cell in the separate p219 Kiev source model.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import itertools
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(pdf=None):
    data = json.loads((HERE / "kiev_inputs.json").read_text())
    for dep in data["dependencies"]:
        assert hashlib.sha256((ROOT / dep["path"]).read_bytes()).hexdigest() == dep["sha256"], dep["path"]
    source_dir = ROOT / data["source_package"]
    source = load_module("kiev_source", source_dir / "verify.py")
    original, _ = source.build(pdf)
    assert original == json.loads((source_dir / "certificates.json").read_text())
    manifest = json.loads((source_dir / "inputs.json").read_text())
    shared = load_module("breslau_digits", HERE / "verify_breslau.py").run()
    assert shared == json.loads((ROOT / data["shared_square_certificate"]).read_text())
    reader = load_module("nov25_reader", ROOT / "experiments/nov25_letter_constraint/verify.py")
    partial = shared["conditional_partial_square"]
    baseline, ranks = manifest["key"]["square"], manifest["key"]["column_rank_order"]
    literal, _, _ = source.parse_annotations(manifest["records"][0]["source_rows_annotated"])
    converted = "".join("?" if c == "?" else partial[baseline.index(c)]
                        for c in manifest["primary_template"])
    proposal = data["name_proposal"]
    start, end = proposal["range"]
    assert converted[start:end] == proposal["conditional_raw"]
    template = converted[:start] + proposal["proposed"] + converted[end:]
    coordinates = "".join("??" if c == "?" else reader.CO[partial.index(c) // 6] +
                          reader.CO[partial.index(c) % 6] for c in template)
    wanted = "".join(coordinates[c::len(ranks)]
                     for c in sorted(range(len(ranks)), key=lambda c: ranks[c]))
    prices, candidates = [], []
    for choices, duplicate in itertools.product(itertools.product([0, 1, 2], repeat=3), [None, 0, 5]):
        native, mapping, excluded = source.frame(literal, choices, duplicate)
        edited = "".join(b if b != "?" else a for a, b in zip(native, wanted))
        changes = [{"frame_index": i, "source_index": mapping[i], "from": a, "to": b,
                    "kind": "inserted_fill" if a == "?" else "observed_substitution"}
                   for i, (a, b) in enumerate(zip(native, edited)) if a != b]
        price = {"parenthetical_choices": list(choices), "duplicate_excluded_start": duplicate,
                 "observed_substitutions": sum(c["kind"] == "observed_substitution" for c in changes),
                 "inserted_fills": sum(c["kind"] == "inserted_fill" for c in changes)}
        decoded = reader.read(edited, ranks, partial)
        assert all(a == "?" or a == b for a, b in zip(template, decoded["plaintext"]))
        candidates.append({**price, "native_ciphertext": native, "edited_ciphertext": edited,
                           "frame_to_source_indices": mapping, "excluded_source_indices": excluded,
                           "conditional_plaintext": decoded["plaintext"], "coordinate_changes": changes,
                           "full_square_witness": reader.witness(edited, ranks, partial)})
        prices.append(price)
    minimum = min(p["observed_substitutions"] for p in prices)
    minima = [r for r in candidates if r["observed_substitutions"] == minimum]
    assert {tuple(r["parenthetical_choices"]) for r in minima} == {(1, 2, 0), (2, 2, 0)}
    assert {r["duplicate_excluded_start"] for r in minima} == {0, 5}
    assert {r["conditional_plaintext"][66:68] for r in minima} == {"6?", "B?"}
    selected = next(r for r in minima if r["parenthetical_choices"] == [1, 2, 0]
                    and r["duplicate_excluded_start"] == 0)
    pos = reader.read(selected["native_ciphertext"], ranks, baseline)["positions"][proposal["shared_letter_position"]]
    assert pos["pair"] == proposal["shared_pair"]
    assert [selected["frame_to_source_indices"][i] for i in pos["frame_indices"]] == proposal["source_indices"]
    assert all(selected["edited_ciphertext"][i] == selected["native_ciphertext"][i] for i in pos["frame_indices"])
    previous = original["records"][0]["optional_name_candidates"]["leader"]
    removed = [c for c in previous["known_coordinate_substitutions"]
               if c["model_index"] in pos["frame_indices"]]
    assert {(c["source_index"], c["from"], c["to"]) for c in removed} == {(181, "V", "F"), (212, "D", "X")}
    assert {(c["source_index"], c["from"], c["to"]) for c in selected["coordinate_changes"]
            if c["kind"] == "observed_substitution"} == {(10, "V", "X"), (155, "A", "F")}
    summary = {"physical_records": 1, "source_observations": len(literal),
               "modeled_coordinates": len(selected["native_ciphertext"]),
               "excluded_observed_coordinates": len(selected["excluded_source_indices"]),
               "added_unknown_slots": selected["native_ciphertext"].count("?"),
               "declared_geometry_maps": len(prices), "minimum_observed_substitutions": minimum,
               "minimum_maps": len(minima), "distinct_edited_streams": len({r["edited_ciphertext"] for r in minima}),
               "inserted_fills": selected["inserted_fills"],
               "prior_name_substitutions": len(previous["known_coordinate_substitutions"]),
               "removed_observed_substitutions": len(removed)}
    assert summary == data["expected"], summary
    case = (ROOT / data["case_path"]).read_text()
    assert "`PEDFJ?RA`" in case and "**two observed-coordinate changes**" in case
    return {"schema": "adfgvx-nov25-kiev-joint-certificate-v1",
            "prepared_by": data["prepared_by"],
            "input_sha256": hashlib.sha256((HERE / "kiev_inputs.json").read_bytes()).hexdigest(),
            "conditional_square": partial, "conditional_template": template,
            "summary": summary, "removed_prior_substitutions": removed,
            "all_geometry_prices": prices, "all_minimum_models": minima,
            "limits": data["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    result = run(args.pdf)
    target = HERE / "kiev_certificate.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
