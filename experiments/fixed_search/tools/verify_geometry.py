"""Check the deterministic screen's exact count and optional positive control."""
import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from coordinate_geometry_screen import P, routes, score


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    recorded = json.loads((ROOT / "data/coordinate_geometry_recorded_result.json").read_text())
    fixture = ROOT / "data/geometry_repository/data"
    keys = [k for k in json.loads((fixture / "keys.json").read_text())["keys"] if k["square"].count("?") < 36]
    messages = json.loads((fixture / "messages.json").read_text())["messages"]
    variants = [("synthetic_route_relabel_control", recorded["control"]["ciphertext"])]
    for message in messages:
        ciphertext = message["transcript"]["analysis_ciphertext"]
        if message["id"] == "p198":
            variants.extend(("p198", ciphertext[:gap] + "?????" + ciphertext[gap:]) for gap in range(0, 166, 5))
        else:
            variants.append((message["id"], ciphertext))
    evaluations = 0
    for _, ciphertext in variants:
        for key in keys:
            for ix, _ in routes(len(ciphertext), key["column_rank_order"]):
                assert sorted(map(int, ix)) == list(range(len(ciphertext)))
                evaluations += 2 * len(P)
    assert evaluations == recorded["evaluated_hypotheses"] == 20666880
    assert len(variants) == 39 and len(keys) == 23 and len(P) == 720
    result = {"keys": len(keys), "input_variants": len(variants), "evaluated_hypotheses": evaluations,
              "all_routes_are_coordinate_permutations": True, "matches_recorded_count": True}
    if args.model is not None:
        import hashlib
        assert hashlib.sha256(args.model.read_bytes()).hexdigest() == recorded["model_sha256"]
        quad = np.fromfile(args.model, dtype="<f4")
        ciphertext = recorded["control"]["ciphertext"]
        candidates = []
        for key in keys:
            for ix, route in routes(len(ciphertext), key["column_rank_order"]):
                for swapped in [False, True]:
                    item = score(ciphertext, key["square"], ix, quad, swapped)
                    candidates.append({**item, "key_id": key["id"], "route": route, "gap_position": None})
        best = max(candidates, key=lambda x: x["score"])
        assert best["plaintext"] == recorded["control"]["expected_plaintext"]
        assert best == recorded["results"]["synthetic_route_relabel_control"][0]
        result.update(positive_control_rank_one=True, positive_control_matches_recorded_candidate=True,
                      positive_control_evaluations=len(candidates) * len(P))
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
