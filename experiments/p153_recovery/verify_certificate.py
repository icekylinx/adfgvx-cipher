"""Verify the p153 arithmetic and every explicitly distinguished evidence layer."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
SYMBOLS = 'ADFGVX'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def order(length,ranks):
    assert sorted(ranks) == list(range(1,len(ranks)+1))
    return [index for column in sorted(range(len(ranks)),key=ranks.__getitem__)
            for index in range(column,length,len(ranks))]


def interim(ciphertext,ranks):
    assert len(ciphertext)%2 == 0 and set(ciphertext) <= set(SYMBOLS+'?')
    result=['']*len(ciphertext)
    for char,index in zip(ciphertext,order(len(ciphertext),ranks)):
        result[index]=char
    return ''.join(result)


def decode(ciphertext,ranks,square):
    known=[char for char in square if char!='?']
    assert len(square)==36 and len(set(known))==len(known)
    text=interim(ciphertext,ranks)
    return ''.join('?' if '?' in text[i:i+2] else square[
        6*SYMBOLS.index(text[i])+SYMBOLS.index(text[i+1])]
        for i in range(0,len(text),2))


def encode(text,ranks,square):
    coordinates=''.join('??' if char=='?' else SYMBOLS[square.index(char)//6]+SYMBOLS[square.index(char)%6]
                        for char in text)
    return ''.join(coordinates[index] for index in order(len(coordinates),ranks))


def main():
    record=json.loads((ROOT.parent.parent/'data/certificates/p153.json').read_text())
    ciphertexts,ranks=record['ciphertexts'],record['ranks']
    square,partial=record['raw_search_square'],record['core_partial_square']
    assert sorted(square)==sorted(ALPHABET)
    assert sum(char!='?' for char in partial)==19
    assert [hashlib.sha256(ct.encode()).hexdigest() for ct in ciphertexts]==record['ciphertext_sha256']
    assert [decode(ct,ranks,square) for ct in ciphertexts]==record['raw_search_decodes']
    assert [decode(ct,ranks,partial) for ct in ciphertexts]==record['core_decodes']
    raw_roundtrip=[]
    for index,ct in enumerate(ciphertexts):
        regenerated=encode(record['raw_search_decodes'][index],ranks,square)
        comparable=[i for i,(a,b) in enumerate(zip(ct,regenerated)) if a!='?' and b!='?']
        assert all(ct[i]==regenerated[i] for i in comparable)
        # Every surviving half-coordinate is explicitly retained in the interim map.
        text=interim(ct,ranks)
        indices=order(len(ct),ranks)
        reverse={target:source for source,target in enumerate(indices)}
        for position,row in enumerate(record['source_coordinate_maps'][index]):
            assert row['received_coordinate_positions']==[reverse[2*position],reverse[2*position+1]]
            assert row['received_digraph']==text[2*position:2*position+2]
            for source,target in zip(row['received_coordinate_positions'],[2*position,2*position+1]):
                assert ct[source]==text[target]
        raw_roundtrip.append(dict(received_coordinates=len(ct),known_coordinates=sum(c!='?' for c in ct),
                                  fully_observed_digraph_coordinates_checked=len(comparable),
                                  surviving_half_coordinates_preserved_by_map=True))
    for span in record['clear_spans_part5']:
        assert record['core_decodes'][0][span['start']:span['end_exclusive']]==span['text']
    body=record['part6_body_hypothesis']
    expected=encode(body['text']+'?'*12,ranks,partial)
    assert expected==body['constrained_received_stream']
    differences=[dict(received_position=i,printed=a,body_requires=b)
                 for i,(a,b) in enumerate(zip(ciphertexts[1],expected))
                 if a!='?' and b!='?' and a!=b]
    fills=[dict(received_position=i,proposed_coordinate=b)
           for i,(a,b) in enumerate(zip(ciphertexts[1],expected)) if a=='?' and b!='?']
    assert differences==body['printed_coordinate_disagreements']
    assert fills==body['inferred_erased_coordinates']
    assert [row['received_position'] for row in differences]==[3,4]
    assert len(fills)==12
    constrained=sum(a!='?' and b!='?' for a,b in zip(ciphertexts[1],expected))
    assert constrained==72
    assert constrained-len(differences)==70
    assert len({row['square_cell'] for row in record['numeral_cells']})==4
    assert all(row['assigned_plaintext'] is None for row in record['numeral_cells'])
    result=dict(schema='adfgvx-p153-certificate-verification-v1',passed=True,
                source_coordinates_changed=0,raw_layers=raw_roundtrip,
                core_square_cells=19,core_letter_positions=record['core_letter_positions'],
                body_erasure_completions_checked=12,body_observed_coordinate_disagreements=[3,4],
                unresolved_numeral_cells=4,
                scope='Arithmetic/source consistency; not proof of historical authenticity or of the proposed two-coordinate emendation.')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
