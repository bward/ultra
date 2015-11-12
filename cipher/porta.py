#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import autocorrelation
import maths
import frequencies
from config import _alph, _alph_indexes, _alph_length
from metacipher import Metacipher

class Porta(Metacipher):
    title = 'Porta'
    caption = 'Porta'
    solve = True
    
    def ask_for_key(self, key = ''):
        if self._display == None:
            return None
        rvalues, tvalues = self._display.key_dialog(textboxes = [('Porta key', key)], title = 'Porta key')
        if [None] in tvalues:
            return None
        key = tvalues[0]
        return key, True
    
    def sanitize_key(self, key):
        global _alph
        sanitized_key = ''
        for key_char in key:
            if key_char in _alph[0] + _alph[1]:
                sanitized_key += key_char
        if key == '':
            sanitized_key = None
        
        return sanitized_key
    
    def encrypt(self, key = '', in_str = ''):
        return self.crypt(key, in_str)
        
    def decrypt(self, key = '', in_str = ''):
        return self.crypt(key, in_str)
        
    def crypt(self = None, key = '', in_str = ''):
        global _alph, _alph_indexes, _alph_length
        out_str = ''
        key = key.upper()
        key_i = 0
        for in_char in in_str:
            
            in_upp = in_char in _alph[0]
            in_low = in_char in _alph[1]
            
            if in_upp or in_low:
                key_char = key[key_i]
                key_index = _alph_indexes[0][key_char]/2
                
                if in_upp:
                    old_index = _alph_indexes[0][in_char]
                elif in_low:
                    old_index = _alph_indexes[1][in_char]
                
                #indexes = range(_alph_length/2, _alph_length)[key_index:] + range(_alph_length/2, _alph_length)[:key_index]
                if key_index == 0:
                    indexes = range(_alph_length/2, _alph_length)
                else:
                    indexes = range(_alph_length/2, _alph_length)[::-1][:key_index][::-1] + range(_alph_length/2, _alph_length)[:-key_index]
                
                if old_index < _alph_length/2:
                    new_index = indexes[old_index]
                else:
                    new_index = indexes.index(old_index)
                
                if in_upp:
                    out_char = _alph[0][new_index]
                elif in_low:
                    out_char = _alph[1][new_index]
                
                key_i = (key_i + 1) % len(key)
                out_str += out_char
            
            else:
                out_str += in_char
        return out_str
        
    def crack_key(self, in_str):
        global _alph, _alph_length
        ac = autocorrelation.AutoCorrelation(self._display, independent = False)
        data = ac.run(in_str, title = self.title)
        limit = max(data)
        key_length = -1
        out_key = ''
        done = False
        
        while not done:
            counts = 0
            first_index = -1
            values = []
            for i, count in enumerate(data):
                if count >= limit:
                    counts += 1
                    values.append(i)
            if counts >= (100/12):
                a, b = maths.closest_pair(values)
                key_length = maths.euclid(a, b)
                done = True
                break
            limit -= 1
            
        slices = [''] * key_length
        char_index = 0
        for char in in_str:
            if char in _alph[0] + _alph[1]:
                slices[char_index % key_length] += char
                char_index += 1

        freq = frequencies.Frequencies(self._display, independent = False)

        
        for slice in slices:
            min_i = 0
            min_score = None
            
            for i in range(_alph_length/2):
                score = 0
                decrypted = self.crypt(in_str = slice, key=_alph[0][i*2])
                percentages, counts, exp_percentages = freq.run(decrypted, title = self.title)

                for j in range(_alph_length):
                    diff_sq = (exp_percentages[j] - percentages[j]) ** 2
                    score += diff_sq
                    
                if score < min_score or min_score == None:
                    min_score = score
                    min_i = i
                    
            out_key += _alph[0][min_i*2]
            
        return out_key

                
        
