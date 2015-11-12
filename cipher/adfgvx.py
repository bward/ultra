from metacipher import Metacipher
import transposition
import graph as graphing
import digraphs
import frequencies
import itertools
import monoalphabetic
import churn
from random import randrange
import text
import string
#Rough'n'ready ADFGVX solver. A bit wonky around the edges, only works with caps.

class ADFGVX(Metacipher):
    title = 'ADFGVX'
    caption = 'ADFGVX'
    solve = True
        
    def ask_for_key(self, key=('','')):
        if self._display == None:
            return None
        if not key:
            key = ('','')
        rvalues, tvalues = self._display.key_dialog(radioboxes = [['Decrypt', 'Encrypt'], ['Text key', 'Numeric key']], textboxes = [('Fractionating Key', key[0]), ('Transposition Key', key[1])], title = 'ADFGVX Keys')        
        f_key, t_key = tvalues[0], tvalues[1]
        encryption = (rvalues[0] == 1)
        text_key = (rvalues[1] == 0)
        return (f_key, t_key, text_key), encryption
        
    def sanitise_key(self, keys, encrypt=True):
        if type(keys[0]) == unicode or type(keys[0]) == str:
            f_key = self.polybius_square(keys[0], reverse=not encrypt)
        elif type(keys[0]) == dict:
            f_key = keys[0]
        else:
            print 'Bad fractionation key'
        
        if keys[2]:
            t_key = [sorted(keys[1]).index(c) + 1 for c in keys[1]] #enumerate a wordy transpo key
            x=[]
            for i in range(len(t_key)):
                x.append(t_key[i])
                t_key[i] += x.count(t_key[i]) - 1
        else:
            t_key = [int(c) for c in keys[1].split(',')]
        
        return f_key, t_key
        
            
    
    def encrypt(self, key = ('','', 1), in_str = ''):
        f_key, t_key = self.sanitise_key(key)
        transpo = transposition.Transposition(self._display, independent = False)
        
        #fractionate
        out_str = ''
        for char in in_str:
            out_str += f_key[char]
         
        #transpose
        out_str = transpo.encrypt(t_key, out_str)
        
        return out_str
        
                
    def decrypt(self, key = ('', ''), in_str = ''):
        f_key, t_key = self.sanitise_key(key, encrypt=False)
        str = ''
        out_str = ''
        transpo = transposition.Transposition(self._display, independent = False)
        #transpose
        str = transpo.decrypt(t_key, in_str, 1)
        
        #fractionate
        str = [str[x:x+2] for x in range(0, len(str), 2)]

        for digraph in str:
            out_str += f_key[digraph]
        
        return out_str
        
    
    def ask_for_crack_key(self):
        if self._display == None:
            return None
        rvalues, tvalues = self._display.key_dialog(textboxes = [('Key length', '5')], title= 'ADFGVX Key Cracker')
        
        return int(tvalues[0])
        
    def dict(self):
        in_str = self._display.get_input()
        dict_location = self._display.key_dialog(textboxes=[('Dictionary location', 'cipher/dict.txt')], title = 'Dictionary location')[1][0]
        dict = [text.clean(word).upper() for word in open(dict_location).readlines()]
        transpo = transposition.Transposition(None, independent = False)
        monoalph = monoalphabetic.Monoalphabetic(None, independent = False)
        freq = frequencies.Frequencies(None, independent = False)

        best_score = 10000.0
        best_key = ''
        for word in dict:
            if len(word) > 0:
                decrypted = transpo._perform((word, 0, 1, 0, 0), in_str)
                score = freq.analyse(decrypted, graph = False)
                if score < best_score:
                    best_score = score
                    best_key = word
                if score < 10:
                     print '%s : %d : %s' % (word, score, self.decrypt((self.generate_key(decrypted), 'A', 1), decrypted)[:20])
        print 'Best key is %s' % best_key
        best_key = self._display.key_dialog(textboxes=[('Transposition key', str(best_key).strip('()'))], title = 'Transposition Key')[1][0]
        in_str = transpo._perform((best_key, 0, 1, 0, 0), in_str)
        f_key = self.generate_key(in_str)
        in_str = self.decrypt((f_key, '1', 0), in_str)
        monoalph = monoalphabetic.Monoalphabetic(self._display, independent = False)
        f_key = monoalph.crack_key(in_str)
        out_str = monoalph.decrypt(f_key, in_str)
        self._display.show_output(out_str)
        

        
        
    def crack_key(self, in_str):
        length = self.ask_for_crack_key()
        keys = itertools.permutations(range(1, length+1))
        transpo = transposition.Transposition(None, independent = False)
        scorer = churn.Churn(use_tetragraphs=True)
        freq = frequencies.Frequencies(None, independent = False)
        best_score = 100000
        best_key = []
        best_keys = []
        print 'Attempting to crack transposition key\n'
        for key in keys:
            temp = transpo.decrypt(key, in_str, 1)
            score = freq.analyse(temp, graph=False)
            if score < best_score:
                best_score = score
                best_key = key
            if score < 10:
                print str(key) + ' : ' + str(score)
                best_keys.append(key)
        
        best_score = 0
        best_key = None
        for key in best_keys:
            t_decrypted = transpo.decrypt(key, in_str, 1)
            f_key = self.generate_key(t_decrypted)
            decrypted = self.decrypt((f_key, '1', 0), t_decrypted)
            score = scorer.get_score(decrypted)
            print '%s : %s : %d' % (str(key), decrypted[:20], score)
            if score > best_score:
                best_score = score
                best_key = key                       
               
        print '\nBest key is %s\n' % str(best_key)        
        rvalues, tvalues = self._display.key_dialog(textboxes=[('Transposition key', str(best_key).strip('()'))], title = 'Transposition Key')
        t_key = [int(c) for c in tvalues[0].split(',')]
        in_str = transpo.decrypt(t_key, in_str, 1)
        
        #crack fractionation key
        print t_key
        f_key = self.generate_key(in_str)
        in_str = self.decrypt((f_key, '1', 0), in_str)
        monoalph = monoalphabetic.Monoalphabetic(self._display, independent = False)
        f_key = monoalph.crack_key(in_str)
        out_str = monoalph.decrypt(f_key, in_str)
        self._display.show_output(out_str)
        print f_key
        print t_key
        return
        


    def polybius_square(self, key, reverse = False):
        str = ''
        for char in key:
            if char not in str:
                str += char
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
            if char not in str:
                str += char
        polybius = {}
        for i, digraph in enumerate(sum([[x+y for y in 'ADFGVX'] for x in 'ADFGVX'], [])):
            if reverse:
                polybius[digraph] = str[i]
            else:
                polybius[str[i]] = digraph
        return polybius
        
    def generate_key(self, in_str):
        counts = {}
        sorted_alph = 'ETAOINSHRDLCUMWFGYPBVKJXQZ1234567890'

        for i in range(0, len(in_str), 2):
            if counts.has_key(in_str[i:i+2]):
                counts[in_str[i:i+2]] += 1
            else:
                counts[in_str[i:i+2]] = 1 

        possible_digraphs = [x[0] + x[1] for x in itertools.product('ADFGVX', repeat = 2)]        
        for digraph in possible_digraphs:
            if digraph not in counts:
                counts[digraph] = 0
                
        sorted_counts = [x[0] for x in sorted(counts.iteritems(), key = lambda (k, v): (v, k), reverse = True)]
        f_key = {}
        for digraph in sorted_counts:
            f_key[digraph] = sorted_alph[sorted_counts.index(digraph)]
        
        return f_key
        

        
    def menus(self):
        self._display.add_menu_item(menu = '&Ciphers', caption = self.caption, function = self._cipher_callback)
        if self.solve:
            self._display.add_menu_item(menu = '&Solve', caption = self.caption, function = self._solve_callback)
            self._display.add_menu_item(menu = '&Solve', caption = 'ADFGVX Dict', function = self.dict)
            
    def run(self, key_specified = True):
        if self._display == None:
            return None
        self._in = self._display.get_input()
        key = ''
        if not key_specified:
            title = self.title + ': "' + string.strip(self._in[0:10]) + '"'
            key = self.crack_key(self._in)
        self._key_raw = self.ask_for_key(key)
        if None in self._key_raw:
            return
        self._out = self._perform(self._key_raw, self._in)
        self._display.show_output(self._out)
            
