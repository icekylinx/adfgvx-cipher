#!/usr/bin/env python3
"""Verify the whole-material boundary census and report live source coverage.

The source denominator is manually reviewed. Catalogue membership is live. Label
counts are admitted only through explicit structured contracts and independent
ragged-grid arithmetic; unsupported evidence stays unquantified. This program
does not run source-package generators, change certificates, or count readable
prose as evidence. Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.catalog import load_catalog, physical_source_accounting

DEFAULT = ROOT / 'data/reviews/childs_material_census_20261103.json'
REPORT = ROOT / 'docs/whole-material-coverage.md'
C = 'ADFGVX'
LABELS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')


class Unsupported(Exception):
    """The current contract cannot safely quantify this record."""


@lru_cache(maxsize=None)
def read(relative):
    return json.loads((ROOT / relative).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(text):
    return ''.join(text.split())


def rows(data):
    if isinstance(data.get('records'), list):
        return data['records']
    if isinstance(data.get('record'), dict):
        return [data['record']]
    if isinstance(data.get('record_id'), str):
        return [dict(data, id=data['record_id'])]
    if data.get('schema') == 'adfgvx-cross-key-source-input-v1':
        return data['messages']
    if data.get('schema') == 'adfgvx-cross-key-source-audit-v1':
        return data['results']
    if data.get('schema') in {'adfgvx-nov9-operations-map-sheets-certificate-v1',
                              'adfgvx-warsaw-station-missing-row-input-v1',
                              'adfgvx-warsaw-station-missing-row-certificate-v1'}:
        return [dict(data, id=data['source_record'])]
    if data.get('schema') == 'adfgvx-siedlce-withdrawal-certificate-v1':
        return [dict(data, id='p200_A')]
    return []


def record(data, rid):
    selected = [r for r in rows(data) if r.get('id') == rid]
    if len(selected) != 1:
        raise Unsupported('no unique primary record in the supported root structure')
    return selected[0]


def literal(r):
    candidates = []
    if isinstance(r.get('source_rows'), list) and all(isinstance(x, str) for x in r['source_rows']):
        candidates.append(compact(''.join(r['source_rows'])))
    for name in ['literal_source', 'source_literal', 'raw_source_compact', 'literal', 'literal_ciphertext']:
        if isinstance(r.get(name), str):
            candidates.append(compact(r[name]))
    if not candidates:
        raise Unsupported('no supported literal-source field')
    assert candidates[0] and len(set(candidates)) == 1, 'conflicting literal-source fields'
    return candidates[0]


def key_for(data, r, cr):
    value = data.get('key')
    if not isinstance(value, dict):
        keys = data.get('keys')
        kid = r.get('key_id', cr.get('key_id'))
        if isinstance(keys, dict):
            value = keys.get(kid)
        elif isinstance(keys, list):
            value = next((k for k in keys if k.get('id') == kid), None)
    if not isinstance(value, dict) or not {'id', 'square', 'column_rank_order'} <= value.keys():
        raise Unsupported('no unambiguous declared registered key')
    registry = {k['id']: k for k in read('data/keys.json')['keys']}
    if value['id'] not in registry:
        raise Unsupported('key is not in the registered key set')
    registered = registry[value['id']]
    assert value['square'] == registered['square'], 'square differs from the registered conservative key'
    assert value['column_rank_order'] == registered['column_rank_order'], 'column order differs from registered key'
    return value


def order(n, ranks):
    """Explicitly fill ragged columns, then return the row-major read order."""
    width = len(ranks)
    grid = [[None] * min(width, n - start) for start in range(0, n, width)]
    at = 0
    for col in sorted(range(width), key=lambda j: ranks[j]):
        for row in grid:
            if col < len(row):
                row[col] = at
                at += 1
    assert at == n
    return [i for row in grid for i in row]


def decode(cipher, key):
    assert set(cipher) <= set(C + '?')
    sequence = order(len(cipher), key['column_rank_order'])
    absent = LABELS - set(key['square'])
    output = []
    for j in range(0, len(sequence) - 1, 2):
        pair = ''.join(cipher[i] for i in sequence[j:j + 2])
        domain = set()
        for a in C if pair[0] == '?' else pair[0]:
            for b in C if pair[1] == '?' else pair[1]:
                v = key['square'][C.index(a) * 6 + C.index(b)]
                domain.update(absent if v == '?' else [v])
        output.append(next(iter(domain)) if len(domain) == 1 else '?')
    return ''.join(output), sequence[-1] if len(sequence) % 2 else None


def raw_text(r):
    for name in ['raw', 'raw_plaintext', 'raw_within_working_frame', 'raw_reading',
                 'working_reading', 'conditional_frame_reading', 'direct']:
        value = r.get(name)
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            for child in ['raw', 'plaintext']:
                if isinstance(value.get(child), str):
                    return value[child]
    selected = r.get('selected_edition')
    if isinstance(selected, dict):
        for field in ['working_raw_reading', 'raw']:
            value = selected.get(field)
            if isinstance(value, dict):
                for child in ['raw', 'plaintext']:
                    if isinstance(value.get(child), str):
                        return value[child]
    raise Unsupported('no supported primary raw stream')


def first_string(r, fields):
    for field in fields:
        if isinstance(r.get(field), str):
            return r[field]
    return None


def quantify(certificate_path, rid):
    """One explicit primary record; alternative models are never pooled."""
    cp = Path(certificate_path)
    if cp.parts[0] != 'experiments':
        raise Unsupported('legacy certificate requires a dedicated primary-model adapter')
    ip = cp.parent / 'inputs.json'
    if not (ROOT / ip).exists():
        raise Unsupported('no package inputs.json')
    data, certificate = read(str(ip)), read(str(cp))
    ir, cr = record(data, rid), record(certificate, rid)
    source = literal(ir)
    source_tokenization = 'Whitespace removed; every remaining literal glyph occupies one source slot.'
    if certificate.get('schema') == 'adfgvx-p64-oil-and-radio-certificate-v1' and rid == 'p64_A2':
        # Parentheses mark two uncertain printed coordinates, not four further
        # coordinate slots. Keep and verify the exact declared positions.
        tokens = re.findall(r'\(([ADFGVX])\)|([^()])', source)
        stripped = ''.join(a or b for a, b in tokens)
        indices = [i for i, (a, _) in enumerate(tokens) if a]
        assert len(indices) == 2 and indices == cr['parenthesized_coordinate_indices']
        assert re.sub(r'\(([ADFGVX])\)', r'\1', source) == stripped
        source = stripped
        source_tokenization = 'p64 A2: parentheses annotate two printed X coordinates; their indices are independently checked. Delimiters are not source slots.'
    if certificate.get('schema') == 'adfgvx-transylvania-situation-certificate-v1' and rid == 'p137_A5':
        assert source.count('{INTERFERENCE_1}') == source.count('{INTERFERENCE_2}') == 1
        source = source.replace('{INTERFERENCE_1}', '').replace('{INTERFERENCE_2}', '')
        assert len(source) == ir['source_slots']
        source_tokenization = 'p137 A5: two named interference annotations are not occupied source glyphs; the explicit frame separately accounts for its hypothesized missing coordinates.'
    try:
        assert literal(cr) == source, 'certificate/input literal-source mismatch'
    except Unsupported:
        pass
    key = key_for(data, ir, cr)
    primary_selection = 'Primary record directly named by the certificate.'
    if certificate.get('schema') in {'adfgvx-october-requests-certificate-v1',
                                      'adfgvx-october-caucasus-certificate-v1'}:
        if len(cr.get('models', [])) != 1:
            raise Unsupported('multiple explicit geometry models; no single primary model selected by this adapter')
        primary_selection = 'The certificate contains exactly one geometry model: ' + cr['models'][0]['id']
        cr = cr['models'][0]
    if certificate.get('schema') == 'adfgvx-cross-source-seifert-witness-certificate-v1':
        # This schema names one primary map and keeps every tied map separately.
        # Quantifying the primary does not add the alternative maps as sources.
        assert isinstance(cr.get('primary'), dict)
        assert cr['primary']['excluded_source_index'] == ir['primary_excluded_source_index']
        cr = cr['primary']
    if certificate.get('schema') == 'adfgvx-warsaw-station-missing-row-certificate-v1':
        model = ir['primary_model']
        gap = model['source_insertion_index']
        added = model['missing_coordinates']
        assert 0 <= gap <= len(source) and added == 40
        assert cr['primary_gap'] == gap
        witnesses = [w for w in cr['zero_change_witnesses'] if w['gap_start'] == gap]
        assert len(witnesses) == 1
        selected = witnesses[0]
        expected_map = list(range(gap)) + [None] * added + list(range(gap, len(source)))
        assert selected['model_to_source_indices'] == expected_map
        cr = dict(selected['baseline'], ciphertext=selected['frame'], model_to_source_indices=expected_map)
        primary_selection = 'The input explicitly selects gap ' + str(gap) + '; other zero-change branches are not pooled.'
    expected = raw_text(cr)
    assert set(expected) <= LABELS | {'?'}, 'unexpected raw label alphabet'
    native = ''.join(x if x in C else '?' for x in source)
    frame = first_string(cr, ['ciphertext', 'ciphertext_with_unfilled_additions',
                             'analysis_frame', 'framed_ciphertext', 'analysis_ciphertext',
                             'model_ciphertext', 'layout_ciphertext'])
    mapping = None
    for field in ['model_to_source_indices', 'working_to_source_indices',
                  'frame_to_source_indices', 'frame_to_original_source_index', 'source_map',
                  'layout_source_offsets', 'framed_position_to_received_position_0based']:
        if isinstance(cr.get(field), list):
            mapping = cr[field]
            break
    if mapping is None:
        # Explicit input maps describe a selected transmitted-coordinate frame.
        # No source indices are guessed from plaintext or from status prose.
        for field in ['model_to_source_indices', 'source_origin_map', 'working_source_indices']:
            if isinstance(ir.get(field), list):
                mapping = ir[field]
                break
    if mapping is None and isinstance(ir.get('geometry'), dict):
        if isinstance(ir['geometry'].get('source_origin_map'), list):
            mapping = ir['geometry']['source_origin_map']
    if mapping is None and isinstance(ir.get('excluded_source_indices'), list):
        excluded = ir['excluded_source_indices']
        assert len(excluded) == len(set(excluded)) and all(isinstance(i, int) and 0 <= i < len(source) for i in excluded)
        mapping = [i for i in range(len(source)) if i not in excluded]
    if mapping is None and certificate.get('schema') == 'adfgvx-nov8-map-and-boundary-certificates-v1':
        boundary = ir.get('model_insert_before_source_index')
        if isinstance(boundary, int):
            assert 0 <= boundary <= len(source)
            mapping = list(range(boundary)) + [None] + list(range(boundary, len(source)))
    if frame is None and mapping is not None:
        # Recover only an unfilled model from its explicit source map. Any
        # source-linked coordinate must be explicit in a frame field instead.
        if not all(i is None or isinstance(i, int) for i in mapping):
            raise Unsupported('non-integer source map needs a dedicated adapter')
        frame = ''.join('?' if i is None else native[i] for i in mapping)
    if frame is None:
        # This limited native contract is accepted only if the independently
        # decoded input exactly equals the primary certificate's raw stream.
        candidate_raw, _ = decode(native, key)
        if candidate_raw != expected:
            raise Unsupported('no explicit model frame and native stream is not the primary raw stream')
        frame = native
        mapping = list(range(len(source)))
    frame = compact(frame)
    assert set(frame) <= set(C + '?'), 'unsupported model coordinate alphabet'
    if mapping is None:
        if frame != native:
            raise Unsupported('modified primary frame lacks a supported full source map')
        mapping = list(range(len(source)))
    if not all(i is None or isinstance(i, int) for i in mapping):
        raise Unsupported('non-integer source map needs a dedicated adapter')
    assert len(mapping) == len(frame), 'source map length mismatch'
    retained = [i for i in mapping if i is not None]
    assert all(0 <= i < len(source) for i in retained), 'source map index out of range'
    assert len(retained) == len(set(retained)), 'source coordinate repeated inside primary map'
    for char, origin in zip(frame, mapping):
        if origin is not None and source[origin] in C:
            assert char == source[origin], 'raw frame silently changes an observed coordinate'
    got, orphan = decode(frame, key)
    assert got == expected, 'independent decryption differs from primary raw stream'
    for name in ['fixed_positions', 'raw_fixed_positions', 'base_fixed_positions']:
        if isinstance(cr.get(name), int):
            assert cr[name] == len(got) - got.count('?'), 'raw fixed-position count mismatch'
    pure = ''.join(source[i] if i is not None and source[i] in C else '?' for i in mapping)
    direct, _ = decode(pure, key)
    supplied = [i for i, (a, b) in enumerate(zip(pure, frame)) if a != b]
    native_raw, native_orphan = decode(native, key)
    excluded = sorted(set(range(len(source))) - set(retained))
    native_geometry = mapping == list(range(len(source))) and len(frame) == len(source)
    result = {
        'record_id': rid, 'certificate': str(cp), 'certificate_schema': certificate.get('schema'),
        'inputs': str(ip), 'key_id': key['id'],
        'primary_selection': primary_selection,
        'source_tokenization': source_tokenization,
        'native_source_slots': len(source), 'valid_source_coordinates': sum(x in C for x in source),
        'native_mask_slots': sum(x not in C for x in source),
        'native_paired_positions': len(native_raw), 'native_orphan_source_index': native_orphan,
        'frame_kind': 'native_order_and_length' if native_geometry else 'modified_frame',
        'model_slots': len(frame), 'model_positions': len(got), 'model_orphan_index': orphan,
        'fixed_raw_labels_with_all_unobserved_coordinates_unassigned': len(direct) - direct.count('?'),
        'fixed_raw_labels_as_displayed_in_primary_certificate': len(got) - got.count('?'),
        'additional_fixed_labels_from_supplied_unobserved_coordinates': direct.count('?') - got.count('?'),
        'prefilled_unobserved_model_indices': supplied,
        'added_model_slots': sum(i is None for i in mapping),
        'excluded_source_slots': len(excluded),
        'excluded_valid_source_coordinates': sum(source[i] in C for i in excluded),
        'candidate_counts': None,
    }
    cc = cr.get('readable_candidate')
    if isinstance(cc, dict) and isinstance(cc.get('ciphertext'), str) and isinstance(cc.get('raw'), str):
        edited = cc['ciphertext']
        assert len(edited) == len(frame), 'candidate changes the selected frame length'
        reading, _ = decode(edited, key)
        assert reading == cc['raw'], 'candidate does not independently decode to its stated raw stream'
        changes = [(i, a, b) for i, (a, b) in enumerate(zip(frame, edited)) if a != b]
        assert all(b in C for _, _, b in changes), 'candidate removes evidence instead of assigning coordinates'
        costs = {'fixed_candidate_labels': len(reading) - reading.count('?'),
                 'observed_coordinate_substitutions': 0, 'source_mask_fills': 0,
                 'added_coordinate_fills': 0}
        for i, a, b in changes:
            origin = mapping[i]
            name = 'added_coordinate_fills' if origin is None else (
                'observed_coordinate_substitutions' if source[origin] in C else 'source_mask_fills')
            costs[name] += 1
        result['candidate_counts'] = costs
    return result


def validate_census(manifest, pdf=None):
    assert manifest['schema'] == 'adfgvx-childs-whole-material-census-v1'
    pages = manifest['log_pages']
    assert [p['printed_page'] for p in pages] == list(range(56, 231))
    locations = []
    for p in pages:
        assert p['pdf_page_1based'] == p['printed_page'] + 3
        assert p['reviewer'] and p['review_basis']
        assert len(set(p['ciphertext_body_sections'])) == len(p['ciphertext_body_sections'])
        locations.extend((p['printed_page'], s) for s in p['ciphertext_body_sections'])
    assert len(locations) == len(set(locations)) == 679
    baseline = manifest['baseline_snapshot']
    assert len(baseline['entries']) == baseline['reviewed_catalogue_entries'] == 640
    oldlocations = {(r['printed_page'], r['source_section']) for r in baseline['entries']}
    assert len(oldlocations) == baseline['unique_catalogued_physical_sources'] == 639
    assert oldlocations <= set(locations)
    assert len(set(locations) - oldlocations) == baseline['uncatalogued_ciphertext_bodies'] == 40
    assert sum(r['group'] == 'challenge' for r in baseline['entries']) == 22
    keys = {k['id'] for k in read('data/keys.json')['keys']}
    unit = next(x for x in manifest['nonlog_material_units'] if x['id'] == 'appendix_C_keys')
    assert len(unit['registered_keys']) == unit['distinct_printed_key_tables'] == 15
    assert all(k['key_id'] in keys for k in unit['registered_keys'])
    if pdf:
        assert pdf.stat().st_size == manifest['source']['pdf_bytes']
        assert sha(pdf) == manifest['source']['pdf_sha256']
        import fitz
        with fitz.open(pdf) as doc:
            assert len(doc) == manifest['source']['pdf_page_count'] == 248
    return set(locations)


def build(manifest, pdf=None):
    expected = validate_census(manifest, pdf)
    catalogue = load_catalog()
    account = physical_source_accounting(catalogue)
    core = {m['id']: m for m in read('data/messages.json')['messages']}
    current = {}
    for group in ['challenge', 'other']:
        for e in catalogue[group]:
            loc = tuple(account['locations'][e['id']])
            assert loc in expected, ('catalogue location missing from reviewed census', e['id'], loc)
            current.setdefault(loc, []).append(dict(e, group=group))
    local = {}
    for package in manifest['additional_review_packages']:
        path = ROOT / 'experiments' / package / 'inputs.json'
        if not path.exists():
            continue
        for ir in rows(read(str(path.relative_to(ROOT)))):
            if not {'printed_page', 'source_section'} <= ir.keys():
                continue
            loc = (ir['printed_page'], ir['source_section'])
            assert loc in expected, ('local edition absent from census', package, ir['id'])
            local.setdefault(loc, []).append({'id': ir['id'], 'package': package})
    result = []
    integrity_errors = []
    for page, section in sorted(expected):
        loc = (page, section)
        entries = current.get(loc, [])
        evidence = []
        source_reviewed = False
        for e in entries:
            if e['group'] == 'challenge':
                source_reviewed |= bool(core[e['id']]['transcript'].get('verification'))
            else:
                source_reviewed |= e.get('source_reviewed') is True
            evidence.extend((p, e['id']) for p in e.get('evidence', [])
                            if 'certificat' in p and p.endswith('.json'))
        for e in local.get(loc, []):
            evidence.append((f"experiments/{e['package']}/certificates.json", e['id']))
        count = None
        reasons = []
        for ep, rid in dict.fromkeys(evidence):
            if not (ROOT / ep).exists():
                reasons.append(f'{ep}: unavailable in this tree')
                continue
            try:
                count = quantify(ep, rid)
                break
            except Unsupported as exc:
                reasons.append(f'{ep}: {exc}')
            except (AssertionError, KeyError, IndexError, ValueError) as exc:
                integrity_errors.append({'printed_page': page, 'source_section': section,
                                         'record_id': rid, 'certificate': ep, 'error': str(exc)})
                reasons.append(f'{ep}: structured contract rejected ({exc})')
        source_slots = None
        if count:
            source_slots = count['native_source_slots']
        else:
            challenge = next((e for e in entries if e['group'] == 'challenge'), None)
            if challenge:
                source_slots = len(core[challenge['id']]['transcript']['raw_source_compact'])
        result.append({'printed_page': page, 'source_section': section,
                       'catalogue_edition_ids': [e['id'] for e in entries],
                       'source_reviewed_in_current_catalogue_metadata': source_reviewed,
                       'current_catalogue_statuses': [e['status'] for e in entries],
                       'local_review_packages_not_yet_catalogued': [e['package'] for e in local.get(loc, [])] if not entries else [],
                       'native_source_slots_if_known': source_slots,
                       'quantitative_status': 'independently_recomputed_primary_record' if count else 'unquantified_primary_record',
                       'counts': count,
                       'unquantified_reasons': (reasons or ['No supported primary certificate is referenced for this physical body.']) if not count else []})
    quantified = [r for r in result if r['counts']]
    totals = {}
    for kind in ['native_order_and_length', 'modified_frame']:
        rows_for_kind = [r['counts'] for r in quantified if r['counts']['frame_kind'] == kind]
        totals[kind] = {'physical_sources': len(rows_for_kind)}
        totals[kind]['native_unpaired_orphan_coordinates'] = sum(r['native_orphan_source_index'] is not None for r in rows_for_kind)
        totals[kind]['model_unpaired_orphan_coordinates'] = sum(r['model_orphan_index'] is not None for r in rows_for_kind)
        for name in ['native_source_slots', 'valid_source_coordinates', 'native_mask_slots',
                     'model_slots', 'model_positions', 'fixed_raw_labels_with_all_unobserved_coordinates_unassigned',
                     'fixed_raw_labels_as_displayed_in_primary_certificate',
                     'additional_fixed_labels_from_supplied_unobserved_coordinates',
                     'added_model_slots', 'excluded_source_slots', 'excluded_valid_source_coordinates']:
            totals[kind][name] = sum(r[name] for r in rows_for_kind)
    return {
        'schema': 'adfgvx-live-whole-material-coverage-v1', 'authors': manifest['authors'],
        'census_sha256': sha(DEFAULT),
        'current_catalogue_sha256': sha(ROOT / 'data/reading_catalog.json'),
        'historical_log_pages': 175, 'actual_printed_ciphertext_bodies': 679,
        'baseline_snapshot': {k: v for k, v in manifest['baseline_snapshot'].items() if k != 'entries'},
        'current': {'catalogue_entries': account['reviewed_entries'],
                    'catalogued_physical_sources': len(current),
                    'source_reviewed_physical_sources_per_metadata': sum(r['source_reviewed_in_current_catalogue_metadata'] for r in result),
                    'challenge_entries': len(catalogue['challenge']),
                    'other_entries': len(catalogue['other']),
                    'additional_physical_sources_beyond_challenges': account['additional_physical_sources'],
                    'uncatalogued_bodies': 679 - len(current),
                    'independently_quantified_primary_records': len(quantified),
                    'unquantified_primary_records': 679 - len(quantified),
                    'uncatalogued_bodies_with_registered_local_review_package': sum(bool(r['local_review_packages_not_yet_catalogued']) for r in result)},
        'quantified_subset_totals': totals,
        'quantitative_contract_rejections': integrity_errors,
        'records': result,
        'limits': manifest['limits'] + [
            'Quantified model-position totals describe only the explicitly counted records. They are not a denominator or completion percentage for all 679 bodies.',
            'Native fixed-label streams can still contain lexical garbles. Modified frames can remain conditional. Candidate repairs and a completely fixed template do not establish a fully understood original message.',
            'Each physical source contributes at most one primary quantitative record; later editions, optional readings and alternative model families are not added as further sources.',
            'The read-only structured checker confirms arithmetic and source maps. It does not replace the original manual glyph review or rerun every source package verifier.'
        ]}


def render(report, manifest):
    now = report['current']
    lines = ['# Whole-material source coverage', '',
             'Prepared by **icekylinx and GPT-6 Astra Pro**. This dashboard separates source boundaries, catalogue editions, and decipherment evidence.', '',
             '## Scope and denominator', '',
             '**Appendix B contains 679 actual printed ciphertext bodies on printed pages 56–230 (175 pages).** A separately printed part or received copy is one physical body. Surviving damaged fragments count; advertised but absent parts do not. The two literal `AAA` items at p58 A1/A2 remain separately registered ambiguous stubs, outside this body count.', '',
             'Every log page has a recorded boundary review. That review checks where bodies begin and end; it does not claim a fresh transcription of every glyph, a unique key for every body, or complete plaintext recovery.', '',
             '## Current tree and preserved starting snapshot', '',
             '| Measure | Current tree | Starting snapshot, 2026-11-03 08:04:46 UTC |',
             '|---|---:|---:|',
             f"| Reviewed catalogue edition entries | {now['catalogue_entries']} | 640 |",
             f"| Distinct catalogued physical bodies | {now['catalogued_physical_sources']} | 639 |",
             f"| Original challenge entries | {now['challenge_entries']} | 22 |",
             f"| Other catalogue entries | {now['other_entries']} | 618 |",
             f"| Additional physical bodies beyond challenges | {now['additional_physical_sources_beyond_challenges']} | 617 |",
             f"| Bodies outside the current catalogue | {now['uncatalogued_bodies']} | 40 |", '',
             f"Current catalogue metadata records source review for **{now['source_reviewed_physical_sources_per_metadata']} distinct bodies**. This is the existing source-review evidence status, not a number of solved messages. The registered p132 / p132_B overlap is one physical body with two edition entries. The current counts come from the files in this checkout; the fixed baseline is never substituted for them.", '',
             f"There are **{now['uncatalogued_bodies_with_registered_local_review_package']} uncatalogued bodies** with an explicitly registered local review package in this checkout. They remain outside the catalogue count until integration. Publication status and local research status are distinct.", '',
             '## Quantitative evidence coverage', '',
             f"The bounded structured adapters independently recompute primary source/model accounting for **{now['independently_quantified_primary_records']} of the 679 bodies**. The other **{now['unquantified_primary_records']} bodies remain unquantified by this dashboard**; that includes unsupported legacy certificate shapes and genuinely missing editions. It does not mean that all of them lack prior decipherment work.", '',
             '| Verified primary frame class | Physical bodies | Native slots | Model positions | Fixed raw labels, all unobserved coordinates unassigned | Extra fixed labels from supplied unobserved coordinates |',
             '|---|---:|---:|---:|---:|---:|']
    for kind, name in [('native_order_and_length', 'Native order and length'), ('modified_frame', 'Modified frame; its stated assumptions still apply')]:
        t = report['quantified_subset_totals'][kind]
        lines.append(f"| {name} | {t['physical_sources']} | {t['native_source_slots']} | {t['model_positions']} | {t['fixed_raw_labels_with_all_unobserved_coordinates_unassigned']} | {t['additional_fixed_labels_from_supplied_unobserved_coordinates']} |")
    lines += ['', 'These position totals cover only the quantified subset. **They are not a whole-corpus plaintext-completion percentage.** A fully fixed raw stream can retain garbles or uninterpreted numbers. The checker separates native source slots, conditional model additions/exclusions, and coordinates supplied from another witness; it does not combine alternative models or optional prose into a primary total.', '',
              'The per-body JSON output includes exact evidence paths and explicit reasons when a primary record cannot yet be quantified. Candidate-label and repair counts are included only where the candidate contract can also be independently decoded.', '',
              '## Complete current catalogue gap list', '',
              '| Printed page | Actual body sections outside catalogue | Registered local edition or existing artifact lead |',
              '|---:|---|---|']
    gaps = [r for r in report['records'] if not r['catalogue_edition_ids']]
    for page in sorted({r['printed_page'] for r in gaps}):
        rr = [r for r in gaps if r['printed_page'] == page]
        leads = []
        for r in rr:
            for name in r['local_review_packages_not_yet_catalogued']:
                leads.append(f"{r['source_section']}: `{name}` (local reviewed edition)")
            rid = f"p{page}_{r['source_section']}"
            for path in manifest['artifact_leads'].get(rid, []):
                package = str(Path(path).parent)
                if package.split('/')[-1] not in r['local_review_packages_not_yet_catalogued']:
                    leads.append(f"{r['source_section']}: `{path}` (lead; coverage not inferred)")
        lines.append(f"| {page} | {', '.join(r['source_section'] for r in rr)} | {'; '.join(dict.fromkeys(leads)) or 'No structured edition registered here'} |")
    lines += ['', 'An artifact lead can be a diagnostic or contextual mention. Its existence does not count as a recovered body. The local label A16 at p163 identifies the actual fragment between printed parts 15 and 17; it does not assert a printed `16 TL` heading.', '',
              '## Other material in the volume', '',
              '| Material | Printed pages | Separate accounting |', '|---|---|---|',
              '| Childs technical explanation | 1–22 | Includes reused cipher figures and an internal numeric teaching example; figures are not new intercepted messages. |',
              '| Twelve numbered teaching cryptograms I–XII | 19–22 | 12 instructional items under the published VIKINGSCROWNHOTEL example key; kept outside the 679-body log denominator. |',
              '| Konheim Appendix A | 23–54 | Theory and numerical 5×5 teaching examples, including repeated or excerpted ciphertext illustrations; no new historical-message count. |',
              '| Appendix B title | 55 | Ciphertext log starts on p56. |',
              '| Appendix C key tables | 232–244 | 15 printed tables on 13 pages, all represented by existing key IDs; unknown cells remain unknown. |',
              '| Cleartext, short stubs, header-only items and missing-part notes | Within the log | Explicit exceptions are retained separately in the census; they do not create invented ciphertext bodies. |', '',
              'The frozen OCR pool has **788 unverified blocks on pp57–230**, omitting p56. Blocks can split, merge, or omit real bodies; subtracting catalogue entries from 788 does not measure remaining messages. Duplicate transmissions and separately printed parts are retained as physical witnesses. Their number is not a claim about the number of distinct complete historical messages.', '',
              '## Reproduction', '', '```bash',
              'python data/reviews/verify_childs_material_coverage.py --verify',
              'python data/reviews/verify_childs_material_coverage.py --json > /tmp/childs-current-coverage.json',
              'python data/reviews/verify_childs_material_coverage.py --verify --pdf /path/to/childs.pdf',
              'python data/reviews/verify_childs_material_coverage.py --write-report', '```', '',
              '`--verify` is read-only. `--write-report` explicitly refreshes this dashboard from the live tree. The optional PDF check pins the original file bytes and page count; the source-boundary inspection itself is a recorded manual review, not an automated glyph-recognition claim.', '',
              f"Current catalogue SHA-256: `{report['current_catalogue_sha256']}`.",
              f"Census SHA-256: `{report['census_sha256']}`.", '',
              'Source: J. Rives Childs, *General Solution of the ADFGVX Cipher System*, [complete scanned volume](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). See the [machine-readable census](../data/reviews/childs_material_census_20261103.json) for page-level review bases and material exceptions.', '']
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--json', action='store_true')
    p.add_argument('--pdf', type=Path)
    p.add_argument('--write-report', action='store_true')
    args = p.parse_args()
    manifest = json.loads(DEFAULT.read_text())
    report = build(manifest, args.pdf)
    if args.verify:
        assert not report['quantitative_contract_rejections'], report['quantitative_contract_rejections']
    if args.write_report:
        assert not report['quantitative_contract_rejections'], report['quantitative_contract_rejections']
        REPORT.write_text(render(report, manifest))
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(json.dumps({'verified': args.verify, **report['current'],
                          'quantified_subset_totals': report['quantified_subset_totals'],
                          'quantitative_contract_rejections': report['quantitative_contract_rejections']}, indent=2))


if __name__ == '__main__':
    main()
