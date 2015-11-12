#!/usr/bin/python

from config import _alph

def clean(in_str, valid = _alph[0] + _alph[1], one_case = True):
    out_str = ''
    for char in in_str:
        if char in valid:
            out_str += char
    if one_case:
        return out_str.upper()
    else:
        return out_str

def pad_key(in_str, alphabet = _alph[0]):
    in_str = clean(in_str)
    key = ''
    for c in in_str + alphabet:
        if not c in key and c in alphabet:
            key += c
    return key
