#!/usr/bin/env python

# This counts the frequency of occurrance of the letters in the ciphertext and displays them on a graph alonside the expected frequencies of standard English.

import graph as graphing

class Frequencies:
    display = None
    in_str = None
    title = None
    data = None
    
    alph_upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alph_low = "abcdefghijklmnopqrstuvwxyz"
    alph_upp_indexes = dict([(value, key) for (key, value) in enumerate(alph_upp)])
    alph_low_indexes = dict([(value, key) for (key, value) in enumerate(alph_low)])
    alph_length = len(alph_upp)
    
    counts_compare = [
        146882,
        30024,
        52411,
        73873,
        234185,
        41702,
        38564,
        103860,
        134842,
        2897,
        14031,
        75032,
        49731,
        131219,
        145179,
        35232,
        1722,
        113111,
        118258,
        173097,
        53512,
        19655,
        38772,
        3227,
        38795,
        2241
    ]
    
    def __init__(self, display, independent = True):
        self._display = display
        self._independent = independent
        if self._independent:
            self._display.add_menu_item(menu = '&Analysis', caption = '&Letter Count', function = self.run)
            self._display.add_menu_item(menu = '&Analysis', caption = 'Fitness', function = self._analyse_callback)
        
    def counts(self, in_str):
        counts = [0 for i in self.alph_upp]
        if in_str == "":
            return counts
        for char in in_str:
            if char in self.alph_upp:
                index = self.alph_upp_indexes[char]
                counts[index] += 1
            elif char in self.alph_low:
                index = self.alph_low_indexes[char]
                counts[index] += 1
        return counts
    
    def percentages(self, counts):
        total = sum(counts)
        percentages = [(float(x)/total)*100.0 for x in counts]
        return (percentages, total)
    
    def graph(self, title = 'Frequencies'):
        colours = [(100, 100, 255), (255, 0, 0)]
        graph = graphing.Graph(self.data, labels = True, percentages = True, size = (485, 300), grid = True, line_colours = colours)
        image = graph.draw()
        self._display.show_image(image, title = title)
    
    def run(self, in_str = None, title = 'Frequencies'):
        self.title = title
        if in_str == None and self._independent:
            self.in_str = self._display.get_input()
        else:
            self.in_str = in_str
            
        if self.in_str == '':
            return None
        
        counts_compare = self.counts_compare
        percentages_compare = self.percentages(counts_compare)[0]
            
        counts_in = self.counts(self.in_str)
        percentages_in = self.percentages(counts_in)[0]
        
        self.data = [(self.alph_upp[x], percentages_compare[x], percentages_in[x]) for x in range(self.alph_length)]
        
        if self._independent:
            self.graph(title)
        return (percentages_in, counts_in, percentages_compare)


    def analyse(self, in_str, graph=True):   
        expected = sorted(self.percentages(self.counts_compare)[0], reverse = True)
        counts = {}
        
        for i in range(0, len(in_str), 2):
            if counts.has_key(in_str[i:i+2]):
                counts[in_str[i:i+2]] += 1
            else:
                counts[in_str[i:i+2]] = 1

        counts = sorted(counts.values(), reverse = True)[:26]
        while len(counts) != 26:
            counts.append(0)
        l = len(in_str)/2
        counts = [(float(x)/l)*100.0 for x in counts]

        data = [(str(x), expected[x], counts[x]) for x in range(26)]
        
        if self._independent and graph:
            self.graph = graphing.Graph(data, labels = True, percentages = True, size = (485, 300), grid = True)
            image = self.graph.draw()
            self._display.show_image(image, title='Fitness analysis')
            
        #calculate score
        score = 0.0
        for x in range(26):
            score += (expected[x] - counts[x]) ** 2

        return score

    def _analyse_callback(self):
        return self.analyse(self._display.get_input())