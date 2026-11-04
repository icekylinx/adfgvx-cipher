#!/usr/bin/env python3
"""Audit all reviewed Nov13-15b sources and two new p186 A2 reference labels.

Independent standard-library inverse/forward transforms; no cipher-module import.
The original source records and existing conditional frames are immutable inputs.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = 'ADFGVX'
ALPH = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def read(path):
    return json.loads((ROOT / path).read_text())

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def clean(text):
    return ''.join(c if c in CO else '?' for c in text)

def inverse(wire, square, ranks):
    width = len(ranks)
    rows, extra = divmod(len(wire), width)
    source_for_stream = [None] * len(wire)
    offset = 0
    for column in sorted(range(width), key=lambda c: ranks[c]):
        for row in range(rows + (column < extra)):
            source_for_stream[row * width + column] = offset
            offset += 1
    assert sorted(source_for_stream) == list(range(len(wire)))
    output, positions = [], []
    unused = ALPH - set(square)
    for at in range(0, len(source_for_stream) - 1, 2):
        indices = source_for_stream[at:at + 2]
        pair = ''.join(wire[i] for i in indices)
        domain = set()
        for a in CO if pair[0] == '?' else pair[0]:
            for b in CO if pair[1] == '?' else pair[1]:
                symbol = square[CO.index(a) * 6 + CO.index(b)]
                domain.update(unused if symbol == '?' else symbol)
        domain = ''.join(sorted(domain))
        output.append(domain if len(domain) == 1 else '?')
        positions.append({'plaintext_index': at // 2, 'model_indices': indices,
                          'pair': pair, 'domain': domain})
    return ''.join(output), positions

def transpose(stream, ranks):
    return ''.join(stream[column::len(ranks)]
                   for column in sorted(range(len(ranks)), key=lambda c: ranks[c]))

def encrypt(plaintext, square, ranks):
    assert '?' not in square and len(set(square)) == 36
    stream = ''.join(CO[square.index(c) // 6] + CO[square.index(c) % 6]
                     for c in plaintext)
    return transpose(stream, ranks)

def build():
    data = read('experiments/nov13_joint_completion/coverage_inputs.json')
    for path, digest in data['dependencies'].items():
        assert sha(path) == digest, path
    assert data['conditional_assignments'] == {'XX': 'Q', 'VG': '2'}
    key=next(k for k in read('data/keys.json')['keys'] if k['id']=='Nov13-15b');base=key['square'];ranks=key['column_rank_order'];joint=list(base)
    for pair,label in [('XX','Q'),('VG','2')]:
     i=CO.index(pair[0])*6+CO.index(pair[1]);assert joint[i]=='?';joint[i]=label
    joint=''.join(joint)
    assert joint==read('experiments/nov13_joint_completion/inputs.json')['joint_square']
    cat=read('data/reading_catalog.json');entries=[e for e in cat['challenge']+cat['other'] if e.get('source_reviewed')]
    existing={r['id'] for p in ['experiments/nov13_joint_completion/inputs.json','experiments/nov13_joint_completion/traffic_inputs.json'] for r in read(p)['records']}|{'p189_E'}
    known_conflicts={'p191_A1'}
    records=[];unsupported=[];excluded=[]
    def string_raw(v):
     if isinstance(v,str):return v
     if isinstance(v,dict):
      for field in ['plaintext','raw']: 
       if isinstance(v.get(field),str):return v[field]
     return None
    def add(rid,source,mapping,expected,editions,provenance,variant='primary'):
     assert mapping is not None and all(i is None or isinstance(i,int) for i in mapping)
     assert len([i for i in mapping if i is not None])==len(set(i for i in mapping if i is not None))
     native=''.join('?' if i is None else clean(source[i]) for i in mapping)
     raw,np=inverse(native,base,ranks);new,ns=inverse(native,joint,ranks)
     if expected is not None:assert raw==expected,(rid,variant,raw,expected)
     hits=[]
     for p in ns:
      if p['pair'] not in ('XX','VG'):continue
      origins=[mapping[i] for i in p['model_indices']]
      assert None not in origins and ''.join(source[i] for i in origins)==p['pair']
      hits.append({**p,'source_indices':origins,'before':raw[p['plaintext_index']],'after':new[p['plaintext_index']],'context_before':raw[max(0,p['plaintext_index']-14):p['plaintext_index']+15],'context_after':new[max(0,p['plaintext_index']-14):p['plaintext_index']+15]})
     eds=[]
     for name,cipher,etext in editions:
      assert len(cipher)==len(native),(rid,name,len(cipher),len(native))
      before,ep=inverse(cipher,base,ranks);after,aps=inverse(cipher,joint,ranks)
      if etext is not None:assert before==etext,(rid,name,before,etext)
      changes=[];fills=[]
      for m,(a,b) in enumerate(zip(native,cipher)):
       if a==b:continue
       origin=mapping[m]
       (changes if origin is not None and source[origin] in CO else fills).append({'model_index':m,'source_index':origin,'before':a,'after':b})
      gains=[{**p,'source_indices':[mapping[i] for i in p['model_indices']],'symbol':after[p['plaintext_index']],'native_pair':np[p['plaintext_index']]['pair'],'context':after[max(0,p['plaintext_index']-14):p['plaintext_index']+15]} for p in aps if before[p['plaintext_index']]=='?' and after[p['plaintext_index']]!='?']
      altered_native_hits=[{'plaintext_index':p['plaintext_index'],'native_pair':p['pair'],'native_conditional_label':p['after'],'edition_pair':ep[p['plaintext_index']]['pair'],'edition_label':before[p['plaintext_index']],'edition_source_changes':[x for x in changes if x['model_index'] in p['model_indices']]} for p in hits if ep[p['plaintext_index']]['pair']!=p['pair']]
      eds.append({'name':name,'before':before,'after':after,'fixed_before':len(before)-before.count('?'),'fixed_after':len(after)-after.count('?'),'gains':gains,'observed_substitutions':changes,'mask_or_added_fills':fills,'native_target_pairs_changed_in_edition':altered_native_hits})
     records.append({'id':rid,'variant':variant,'provenance':provenance,'literal_source':source,'model_to_source_indices':mapping,'source_slots':len(source),'model_slots':len(native),'positions':len(raw),'raw_before':raw,'raw_after':new,'fixed_raw_before':len(raw)-raw.count('?'),'fixed_raw_after':len(new)-new.count('?'),'native_target_pairs':hits,'editions':eds,'previously_in_gain_layer':rid in existing,'previously_conflict':rid in known_conflicts})

    ips=sorted({p for e in entries for p in e.get('evidence',[]) if p.endswith('/inputs.json') and (ROOT/p).exists() and 'Nov13-15b' in (ROOT/p).read_text()})
    for ip in ips:
     d=read(ip)
     irs=d.get('records',[d['record']] if isinstance(d.get('record'),dict) else [])
     for ir in irs:
      rid=ir['id'];kid=ir.get('key_id',d.get('key',{}).get('id'))
      if kid!='Nov13-15b':continue
      refs=[e for e in entries if e['id']==rid and ip in e.get('evidence',[])]
      if not refs:excluded.append({'id':rid,'input':ip,'reason':'not directly listed as a source-reviewed catalogue row for this input'});continue
      cp=str(Path(ip).parent/'certificates.json')
      if not (ROOT/cp).exists():unsupported.append({'id':rid,'input':ip,'reason':'needs dedicated singular-certificate adapter'});continue
      cert=read(cp);crs=cert.get('records',[]);matches=[r for r in crs if r['id']==rid]
      if len(matches)!=1:unsupported.append({'id':rid,'input':ip,'reason':'no unique primary certificate row'});continue
      cr=matches[0];source=''.join(''.join(ir['source_rows']).split())
      stated=cr.get('literal_source',cr.get('source_literal'))
      assert source==stated,(rid,'literal mismatch')
      mapping=next((cr[f] for f in ['model_to_source_indices','frame_to_source_indices','conditional_model_to_source'] if f in cr),None)
      if mapping is None:unsupported.append({'id':rid,'input':ip,'reason':'no explicit primary source map'});continue
      expected=string_raw(cr.get('conditional_raw',cr.get('raw')))
      editions=[]
      for field in ['readable_candidate','edition']:
       v=cr.get(field)
       if isinstance(v,dict) and 'ciphertext' in v:editions.append((field,v['ciphertext'],string_raw(v.get('reading',v.get('raw')))))
      for i,v in enumerate(cr.get('editorial_candidates',[])):
       if 'ciphertext' in v:editions.append(('editorial_candidates/'+str(i)+'/'+v.get('id',''),v['ciphertext'],string_raw(v.get('raw'))))
      add(rid,source,mapping,expected,editions,{'inputs':ip,'inputs_sha256':sha(ip),'certificate':cp,'certificate_sha256':sha(cp)})

    # Explicit adapters for older source editions; no fresh geometry is selected.
    for pkg in ['boots_request','siedlce_withdrawal']:
     ip=f'experiments/{pkg}/inputs.json';cp=f'experiments/{pkg}/certificate.json';d=read(ip);cert=read(cp)
     irs=d.get('records',[d['record']] if 'record' in d else [])
     for ir in irs:
      rid=ir['id'];cr=next((r for r in cert.get('records',[]) if r['id']==rid),cert)
      source=''.join(''.join(ir['source_rows']).split());assert source==cr.get('literal_source',cr.get('source_literal'))
      mapping=cr.get('framed_position_to_received_position_0based',list(range(len(source))))
      expected=string_raw(cr.get('conditional_frame_reading',cr.get('raw')))
      ed=cr['edition'];editions=[('edition',ed['ciphertext'],string_raw(ed['reading']))]
      add(rid,source,mapping,expected,editions,{'inputs':ip,'inputs_sha256':sha(ip),'certificate':cp,'certificate_sha256':sha(cp)})
      unsupported=[u for u in unsupported if u['id']!=rid]

    cp='data/certificates/p185_D_transport.json';d=read(cp);pro={'certificate':cp,'certificate_sha256':sha(cp)}
    source=d['source']['ciphertext'];assert source==''.join(d['source']['ciphertext_grouped'].split())
    g=d['selected_geometry'];add('p185_D',source,g['corrected_to_source_index'],g['analysis']['raw_partial_plaintext'],[],pro)
    for row in d['direct_transport_context']:
     r=row['source'];rid=r['id'];source=r['raw_literal'];eds=[]
     assert clean(source)==r['analysis_ciphertext']
     if rid=='p189_E':
      ec=read('experiments/nov13_joint_completion/transport_certificate.json')['record']['edited_ciphertext']
      eds=[('existing_transport_word_fill',ec,None)]
     if rid in ['p194_A','p196_B']:
      composite=d['source_supported_transport_composite']
      eds=[('existing_cross_copy_composite',composite['corrected_ciphertext'],composite['analysis']['raw_partial_plaintext'])]
     add(rid,source,list(range(len(source))),r['raw_plaintext'],eds,pro)

    cp='data/certificates/p189.json';d=read(cp);source=d['p185']['ciphertext']
    add('p185_C',source,list(range(len(source))),d['p185']['plaintext'],[],{'certificate':cp,'certificate_sha256':sha(cp)})

    cp='data/reviews/p186_chi_parallel.json'
    for r in read(cp):
     source=r.get('conservative_ciphertext',r['ciphertext']);expected=r.get('conservative_raw_partial_plaintext',r['raw_partial_plaintext'])
     if r['id']=='p186_A1':
      old=read('experiments/source_followup/p186_source_and_suffix_delta.json')['p186_A1_conditional_erasure_fills']
      editions=[('existing_cross_copy_erasure_fills',old['ciphertext'],old['plaintext'])]
     else:
      editions=[('earlier_V_glyph_interpretation_not_native_certainty',r['ciphertext'],r['raw_partial_plaintext'])]
     add(r['id'],source,list(range(len(source))),expected,editions,{'certificate':cp,'certificate_sha256':sha(cp),'source_note':'Use the declared conservative glyph layer where present; the earlier V-glyph interpretation is not native certainty.'})

    cp='experiments/source_similarity_extension/source_inspection.json';d=read(cp)
    source=''.join(''.join(d['source']['source_rows']).split());assert source==d['layers']['image_reviewed_transcript']['ciphertext']
    expected=next(x['raw_plaintext'] for x in d['unchanged_key_decodes'] if x['key_id']=='Nov13-15b')
    ed=d['editorial_reading'];add('p189_C',source,list(range(len(source))),expected,[('editorial_reading',ed['reencrypted_candidate'],ed['plaintext'])],{'certificate':cp,'certificate_sha256':sha(cp)})

    cp='data/certificates/p197_p198_transport.json';d=read(cp);rs={r['id']:r for r in d['records']};pro={'certificate':cp,'certificate_sha256':sha(cp)}
    for rid,section in [('p197_C','missing_group_alignment'),('p197_D','erasure_relocation'),('p198_E','duplicate_group_repair')]:
     source=rs[rid]['raw_literal'];vs=d[section].get('best_alignments',d[section].get('candidates'))
     for i,v in enumerate(vs):
      add(rid,source,v['corrected_to_source_index'],v['analysis']['raw_partial_plaintext'],[],pro,'primary' if i==0 else 'retained_geometry_'+str(i))
    source=rs['p198_B']['raw_literal'];add('p198_B',source,list(range(len(source))),rs['p198_B']['literal_analysis']['raw_partial_plaintext'],[],pro)

    # Include only already enumerated source alternatives, not a new geometry search.
    # They do not multiply the distinct-physical-source denominator below.
    for cp,rid,section in [
     ('experiments/benzol_pump_query/certificates.json','p189_D','all_five_short_group_candidates'),
     ('experiments/black_sea_shipping/certificates.json','p199_A1','geometry_screen/all_minimum_model_readings'),
     ('experiments/black_sea_shipping/certificates.json','p199_A3','geometry_screen/all_minimum_model_readings'),
     ('experiments/nov13_congratulation_conditional_frame/certificates.json','p193_F','endpoint_alternatives'),
     ('experiments/warsaw_service_messages/certificates.json','p192_B','geometry_screen/all_tied_minima'),
    ]:
     cr=next(r for r in read(cp)['records'] if r['id']==rid);source=cr['literal_source'];vs=cr
     for field in section.split('/'):vs=vs[field]
     for i,v in enumerate(vs):
      mapping=v.get('model_to_source_indices')
      if rid=='p193_F':mapping=[j for j in range(len(source)) if j!=v['excluded_source_index']]
      if rid=='p192_B':
       gap=v['source_gap'];mapping=list(range(gap))+[None]+list(range(gap,len(source)))
      if any(r['id']==rid and r['model_to_source_indices']==mapping for r in records):continue
      eds=[]
      if rid=='p189_D':
       ed=v['readable_candidate'];eds=[('existing_alternative_readable_candidate',ed['ciphertext'],string_raw(ed.get('reading',ed.get('raw'))))]
      if rid=='p193_F':
       ed=v['edited'];eds=[('existing_alternative_edited',ed['ciphertext'],string_raw(ed.get('reading',ed.get('raw'))))]
      if rid=='p199_A3' and 'body_candidate' in v:
       ed=v['body_candidate'];eds=[('existing_alternative_body_candidate',ed['ciphertext'],string_raw(ed.get('reading',ed.get('raw'))))]
      if rid=='p192_B':
       ed=v['repaired'];eds=[('existing_alternative_repaired',ed['ciphertext'],string_raw(ed.get('reading',ed.get('raw'))))]
      add(rid,source,mapping,string_raw(v.get('raw',v.get('unfilled_model'))),eds,
          {'certificate':cp,'certificate_sha256':sha(cp),'retained_alternative_section':section},
          'retained_source_alternative_'+str(i))

    # Existing cross-copy editorials are assessed at their specified letters only.
    # The certificate's complete minimum-cost witnesses arbitrarily fill unresolved
    # letters and are not promoted to source readings here.
    cp='data/certificates/p197_p198_transport.json';d=read(cp)
    composite_checks=[]
    for name,ids in [('equipment_for_darmstadt',['p197_C','p198_B']),('lorry_and_petrol_pump',['p197_D','p198_E'])]:
     ed=d['editorial_readings'][name];target=ed['normalized_editorial_target'];cost=ed['combined_coordinate_cost'];repairs=[]
     for rid in ids:
      rr=next(r for r in records if r['id']==rid and r['variant']=='primary')
      for hit in rr['native_target_pairs']:
       j=hit['plaintext_index'];label=target[j]
       if label=='?':continue
       cell=base.index(label);required=CO[cell//6]+CO[cell%6]
       per=next(p for p in ed['per_letter_support'] if p['plaintext_index']==j)
       assert per['plaintext_index']==j and per['editorial_character']==label
       changes=[{'source_index':si,'before':a,'after':b} for si,a,b in zip(hit['source_indices'],hit['pair'],required) if a!=b]
       repairs.append({'id':rid,'plaintext_index':j,'native_pair':hit['pair'],'native_conditional_label':hit['after'],'existing_editorial_label':label,'existing_editorial_pair':required,'existing_observed_substitutions':changes,'per_letter_support':per})
     composite_checks.append({'name':name,'source_ids':ids,'native_target_pair_consequences':repairs,
      'existing_combined_unconstrained_minimum':cost['unconstrained_attainable_minimum'],
      'existing_combined_specified_editorial_cost':cost['editorial_cost_at_specified_positions'],
      'existing_combined_complete_attainment_cost':cost['attainable_minimum_with_specified_editorial_letters'],
      'limits':'No source edit or new reconstruction is made. The existing composite costs and unresolved positions remain unchanged.'})

    primary=[r for r in records if r['variant']=='primary']
    assert len({r['id'] for r in primary})==len(primary)
    assert not unsupported and not excluded
    assert all(any(e['id']==r['id'] for e in entries) for r in primary)
    native_hits=[(r,p) for r in primary for p in r['native_target_pairs']]
    categories={
     'already_in_conditional_gain_layer':[(r,p) for r,p in native_hits if r['previously_in_gain_layer']],
     'previously_recorded_quantity_conflict':[(r,p) for r,p in native_hits if r['previously_conflict']],
     'new_unedited_reference_labels':[(r,p) for r,p in native_hits if r['id']=='p186_A2'],
     'other_native_corruption_or_earlier_editorial_repair':[(r,p) for r,p in native_hits if not r['previously_in_gain_layer'] and not r['previously_conflict'] and r['id']!='p186_A2'],
    }
    summary={'distinct_source_reviewed_physical_sources':len(primary),'audited_primary_and_retained_source_frames':len(records),'native_target_pairs_in_primary_frames':len(native_hits),'physical_sources_with_native_target_pairs':len({r['id'] for r,p in native_hits}),
     'category_counts':{k:{'sources':len({r['id'] for r,p in v}),'pairs':len(v)} for k,v in categories.items()},
     'physical_sources_without_native_target_pairs':len([r for r in primary if not r['native_target_pairs']]),
     'raw_fixed_total_before':sum(r['fixed_raw_before'] for r in primary),'raw_fixed_total_after':sum(r['fixed_raw_after'] for r in primary),
     'new_source_edits':0,'new_source_mask_fills':0,'new_geometry_searches':0,'new_square_values':0}
    assert summary['native_target_pairs_in_primary_frames']==30 and summary['distinct_source_reviewed_physical_sources']==54
    assert sum(len(v) for v in categories.values())==len(native_hits)

    assert sorted(r['id'] for r in primary) == data['source_ids']
    assert summary['category_counts'] == data['expected_primary_occurrence_categories']
    assert len(records) == 71
    for r in records:
        native = ''.join('?' if i is None else clean(r['literal_source'][i])
                         for i in r['model_to_source_indices'])
        _, ps = inverse(native, base, ranks)
        assert len(native) % 2 == 0
        intermediate = ''.join(native[i] for p in ps for i in p['model_indices'])
        assert transpose(intermediate, ranks) == native

    # A catalogue evidence file may contain other keys in the same package.
    # Account for every such source explicitly instead of accepting a text match.
    cross_key = []
    covered_ids = set(data['source_ids'])
    for entry in entries:
        if entry['id'] in covered_ids:
            continue
        refs = [p for p in entry.get('evidence', [])
                if (ROOT / p).is_file() and (ROOT / p).suffix in ('.json', '.md', '.py')
                and 'Nov13-15b' in (ROOT / p).read_text()]
        if not refs:
            continue
        actual_keys = set()
        for path in entry.get('evidence', []):
            if not path.endswith('.json'):
                continue
            evidence = read(path)
            if not isinstance(evidence, dict):
                continue
            for row in evidence.get('records', [evidence.get('record')]):
                if isinstance(row, dict) and row.get('id') == entry['id']:
                    key_id = row.get('key_id', evidence.get('key_id', evidence.get('key', {}).get('id')))
                    if key_id:
                        actual_keys.add(key_id)
        assert actual_keys and 'Nov13-15b' not in actual_keys, (entry['id'], actual_keys)
        cross_key.append({'id': entry['id'], 'audited_key_ids': sorted(actual_keys)})

    native_occurrences = []
    for category, items in categories.items():
        for row, hit in items:
            prior_repairs = []
            for edition in row['editions']:
                prior_repairs.extend(x for x in edition['native_target_pairs_changed_in_edition']
                                     if x['plaintext_index'] == hit['plaintext_index'])
            for composite in composite_checks:
                prior_repairs.extend(x for x in composite['native_target_pair_consequences']
                                     if x['id'] == row['id'] and x['plaintext_index'] == hit['plaintext_index'])
            native_occurrences.append({'id': row['id'], 'category': category, **hit,
                                       'existing_editorial_repairs': prior_repairs})

    inventory = []
    for row in sorted(primary, key=lambda r: r['id']):
        inventory.append({
            'id': row['id'], 'source_evidence': row['provenance'],
            'source_slots': row['source_slots'], 'primary_model_slots': row['model_slots'],
            'plaintext_positions': row['positions'],
            'raw_fixed_before': row['fixed_raw_before'], 'raw_fixed_after': row['fixed_raw_after'],
            'native_target_pair_count': len(row['native_target_pairs']),
            'audited_source_views': sum(r['id'] == row['id'] for r in records),
            'previous_editorial_layers': [{
                'name': e['name'], 'fixed_before': e['fixed_before'], 'fixed_after': e['fixed_after'],
                'observed_coordinate_substitutions': len(e['observed_substitutions']),
                'mask_or_added_coordinate_fills': len(e['mask_or_added_fills']),
                'newly_fixed_labels_under_shared_square': [
                    {'plaintext_index': g['plaintext_index'], 'pair': g['pair'],
                     'native_pair': g['native_pair'], 'label': g['symbol']}
                    for g in e['gains']],
            } for e in row['editions']],
        })
    retained = [{
        'id': r['id'], 'view': r['variant'],
        'source_evidence': r['provenance']['certificate'],
        'source_map_sha256': hashlib.sha256(json.dumps(r['model_to_source_indices'], separators=(',', ':')).encode()).hexdigest(),
        'raw_before': r['raw_before'], 'raw_after': r['raw_after'],
        'fixed_before': r['fixed_raw_before'], 'fixed_after': r['fixed_raw_after'],
        'native_target_pairs': r['native_target_pairs'],
    } for r in records if r['variant'] != 'primary']

    # The two new labels are native VG pairs in the conservative source layer.
    spec = data['p186_A2']
    row = next(r for r in primary if r['id'] == 'p186_A2')
    source_record = next(r for r in read(spec['record']) if r['id'] == 'p186_A2')
    assert row['literal_source'] == source_record[spec['source_layer']]
    assert row['model_to_source_indices'] == list(range(174))
    assert row['raw_after'] == spec['expected_interpretation']
    assert [i for i, c in enumerate(row['literal_source']) if c not in CO] == spec['preserved_conservative_source_masks']
    gains = [{'plaintext_index': p['plaintext_index'], 'pair': p['pair'],
              'source_indices': p['source_indices'], 'symbol': p['after']}
             for p in row['native_target_pairs']]
    assert gains == spec['gains']
    assert (row['fixed_raw_before'], row['fixed_raw_after'], row['positions']) == (80, 82, 87)
    _, ps = inverse(row['literal_source'], joint, ranks)
    cells = [i for i, c in enumerate(joint) if c == '?']
    labels = sorted(ALPH - set(joint))
    witness_ciphertext = clean(row['literal_source']).replace('?', 'A')
    completed_squares = 0
    for values in itertools.permutations(labels):
        full = list(joint)
        for i, value in zip(cells, values):
            full[i] = value
        square = ''.join(full)
        plaintext, _ = inverse(witness_ciphertext, square, ranks)
        assert all(a == '?' or a == b for a, b in zip(row['raw_after'], plaintext))
        assert all(c in p['domain'] for c, p in zip(plaintext, ps))
        assert encrypt(plaintext, square, ranks) == witness_ciphertext
        completed_squares += 1
    assert completed_squares == 720
    for text in spec['case_fields']:
        assert text in (ROOT / spec['case']).read_text(), text

    return {
        'schema': 'adfgvx-nov13-complete-coverage-v1', 'authors': data['authors'],
        'input_sha256': sha('experiments/nov13_joint_completion/coverage_inputs.json'),
        'indexing': 'Zero-based plaintext and source positions.',
        'scope': data['scope'], 'published_square': base, 'conditional_square': joint,
        'summary': summary, 'source_inventory': inventory,
        'all_primary_native_occurrences': sorted(native_occurrences, key=lambda x: (x['id'], x['plaintext_index'])),
        'retained_source_alternatives': retained,
        'existing_composite_consequences': composite_checks,
        'same_package_cross_key_sources_excluded': sorted(cross_key, key=lambda x: x['id']),
        'p186_A2_extension': {
            'source_layer': spec['source_layer'], 'source_slots': 174,
            'published_key_reading': row['raw_before'], 'conditional_reading': row['raw_after'],
            'plaintext_positions': 87, 'fixed_before': 80, 'fixed_after': 82,
            'new_native_pair_labels': gains, 'additional_observed_substitutions': [],
            'additional_mask_fills': [], 'preserved_source_masks': [20, 29],
            'remaining_domains': [p for p in ps if len(p['domain']) > 1],
            'remaining_full_square_completions_checked': completed_squares,
            'coordinate_witness_scope': 'Every remaining square completion has an exact forward/inverse witness using arbitrary A for the two masked source coordinates. Those fills and unused square values are not readings.',
            'visual_review': spec['visual_review'],
        },
        'source_coordinate_roundtrip_views_checked': len(records),
        'limits': data['limits'],
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'coverage_certificate.json'
    if args.verify:
        assert json.loads(path.read_text()) == result
    else:
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('Nov13 coverage: 54 physical sources, 71 existing views, 30 native pairs = 14 earlier + 1 known conflict + 2 new p186 labels + 13 other adverse occurrences; p186 A2 80 -> 82/87 with no edits.')

if __name__ == '__main__':
    main()
