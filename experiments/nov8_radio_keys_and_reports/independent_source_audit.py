#!/usr/bin/env python3
"""Independent source and candidate audit of the p160/p161 source edition.

Prepared by icekylinx and GPT-6 Astra Pro. Standard library only. The manual
source-glyph review is a separately declared observation; the executable
replays literal rows, cipher costs, coupled key witnesses and every fixed-
template exclusion set without importing the shared cipher or parent verifier.
"""
import argparse, collections, hashlib, itertools, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CO='ADFGVX'
RANKS=[6,12,7,15,1,11,16,5,8,14,3,18,9,13,2,17,20,10,19,4]
SQUARE='PRMYUW3LZGES8C71QOV29ITB40?KXH?AJNDF'
ROWS={
'p160_A2':'''AADDG VXDAD ADADG GDGDXF XGDAV DXAADG VGVDV XXXDD
DFXVG XGVVF AGDVV XGVVX AXXDG VDAXV FDGDX GVAGX
GDVXA AFDFV XFXVD FGXGG VAVGA AFADV VDGVG DVDVA
DFXVV GFDVD VDXDX VVVVF GGDXA DVVVD VGGXX GVVXV
GFGDD GFDDX GGVVV DGVXD XDA-G ADDXD DGVXX VDVGG
XVDGF FDXFV FXGVX DGAAD FDVGD DAAGD DFVFD DAG''',
'p160_B1':'''FAAVV DVGGA VGFAV VGVDV DDDFF XDDFF AXAXA AFVAA
DVAAA AXGXD XFFDV VGGAG XFXXG XGXXV VXVDD DVADX
VDVXV VDXAA GVDVD VGDXX XXDDD DDDDD DXFVF XDADX
VVFGG GXGDV FGDDA VDGDG GXVAG GVDGV VXVDD DVVVV
XFDDD VVXDV XGDVD XGVXG AVVGD DDVXV VVXVV VDDGF
DDDGD VVVVG XGXFA DXAXG GDGAV DVDVX VVXAG FXGFV
DGDGA GDDDV DDVXF DGGDF VVVAD FVVFG DAGGF FDVXX
DX''',
'p160_B2':'''AGXXG AFFCG XFXXD DFGVA GFDVX DVDDV ADVFD VXFDD
XADXG XAAFX ADDDG VXVDV DVVVA GGDGA DGVFG GVFFV
FAVB''',
'p160_C1':'''GDDGV VVAVG XVDDD DADXF VVAXD AFVDD DGVDX FGDDD
GXXFV GDXDV XFVGD DVDVV XVXXV GAVGD VGDDD DDXGD
VDDGA DGDGX DAXFX GGXXG VFAAX ADGGA XDAXV DXAGD
XDFAD XDGVV DGDFG GVXDV DGXDA XXVDX VVFVA GVAVV
VDXGX GVVVV GGDXV VDDXV VGXXF GVGDF XVVXX XGVXV
VFDXD DVVGV VGDXG XXGAV GXFVD DVGVX XVDGD DXVXG
DGGAA DAADX GDVAF DXDDV DVFXX VGDXF GVAGX DVGAV
FAGVGD XDXGX DDVVF GVFFG XDD-- ADD''',
'p160_C2':'''GGAXA GDAVG GDXGG GADXV GXVAD XXAVG XXAGX XADVV
DFGFV DVDDV VADDG XVVDF AAXXV VVVVX DAAXF GFVVG
XFDVV DFVGX FGGAF XVAXV AXVVV VXXVD GGFAD XDVGX
GDFXD DVDVX DDDAG VXAXD DDFF''',
'p160_D1':'''DGDXV XGFDA XDVXG VXXXX VVFDF VAVGD DXDFX AXGVV
DXFGG DFAVG DVDAA FDGFV GADXG DDDAG DVVGV DVADX
GAGAX XXVVD VVGGV V--XX XVGDV -G--X ADDVF GVVGG
VVGXG XDAFV DFDVG XADXV''',
'p161_A2':'''VAFDF VADVX VDXGD VGDAX XVVGX XXXGX XFDAX AXDGG
DDFXA AGGXD GAGXG FADVD DXGVV DXVDG FDVDF GFVVC
XDDVG VXDXF GVDXD VVGDX DVFAV VDXDG VVVGV FXAXC
XDGXD DGV'''}



