#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# This is a fairly simple monoalphabetic substitution cipher. It does some funky shit with the Churn algorithm at the end which is cool.

import churn
import text
from random import randrange
from config import _alph, _alph_indexes, _alph_length
from metacipher import Metacipher
import frequencies

class Monoalphabetic(Metacipher):
    title = 'Monoalphabetic'
    caption = '&Monoalphabetic'
    solve = True
    
    def encrypt(self = None, key = '', in_str = ''):
        global _alph
        _key = (key.upper(), key.lower())
        _key_indexes = tuple([dict([(value, index) for (index, value) in enumerate(keystr)]) for keystr in _key])
        out_str = ''
        for in_char in in_str:
            in_upp = in_char in _alph[0]
            in_low = in_char in _alph[1]
            
            if in_upp or in_low:
                if in_upp:
                    out_str += _key[0][_alph_indexes[0][in_char]]
                elif in_low:
                    out_str += _key[1][_alph_indexes[1][in_char]]
            else:
                out_str += in_char
        return out_str
    
    def decrypt(self = None, key = '', in_str = ''):
        global _alph
        _key = (key.upper(), key.lower())
        _key_indexes = tuple([dict([(value, index) for (index, value) in enumerate(keystr)]) for keystr in _key])
        out_str = ''
        for in_char in in_str:
            in_upp = in_char in _alph[0]
            in_low = in_char in _alph[1]
            
            if in_upp or in_low:
                if in_upp:
                    out_str += _alph[0][_key_indexes[0][in_char]]
                elif in_low:
                    out_str += _alph[1][_key_indexes[1][in_char]]
            else:
                out_str += in_char
        return out_str
    
    # So it turns out trying to run the Hungarian algorithm to break a monoalphabetic substitution cipher is a fucking stupid idea. Let's stick to Churn :)
    def crack_key(self = None, in_str = ''):
        thread = ChurnMonoalphThread(self, self._display, in_str)
        thread.start()
        self._display.churn_dialog()
        final_key = thread.stop()
        return final_key
    
    def sanitize_key(self, key):
        global _alph_length, _alph
        if key == None:
            return None
        else:
            key = key.upper()
            key = text.clean(key, _alph[0])
            key_charpool = key + _alph[0]
            key = ''
            i = 0
            while len(key) != _alph_length:
                if key_charpool[i] not in key:
                    key += key_charpool[i]
                i += 1
        return key
    

class ChurnMonoalphThread(churn.ChurnThread):
    
    def churn_key(self, old_key):
        if old_key == None:
            letter_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
            f = frequencies.Frequencies(None, independent=False)
            counts = f.counts(self.in_str)
            sorted_alph = ''.join(pair[1] for pair in sorted(zip(counts, _alph[0]), reverse=True))
            key = ''.join([sorted_alph[letter_order.index(_alph[0][i])] for i in range(_alph_length)])
            return key
    
        else:
            new_key = old_key
            p = new_key[randrange(26)]
            q = new_key[randrange(26)]
            new_key = new_key.replace(p, '1')
            new_key = new_key.replace(q, '2')
            new_key = new_key.replace('1', q)
            new_key = new_key.replace('2', p)
            return new_key
        
        

