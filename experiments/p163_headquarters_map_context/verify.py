#!/usr/bin/env python3
"""Verify the retained source crops and their limited p163 A17 comparison."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import struct
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify(cache: Path | None = None, fetch: bool = False) -> dict:
    data = json.loads((HERE / "context.json").read_text())
    require(data["schema"] == "adfgvx.primary-map-context.v1", "Schema changed")
    require(data["archive"]["reference"] == "500-12519-274", "Archive reference changed")
    dates = data["date_bounds"]
    require((dates["catalogue_start"], dates["catalogue_end"]) ==
            ("1918-11-13", "1918-11-18"), "Map interval changed")
    require(dates["headquarters_symbol_exact_date"] is None,
            "The map does not date the headquarters symbols individually")
    crops = data["crops"]
    require(len(crops) == 2, "Expected two source crops")
    for crop in crops:
        path = HERE / crop["file"]
        require(digest(path) == crop["sha256"], f"Crop digest differs: {path.name}")
        raw = path.read_bytes()
        require(raw[:8] == b"\x89PNG\r\n\x1a\n", f"Not PNG: {path.name}")
        require(raw[12:16] == b"IHDR", f"Missing PNG IHDR: {path.name}")
        require(list(struct.unpack(">II", raw[16:24])) == crop["dimensions"],
                f"PNG dimensions differ: {path.name}")
    detail, label = crops
    require(detail["tile_zoom"] == 5 and detail["tile_size"] == 256,
            "Detail tile geometry changed")
    require(detail["tile_grid_bbox_xyxy"] == [20, 2, 23, 4], "Tile bounds differ")
    require(detail["tile_pixel_bbox_xyxy"] == [5120, 512, 5888, 1024],
            "Tile pixel bounds differ")
    require([(t["x"], t["y"]) for t in detail["tiles"]] ==
            [(x, y) for y in range(2, 4) for x in range(20, 23)],
            "Missing, repeated, or unordered source tiles")
    require(label["source_bbox_xyxy"] == [335, 225, 660, 415], "Date crop bounds differ")

    link = data["existing_cipher_link"]
    require(link["additional_plaintext_positions"] == 0 and
            link["additional_coordinate_repairs"] == 0,
            "This context package must not claim new cipher recovery")
    cert = json.loads((ROOT / link["certificate_file"]).read_text())
    rec = next(r for r in cert["records"] if r["id"] == link["record"])
    require(rec["source_sha256"] == link["source_sha256"], "Cipher source changed")
    start, end = link["plaintext_span_0based_half_open"]
    require([start, end] == [121, 132], "Cipher span changed")
    require(rec["raw"]["plaintext"][start:end] == link["raw_span"] == "CA2IMANESTI",
            "Raw comparison span changed")
    require(rec["edition"]["reading"]["plaintext"][start:end] ==
            link["edited_span"] == "CALIMANESTI", "Edited comparison span changed")
    pos = link["changed_plaintext_position_0based"]
    pair = rec["raw"]["source_position_pairs_0based"][pos]
    require(pos == 123 and pair == link["source_coordinate_pair_0based"] == [211, 64],
            "Cipher coordinate alignment changed")
    changes = [(i, rec["source_ciphertext"][i], rec["edition"]["ciphertext"][i])
               for i in pair if rec["source_ciphertext"][i] != rec["edition"]["ciphertext"][i]]
    require(changes == [(211, "G", "D")], "Existing repair differs")
    repair = link["existing_coordinate_repair"]
    require(repair == {"source_position_0based": 211, "observed": "G", "proposed": "D"},
            "Documented existing repair differs")

    pixel_comparison = False
    if cache is not None:
        from PIL import Image
        archive = data["archive"]
        items = [dict(url=archive["whole_map_image_url"],
                      cached_name=archive["whole_map_cached_name"],
                      sha256=archive["whole_map_image_sha256"])] + detail["tiles"]
        for item in items:
            path = cache / item["cached_name"]
            if fetch and not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                with urlopen(item["url"], timeout=30) as response:
                    path.write_bytes(response.read())
            require(digest(path) == item["sha256"], f"Source digest differs: {path.name}")
        rebuilt = Image.new("RGB", tuple(detail["dimensions"]))
        for tile in detail["tiles"]:
            with Image.open(cache / tile["cached_name"]) as source:
                require(source.size == (256, 256), "Unexpected tile dimensions")
                rebuilt.paste(source.convert("RGB"),
                              ((tile["x"] - 20) * 256, (tile["y"] - 2) * 256))
        with Image.open(HERE / detail["file"]) as source:
            require(rebuilt.tobytes() == source.convert("RGB").tobytes(),
                    "Headquarters crop pixels differ from original tiles")
        with Image.open(cache / archive["whole_map_cached_name"]) as source:
            require(list(source.size) == archive["whole_map_render_dimensions"],
                    "Whole-map render dimensions differ")
            rebuilt = source.crop(tuple(label["source_bbox_xyxy"])).convert("RGB")
        with Image.open(HERE / label["file"]) as source:
            require(rebuilt.tobytes() == source.convert("RGB").tobytes(),
                    "Date crop pixels differ from original map render")
        pixel_comparison = True
    return dict(status="verified", source_crops=len(crops),
                archive_reference=data["archive"]["reference"],
                source_pixel_comparison=pixel_comparison,
                additional_plaintext_positions=0, additional_coordinate_repairs=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Run local verification (default)")
    parser.add_argument("--source-cache", type=Path, help="Also compare against original source images")
    parser.add_argument("--fetch", action="store_true", help="Fetch missing public images into --source-cache")
    args = parser.parse_args()
    parser.error("--fetch requires --source-cache") if args.fetch and not args.source_cache else None
    print(json.dumps(verify(args.source_cache, args.fetch), indent=2))
