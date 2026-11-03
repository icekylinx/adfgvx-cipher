#!/usr/bin/env python3
"""Check delivered crops against the existing source-review references."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.source_evidence import verify_source_evidence


def verify(pdf=None):
    manifest = json.loads((ROOT / 'data/reviews/source_image_publication_20261103.json').read_text())
    assert manifest['schema'] == 'adfgvx-source-image-publication-v1'
    inventory = json.loads((ROOT / manifest['references']).read_text())
    references = {r['reference_id']: r for r in inventory['external_source_references']}
    images = manifest['images']
    assert len(images) == len({r['reference_id'] for r in images}) == 40
    assert {r['reference_id'] for r in images} == set(references)
    assert len({r['path'] for r in images}) == len(images)
    crops = []
    for image in images:
        reference = references[image['reference_id']]
        path = (ROOT / image['path']).resolve()
        assert path.is_relative_to(ROOT) and path.suffix == '.png'
        crop = dict(reference, path=image['path'], storage='embedded_png')
        prior_hash = reference.get('png_sha256', reference.get('sha256',
                                   reference.get('reviewed_local_image_sha256')))
        if prior_hash is not None:
            assert image['png_sha256'] == prior_hash, image['path']
        crop['png_sha256'] = image['png_sha256']
        crops.append(crop)
    report = verify_source_evidence(pdf, inventory['source_pdf'], crops, ROOT)
    assert report['summary']['embedded_pngs_checked'] == len(images)
    assert report['summary']['crops_checked_against_pdf_pixels'] == (len(images) if pdf else 0)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.pdf)['summary'], indent=2))
