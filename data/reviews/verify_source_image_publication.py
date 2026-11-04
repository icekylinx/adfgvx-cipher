#!/usr/bin/env python3
"""Check delivered crops against their self-contained source recipes."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.source_evidence import verify_source_evidence


def verify(pdf=None):
    manifest = json.loads((ROOT / 'data/reviews/source_image_publication_20261103.json').read_text())
    assert manifest['schema'] == 'adfgvx-source-image-publication-v2'
    images = manifest['images']
    assert len(images) == len({r['reference_id'] for r in images}) == 40
    assert len({r['path'] for r in images}) == len(images)
    crops = []
    for image in images:
        path = (ROOT / image['path']).resolve()
        assert path.is_relative_to(ROOT) and path.suffix == '.png'
        crop = dict(image, storage='embedded_png')
        crops.append(crop)
    report = verify_source_evidence(pdf, manifest['source_pdf'], crops, ROOT)
    assert report['summary']['embedded_pngs_checked'] == len(images)
    assert report['summary']['crops_checked_against_pdf_pixels'] == (len(images) if pdf else 0)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.pdf)['summary'], indent=2))
