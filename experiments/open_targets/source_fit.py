#!/usr/bin/env python3
"""Global injective-square feasibility for a proposed full plaintext.

ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
A positionwise union of unknown cells is weaker than this joint check: every
occurrence of a plaintext character must use the same cell, and all36 symbols
must occupy distinct cells. Used for planted-control evaluation only.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from adfgvx.cipher import ALPHABET,SYMBOLS,encrypt,untranspose


def complete_square_for_plaintext(ciphertext,ranks,partial,plaintext):
    assert len(ciphertext)==2*len(plaintext) and len(partial)==36
    assert set(plaintext)<=set(ALPHABET)
    unused={i for i,ch in enumerate(partial) if ch=='?'}
    allowed={ch:({partial.index(ch)} if ch in partial else set(unused)) for ch in ALPHABET}
    stream=untranspose(ciphertext,ranks)
    for ch,a,b in zip(plaintext,stream[::2],stream[1::2]):
        allowed[ch]&={cell for cell in range(36) if (a=='?' or a==SYMBOLS[cell//6]) and (b=='?' or b==SYMBOLS[cell%6])}
    empty=[ch for ch in ALPHABET if not allowed[ch]]
    if empty:return dict(compatible=False,empty_character_domains=empty)
    owners={}
    def augment(ch,seen):
        for cell in sorted(allowed[ch]):
            if cell in seen:continue
            seen.add(cell)
            if cell not in owners or augment(owners[cell],seen):
                owners[cell]=ch;return True
        return False
    for ch in sorted(ALPHABET,key=lambda ch:len(allowed[ch])):
        if not augment(ch,set()):return dict(compatible=False,empty_character_domains=[],reason='No injective matching of plaintext symbols to their permitted square cells')
    square=''.join(owners[i]for i in range(36))
    assert all(a=='?' or a==b for a,b in zip(partial,square))
    generated=encrypt(plaintext,ranks,square)
    assert all(a=='?' or a==b for a,b in zip(ciphertext,generated))
    return dict(compatible=True,completion_witness=square)
