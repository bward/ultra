# Lots of juicy text operations. We've even got a base class for overloading.

import text
import string
import churn
from metacipher import Metacipher
from config import _alph, _alph_indexes, _alph_length
import cPickle as pickle
import vigenere

def textops(display):
    textops = [
        Clean(display),
        Lines(display),
        Spaces(display),
        Rotate(display),
        Upper(display),
        Quickspace(display),
        Slowspace(display),
        #Solitaire(display)
    ]
    return textops

class Metatext(Metacipher):
    title = 'Metatext'
    caption = '&Metatext'
    key = ''
    
    def menus(self):
        self._display.add_menu_item(menu = '&Text Operations', caption = self.caption, function = self._menu_callback)    
    
    def _menu_callback(self):
        self.run()
        
    def run(self):
        if self._display == None:
            return None
        self._in = self._display.get_input()
        key = self.key
        self._key_raw = self.ask_for_key(str(key))
        if None == self._key_raw:
            return
        self._out = self._perform(self._key_raw, self._in)
        self._display.show_output(self._out)
    
    def ask_for_key(self, key = ''):
        if self._display == None:
            return None
        rvalues, tvalues = self._display.key_dialog(textboxes = [(self.title + ' parameter', key)], title = self.title + ' parameter')
        key = self.sanitize_key(tvalues[0])
        return key
    
    def _perform(self, key_raw, in_str):
        return in_str

"""class Solitaire(Metatext):
    title = 'Solitaire'
    caption = '&Solitaire'
    key = ''
    
    def __perform(self, key, in_str):
        nulls = [2, 3, 5, 9, 15, 16, 19, 40, 47, 50, 1]
        for null in nulls:
            for null2 in nulls:
                str11 = key.replace('-11', str(null))
                str13 = str11.replace('-13', str(null2))
                out, limit, stream = self.__perform(str13, in_str)
                negs = []
                for c in stream:
                    if int(c) <= 0:
                        negs.append(c)
                printstr = out[0:limit] + ' ' + ','.join([str(c) for c in negs]) + ' ' + str(null) + ',' + str(null2)
                print printstr
        return out
    
    def _perform(self, key, in_str):
        length = 50
        order = key.split(',')
        key_stream = []
        break_index = 0
        for keystream_index in range(length):
            # Move first joker down by 1 (Step 2)
            joker1pos = order.index('53')
            if joker1pos == 53:
                order = [order[0]] + [order[joker1pos]] + order[1:-1]
            else:
                order = order[0:joker1pos] + [order[joker1pos + 1]] + [order[joker1pos]] + order[joker1pos + 2:]
            # Move second joker down by 2 (Step 3)
            joker2pos = order.index('54')
            if joker2pos == 52:
                order = [order[0]] + [order[joker2pos]] + order[1:-2] + [order[-1]]
            elif joker2pos == 53:
                order = order[0:2] + [order[joker2pos]] + order[2:-1]
            else:
                order = order[0:joker2pos] + order[joker2pos + 1: joker2pos + 3] + [order[joker2pos]] + order[joker2pos + 3:]
            # Cut by jokers (Step 4)
            jokers = [order.index('53'), order.index('54')]
            jokers.sort()
            cuts = [[], [], []]
            for i in range(len(order)):
                if i < jokers[0]:
                    cuts[0].append(order[i])
                elif i >= jokers[0] and i <= jokers[1]:
                    cuts[1].append(order[i])
                elif i > jokers[1]:
                    cuts[2].append(order[i])
            # Flip cuts
            cuts.reverse()
            order = cuts[0] + cuts[1] + cuts[2]
            # Step 5
            real_bottom = int(order[-1])
            if real_bottom == 54:
                bottom = 53
            elif real_bottom <= 0:
                break_index = keystream_index
                print 'Hit 0 on bottom in step 5 at value ' + str(real_bottom)
                print ','.join(order)
                break
            else:
                bottom = real_bottom
            order = order[bottom:-1] + order[0:bottom] + [order[-1]]
            # Step 6
            temp_out = ''
            for c in order:
                temp_out += c + ','
            #print temp_out
            top = int(order[0])
            if top == 54:
                top = 53
            key_char = int(order[top])
            if not (key_char in (53, 54)):
                key_stream.append(key_char)
        global _alph
        key_stream_str = ''
        for c in key_stream:
            key_stream_str += _alph[0][c % 26]
        print key_stream
        print key_stream_str
        
        v = vigenere.Vigenere(independent = False)
        #return (v.decrypt(key_stream_str, self._display.get_input()), break_index, key_stream)
        return v.decrypt(key_stream_str, self._display.get_input())"""

