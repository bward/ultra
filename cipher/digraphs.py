#!/usr/bin/env python

# This counts the frequency of occurrance of digraphs (2-letter pairs) in the ciphertext.
# It displays it on a pseudo-3D graph (graph3dp) of first letter x second letter x greyness of square.
# It can also return the logarithms of the frequencies for the purpose of making the more common digraphs (like TH and HE) less significant.

import graph3dp
import text
import math
import cPickle as pickle

class Digraphs:
    display = None
    in_str = None
    title = None
    
    alph_upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alph_low = "abcdefghijklmnopqrstuvwxyz"
    alph_upp_indexes = dict([(value, key) for (key, value) in enumerate(alph_upp)])
    alph_low_indexes = dict([(value, key) for (key, value) in enumerate(alph_low)])
    alph_length = len(alph_upp)
    
    def __init__(self, display, independent = True):
        self.display = display
        self._independent = independent
        if independent:
            self.display.add_menu_item(menu = '&Analysis', caption = '&Digraph Count', function = self.run)
            self.display.add_menu_item(menu = '&Analysis', caption = 'L&og Digraph Count', function = self.log_callback)
    
    def log_callback(self):
        self.run(log = True)
    
    def counts(self, in_str):
        # data[i][j] is digraph frequency of <i><j> in in_str
        temp_row = [0 for i in self.alph_upp]
        data = [temp_row[:] for i in self.alph_upp]
        
        in_str = text.clean(in_str, self.alph_upp + self.alph_low)
        length = len(in_str)
        for i in range(length - 1):
            fi = self.alph_upp_indexes[in_str[i]]
            se = self.alph_upp_indexes[in_str[i + 1]]
            data[fi][se] += 1
        return data
    
    def log_counts(self, data):
        data_log = data[:]
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                data_log[i][j] = math.log(cell + 1)
        return data_log
    
    def graph(self, data, labels, title = 'Digraphs'):
        graph = graph3dp.Graph3Dp(data = data, labels = labels, size = (400, 400), offset = (20, 20, 5, 5))
        image = graph.draw()
        self.display.show_image(image, title = title)
    
    def run(self, in_str = None, title = 'Digraphs', show_graph = True, log = False):
        self.title = title
        if in_str == None:
            self.in_str = self.display.get_input()
        else:
            self.in_str = in_str
            
        if self.in_str == '':
            return None
        
        if title == 'Digraphs' and log:
            title = 'Digraphs (logged)'
        
        with open('cipher/digraphs.pickle', 'r') as digraphs_file:
            digraphs_compare = pickle.load(digraphs_file)
            
        counts_in = self.counts(self.in_str)
        if log:
            counts_in = self.log_counts(counts_in)
            digraphs_compare = self.log_counts(digraphs_compare)
        
        counts = [zip(obs, exp) for obs, exp in zip(counts_in, digraphs_compare)]
        
        if show_graph:
            counts_graph = [[(cell,) for cell in row] for row in counts_in]
            labels = ([c for c in self.alph_upp],) * 2
            self.graph(counts_graph, labels, title)
        
        return counts

if __name__ == "__main__":
    d = Digraphs(None, independent = False)
    print d.run('aa', show_graph = False)
