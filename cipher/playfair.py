#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import churn
import maths
from random import randrange
import text

class Playfair:
    _display = None
    in_str = None
    out_str = None
    
    def __init__(self, display):
        self._display = display
        self._display.add_menu_item(menu = '&Solve', caption = '&Playfair', function = self.solve_callback)
        self._display.add_menu_item(menu = '&Ciphers', caption = '&Playfair', function = self.cipher_callback)
        
    def solve_callback(self):
        self.run(key_specified = False)
    
    def cipher_callback(self):
        self.run(key_specified = True)
    
    def decrypt(self, key, in_str):
        return self.crypt(key, in_str, False)
        
    def encrypt(self, key, in_str):
        return self.crypt(key, in_str, True)
    
    def _keysquare(self, key):
        rows = 5*['']
        cols = 5*['']
        for i in range(0,5):
            rows[i] = key[i*5:i*5+5]
        for char in key:
            cols[key.find(char)%5] += char

        return rows, cols
            
    def crypt(self, key, in_str, encrypt = False):
        #Create key square
        rows, cols = self._keysquare(key)
        
        # Clean the in_str so we don't bugger up the digraphs
        in_str = text.clean(in_str)
        
        #Fix double letters in plaintext and pad, if we're encrypting
        if encrypt:
            i=0
            list_input = list(in_str)
            while i < len(list_input) - 1:
                if list_input[i] == list_input[i+1]:
                    list_input.insert(i+1,'X')
                i += 1
            in_str = ''.join(list_input)
            
            if len(in_str)%2 != 0:
                in_str += 'X'
            
        #Iterate digraphs
        out_str = ''
        for i in range(0, len(in_str)/2):
            digraph = in_str[i*2:i*2+2]
            first = digraph[0]
            second = digraph[1]
            #Find row/column of each character
            for i in range(0,5):
                #Get row/column indices
                if rows[i].find(first) != -1:
                    fri = i
                if rows[i].find(second) != -1:
                    sri = i
                if cols[i].find(first) != -1:
                    fci = i
                if cols[i].find(second) != -1:
                    sci = i
            #We have the row/column of each letters, so time to go through the three cases as defined here: http://en.wikipedia.org/wiki/Playfair_cipher#Clarification_with_picture
            if encrypt:
                if fri == sri:
                    #case 1
                    plain_digraph = rows[fri][(fci + 1) % 5] + rows[sri][(sci + 1) % 5]
                
                
                elif fci == sci:
                    #case 2
                    plain_digraph = cols[fci][(fri + 1) % 5] + cols[sci][(sri + 1) % 5]
            
                else:
                    #case 3
                    plain_digraph = rows[fri][sci] + rows[sri][fci]
                    
            else:
                if fri == sri:
                    #case 1
                    plain_digraph = rows[fri][(fci - 1) % 5] + rows[sri][(sci - 1) % 5]
                
                
                elif fci == sci:
                    #case 2
                    plain_digraph = cols[fci][(fri - 1) % 5] + cols[sci][(sri - 1) % 5]
            
                else:
                    #case 3
                    plain_digraph = rows[fri][sci] + rows[sri][fci]
            
            out_str += plain_digraph
            
        return out_str                
        
    def crack(self, in_str):
        thread = PlayfairChurnThread(self, self._display, in_str)
        thread.start()
        self._display.churn_dialog()
        final_key = thread.stop()
        return final_key
        
        
    def ask_for_key(self, key=''):
        rvalues, tvalues = self._display.key_dialog(radioboxes = [['Decrypt', 'Encrypt']], textboxes = [('Playfair Key', key)], title = 'Playfair key')
        key = text.pad_key(tvalues[0], 'ABCDEFGHIKLMNOPQRSTUVWXYZ')
        encryption = (rvalues[0] == 1)
        if key == None:
            return None
        elif len(key) != 25:
            self._display.error_dialog('Bad key, must be 25 characters long')
            return None
        sanitized_key = key.upper()
        return sanitized_key, encryption
    
    def run(self, key_specified=True):
        self.in_str = self._display.get_input()
        key = ''
        if self.in_str == '':
            return
        if not key_specified:
            key = self.crack(self.in_str)

            
        key, encryption = self.ask_for_key(key)
        
        if not encryption:
            self.out_str = self.decrypt(key, self.in_str)
        else:
            self.out_str = self.encrypt(key, self.in_str)
            
        self._display.show_output(self.out_str)
        return
        
class PlayfairChurnThread(churn.ChurnThread):
    start_key = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'     
    def churn_key(self, old_key):
        if old_key == None:
            return self.start_key
    
        else:
            new_key = old_key
            rows, cols = self.parent._keysquare(old_key)
     
            #Several different things we can do to the keysquare here, choose between them at random
            choice = randrange(50)
            if choice == 0:
                #diagonal flip
                pass
            elif choice == 1:
                #top to bottom flip
                pass
            elif choice == 2:
                #left to right flip
                pass
            elif choice == 3:
                fri, sri = maths.unique_random_pair(5)
                rows[fri], rows[sri] = rows[sri], rows[fri]
                new_key = ''.join(rows)

            elif choice == 4:
               fci, sci = maths.unique_random_pair(5)
               cols[fci], cols[sci] = cols[sci], cols[fci]
               #join cols

            elif choice > 4:
                p = new_key[randrange(25)]
                q = new_key[randrange(25)]
                new_key = new_key.replace(p, '1')
                new_key = new_key.replace(q, '2')
                new_key = new_key.replace('1', q)
                new_key = new_key.replace('2', p)
            #print new_key
            return new_key
