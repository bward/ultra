#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import string
from config import _alph, _alph_indexes, _alph_length
from metacipher import Metacipher

class Affine(Metacipher):
    title = 'Affine'
    caption = '&Affine'
    solve = True
    
    def ask_for_key(self, key = '1,1'):
        if self._display == None:
            return None
        if not key:
            key = '1,1'
        rvalues, tvalues = self._display.key_dialog(radioboxes = [['Decrypt', 'Encrypt']], textboxes = [('a', key.split(',')[0]), ('b', key.split(',')[1])], title = self.title + ' key')
        key = self.sanitize_key(tvalues)
        encryption = (rvalues[0] == 1)
        return key, encryption
        
    def sanitize_key(self, key):
        global _alph_length
        if key == None:
            return None
        try:
            sanitized_key = [int(value) for value in key]
        except ValueError:
            self._display.error_dialog('Bad keys, must be int()-able')
            return None
        a = sanitized_key[0]
        b = _alph_length
        
        if not self.is_coprime(sanitized_key[0], _alph_length):
            self._display.error_dialog('Bad keys, a must be coprime to alphabet length')
            return None
        return sanitized_key

    def crack_key(self = None, in_str = ''):
        global _alph_length
        import frequencies
        freq = frequencies.Frequencies(self._display, independent = False)
        percentages, counts, exp_percentages = freq.run(in_str, title = self.title)
        min_score = None
        min_a = 0
        min_b = 0
        for a in range(_alph_length):
            if self.is_coprime(a, _alph_length):
                for b in range(_alph_length):
                    score = 0
                    for i in range(_alph_length):
                        diff_sq = (exp_percentages[i] - percentages[(i * a + b) % _alph_length]) ** 2
                        score += diff_sq
                    if score < min_score or min_score == None:
                        min_score = score
                        min_a = a
                        min_b = b
        return str(min_a) + ',' + str(min_b)
                    
            

    def decrypt(self = None, key = (1,1), in_str = ''):
        global _alph_length
        inverse = self.mod_mult_inv(key[0], _alph_length)
        key[0], key[1] = inverse, -1 * key[1] * inverse
        out_str = self.encrypt(key, in_str)
        return out_str
        
    def encrypt(self = None, key = (1,1), in_str = ''):
        global _alph, _alph_indexes, _alph_length
        out_str = ''
        for old_char in in_str:
            if old_char in _alph[0]:
                old_index = _alph_indexes[0][old_char]
                new_index = (key[0] * old_index + key[1]) % _alph_length
                new_char = _alph[0][new_index]
                out_str += new_char
            elif old_char in _alph[1]:
                old_index = _alph_indexes[1][old_char]
                new_index = (key[0] * old_index + key[1]) % _alph_length
                new_char = _alph[1][new_index]
                out_str += new_char
            else:
                out_str += old_char
        
        return out_str
    
    def mod_mult_inv(self, a, m):
        a %= m
        for x in range(1, m):
            if a * x % m == 1:
                return x
        return None
        
    def is_coprime(self, a, b):
        while b: a,b = b, a%b
        return a == 1
            
