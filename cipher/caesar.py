#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# A Caesar cipher is where every letter is shifted n places down the alphabet.
# It can be broken easily by analysing the frequency of occurrence of letters in the ciphertext, and attempting to match those frequencies with frequencies of standard English.

import string
from config import _alph, _alph_indexes, _alph_length
from metacipher import Metacipher

class Caesar(Metacipher):
    title = 'Caesar'
    caption = '&Caesar'
    solve = True
    
    def sanitize_key(self, key):
        global _alph_length
        if key == None:
            return None
        try:
            sanitized_key = int(key) % _alph_length
        except ValueError:
            self._display.error_dialog('Bad key, must be int()-able')
            return None
        return sanitized_key

    def crack_key(self = None, in_str = ''):
        import frequencies as freq_an
        global _alph_length
        # Count the frequencies
        frequencies = freq_an.Frequencies(self._display, independent = False)
        percentages, counts, exp_percentages = frequencies.run(in_str, title = self.title)
        if (not self == None) and self._independent == True:
            frequencies.graph()
        # This is quite a cool algorithm I reinvented which turned out to be a simplified chi-squared test for goodness of fit.
        # If we shift the frequencies down the alphabet 26 times, the one which fits best with standard English is most likely to be the key.
        # Goodness of fit is calculated by sum((O-E)^2). Minimum wins.
        min_score = None
        min_i = 0
        for i in range(_alph_length):
            score = 0
            for j in range(_alph_length):
                diff_sq = (exp_percentages[j] - percentages[(i + j) % _alph_length]) ** 2
                score += diff_sq
            if score < min_score or min_score == None:
                min_score = score
                min_i = i
        return min_i

    def decrypt(self = None, key = 0, in_str = ''):
        # Decrypt algorithm
        out_str = self.encrypt(-1 * key, in_str)
        return out_str
        
    def encrypt(self = None, key = 0, in_str = ''):
        global _alph, _alph_indexes, _alph_length
        
        # Encrypt algorithm
        out_str = ''
        for old_char in in_str:
            if old_char in _alph[0]:
                old_index = _alph_indexes[0][old_char]
                new_index = (old_index + key) % _alph_length
                new_char = _alph[0][new_index]
                out_str += new_char
            elif old_char in _alph[1]:
                old_index = _alph_indexes[1][old_char]
                new_index = (old_index + key) % _alph_length
                new_char = _alph[1][new_index]
                out_str += new_char
            else:
                out_str += old_char
        
        return out_str

if __name__ == "__main__":
    c = Caesar(independent = False)
    ciphertext = c.encrypt(5, 'Richard Feynman (1918-88) was one of the most remarkable and gifted theoretical physicists of any generation. He was also known as the \'Great Explainer\' because of his passion for helping non-scientists to imagine something of the beauty and order of the universe as he saw it.')
    print ciphertext
    print c.decrypt(5, ciphertext)
