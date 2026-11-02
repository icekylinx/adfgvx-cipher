"""Portable orchestration for the three archived fixed-permutation searches.

The C engines are preserved without changes. This layer validates inputs,
records exact models and seeds, and keeps fitted candidates unaccepted.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from cipher import (ALPHABET, SYMBOLS, decode, decode_cells, indices, transpose,
                    untranspose, validate_ciphertext, validate_square,
                    whole_cells)

ROOT = Path(__file__).resolve().parent.parent
FAMILIES = {
    "fixed": {"solver": "subsolve", "restarts": 1000, "iterations": 60000,
              "model_kind": "general", "results_directory": "fixed_transposition"},
    "dictionary": {"solver": "marginal_subsolve", "restarts": 1000,
                   "iterations": 60000, "model_kind": "military",
                   "results_directory": "dictionary_permutation_fits"},
    "gap": {"solver": "marginal_subsolve6", "restarts": 120,
            "iterations": 100000, "model_kind": "military",
            "results_directory": "p198_domain_refinement"},
}


def read(path):
    return json.loads(Path(path).read_text())


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(path)


def _part(mid, ciphertext, ranks):
    validate_ciphertext(ciphertext, even=False)
    interim = untranspose(ciphertext, ranks)
    assert transpose(interim, ranks) == ciphertext
    return {"id": mid, "ciphertext": ciphertext, "interim": interim,
            "cells": whole_cells(interim),
            "abandoned_odd_interim_suffix": interim[2 * (len(interim) // 2):],
            "abandoned_odd_source_index": indices(len(ciphertext), ranks).index(len(ciphertext) - 1) if len(ciphertext) % 2 else None,
            "partial_pairs_reduced_to_whole_cell_wildcards": [
                i // 2 for i in range(0, len(interim) - 1, 2)
                if (interim[i] == "?") != (interim[i + 1] == "?")],
            }


def jobs(family, data_directory=ROOT / "data"):
    data_directory = Path(data_directory)
    data = read(data_directory / "input_layers.json")
    inputs = data["archived_inputs"]
    if family == "fixed":
        for mid in ["p73", "p152", "p153a", "p153b", "p170", "p176b", "p189", "p198"]:
            for key in data["fixed_rank_families"]:
                part = _part(mid, inputs[mid]["fixed_search_ciphertext"], key["ranks"])
                yield {"id": mid, "label": mid + "__" + key["id"],
                       "key_id": key["id"], "ranks": key["ranks"],
                       "parts": [part], "cells": part["cells"],
                       "input_layer": "archived fixed_search_ciphertext"}
        for key in data["fixed_rank_families"]:
            parts = [_part(mid, inputs[mid]["fixed_search_ciphertext"], key["ranks"])
                     for mid in ["p153a", "p153b"]]
            yield {"id": "p153_joint", "label": "p153_joint__" + key["id"],
                   "key_id": key["id"], "ranks": key["ranks"], "parts": parts,
                   "cells": "????".join(p["cells"] for p in parts),
                   "part_separator": "Four artificial whole-cell wildcards; transposition resets per part.",
                   "input_layer": "archived fixed_search_ciphertext"}
    elif family == "dictionary":
        selected = read(data_directory / "dictionary_candidates.json")
        pending = []
        for mid in ["p73", "p170"]:
            source = selected["messages"][mid]
            ciphertext = source["ciphertext"]
            validate_ciphertext(ciphertext)
            unique = {}
            for candidate in source["candidates"]:
                ranks = tuple(candidate["ranks"])
                item = unique.setdefault(ranks, {"id": mid, "ciphertext": ciphertext,
                    "ranks": list(ranks), "selection_records": []})
                item["selection_records"].append({k: v for k, v in candidate.items()
                                                   if k not in ["ranks", "cells"]})
            for item in unique.values():
                item["priority"] = min(x["rank"] for x in item["selection_records"])
                item["interim"] = untranspose(ciphertext, item["ranks"])
                item["label"] = mid + "__" + hashlib.sha256(json.dumps(item["ranks"]).encode()).hexdigest()[:16]
                item["input_layer"] = "exact archived dictionary selector ciphertext"
                pending.append(item)
        yield from sorted(pending, key=lambda x: (x["priority"], len(x["ranks"]), x["id"]))
    elif family == "gap":
        seeds = read(data_directory / "p198_warm_starts.json")
        ciphertext = inputs["p198"]["archived_ciphertext"]
        assert len(ciphertext) == 165
        for seed in seeds["cases"]:
            ranks = seeds["keys"][seed["key_id"]]
            gap = seed["gap_position"]
            restored = ciphertext[:gap] + "?????" + ciphertext[gap:]
            validate_ciphertext(restored)
            if seed["initial_square"] is not None:
                validate_square(seed["initial_square"])
            yield {**seed, "id": "p198", "ranks": ranks,
                   "received_ciphertext": ciphertext, "ciphertext": restored,
                   "gap_length": 5, "interim": untranspose(restored, ranks),
                   "sixgram_weight": 0.7, "input_layer": "received source plus five unresolved slots"}
    else:
        raise ValueError(f"Unknown family {family}")


def seed_for(family, label, offset=0):
    size = 4 if family == "fixed" else 8
    base = int.from_bytes(hashlib.sha256(label.encode()).digest()[:size], "little")
    return (base + (1918 if family == "fixed" else 0) + offset) % (2 ** 64)


def validate_result(family, job, best):
    validate_square(best["square"])
    if family == "fixed":
        assert decode_cells(job["cells"], best["square"]) == best["plaintext"]
        for part in job["parts"]:
            assert transpose(part["interim"], job["ranks"]) == part["ciphertext"]
    else:
        assert decode(job["interim"], best["square"]) == best["plaintext"]
        assert transpose(job["interim"], job["ranks"]) == job["ciphertext"]
    return True


def main(family):
    defaults = FAMILIES[family]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-directory", type=Path, default=ROOT / "data")
    parser.add_argument("--model", type=Path, help="Exact 36^4 float32 quadgram table")
    parser.add_argument("--six-model", type=Path, help="G6HASH2 table, required by gap refinement")
    parser.add_argument("--solver", type=Path, default=ROOT / "bin" / defaults["solver"])
    parser.add_argument("--output", type=Path, default=ROOT / "work" / defaults["results_directory"])
    parser.add_argument("--restarts", type=int, default=defaults["restarts"])
    parser.add_argument("--iterations", type=int, default=defaults["iterations"])
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--only", action="append", default=[], help="Case-label glob; repeatable")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--list", action="store_true", help="List selected cases without fitting")
    parser.add_argument("--allow-different-model", action="store_true", help="Mark a new experiment with a different table")
    args = parser.parse_args()
    if not 1 <= args.restarts <= 2147483647 or not 1 <= args.iterations <= 2147483647 or args.workers < 1 or args.limit < 0:
        parser.error("Restart and iteration counts must fit positive C int; workers must be positive and limit nonnegative")
    selected = [j for j in jobs(family, args.data_directory)
                if not args.only or any(fnmatch.fnmatchcase(j["label"], p) for p in args.only)]
    if args.reverse:
        selected.reverse()
    if args.limit:
        selected = selected[:args.limit]
    if args.list:
        print(json.dumps({"family": family, "cases": len(selected), "labels": [j["label"] for j in selected]}, indent=2))
        return
    if args.model is None or (family == "gap" and args.six_model is None):
        parser.error("--model is required; gap refinement also requires --six-model")
    if sys.byteorder != "little":
        parser.error("The archived native C solvers require a little-endian platform")
    if args.model.stat().st_size != 4 * 36 ** 4:
        parser.error("The quadgram table must contain exactly 36^4 float32 values")
    provenance = read(args.data_directory / "model_provenance.json")
    expected = (provenance["general_model"]["sha256"] if family == "fixed"
                else provenance["military_model"]["quad"]["sha256"])
    model_hash = sha256(args.model)
    six_hash = sha256(args.six_model) if args.six_model else None
    canonical = model_hash == expected and (family != "gap" or six_hash == provenance["military_model"]["six"]["sha256"])
    if not canonical and not args.allow_different_model:
        parser.error("Model hashes differ from the archived recipe; use --allow-different-model for a new experiment")
    args.output.mkdir(parents=True, exist_ok=True)
    run = {"family": family, "case_count": len(selected), "restarts_per_case": args.restarts,
           "iterations_per_restart": args.iterations,
           "configured_proposal_slots": len(selected) * args.restarts * args.iterations,
           "model_sha256": model_hash, "six_model_sha256": six_hash,
           "solver_sha256": sha256(args.solver), "canonical_model_hashes": canonical,
           "seed_offset": args.seed_offset, "classification": "No plaintext is accepted automatically.",
           "started_utc": datetime.now(timezone.utc).isoformat()}
    def recipe(job):
        seed = seed_for(family, job["label"], args.seed_offset)
        fingerprint_data = {"job": job, "seed": seed, "restarts": args.restarts,
                            "iterations": args.iterations, "model": model_hash,
                            "six_model": six_hash, "solver": run["solver_sha256"]}
        fingerprint = hashlib.sha256(json.dumps(fingerprint_data, sort_keys=True).encode()).hexdigest()
        return seed, fingerprint

    # Reject incompatible reuse before replacing the directory's run manifest.
    for job in selected:
        destination = args.output / (job["label"] + ".json")
        if destination.exists() and read(destination).get("recipe_sha256") != recipe(job)[1]:
            raise ValueError(f"Existing result uses a different or unrecorded recipe: {destination}")
    atomic_json(args.output / "RUN.json", run)

    def fit(job):
        seed, fingerprint = recipe(job)
        destination = args.output / (job["label"] + ".json")
        if destination.exists():
            prior = read(destination)
            if prior.get("recipe_sha256") != fingerprint:
                raise ValueError(f"Existing result uses a different or unrecorded recipe: {destination}")
            validate_result(family, job, prior["best"])
            return prior
        if family == "fixed":
            command = [args.solver, args.model, job["cells"], args.restarts, args.iterations, seed]
        elif family == "dictionary":
            command = [args.solver, args.model, job["interim"], args.restarts, args.iterations, seed]
        else:
            command = [args.solver, args.model, args.six_model, job["sixgram_weight"],
                       job["interim"], args.restarts, args.iterations, seed]
            if job["initial_square"] is not None:
                command.append(job["initial_square"])
        started = time.monotonic()
        result = subprocess.run([str(x) for x in command], check=True, capture_output=True, text=True)
        trace = args.output / (job["label"] + ".jsonl")
        trace.write_text(result.stdout)
        rows = [json.loads(line) for line in result.stdout.splitlines()]
        if not rows:
            raise RuntimeError("Archived engine emitted no incumbent; its trace is retained. See the legacy subsolve limitation.")
        best = rows[-1]
        validate_result(family, job, best)
        record = {**job, "best": best, "seed": seed, "restarts": args.restarts,
                  "iterations_per_restart": args.iterations, "seconds": time.monotonic() - started,
                  "recipe_sha256": fingerprint, "model_sha256": model_hash,
                  "six_model_sha256": six_hash, "solver_sha256": run["solver_sha256"],
                  "classification": "unvalidated_search_candidate", "accepted_plaintext": False}
        atomic_json(destination, record)
        return record

    completed = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(fit, job) for job in selected]
        for future in as_completed(futures):
            result = future.result()
            completed.append(result["label"])
            print(json.dumps({"completed": len(completed), "total": len(selected),
                              "label": result["label"], "score": result["best"]["score"]}), flush=True)
    atomic_json(args.output / "SUMMARY.json", {**run, "completed": len(completed),
                "accepted_plaintexts": 0, "completed_labels": sorted(completed),
                "finished_utc": datetime.now(timezone.utc).isoformat()})
