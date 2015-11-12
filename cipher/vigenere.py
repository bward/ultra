#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Vigenere ciphers are pretty cool, but a bit complicated to explain in a comment.
# https://secure.wikimedia.org/wikipedia/en/wiki/Vigenere_cipher

import caesar
import graph
import maths
from config import _alph, _alph_indexes, _alph_length
from metacipher import Metacipher


class Vigenere(Metacipher):
    title = u'Vigenère'
    caption = u'&Vigenère'
    solve = True
    
    _start_point = 0
    
    def ask_for_key_length(self, key_length = 0):
        tboxes = self._display.key_dialog(textboxes = [('Key length', str(key_length))], title = u'Vigenère key length')[1]
        try:
            key_length = int(tboxes[0])
        except ValueError:
            self._display.error_dialog('Bad key length, must be int()-able')
            return None
        return key_length
    
    def sanitize_key(self, key, start_point):
        global _alph
        sanitized_key = ''
        for key_char in key:
            if key_char in _alph[0] + _alph[1]:
                sanitized_key += key_char
        if key == '':
            sanitized_key = None
        try:
            start_point = int(start_point)
        except ValueError:
            display.error_dialog('Bad starting point, must be int()-able')
            return (None, None)
        return sanitized_key, start_point
    
    def encrypt(self, key = '', in_str = ''):
        start_point = self._start_point
        return self.crypt(key, in_str, encrypt = True, start_point = start_point)
        
    def decrypt(self, key = '', in_str = ''):
        start_point = self._start_point
        return self.crypt(key, in_str, encrypt = False, start_point = start_point)
        
    def crypt(self = None, key = '', in_str = '', encrypt = True, start_point = 0):
        global _alph, _alph_indexes
        out_str = ''
        key = key.upper()
        key_i = 0
        for in_char in in_str:
            in_upp = in_char in _alph[0]
            in_low = in_char in _alph[1]
            if in_upp or in_low:
                key_char = key[key_i]
                key_index = _alph_indexes[0][key_char] + start_point
                if in_upp:
                    old_index = _alph_indexes[0][in_char] + start_point
                elif in_low:
                    old_index = _alph_indexes[1][in_char] + start_point
                    
                if encrypt:
                    new_index = (old_index + key_index) % 26
                else:
                    new_index = (old_index - key_index) % 26
                
                if in_upp:
                    out_char = _alph[0][new_index - start_point]
                elif in_low:
                    out_char = _alph[1][new_index - start_point]
                key_i = (key_i + 1) % len(key)
            else:
                out_char = in_char
            out_str += out_char
        return out_str
    
    def crack_key(self, in_str):
        import autocorrelation
        global _alph
        # Work out the length of the key
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
            if counts >= (100/12): # 12-letter (or lower) key
                a, b = maths.closest_pair(values)
                key_length = maths.euclid(a, b)
                done = True
                break
            limit -= 1
        # Check it with the user
        if self._independent:
            key_length = self.ask_for_key_length(key_length)
        # Plop every n characters into separate strings:
        # e.g. 'ABCDABCDABCD' would become ['AAAA', 'BBBB', 'CCCC', 'DDDD'] for a key length of 4.
        caesars = [''] * key_length
        char_index = 0
        # Break each string in the list as individual Caesar ciphers to obtain the Vigenere key
        c = caesar.Caesar(None, independent = False)
        for char in in_str:
            if char in _alph[0] + _alph[1]:
                caesars[char_index % key_length] += char
                char_index += 1
        for caesar_str in caesars:
            num_key = (c.crack_key(in_str = caesar_str) - self._start_point) % 26
            key_char = _alph[0][num_key]
            out_key += key_char
        # Important: no actual decryption is done here, just finding the key.
        return out_key
    
    def ask_for_key(self, key = ''):
        if self._display == None:
            return None
        rvalues, tvalues = self._display.key_dialog(radioboxes = [['Decrypt', 'Encrypt']], textboxes = [(self.title + ' key', key), ('Start counting from', str(self._start_point))], title = self.title + ' key')
        if [None] in (rvalues, tvalues):
            return (None, None)
        key, self._start_point = self.sanitize_key(tvalues[0], tvalues[1])
        encryption = (rvalues[0] == 1)
        return key, encryption

if __name__ == "__main__":
    v = Vigenere(independent = False)
    in_str = """TYKZK LASFY YDKYC DERKF LRJKY AIFEU HSZER LRVJR
PNXKM ZAPKF LLVRQ AWVFZ AAZEC KPYFR VSFWR OEEVU
JIGYC YMRTF PNVRL KBVCG LVVZR VREFR HFLCJ ZEKFD
DIIZL NDZRE YADJR VGVKF LRNZR OTYVQ LTKZL NSWFP
AHVEC ETDFL AHRJD HRRJG RNFNM BRGIC ZEETC DAJEM
ADVKC JTVUR OEIVU HSEFQ PGEFD SIWVY UDZXS LSJFS
YDZMC YSZFL DOIBC KTYVJ VWMZQ PBZCG AYFER OEZTC
OECGC KTYVK HCYZL LIJKS KIVUU HSIVK HRBRZ SYLEQ
VPYZQ AITRR LDREB IOIVJ PTKCC YEJVK ILREA LTFKF
LTVEU OEVCP VTFIK HCYZL LOLIA VNKRA ASYRB SEULQ
AOVON LCKZR TAPSC AHRKY ZANVY AHVIQ AAKZM UMFUC
SIKYY ZBVVL REGKQ PMGCC AHVPK HYRCQ VHRMC IEVEU
VRIZC KTYRR PTNFS SDWRJ SIEKM LNVDW OAEUQ HNUKF
LRVWM YEYRT LIJJS LDFEJ FTYZQ WRFKM AYGVL VNVKF
LLVJQ AHVPQ LEDTM UVZEA LDFWG ASJVA BRZKW AIDVU
PLCKC SLZNG SLXZT LAWLJ SEIIC WOIKM UTYVQ ARLTR
BRVFD AHVDY JHZEC PTJFN LRRKG VNREB PTJTS YRVER
ZEKKG UGJZL TYEVV AMVJQ HGVSW AHVNY FIWFS UDKYC
LNTCM ZEUGJ HIEKC ETEVV ATFKF LMRTF PNVRL KIKCM
VKVUY ZTYFS NHZKU HSRSM BTKFZ LSVER PTDRW IENFP
AHCZQ AEEZL NOLKD VRKYC UEOKU LAKYC YSKRR POEKP
HNJDG ZSZFL PNKYC TERER PMVZU PLCRR AATBR OECRR
LSKJM CIVKK LSJRE LTYVW ZEVDR VHRMC ZCRCC KUGKF
LSVTS YIKPY NAZER OOLXF PDFER AHZEI AHZJM UELJC
ZTYVP VTFIK HCYZL LSFZR ZHFLJ KNKSC AOFJR LEG"""
    key = 'HARRY'
    out_str = v.decrypt(key, in_str)
    print out_str
