import text
from config import _alph
from metacipher import Metacipher

# This implements your bog-standard column-transposition cipher.
# TODO: cracking

class Transposition(Metacipher):
    title = 'Transposition'
    caption = '&Transposition'
    
    def ask_for_key(self, key = ''):
        rvalues, tvalues = self._display.key_dialog(radioboxes = [['Decrypt', 'Encrypt'], ['Along rows', 'Down columns'], ['Comma separated', 'Text'], ['Strip whitespace', 'Don\'t']], textboxes = [('Transposition key', '1,2,3,4,5')], title='Transposition Key')
        key = tvalues[0]
        encryption = (rvalues[0] == 1)
        method = rvalues[1]
        comma_separated = (rvalues[2] == 0)
        strip_whitespace = (rvalues[3] == 0)
        return key, encryption, method, comma_separated, strip_whitespace
    
    def _perform(self, key, in_str):
        self._key = key[0]
        self._encryption = key[1]
        self._method = key[2]
        if key[4]:
            in_str = in_str.replace(' ', '').replace('\t', '').replace('\n', '')
        
        if key[3]:
            self._key = [int(c) for c in self._key.split(',')]
        else:
            self._key = [sorted(self._key).index(c) + 1 for c in self._key]
            x = []
            for i in range(len(self._key)):
                x.append(self._key[i])
                self._key[i] += x.count(self._key[i]) - 1
        if self._encryption and self._method == 1:
            out_str = self.encrypt(self._key, in_str)
        else:
            out_str = self.decrypt(self._key, in_str, self._method)
        return out_str
        
    def encrypt(self, key, in_str):
        key = [key.index(i) for i in range(1, len(key) + 1)] #'reverse' key for encryption purposes
        out_str = ''
        
        overflows = len(in_str) % len(key)

        for i in key:
            for j in range(len(in_str)/len(key) + (1 if i < overflows else 0)):
                out_str += in_str[j * len(key) + i]
        
        return out_str
    
    def decrypt(self, key, in_str, method): #or encrypt for along rows, as it's symmetrical
        global _alph
        out_str = ''
        
        if method == 1: #columnar, so convert to along the rows            
            in_str_list = list(in_str)
            rows = len(in_str) / len(key)
            rearranged = ''
            overflow = len(in_str) % len(key)
            indexes = [0]
            for i in range(len(key) - 1):
                indexes.append(indexes[-1] + rows + (1 if key.index(i + 1) < overflow else 0)) #do magic
            
            #work out complete rows
            for i in range(rows):
                for j in indexes:
                    try: rearranged += in_str_list.pop(j - (i + 1) * indexes.index(j))
                    except: break
            
            #now do the incomplete bits
            for i in range(1, len(key)+1):
                if key.index(i) < overflow:
                    rearranged += in_str_list.pop(0)
                else:
                    rearranged += ' '
                
            in_str = rearranged
            
        for i in range(len(in_str)/len(key)):
            slice = in_str[i*len(key):(i+1)*len(key)]
            for j in range(len(key)):
                out_str += slice[key[j]-1]
        
        excess = len(in_str) % len(key)
        if excess != 0:
            final = in_str[-excess:] + 'X' * (len(key) - excess)
            out_str += self.decrypt(key, final, 0)
                                    
        return out_str.rstrip()
        
    def pad_key(self, key, in_str):
        padding = len(in_str) % len(key.split(','))
        if padding == 0:
            padding = len(key)
        in_str += 'X' * (len(key) - padding)
        return in_str