def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def inverse(source):
    q, remainder = divmod(len(source), len(RANKS))
    columns, origin_columns, cursor = {}, {}, 0
    for c in sorted(range(len(RANKS)), key=RANKS.__getitem__):
        length = q + (c < remainder)
        columns[c] = source[cursor:cursor + length]
        origin_columns[c] = list(range(cursor, cursor + length))
        cursor += length
    mid, origins = [], []
    for row in range(q + bool(remainder)):
        for c in range(len(RANKS)):
            if row < len(columns[c]):
                mid.append(columns[c][row])
                origins.append(origin_columns[c][row])
    return ''.join(mid), origins


def inspect(source, square=SQUARE):
    mid, origins = inverse(source)
    unused = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') - set(square)
    domains = []
    for a, b in zip(mid[::2], mid[1::2]):
        possible = set()
        for row in range(6):
            for col in range(6):
                if (a not in CO or a == CO[row]) and (b not in CO or b == CO[col]):
                    symbol = square[6 * row + col]
                    possible.update(unused if symbol == '?' else symbol)
        domains.append(''.join(sorted(possible)))
    return {'plaintext': ''.join(d if len(d) == 1 else '?' for d in domains),
            'domains': domains, 'fixed_positions': sum(len(d) == 1 for d in domains),
            'plaintext_positions': len(domains), 'interim': mid,
            'interim_source_indices': origins,
            'unpaired_interim_coordinate': mid[-1:] if len(mid) % 2 else ''}


