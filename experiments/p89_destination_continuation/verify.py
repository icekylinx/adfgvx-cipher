#!/usr/bin/env python3
"""Verify the conditional p89 destination continuation and its exact prices.

icekylinx and GPT-6 Astra Pro. All indices are zero-based.
The optional --pdf check reproduces five existing Childs crops.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

CO = 'ADFGVX'
ASSIGNMENTS = {129: 'L', 133: 'I', 134: 'E', 135: 'N', 139: 'L',
               140: 'L', 141: 'E', 143: 'X', 164: 'S', 167: 'X'}
SPANS = [dict(start=127, text='MILI'), dict(start=132, text='DIENSTELLENX'),
         dict(start=164, text='S'), dict(start=167, text='X')]


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(data, name):
    return next(r for r in data['records'] if r['id'] == name)


def prior_helpers():
    path = ROOT / 'experiments/p89_guard_battalion_extension/verify.py'
    spec = importlib.util.spec_from_file_location('p89_guard_helpers', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compact(layer):
    return {k: v for k, v in layer.items() if k != 'positions'}


def image_specs(inp):
    results = []
    for ref in inp['source_images']:
        source = ROOT / ref['input_path']; data = load(source)
        entries = data.get('source_images', data.get('source', {}).get('images', []))
        spec = next(x for x in entries if x['path'] == ref['path'])
        path = source.parent / spec['path']
        assert sha(path) == spec['sha256']
        results.append(dict(path=str(path.relative_to(ROOT)), sha256=spec['sha256'],
                            pdf_page_1based=spec['pdf_page_1based'],
                            render_scale=spec.get('render_scale', spec.get('scale')),
                            crop_pdf_points=spec.get('crop_pdf_points', spec.get('clip_points'))))
    assert [x['path'] for x in results] == [
        'experiments/black_sea_evacuation_routes/sources/p89_A3.png',
        'experiments/black_sea_evacuation_routes/sources/p89_A4.png',
        'experiments/black_sea_evacuation_routes/sources/p89_A_header.png',
        'experiments/dunst_assignment/sources/p95_A1.png',
        'experiments/premium_payment_stop/sources/p78_A2.png']
    return results


def check_history(inp):
    from PIL import Image
    assert inp['historical_context'] == dict(path='historical_context.json',
        purpose='Independent contemporary unit-name and city context; no added plaintext labels.')
    data = load(HERE / inp['historical_context']['path']); source = data['source']
    assert source['volume_id'] == '34115495_1918' and source['publication_year'] == 1918
    assert (source['part'], source['printed_page'], source['scan_order']) == ('II', '95', 3421)
    assert source['viewer_url'] == 'https://digital.zlb.de/viewer/image/34115495_1918/3421/'
    full = source['full_image']; region = source['region_image']
    assert (full['file'], region['file']) == ('sources/zlb1918_II95.png', 'sources/zlb1918_II95_guard_infantry.png')
    assert region['region_xywh'] == [1060, 330, 510, 850]
    for item in [full, region]:
        assert sha(HERE / item['file']) == item['sha256']
    original = Image.open(HERE / full['file']).convert('RGB')
    crop = Image.open(HERE / region['file']).convert('RGB')
    assert original.size == (2811, 3876) and crop.size == (510, 850)
    assert original.crop((1060, 330, 1570, 1180)).tobytes() == crop.tobytes()
    return dict(metadata_sha256=sha(HERE / 'historical_context.json'),
                publication_year=1918, part='II', printed_page='95', scan_order=3421,
                full_image_sha256=full['sha256'], region_image_sha256=region['sha256'],
                crop_pixels_verified=True, plaintext_positions_added=0)


def compute():
    inp = load(HERE / 'inputs.json')
    for path, digest in inp['dependencies'].items():
        assert sha(ROOT / path) == digest, path
    assert inp['authors'] == ['icekylinx', 'GPT-6 Astra Pro']
    assert inp['case_path'] == 'cases/military/black_sea_evacuation_routes.md'
    assert len(inp['records']) == 1
    rec = inp['records'][0]
    original_input = load(ROOT / 'experiments/black_sea_evacuation_routes/inputs.json')
    original = record(original_input, 'p89_A3')
    for field in ['id', 'printed_page', 'source_section', 'source_rows', 'source_slots', 'advertised_length', 'expected_raw']:
        assert rec[field] == original[field], field
    assert (rec['id'], rec['printed_page'], rec['source_section']) == ('p89_A3', 89, 'A3')
    assert rec['model'] == dict(source_loss_boundary=200, added_unknown_coordinates=100,
                                model_slots=358, printed_annotation='(missed 20 groups)', plaintext_positions=179)
    key = inp['key']
    assert key == original_input['key'] == next(k for k in load(ROOT / 'data/keys.json')['keys'] if k['id'] == 'Nov1-3')
    assert '?' not in key['square']
    helper = prior_helpers()
    prior_proof = helper.compute()
    prior_layer = prior_proof['layers']['guard_and_berlin_with_prior']
    assert inp['baseline'] == dict(input_path='experiments/p89_guard_battalion_extension/inputs.json',
        certificate_path='experiments/p89_guard_battalion_extension/certificates.json',
        certificate_layer='guard_and_berlin_with_prior', plaintext=prior_layer['raw'],
        fixed_positions=166, observed_substitutions=1, printed_mask_fills=1, lost_coordinate_fills=85)
    assert inp['primary_assignments'] == [dict(plaintext_index=i, label=c) for i, c in ASSIGNMENTS.items()]
    assert inp['proposed_spans'] == SPANS
    literal = ''.join(''.join(rec['source_rows']).split())
    assert len(literal) == 258 and literal.count('-') == 1
    wire = literal[:200].replace('-', '?') + '?' * 100 + literal[200:].replace('-', '?')
    mapping = list(range(200)) + [None] * 100 + list(range(200, 258))
    raw = helper.inspect(wire, key, mapping)
    assert wire == prior_proof['source_frame'] and mapping == prior_proof['model_to_source_indices']
    assert raw['raw'] == rec['expected_raw'] and raw['fixed_positions'] == 81
    baseline = prior_layer['raw']; template = list(baseline)
    for span in SPANS:
        template[span['start']:span['start'] + len(span['text'])] = span['text']
    template = ''.join(template)
    assert template == rec['readable_candidate']
    assert {i: c for i, c in enumerate(template) if c != baseline[i]} == ASSIGNMENTS
    assert all(baseline[i] == '?' for i in ASSIGNMENTS)
    new_positions = [raw['positions'][i] for i in ASSIGNMENTS]
    assert all(p['pair'].count('?') == 1 and ASSIGNMENTS[p['plaintext_index']] in p['domain'] for p in new_positions)
    assert all(mapping[j] is None for p in new_positions for j in p['model_indices'] if wire[j] == '?')
    primary = helper.apply(wire, key, mapping, literal, template)
    assert primary['prices'] == dict(observed_substitution=1, printed_mask_fill=1, lost_coordinate_fill=95)
    assert primary['fixed_positions'] == 176 and primary['unfilled_coordinates'] == 5
    assert primary['exact_compatible_complete_plaintexts'] == '7776'
    old_operations = {(e['model_index'], e['new']) for e in prior_layer['edits']}
    new_edits = [e for e in primary['edits'] if (e['model_index'], e['new']) not in old_operations]
    assert len(new_edits) == 10 and all(e['kind'] == 'lost_coordinate_fill' for e in new_edits)
    assert {e['plaintext_index'] for e in new_edits} == set(ASSIGNMENTS)
    remaining = [p for p in primary['positions'] if len(p['domain']) > 1]
    assert [p['plaintext_index'] for p in remaining] == [131, 169, 172]
    assert [p['domain'] for p in remaining] == ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'] * 2 + ['1346AY']
    spelling = inp['spelling_hypothesis']
    assert spelling == dict(target_start=132, target_literal='DIENSTELLEN', standard_word='DIENSTSTELLEN',
        repeated_digraph='ST', standard_digraph_start=4,
        operation='Collapse one adjacent STST repetition to ST in the proposed plaintext spelling.',
        changes_to_source_geometry=0, normalization_in_primary=False)
    assert spelling['standard_word'][:6] + spelling['standard_word'][8:] == spelling['target_literal']
    assert len(spelling['standard_word']) == 13 and len(spelling['target_literal']) == 11
    assert template[132:143] == 'DIENSTELLEN'
    word_positions = raw['positions'][132:143]
    assert sum(c != '?' for p in word_positions for c in p['pair']) == 16
    assert all(p['pair'] != '??' for p in word_positions)
    assert inp['optional_fully_absent'] == dict(positions=[131, 169], first_position_labels=['T', 'X', 'Z'],
        second_position_label='U', included_in_primary=False)
    optional = []
    for label in ['T', 'X', 'Z']:
        alt = list(template); alt[131] = label; alt[169] = 'U'
        layer = helper.apply(wire, key, mapping, literal, ''.join(alt))
        assert layer['prices'] == dict(observed_substitution=1, printed_mask_fill=1, lost_coordinate_fill=99)
        assert layer['fixed_positions'] == 178 and layer['unfilled_coordinates'] == 1
        optional.append(dict(label_at_131=label, label_at_169='U', included_in_primary=False, **compact(layer)))
    rejected_specs = [dict(start=167, text='U', meaning='Full ZU instead of literal Z X.', included_in_primary=False),
                      dict(start=172, text='X', meaning='Separator before BERLIN.', included_in_primary=False),
                      dict(start=127, text='MILITAERPERSONENX', meaning='Alternative military-persons wording suggested by the next part.', included_in_primary=False)]
    assert inp['separately_priced_rejected_extensions'] == rejected_specs
    rejected = []
    for spec in rejected_specs:
        alt = list(template); alt[spec['start']:spec['start'] + len(spec['text'])] = spec['text']
        layer = helper.apply(wire, key, mapping, literal, ''.join(alt))
        delta = {k: layer['prices'][k] - primary['prices'][k] for k in primary['prices']}
        edits = [e for e in layer['edits'] if primary['ciphertext'][e['model_index']] != e['new']]
        rejected.append(dict(**spec, incremental_prices=delta, differing_operations=edits))
    assert rejected[0]['incremental_prices'] == dict(observed_substitution=1, printed_mask_fill=0, lost_coordinate_fill=0)
    assert rejected[1]['incremental_prices'] == dict(observed_substitution=1, printed_mask_fill=0, lost_coordinate_fill=1)
    assert rejected[0]['differing_operations'][0]['source_index'] == 17
    assert rejected[1]['differing_operations'][0]['source_index'] == 75
    witnesses = []
    expected_witnesses = [('experiments/dunst_assignment/inputs.json', 'p95_A1', 9, 'MILIT', 10),
                          ('experiments/premium_payment_stop/inputs.json', 'p78_A2', 21, 'DIENSTSTELLEN', 26)]
    assert [(s['input_path'], s['record_id'], s['start'], s['text'], s['observed_halves'])
            for s in inp['native_word_witnesses']] == expected_witnesses
    for spec in inp['native_word_witnesses']:
        data = load(ROOT / spec['input_path']); donor = record(data, spec['record_id'])
        if donor['id'] == 'p95_A1':
            donor_literal = ''.join(''.join(donor['rows']).split())
            assert donor_literal == donor['literal_source'] and donor_literal[0] == '-'
            donor_wire = donor_literal[1:]; donor_map = list(range(1, 283))
        else:
            donor_literal = ''.join(''.join(donor['source_rows']).split())
            donor_wire = donor_literal; donor_map = list(range(len(donor_wire)))
        assert set(donor_wire) <= set(CO)
        reading = helper.inspect(donor_wire, data['key'], donor_map)
        assert reading['raw'] == donor['expected_raw']
        a = spec['start']; b = a + len(spec['text']); positions = reading['positions'][a:b]
        assert reading['raw'][a:b] == spec['text']
        assert all('?' not in p['pair'] for p in positions)
        assert 2 * len(positions) == spec['observed_halves']
        witnesses.append(dict(**spec, ciphertext=donor_wire, raw=reading['raw'],
                              positions=positions, native_observed_halves=spec['observed_halves']))
    context = inp['following_part']
    assert context == dict(input_path='experiments/black_sea_evacuation_routes/inputs.json', record_id='p89_A4',
        native_prefix='XIVILPERSONENBERLIN', edited_prefix='ZIVILPERSONENBERLIN',
        native_clause='ZIELFUERGESCHLOSSENETRUPPENTEILE',
        purpose='Source-numbered next part supplies evacuation-category context, not missing target letters.')
    following = record(original_input, 'p89_A4')
    following_wire = ''.join(''.join(following['source_rows']).split())
    assert len(following_wire) == 360 and set(following_wire) <= set(CO)
    following_raw = decrypt(following_wire, key['column_rank_order'], key['square'])
    assert following_raw == following['expected_raw'] and following_raw.startswith(context['native_prefix'])
    assert context['native_clause'] in following_raw
    clause_start = following_raw.index(context['native_clause'])
    corrected_prefix = context['edited_prefix'] + following_raw[len(context['native_prefix']):]
    context_layer = helper.apply(following_wire, key, list(range(360)), following_wire, corrected_prefix)
    assert context_layer['prices'] == dict(observed_substitution=1, printed_mask_fill=0, lost_coordinate_fill=0)
    assert original_input['headers']['assembly_order'][2:4] == ['p89_A3', 'p89_A4']
    history = check_history(inp); images = image_specs(inp)
    search_report = load(HERE / 'search_report.json')
    assert search_report['donor_streams'] == 484 and search_report['donor_characters'] == 51327
    assert search_report['collapsed_variants'] == 110
    assert search_report['historical']['hits'][0]['text'] == 'NDIENSTELLEN'
    assert search_report['historical']['observed_support'] == 16
    assert search_report['null_summary']['count'] == 128 and search_report['null_summary']['matched_at_minimum_length'] == 0
    assert len(search_report['planted']) == 3
    return dict(schema='adfgvx-p89-destination-continuation-certificate-v1', authors=inp['authors'],
        input_sha256=sha(HERE / 'inputs.json'),
        records=[dict(id='p89_A3', ciphertext=wire, raw=raw['raw'], model_to_source_indices=mapping,
                      readable_candidate=compact(primary))],
        new_position_evidence=new_positions, new_operations=new_edits, remaining_domains=remaining,
        spelling_hypothesis=dict(**spelling, native_target_positions=word_positions, observed_halves=16, lost_fills=6),
        optional_completions=optional, rejected_extensions=rejected, native_word_witnesses=witnesses,
        following_part=dict(**context, raw=following_raw, native_clause_start=clause_start,
                            native_clause_observed_halves=2 * len(context['native_clause']),
                            initial_X_to_Z_repair=context_layer['edits']),
        historical_context=history, child_source_images=images,
        search_report_sha256=sha(HERE / 'search_report.json'),
        summary=dict(physical_bodies_added=0, native_source_slots=258, valid_observed_coordinates=257,
                     printed_masks=1, source_declared_added_coordinates=100, model_coordinates=358,
                     plaintext_positions=179, native_fixed_positions=81, baseline_fixed_positions=166,
                     primary_fixed_positions=176, primary_unassigned_positions=3,
                     new_fixed_positions=10, new_positions_with_one_observed_half=10,
                     new_wholly_absent_assignments=0, new_observed_substitutions=0,
                     new_printed_mask_fills=0, new_lost_coordinate_fills=10,
                     total_observed_substitutions=1, total_printed_mask_fills=1,
                     total_lost_coordinate_fills=95, remaining_coordinate_masks=5,
                     exact_compatible_complete_plaintexts='7776', optional_fixed_positions=178,
                     optional_extra_lost_fills=4), limits=inp['limits'])


def verify_pdf(path, proof):
    import fitz
    from PIL import Image
    assert sha(path) == '157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06'
    doc = fitz.open(path)
    for spec in proof['child_source_images']:
        pix = doc[spec['pdf_page_1based'] - 1].get_pixmap(
            matrix=fitz.Matrix(spec['render_scale'], spec['render_scale']),
            clip=fitz.Rect(spec['crop_pdf_points']), alpha=False)
        image = Image.open(ROOT / spec['path']).convert('RGB')
        assert image.size == (pix.width, pix.height) and image.tobytes() == pix.samples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args(); proof = compute(); path = HERE / 'certificates.json'
    if args.verify:
        assert proof == load(path)
    else:
        path.write_text(json.dumps(proof, indent=2) + '\n')
    if args.pdf:
        verify_pdf(args.pdf, proof)
    print(json.dumps(dict(verified=True, **proof['summary'], original_pdf_checked=bool(args.pdf)), indent=2))


if __name__ == '__main__':
    main()
