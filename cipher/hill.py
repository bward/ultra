from numpy import matrix, linalg
from metacipher import Metacipher
from math import sqrt
from maths import mod_mult_inv
from config import _alph, _alph_length
from itertools import permutations
from collections import Counter
import churn
import text
import frequencies

class Hill(Metacipher):
    title = 'Hill'
    caption = '&Hill'
    solve = True
    digraphs = ['TH', 'HE', 'AN', 'IN', 'ER', 'ON']
    trigraphs = ['THE', 'AND', 'THA', 'ENT', 'ION', 'TIO', 'FOR', 'NDE']
    digraph_perms = list(permutations(digraphs, 2))
    trigraph_perms = list(permutations(trigraphs, 3))


    def ask_for_key(self, key=''):
        rvalues, tvalues = self._display.key_dialog(radioboxes = [['Decrypt', 'Encrypt']], textboxes= [['Key, comma separated', key]], title = self.title + ' key')
        key = self.sanitize_key(tvalues[0])
        encryption = (rvalues[0] == 1)
        return key, encryption

    def sanitize_key(self, key):
        key = [int(x) for x in key.split(',')]
        n = int(sqrt(len(key)))
        if len(key)/n == n:
            key = matrix([key[i*n:(i+1)*n] for i in range(n)])
            if int(linalg.det(key)) != 0:
                return key
            else:
                self._display.error_dialog('Bad key matrix, non-invertible')
                return None
        else:
            self._display.error_dialog('Bad key matrix, must be square')
            return None

    def encrypt(self, key, in_str):
        in_str = [_alph[0].index(c) if c in _alph[0] else _alph[1].index(c) for c in text.clean(in_str)]
        out_str = []

        for i in range(0, len(in_str), len(key)):
            digraph = []
            for j in range(len(key)):
                digraph.append([in_str[i+j]])
            digraph = (key * matrix(digraph)) % 26
            for c in digraph:
                out_str.append(c)

        out_str = ''.join([_alph[0][c] for c in out_str])
        return out_str

    def decrypt(self, key, in_str):
        key = self.mod_invert_matrix(key)
        if type(key) != type(None):
            return self.encrypt(key, in_str)
        else:
            return None

    def mod_invert_matrix(self, m, base=26):
        det = linalg.det(m)
        try: m = det * m.I #screw you numpy
        except: return None
        d = mod_mult_inv(int(round(det)), base)
        if d:
            return matrix(matrix((m * d) % base).round(1), int) #seriously, wtf numpy
        else:
            return None


    def crack_key(self, in_str):
        rvalues, tvalues = self._display.key_dialog(radioboxes = [['Auto solve', 'Crib']], textboxes= [['Key length', '2'], ['Crib', ''], ['Index', '0']], title = self.title + ' cracker')
        in_str = text.clean(in_str)
        freq = frequencies.Frequencies(None, independent=False)
        if rvalues[0]==0:
            try: key_length = int(tvalues[0])
            except: self._display.error_dialog('Invalid key length')
            

            if key_length == 2:
                
                most_common = Counter(self.split_str(in_str, 2)).most_common(2)
                d1, d2 = most_common[0][0], most_common[1][0]
                b = matrix([[_alph[0].index(d1[0]), _alph[0].index(d2[0])],[_alph[0].index(d1[1]), _alph[0].index(d2[1])]])
                print b
                print '-----------------------'
                keys = []
                for d in self.digraph_perms:
                    v1, v2, v3, v4 = _alph[0].index(d[0][0]), _alph[0].index(d[0][1]), _alph[0].index(d[1][0]), _alph[0].index(d[1][1])
                    a = matrix([[v1, v3],[v2, v4]])
                    print a
                    print d
                    try:
                        key = (b * self.mod_invert_matrix(a)) % 26

                        keys.append(key)
                    except: print 'fail'                    
                    
                
                
                min_score = None
                best_key = None
                print keys

                for key in keys:
                    print '----'
                    print 'decrypting with'
                    print key
                    score = 0
                    out_str = self.decrypt(key, in_str)
                    if out_str:
                        percentages, counts, exp_percentages = freq.run(out_str, title = self.title)
                        for i in range(_alph_length):
                            diff_sq = (exp_percentages[i] - percentages[i]) ** 2
                            score += diff_sq
                        print score
                        if score < min_score or min_score == None:
                            min_score = score
                            best_key = key
                print best_key
                print min_score

                return ''.join([',' + str(best_key.item(i)) if i > 0 else  str(best_key.item(i)) for i in range(len(best_key)**2)])


    def split_str(self, in_str, c):
        return [in_str[i:i+c] for i in range(0,len(in_str),c)]