def encrypt(text, square=SQUARE):
    mid = ''.join('??' if c == '?' else CO[square.index(c) // 6] + CO[square.index(c) % 6] for c in text)
    return ''.join(mid[c::len(RANKS)] for c in sorted(range(len(RANKS)), key=RANKS.__getitem__))


def witness_set(source, template):
    result = []
    missing = [i for i, c in enumerate(source) if c not in CO]
    for vf, xa in [('5', '6'), ('6', '5')]:
        square = SQUARE[:26] + vf + SQUARE[27:30] + xa + SQUARE[31:]
        assert len(set(square)) == 36
        for fill in itertools.product(CO, repeat=len(missing)):
            cipher = list(source)
            for i, c in zip(missing, fill):
                cipher[i] = c
            cipher = ''.join(cipher)
            text = inspect(cipher, square)['plaintext']
            assert '?' not in text and all(a == '?' or a == b for a, b in zip(template, text))
            assert encrypt(text, square) == cipher
            result.append({'conditional_key_binding': {'VF': vf, 'XA': xa},
                           'remaining_source_mask_values': dict(zip(map(str, missing), fill)),
                           'plaintext': text, 'ciphertext': cipher})
    return result


def geometry(record):
    source, target = record['analysis_source'], encrypt(record['editorial_text'])
    count = len(source) - len(target)
    histogram, best, winners, combined_best, combined_winners, evaluated = collections.Counter(), None, [], None, [], 0
    for indices in itertools.combinations(range(len(source)), count):
        if count == 1:
            i = indices[0]
            candidate = source[:i] + source[i + 1:]
        else:
            i, j = indices
            candidate = source[:i] + source[i + 1:j] + source[j + 1:]
        substitutions = sum(a in CO and b in CO and a != b for a, b in zip(candidate, target))
        exclusions = sum(source[i] in CO for i in indices)
        total = substitutions + exclusions
        histogram[substitutions] += 1
        evaluated += 1
        if best is None or substitutions < best:
            best, winners = substitutions, []
        if substitutions == best:
            winners.append(list(indices))
        if combined_best is None or total < combined_best:
            combined_best, combined_winners = total, []
        if total == combined_best:
            combined_winners.append(list(indices))
    return {'source_id': record['id'], 'completed_exclusion_sets': evaluated,
            'observed_substitution_histogram': {str(k): v for k, v in sorted(histogram.items())},
            'minimum_observed_substitutions': best, 'minimum_substitution_indices': winners,
            'minimum_combined_observed_operations': combined_best,
            'minimum_combined_indices': combined_winners,
            'template_question_marks_are_wildcards': True}


def source_alignment_audit():
    """Independently find all minimum maps using an exact deletion DP."""
    root = HERE.parents[1]
    parallel_path = HERE / 'parallel_witnesses.json'
    military_path = root / 'experiments/p170_continuation/military_records.json'
    parallel = read(parallel_path)
    certified = parallel['p160_A2_p170_B2']['source_only_exclusion_alignment']
    military = read(military_path)
    second = next(r for r in military['records'] if r['id'] == 'p170_B2')
    source = ''.join(c if c in CO else '?' for c in ''.join(ROWS['p160_A2'].split()))
    target_literal = ''.join(''.join(second['raw_source_rows']).split())
    assert target_literal == second['raw_source_compact']
    target = ''.join(c if c in CO else '?' for c in target_literal)
    assert target == second['analysis_ciphertext']
    assert (len(source), len(target)) == (240, 238)
    assert parallel['source_files']['experiments/p170_continuation/military_records.json']['sha256'] == sha(military_path)

    # State (i, d): i source positions consumed, exactly d exclusions used;
    # target index i-d is therefore determined. Only optimum predecessors
    # are retained; traceback enumerates every equally good deletion map.
    costs = {(0, 0): 0}
    parents = {}
    for i in range(len(source)):
        for d in range(3):
            state = (i, d)
            if state not in costs:
                continue
            j = i - d
            successors = []
            if j < len(target):
                penalty = int(source[i] in CO and target[j] in CO and source[i] != target[j])
                successors.append(((i + 1, d), penalty, None))
            if d < 2:
                successors.append(((i + 1, d + 1), 0, i))
            for nxt, penalty, excluded in successors:
                proposed = costs[state] + penalty
                if nxt not in costs or proposed < costs[nxt]:
                    costs[nxt] = proposed
                    parents[nxt] = [(state, excluded)]
                elif proposed == costs[nxt]:
                    parents[nxt].append((state, excluded))

    def traceback(state):
        if state == (0, 0):
            return [()]
        return [previous + (() if excluded is None else (excluded,))
                for parent, excluded in parents[state] for previous in traceback(parent)]

    winners = sorted(traceback((len(source), 2)))
    assert costs[(len(source), 2)] == certified['minimum_observed_disagreements'] == 5
    assert winners == [(18, 26), (18, 27)]
    assert [list(x) for x in winners] == [w['excluded_source_indices_0based'] for w in certified['all_minimum_maps']]
    assert len(winners) == certified['minimum_map_count']
    decoded_maps = []
    for excluded, witness in zip(winners, certified['all_minimum_maps']):
        origins = [i for i in range(len(source)) if i not in excluded]
        frame = ''.join(source[i] for i in origins)
        assert frame == witness['frame']
        decoded = inspect(frame)
        decoded_maps.append(decoded)
        assert decoded['plaintext'] == witness['raw_plaintext']
        assert [{'plaintext_index_0based': i, 'domain': domain}
                for i, domain in enumerate(decoded['domains']) if len(domain) > 1] == witness['unresolved_raw_domains']
        assert decoded['interim'][134:136] == 'XV'
        assert [origins[i] for i in decoded['interim_source_indices'][134:136]] == [19, 199]
    domain_union = [''.join(sorted({c for decoded in decoded_maps for c in decoded['domains'][i]}))
                    for i in range(119)]
    assert domain_union[15] == 'JZ'
    assert [{'plaintext_index_0based': i, 'domain': domain}
            for i, domain in enumerate(domain_union) if len(domain) > 1] == certified['all_minimum_unresolved_domains']
    assert sum(len(domain) == 1 for domain in domain_union) == certified['all_minimum_common_fixed_plaintext_positions'] == 116
    return {
        'method': 'Exact dynamic program over source prefix and number of exclusions, with all optimum predecessor paths retained; no plaintext or language score.',
        'parallel_report_sha256': sha(parallel_path), 'p170_source_record_sha256': sha(military_path),
        'source_id': 'p160_A2', 'target_id': 'p170_B2',
        'reachable_dynamic_program_states': len(costs),
        'minimum_observed_disagreements': costs[(len(source), 2)],
        'all_minimum_exclusion_maps': [list(x) for x in winners],
        'source_only_rd_coordinate_indices': [19, 199],
        'source_only_rd_coordinate_pair': 'XV',
        'source_only_name_position_15_domain': 'JZ',
        'limit': 'This confirms the separate exhaustive source-only minimum and both maps. It does not select the J branch or establish the cause of the surplus glyphs.',
    }


def build():
    inp, cert = read(HERE / 'inputs.json'), read(HERE / 'certificates.json')
    assert cert['inputs_sha256'] == sha(HERE / 'inputs.json')
    assert inp['key']['square'] == SQUARE and inp['key']['column_rank_order'] == RANKS
    certified = {r['id']: r for r in cert['records']}
    assert set(certified) == set(ROWS)
    source_images = {}
    for image in inp['source']['images']:
        assert sha(HERE / image['path']) == image['sha256']
        source_images[image['path']] = image['sha256']
    records, geometries, corpus_witnesses = [], [], []
    for record in inp['records']:
        ident = record['id']
        literal = ''.join(ROWS[ident].split())
        assert literal == record['literal_source'] == ''.join(''.join(record['rows']).split())
        source = ''.join(c if c in CO else '?' for c in literal)
        assert source == record['analysis_source']
        excluded = record['excluded_source_indices']
        origins = [i for i in range(len(source)) if i not in excluded]
        model = ''.join(source[i] for i in origins)
        raw = inspect(model)
        assert raw == certified[ident]['raw_reading'] and raw['plaintext'] == record['expected_raw']
        stencil = encrypt(record['editorial_text'])
        edited = ''.join(a if b == '?' else b for a, b in zip(model, stencil))
        after = inspect(edited)
        assert after == certified[ident]['edited_reading'] and after['plaintext'] == record['editorial_text']
        assert origins == certified[ident]['model_to_source_indices']
        changes = [[origins[i], a, b] for i, (a, b) in enumerate(zip(model, edited)) if a != b]
        assert changes == record['expected_source_changes']
        costs = {'known_coordinate_substitutions': sum(a in CO for _, a, b in changes),
                 'source_mask_fills': sum(a not in CO for _, a, b in changes),
                 'excluded_observed_coordinates': sum(source[i] in CO for i in excluded),
                 'excluded_source_masks': sum(source[i] not in CO for i in excluded)}
        assert costs == record['expected_cost'] == certified[ident]['cost']
        numeral_edits = [{'position': i, 'raw': a, 'edited': b}
                         for i, (a, b) in enumerate(zip(raw['plaintext'], after['plaintext'])) if a.isdigit() and a != b]
        assert numeral_edits == record['explicit_numeral_word_repairs'] == certified[ident]['explicit_numeral_word_repairs']
        witnesses = witness_set(edited, record['editorial_text'])
        assert witnesses == certified[ident]['compatible_completions']['complete_binding_and_fill_witnesses']
        assert [set(d) for d in after['domains']] == [{w['plaintext'][i] for w in witnesses} for i in range(len(after['domains']))]
        if excluded:
            assert inspect(source) == certified[ident]['unaltered_source_diagnostic']
            g = geometry(record)
            parent = next(g for g in cert['fixed_template_exclusion_audits'] if g['source_id'] == ident)
            for field in ['completed_exclusion_sets', 'observed_substitution_histogram', 'minimum_observed_substitutions', 'minimum_combined_observed_operations', 'template_question_marks_are_wildcards']:
                assert g[field] == parent[field], (ident, field)
            assert g['minimum_substitution_indices'] == [x['excluded_source_indices'] for x in parent['all_minimum_substitution_sets']]
            assert g['minimum_combined_indices'] == [x['excluded_source_indices'] for x in parent['all_minimum_combined_sets']]
            geometries.append(g)
        records.append({'id': ident, 'source_slots': len(literal), 'valid_source_coordinates': sum(c in CO for c in literal),
                        'model_slots': len(model), 'plaintext_positions': len(raw['domains']),
                        'raw_fixed_positions': raw['fixed_positions'], 'edited_fixed_positions': after['fixed_positions'],
                        'source_masks': [{'source_index': i, 'glyph': c} for i, c in enumerate(literal) if c not in CO],
                        'changes': changes, 'cost': costs, 'numeric_word_repairs': numeral_edits,
                        'witness_count': len(witnesses), 'witnesses': witnesses})
    for binding in [{'VF': '5', 'XA': '6'}, {'VF': '6', 'XA': '5'}]:
        choices = [[w for w in r['witnesses'] if w['conditional_key_binding'] == binding] for r in records]
        for selected in itertools.product(*choices):
            corpus_witnesses.append({'global_binding': binding,
                                     'source_83_fill': next(w['remaining_source_mask_values']['83'] for w in selected if '83' in w['remaining_source_mask_values']),
                                     'record_plaintexts': {r['id']: w['plaintext'] for r, w in zip(records, selected)}})
    assert len(corpus_witnesses) == 12
    b2 = next(r for r in records if r['id'] == 'p160_B2')
    assert not any(change[0] == 83 for change in b2['changes']) and b2['witness_count'] == 12
    summary = {'physical_records': len(records),
               **{field: sum(r[field] for r in records) for field in ['source_slots', 'valid_source_coordinates', 'model_slots', 'plaintext_positions', 'raw_fixed_positions', 'edited_fixed_positions']},
               **{field: sum(r['cost'][field] for r in records) for field in ['known_coordinate_substitutions', 'source_mask_fills', 'excluded_observed_coordinates', 'excluded_source_masks']},
               'inserted_model_coordinates': 0, 'published_key_changes': 0}
    assert summary == cert['summary'] == inp['expected_totals']
    return {'schema': 'adfgvx-nov8-independent-source-candidate-audit-v1',
            'authors': ['icekylinx', 'GPT-6 Astra Pro'],
            'inputs_sha256': sha(HERE / 'inputs.json'), 'certificates_sha256': sha(HERE / 'certificates.json'),
            'source_image_sha256': source_images,
            'manual_source_review': {
                'scope': 'All seven embedded transcripts were visually checked against the full p160 page and detailed A2/BCD/p161-upper crops. The repository p160 full page and p161 source images bind that source edition; executable replay does not itself perform optical reading.',
                'findings': ['A2 has 240 slots including GDGDXF at 15–20 and DXAADG at 26–31; RICHI-238 is a distinct advertised count.',
                             'C1 has 309 slots including FAGVGD at 280–285; RICHI-308 is a distinct advertised count.',
                             'B2 has C at 8 and B at 83; p161 A2 has C at 79 and 119. They remain noncoordinate masks, without a favorable letter substitution.',
                             'There are 8 printed dashes and 4 invalid letters across the seven source records.',
                             'The cleartext footers ZON and NF NKJ v LP UM are outside the ciphertext body.',
                             'No source-glyph discrepancy was found. p159 A remains outside this seven-record count.']},
            'summary': summary, 'records': records,
            'fixed_template_exclusion_audits': geometries,
            'source_only_parallel_alignment': source_alignment_audit(),
            'global_coupled_completion_count': len(corpus_witnesses), 'global_coupled_completions': corpus_witnesses,
            'limits': ['The observed-coordinate exclusions are separate from substitutions and source-mask fills.',
                       'The full exclusion scans use supplied templates with wildcard question marks; minima do not prove historical plaintext or geometry.',
                       'VF and XA receive complementary 5/6 labels once for the entire corpus. There are 12 global binding-and-fill possibilities, not independent digit choices at each question mark.',
                       'B2 source 83 remains unresolved. Its allowed plaintext labels include letters as well as digits; no numeric formatting assumption is imposed.',
                       'WERGCHEEZ, NAGYBESKEREK, 380L, 170M, TSCHENKE, LI, AWALOFF and STUMM remain literal under the parent edition.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify', action='store_true')
    p.add_argument('--write', action='store_true')
    a = p.parse_args()
    assert a.verify != a.write, 'Choose --verify or --write.'
    result = build()
    out = HERE / 'independent_source_audit.json'
    if a.write:
        out.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == read(out)
    print(json.dumps({'verified': a.verify, 'summary': result['summary'],
                      'geometry_evaluations': sum(g['completed_exclusion_sets'] for g in result['fixed_template_exclusion_audits']),
                      'global_coupled_completions': result['global_coupled_completion_count']}, indent=2))


if __name__ == '__main__':
    main()
