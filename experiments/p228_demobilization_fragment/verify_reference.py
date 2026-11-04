#!/usr/bin/env python3
"""Check the optional B1-to-B2 repeated-reference witness, without numeral relabelling."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = 'ADFGVX'


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def geometry(n, ranks):
    forward = [p for c in sorted(range(len(ranks)), key=lambda c: ranks[c])
               for p in range(c, n, len(ranks))]
    inverse = [0] * n
    for source_index, plaintext_half in enumerate(forward):
        inverse[plaintext_half] = source_index
    return forward, inverse


def decode(wire, square, ranks):
    _, inverse = geometry(len(wire), ranks)
    intermediate = ''.join(wire[i] for i in inverse)
    return ''.join('?' if a not in C or b not in C else square[6*C.index(a)+C.index(b)]
                   for a, b in zip(intermediate[::2], intermediate[1::2]))


def encrypt(plaintext, square, ranks):
    intermediate = ''.join(C[square.index(c)//6] + C[square.index(c)%6] for c in plaintext)
    forward, _ = geometry(len(intermediate), ranks)
    return ''.join(intermediate[i] for i in forward)


def build(pdf=None):
    spec = importlib.util.spec_from_file_location('p228_primary', HERE / 'verify.py')
    primary_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(primary_module)
    primary, _ = primary_module.build(pdf)
    assert primary == load(HERE / 'certificates.json')
    record = primary['records'][0]
    data = load(HERE / 'inputs.json')
    previous_path = ROOT / 'experiments/neuhof_demobilization/inputs.json'
    previous = load(previous_path)
    donor_record = next(r for r in previous['records'] if r['id'] == 'p228_B1')
    donor = ''.join(''.join(donor_record['source_rows']).split())
    key = data['key']
    assert key == previous['key']
    square, ranks = key['square'], key['column_rank_order']
    assert len(set(square)) == len(square) == 36
    assert len(donor) == 246
    donor_raw = decode(donor, square, ranks)
    assert donor_raw == donor_record['expected_raw']
    assert donor_raw[25:35] == 'P680YX4GEH'
    assert record['raw'][55:65] == '2680Y??GEH'
    _, donor_inverse = geometry(246, ranks)
    _, target_inverse = geometry(264, ranks)
    layer = record['readable_candidate']
    wire = list(layer['ciphertext'])
    owners = record['model_to_source_indices']
    transfers = []
    for donor_position, target_position in [(30, 60), (31, 61)]:
        donor_sources = donor_inverse[2*donor_position:2*donor_position+2]
        donor_pair = ''.join(donor[i] for i in donor_sources)
        assert all(c in C for c in donor_pair)
        target_models = target_inverse[2*target_position:2*target_position+2]
        target_sources = [owners[i] for i in target_models]
        target_pair = ''.join(wire[i] for i in target_models)
        assert target_pair.count('?') == 1
        fills = []
        for half, (di, mi, si) in enumerate(zip(donor_sources, target_models, target_sources)):
            assert si is not None
            if wire[mi] == '?':
                assert record['literal_source'][si] == '-'
                wire[mi] = donor[di]
                fills.append(dict(half=half, donor_source_index=di, target_model_index=mi,
                                  target_source_index=si, original_target='-', value=donor[di]))
            else:
                assert wire[mi] == donor[di]
        assert len(fills) == 1
        label = donor_raw[donor_position]
        assert label in record['positions'][target_position]['domain']
        transfers.append(dict(donor_plaintext_index=donor_position, target_plaintext_index=target_position,
                              donor_source_indices=donor_sources, donor_pair=donor_pair,
                              target_source_indices=target_sources, target_pair_before=target_pair,
                              label=label, fills=fills))
    wire = ''.join(wire)
    optional_raw = decode(wire, square, ranks)
    expected = list(layer['raw'])
    expected[60:62] = 'X4'
    assert optional_raw == ''.join(expected)
    assert 132 - optional_raw.count('?') == 123
    assert [(i, b) for i, (a, b) in enumerate(zip(layer['ciphertext'], wire)) if a != b] == [(205, 'D'), (255, 'G')]
    assert all(a == b for i, (a, b) in enumerate(zip(layer['raw'], optional_raw)) if i not in (60, 61))
    full_wire = wire.replace('?', 'A')
    full_plaintext = decode(full_wire, square, ranks)
    assert encrypt(full_plaintext, square, ranks) == full_wire
    donor_full = donor.replace('-', 'A')
    donor_full_plaintext = decode(donor_full, square, ranks)
    assert encrypt(donor_full_plaintext, square, ranks) == donor_full
    donor_image = next(x for x in previous['source_images'] if x['id'] == 'p228_B1')
    image_path = previous_path.parent / donor_image['path']
    assert sha(image_path) == donor_image['sha256']
    if pdf is not None:
        import fitz
        from PIL import Image
        with fitz.open(pdf) as document:
            page = document[previous['source']['pdf_page_1based'] - 1]
            scale = donor_image['scale']
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale),
                                    clip=fitz.Rect(donor_image['crop_rectangle_pdf_points']), alpha=False)
        with Image.open(image_path) as image:
            image = image.convert('RGB')
            assert image.size == (pixmap.width, pixmap.height)
            assert image.tobytes() == pixmap.samples
    return dict(schema='adfgvx-p228-repeated-reference-v1', authors=data['authors'],
                dependencies={str(p.relative_to(ROOT)): sha(p) for p in
                              [HERE/'inputs.json', HERE/'certificates.json', previous_path, image_path]},
                indexing='Zero based; ranges half open.',
                hypothesis='The X4GEH suffix in B1 and the ??GEH suffix in B2 refer to the same order-reference field.',
                donor=dict(id='p228_B1', literal_source=donor, raw=donor_raw,
                           field_span=[25,35], field='P680YX4GEH',
                           original_observations_only=True),
                target=dict(id='p228_B2', primary_field_span=[55,65], primary_field='2680Y??GEH',
                            optional_field='2680YX4GEH', optional_raw=optional_raw,
                            optional_ciphertext=wire, fixed_positions=123,
                            observed_substitutions=5, printed_mask_fills=34,
                            added_observed_substitutions=0, added_printed_mask_fills=2,
                            inserted_slot_fills=0, unresolved_positions=[i for i,c in enumerate(optional_raw) if c=='?']),
                transfers=transfers,
                observed_disagreement=dict(donor_plaintext_index=25, donor_label='P',
                                           target_plaintext_index=55, target_label='2', edited=False),
                common_key=key,
                complete_witnesses=[dict(id='p228_B1', ciphertext=donor_full, plaintext=donor_full_plaintext),
                                    dict(id='p228_B2', ciphertext=full_wire, plaintext=full_plaintext)],
                limits=['Field reuse is a contextual hypothesis; these are separate parts, not duplicate telegrams.',
                        'The P/2 discrepancy is retained. No numeral, unit, date, enclosure or command-field interpretation is added.',
                        'Both donors are complete original observed pairs; no earlier word repair or inferred source slot supplies them.',
                        'The primary 121-position word edition and its frame remain unchanged.',
                        'Residual A fills in complete witnesses verify arithmetic only and are not historical readings.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    result = build(args.pdf)
    path = HERE / 'reference_witness.json'
    if args.verify:
        assert load(path) == result, 'Reference witness differs; inspect before regeneration'
    else:
        path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(verified=True, optional_fixed_positions=123, added_printed_mask_fills=2,
                         added_observed_substitutions=0, donor_observations_checked=True,
                         donor_and_target_pdf_pixels_checked=args.pdf is not None)))


if __name__ == '__main__':
    main()