class Clean(Metatext):
    title = 'Clean text'
    caption = '&Clean text'
    key = _alph[0] + _alph[1]
    
    def _perform(self, key, in_str):
        out = text.clean(in_str, key, one_case = False)
        return out
        
class Upper(Metatext):
    title = 'Upper case'
    caption = '&Upper case'
    def _perform(self, key, in_str):
		out = in_str.upper()
		return out
		
    def ask_for_key(self, key = ''):
        return ''
    
class Lines(Metatext):
    title = 'Line break'
    caption = '&Insert line breaks'
    key = '10'
    
    def _perform(self, key, in_str):
        out = ''
        key = int(key)
        length = len(in_str)
        for i in range(length):
            if i % key == 0 and not i == 0:
                out += "\n"
            out += in_str[i]
        return out

class Spaces(Metatext):
    title = 'Space'
    caption = '&Insert spaces'
    key = '10'
    
    def _perform(self, key, in_str):
        global _alph
        out = ''
        key = int(key)
        length = len(in_str)
        for i in range(length):
            if i % key == 0 and not i == 0:
                out += ' '
            out += in_str[i]
        return out

class Rotate(Metatext):
    title = 'Read down'
    caption = '&Read text down columns'
    key = ''
    
    def _perform(self, key, in_str):
        lines = in_str.splitlines()
        lengths = [len(l) for l in lines]
        across = max(lengths)
        down = len(lines)
        out = [''] * across
        for i in range(across):
            for j in range(down):
                try:
                    out[i] += lines[j][i]
                except IndexError:
                    out[i] += ' '
        return "\n".join(out)
    
    def ask_for_key(self, key = ''):
        return ''

class Quickspace(Metatext):
    title = 'Heuristic spacing'
    caption = 'Quickly guess English words'
    key = 4000
    
    _digraphs = None
    
    def __init__(self, display = None, independent = True):
        Metatext.__init__(self, display = display, independent = independent)
        self._digraph_file_open()
    
    def _digraph_file_open(self):
        with open('cipher/word_boundaries.pickle', 'r') as counts:
            self._digraphs = pickle.load(counts)
        
    def get_digraph_score(self, digraph):
        global _alph_indexes, _alph
        fi = _alph_indexes[0][digraph[0]]
        se = _alph_indexes[0][digraph[1]]
        score = self._digraphs[fi][se]
        return score
    
    def _perform(self, key, in_str):
        words = ['']
        key = int(key)
        for i in range(len(in_str)):
            if len(words[-1]) == 0:
                words[-1] += in_str[i]
            else:
                digraph = words[-1][-1] + in_str[i]
                score = self.get_digraph_score(digraph.upper())
                if score > key:
                    words.append(in_str[i])
                else:
                    words[-1] += in_str[i]
        return ' '.join(words)

import time
    
class Slowspace(Metatext):
    title = 'Heuristic spacing'
    caption = 'Slowly guess English words'
    key = 10
    
    _dictionary = None
    
    def __init__(self, display = None, independent = True):
        Metatext.__init__(self, display = display, independent = independent)
        self._dict_file_open()
    
    def _dict_file_open(self):
        with open('cipher/cracklib-small', 'r') as dict_file:
            dictionary = dict_file.readlines()
        self._dictionary = dictionary
    
    def _perform(self, key, in_str):
        key = int(key)
        words = []
        end = False
        i = 0
        while not i > len(in_str):
            found = False
            offset = key
            while not found:
                word = in_str[i:i + offset]
                if word.lower() + "\n" in self._dictionary:
                    found = True
                offset -= 1
                if offset == 0:
                    offset = key
                    word = in_str[i:i + offset + 1]
                    found = True
            words.append(word)
            i += offset + 1
        return ' '.join(words)
            



















