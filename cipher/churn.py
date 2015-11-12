# This implements the churn algorithm with digraphs and tetragraphs.
# I didn't write this file -- Ben if you feel like commenting your code I'd <3 you for ever.

import threading
import text
from random import randrange
import os

class Churn:
    frequencies = None
    tetragraphs = None
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    values = [0,0,0,0,0,1,1,1,1,1,2,2, 2, 3, 4, 4, 5, 6, 8, 15]
    
    def __init__(self, use_tetragraphs = False):
        if use_tetragraphs == True:
            frequency = [0]*456976
            log_file = open("cipher/TetLogFreq.txt")
            temp_string = log_file.read(456976)
            log_file.close()
            for j in range (456976):
                frequency[j]= ord(temp_string[j])- ord('A')
            self.frequencies = frequency
            self.tetragraphs = True
        else:            
            self.frequencies = [
            4,7,8,7,4,6,7,5,7,3,6,8,7,9,3,7,3,9,8,9,6,7,6,5,7,4,
            7,4,2,0,8,1,1,1,6,3,0,7,2,1,7,1,0,6,5,3,7,1,2,0,6,0,
            8,2,5,2,7,3,2,8,7,2,7,6,2,1,8,2,2,6,4,7,6,1,3,0,4,0,
            7,6,5,6,8,6,5,5,8,4,3,6,6,5,7,5,3,6,7,7,6,5,6,0,6,2,
            9,7,8,8,8,7,6,6,7,4,5,8,7,9,7,7,5,9,9,8,5,7,7,6,7,3,
            7,4,5,3,7,6,4,4,7,2,2,6,5,3,8,4,0,7,5,7,6,2,4,0,5,0,
            7,5,5,4,7,5,5,7,7,3,2,6,5,5,7,5,2,7,6,6,6,3,5,0,5,1,
            8,5,4,4,9,4,3,4,8,3,1,5,5,4,8,4,2,6,5,7,6,2,5,0,5,0,
            7,5,8,7,7,7,7,4,4,2,5,8,7,9,7,6,4,7,8,8,4,7,3,5,0,5,
            5,0,0,0,4,0,0,0,3,0,0,0,0,0,5,0,0,0,0,0,6,0,0,0,0,0,
            5,4,3,2,7,4,2,4,6,2,2,4,3,6,5,3,1,3,6,5,3,0,4,0,5,0,
            8,5,5,7,8,5,4,4,8,2,5,8,5,4,8,5,2,4,6,6,6,5,5,0,7,1,
            8,6,4,3,8,4,2,4,7,1,0,4,6,4,7,6,1,3,6,5,6,1,4,0,6,0,
            8,6,7,8,8,6,9,6,8,4,6,6,5,6,8,5,3,5,8,9,6,5,6,3,6,2,
            6,6,7,7,6,8,6,6,6,3,6,7,8,9,7,7,3,9,7,8,9,6,8,4,5,3,
            7,3,3,3,7,3,2,6,7,2,1,7,3,2,7,6,0,7,6,6,6,0,3,0,4,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,
            8,6,6,7,9,6,6,5,8,3,6,6,6,6,8,6,3,6,8,8,6,5,6,0,7,1,
            8,6,7,6,8,6,5,7,8,4,6,6,6,6,8,7,4,5,8,9,7,4,7,0,6,2,
            8,6,6,5,8,6,5,9,8,3,3,6,6,5,9,6,2,7,8,8,7,4,7,0,7,2,
            6,6,7,6,6,4,6,4,6,2,3,7,7,8,5,6,0,8,8,8,3,3,4,3,4,3,
            6,1,0,0,8,0,0,0,7,0,0,0,0,0,5,0,0,0,1,0,2,1,0,0,3,0,
            7,3,3,4,7,3,2,8,7,2,2,4,4,6,7,3,0,5,5,5,2,1,4,0,3,1,
            4,1,4,2,4,2,0,3,5,1,0,1,1,0,3,5,0,1,2,5,2,0,2,2,3,0,
            6,6,6,6,6,6,5,5,6,3,3,5,6,5,8,6,3,5,7,6,4,3,6,2,4,2,
            4,0,0,0,5,0,0,0,3,0,0,2,0,0,3,0,0,0,1,0,2,0,0,0,4,4,    
            ]
            self.tetragraphs = False
            
    def get_score(self, input):
        #clean up input, doesn't matter what we do to it as this never gets returned
        input = text.clean(input.upper(), self.alphabet)
        
        length = len(input)
        if self.tetragraphs:
            score=0
            for j in range(length-3):
                fi=self.alphabet.index(input[j])
                se=self.alphabet.index(input[j+1])
                th=self.alphabet.index(input[j+2])
                fo=self.alphabet.index(input[j+3])
                position=17576*fi +676*se +26*th +fo
                score += self.frequencies[position]
            return score
        
        else:
            score=0
            for j in range(length-1):
                fi=self.alphabet.index(input[j])
                se=self.alphabet.index(input[j+1])
                product=26*fi+se
                score += self.frequencies[product]

            return score

class ChurnThread(threading.Thread):
    #DisplayAPI object
    display = None
    parent = None
    in_str = None
    halt = False
    churn = None

    def __init__(self, parent, display, in_str):
        threading.Thread.__init__(self)
        self.parent = parent
        self.display = display
        self.in_str = in_str
        self.churn = Churn()
    
    def run(self):
        old_score = 0
        best_score = 0
        old_key = None
        best_key = None
        
        while not self.halt:
            new_key = self.churn_key(old_key)
            # Crucially, we don't need to know the cipher algorithm, just make it work better.
            new_plain = self.parent.decrypt(new_key, self.in_str)
            new_score = self.churn.get_score(new_plain)
            x = randrange(20)
            if new_score > old_score - self.churn.values[x]:
                old_score = new_score
                old_key = new_key
            if new_score > best_score:
                best_score = new_score
                self.best_key = new_key
                if os.name == 'nt':
                    self.display.show_output(new_plain)
                else:
                    print new_plain
        return
            
    def stop(self):
        self.halt = True
        return self.best_key
        
    def restart(self):
        self.halt = False
        return

    def churn_key(self):
        return None
