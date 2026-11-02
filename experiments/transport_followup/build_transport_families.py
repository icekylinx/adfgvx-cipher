#!/usr/bin/env python3
"""Audit two newly linked printed transport pairs without a language model.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
The source texts and previously published key are separate from editorial
readings. Every source map and candidate coordinate is retained in the output.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from adfgvx.transport import characterize

HERE = Path(__file__).resolve().parent
COORDS = 'ADFGVX'


def normalized(raw):
    return ''.join(c if c in COORDS else '?' for c in raw)


def differences(first, second):
    assert len(first) == len(second)
    return [dict(corrected_ciphertext_index=i, first=a, second=b,
                 both_valid_coordinates=a in COORDS and b in COORDS)
            for i, (a, b) in enumerate(zip(first, second)) if a != b]


def build():
    source = json.loads((HERE/'transport_sources.json').read_text())
    key = next(k for k in json.loads((ROOT/'data/keys.json').read_text())['keys']
               if k['id'] == 'Nov13-15b')
    ranks, square = key['column_rank_order'], key['square']
    records = {}
    for item in source['records']:
        raw = ''.join(item['raw_grouped'].split())
        row = dict(item, raw_literal=raw, analysis_ciphertext=normalized(raw),
                   received_slot_count=len(raw),
                   valid_coordinate_count=sum(c in COORDS for c in raw),
                   invalid_source_slots=[dict(source_index=i, printed=c, analysis='?')
                                         for i, c in enumerate(raw) if c not in COORDS])
        if len(raw) % 2 == 0:
            row['literal_analysis'] = characterize(normalized(raw), ranks, square, list(range(len(raw))))
        records[item['id']] = row
    def analyzed(ct, mapping):
        return dict(corrected_ciphertext=ct, corrected_to_source_index=mapping,
                    analysis=characterize(ct, ranks, square, mapping))

    # Independently repeated group in E: either identical copy can be deleted.
    e = records['p198_E']['analysis_ciphertext']
    repairs = []
    for start in [15, 20]:
        ct = e[:start] + e[start + 5:]
        row = analyzed(ct, list(range(start)) + list(range(start + 5, len(e))))
        row.update(deleted_source_indices=list(range(start, start + 5)),
                   deleted_literal=records['p198_E']['raw_literal'][start:start + 5],
                   known_source_substitutions=[])
        repairs.append(row)
    assert repairs[0]['corrected_ciphertext'] == repairs[1]['corrected_ciphertext']
    eref = repairs[0]['corrected_ciphertext']

    # Exhaust all positions; preserve all valid D coordinates and move only the
    # printed dash slot. The two best placements have different raw readings.
    d = records['p197_D']['analysis_ciphertext']
    assert [i for i, c in enumerate(d) if c == '?'] == [89]
    d_without_dash = d[:89] + d[90:]
    d_source_map = list(range(89)) + list(range(90, len(d)))
    d_trials = []
    for gap in range(len(d_without_dash) + 1):
        ct = d_without_dash[:gap] + '?' + d_without_dash[gap:]
        diffs = differences(ct, eref)
        d_trials.append(dict(insert_erasure_before_surviving_source_index=gap,
                             valid_coordinate_disagreements=sum(x['both_valid_coordinates'] for x in diffs)))
    dmin = min(row['valid_coordinate_disagreements'] for row in d_trials)
    dalign = []
    for trial in d_trials:
        if trial['valid_coordinate_disagreements'] != dmin:
            continue
        gap = trial['insert_erasure_before_surviving_source_index']
        ct = d_without_dash[:gap] + '?' + d_without_dash[gap:]
        # The moved slot retains its original printed-slot provenance.
        mapping = d_source_map[:gap] + [89] + d_source_map[gap:]
        row = dict(trial, **analyzed(ct, mapping))
        row['differences_from_duplicate_repaired_p198_E'] = differences(ct, eref)
        dalign.append(row)

    # Exhaust all 186 positions for a missing five-slot block in C.
    c, b = (records[i]['analysis_ciphertext'] for i in ['p197_C', 'p198_B'])
    c_trials = []
    for gap in range(len(c) + 1):
        ct = c[:gap] + '?' * 5 + c[gap:]
        diffs = differences(ct, b)
        c_trials.append(dict(insert_five_erasures_before_source_index=gap,
                             valid_coordinate_disagreements=sum(x['both_valid_coordinates'] for x in diffs)))
    cmin = min(row['valid_coordinate_disagreements'] for row in c_trials)
    calign = []
    for trial in c_trials:
        if trial['valid_coordinate_disagreements'] != cmin:
            continue
        gap = trial['insert_five_erasures_before_source_index']
        ct = c[:gap] + '?' * 5 + c[gap:]
        mapping = list(range(gap)) + [None] * 5 + list(range(gap, len(c)))
        row = dict(trial, **analyzed(ct, mapping))
        row['differences_from_p198_B'] = differences(ct, b)
        calign.append(row)

    # A reading is an editorial target. This audit identifies, for each target
    # letter, whether a complete pair exists in either witness, only a mixture
    # of observed halves suffices, an erasure must be filled, or a literal
    # coordinate must change. It never re-labels those choices as exact decoding.
    def audit_reading(target, first, second):
        fa, sa = first['analysis'], second['analysis']
        assert len(target) == len(fa['domains']) == len(sa['domains'])
        rows = []
        position_costs = []
        unused = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') - set(square)
        for i, ch in enumerate(target):
            ap = fa['domains'][i]['coordinate_pair']
            bp = sa['domains'][i]['coordinate_pair']
            all_pairs = [COORDS[cell // 6] + COORDS[cell % 6] for cell in range(36)]
            costs = [sum(observed != '?' and observed != wanted
                         for pair in [ap, bp] for observed, wanted in zip(pair, wanted_pair))
                     for wanted_pair in all_pairs]
            minimum = min(costs)
            cells = [cell for cell, cost in enumerate(costs) if cost == minimum]
            letters = set()
            for cell in cells:
                letters.update(unused if square[cell] == '?' else square[cell])
            expected = None if ch == '?' else all_pairs[square.index(ch)]
            by_witness = None if expected is None else [sum(a != '?' and a != b for a, b in zip(pair, expected)) for pair in [ap, bp]]
            position_costs.append(dict(plaintext_index=i, first_observed_pair=ap, second_observed_pair=bp,
                minimum_known_coordinate_cost=minimum, minimum_cost_cells=cells,
                minimum_cost_characters=''.join(sorted(letters)), editorial_character=ch,
                editorial_required_pair=expected, editorial_cost_by_witness=by_witness,
                editorial_combined_cost=None if by_witness is None else sum(by_witness)))
            if ch == '?':
                continue
            cell = square.index(ch)
            expected = COORDS[cell // 6] + COORDS[cell % 6]
            a, b = fa['domains'][i], sa['domains'][i]
            ap, bp = a['coordinate_pair'], b['coordinate_pair']
            if expected in [ap, bp]:
                support = 'complete_pair_in_at_least_one_witness'
            elif all(t in [x, y] for t, x, y in zip(expected, ap, bp)):
                support = 'observed_coordinate_composite'
            elif all(t in [x, y] or '?' in [x, y] for t, x, y in zip(expected, ap, bp)):
                support = 'requires_erasure_fill'
            else:
                support = 'requires_unattested_coordinate_emendation'
            rows.append(dict(plaintext_index=i, editorial_character=ch,
                             required_pair=expected, first_observed_pair=ap,
                             second_observed_pair=bp, support=support))
        minimum_total = sum(r['minimum_known_coordinate_cost'] for r in position_costs)
        def attainment(use_editorial):
            pairs = []
            for row in position_costs:
                cell = row['minimum_cost_cells'][0]
                pairs.append(row['editorial_required_pair'] if use_editorial and row['editorial_required_pair'] is not None else COORDS[cell // 6] + COORDS[cell % 6])
            stream = ''.join(pairs)
            ciphertext = ''.join(stream[col::len(ranks)] for col in sorted(range(len(ranks)), key=lambda col: ranks[col]))
            costs_by_witness = [sum(a != '?' and a != b for a, b in zip(witness['intermediate_stream'], stream)) for witness in [fa, sa]]
            return dict(intermediate_coordinate_stream=stream, ciphertext=ciphertext, cost_by_witness=costs_by_witness, combined_cost=sum(costs_by_witness))
        specified_cost = sum(r['editorial_combined_cost'] or 0 for r in position_costs)
        unresolved_minimum = sum(r['minimum_known_coordinate_cost'] for r in position_costs if r['editorial_character'] == '?')
        return dict(normalized_editorial_target=target, per_letter_support=rows,
                    support_counts={label: sum(r['support'] == label for r in rows)
                                    for label in sorted({r['support'] for r in rows})},
                    combined_coordinate_cost=dict(
                        convention='Count each altered valid coordinate separately in each aligned witness; erasure fills and the stated length/slot repairs are not known-coordinate substitutions.',
                        unconstrained_attainable_minimum=minimum_total,
                        editorial_cost_at_specified_positions=specified_cost,
                        minimum_cost_at_unresolved_positions=unresolved_minimum,
                        attainable_minimum_with_specified_editorial_letters=specified_cost+unresolved_minimum,
                        editorial_cost_by_witness_at_specified_positions=[sum(r['editorial_cost_by_witness'][j] for r in position_costs if r['editorial_cost_by_witness'] is not None) for j in range(2)],
                        positions_outside_minimum_cost_domains=[r['plaintext_index'] for r in position_costs if r['editorial_combined_cost'] is not None and r['editorial_combined_cost'] > r['minimum_known_coordinate_cost']],
                        complete_pair_support_is_one_globally_clean_witness=False,
                        minimum_cost_attainment_witness=attainment(False),
                        editorial_cost_attainment_witness=attainment(True),
                        per_position=position_costs))

    e_target = 'ESKOMMTEIN?TONNENAUTOXNURBESTENANHAENGERBELADENXBENZINPUMPEBEREITHALTEN'
    e_audit = audit_reading(e_target, dalign[-1], repairs[0])
    e_audit.update(
        german='Es kommt ein [?]-Tonnen-Auto. Nur besten Anhänger beladen. Benzinpumpe bereithalten.',
        english='An [?]-ton lorry is coming. Load only the best trailer. Have the petrol pump ready.',
        notes=['The tonnage remains unresolved; no digit assignment is added to the published partial square.',
               'The grammatical reading needs explicit emendation beyond the two printed witnesses.',
               'Both equally close D erasure placements are retained; placement 75 is used only to audit the preferred reading.'])
    c_target = 'NACHRCHEFXEINHAFENXZWEIUSGERAETENACHDARMSTADTVERLADENXSTATIONBLEIBTBIS16X0???BETRBEREITXSEIFERT'
    c_audit = audit_reading(c_target, calign[-1], dict(analysis=records['p198_B']['literal_analysis']))
    c_audit.update(
        german='Nachr.-Chef. [EINHAFEN: unclear designation]. Zwei US-Geräte nach Darmstadt verladen. Station bleibt bis [16X0???] betr.-bereit. Seifert.',
        english='Chief of signals. [EINHAFEN: unclear designation]. Load two US apparatuses for Darmstadt. The station remains operational until [16X0???]. Seifert.',
        notes=['NACHRCHEF is read as the abbreviation Nachrichtenchef; its expansion is editorial.',
               'EINHAFEN is the source-composite letter sequence, not an independently identified place.',
               'US is retained as printed rather than expanded speculatively.',
               'The time or date is not normalized to 16:00; its trailing positions disagree or remain unknown.',
               'BETRBEREIT is treated as the abbreviation betriebsbereit, not as a recovered full spelling.'])
    return dict(format_version=1, project=source['project'], review_credit=source['review_credit'],
                review_date=source['review_date'], source=source['source'],
                source_transcription_sha256=hashlib.sha256((HERE/'transport_sources.json').read_bytes()).hexdigest(),
                key={k: key[k] for k in ['id', 'square', 'column_rank_order', 'provenance']},
                records=list(records.values()),
                scope='Transport context only. None of these readings solves the separate p198 section D / CHI-170 target.',
                duplicate_group_repair=dict(source_id='p198_E',
                    hypothesis='One of two adjacent, identical XAXVV groups is a copied duplicate.',
                    candidates=repairs, corrected_length=142,
                    retained_valid_coordinate_count=141,
                    corrected_ciphertext_identical_for_both_choices=True),
                erasure_relocation=dict(source_id='p197_D', reference_source_id='p198_E',
                    hypothesis='The single printed dash is at the wrong position; valid coordinates keep their exact order.',
                    tested_placements=len(d_trials), all_trial_distances=d_trials,
                    minimum_valid_coordinate_disagreements=dmin, best_alignments=dalign),
                missing_group_alignment=dict(source_id='p197_C', reference_source_id='p198_B',
                    hypothesis='One five-slot group is absent from the 185-slot source.',
                    tested_placements=len(c_trials), all_trial_distances=c_trials,
                    minimum_valid_coordinate_disagreements=cmin, best_alignments=calign,
                    corrected_ciphertexts_identical=len({r['corrected_ciphertext'] for r in calign}) == 1),
                editorial_readings=dict(lorry_and_petrol_pump=e_audit, equipment_for_darmstadt=c_audit),
                limitations=['Minimum coordinate disagreement is an alignment criterion, not proof of unique original plaintext.',
                             'The source callsigns, times, prefixes and advertised lengths stay literal even where irregular.',
                             'Published key provenance is retained; this review contributes new source linkage and explicit edit accounting.'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'data/certificates/p197_p198_transport.json')
    args=parser.parse_args()
    result=build()
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(output=str(args.output),
        source_ids=[r['id'] for r in result['records']],
        d_best_erasure_positions=[r['insert_erasure_before_surviving_source_index'] for r in result['erasure_relocation']['best_alignments']],
        c_best_gap_positions=[r['insert_five_erasures_before_source_index'] for r in result['missing_group_alignment']['best_alignments']],
        editorial_support={k:v['support_counts'] for k,v in result['editorial_readings'].items()}), indent=2))

if __name__=='__main__': main()
