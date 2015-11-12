#!/usr/bin/env python
import random

# Euclid's algorithm in 5 lines
def euclid(a, b):
    r = b % a
    if r == 0:
        return a
    return euclid(r, a)

def mod_mult_inv(a, m):
    a %= m
    for x in range(1, m):
        if a * x % m == 1:
            return x
    return None

def closest_pair(data):
    data = sorted(data)
    minimum = data[-1] - data[0]
    min_tuple = (data[0], data[-1])
    length = len(data)
    for i in range(length - 1):
        current = (data[i], data[i + 1])
        difference = current[1] - current[0]
        if difference < minimum:
            min_tuple = current
            minimum = difference
    return min_tuple

# Note to self: do this properly using zip() and obsolete this silly function.
def range_tuples(tuples, irange):
    maximum = tuples[0][irange[0]]
    minimum = tuples[0][irange[0]]
    for tup in tuples:
        for value in tup[irange[0]:irange[1]]:
            if value > maximum:
                maximum = value
            if value < minimum:
                minumum = value
    return (maximum, minimum)

# Recursive max()
def max_r(l):
    try:
        l + 0
        return l
    except TypeError:
        max_list = []
        for sub_list in l:
            max_list.append(max_r(sub_list))
        return max(max_list)

def unique_random_pair(limit):
    first = random.randrange(limit)
    second = random.randrange(limit)
    while first == second:
        second = random.randrange(limit)
    return first, second

# The Hungarian Algorithm produces a minimum-weight matching for a weighted bipartite graph.
# This is the algorithm as described at https://secure.wikimedia.org/wikipedia/en/wiki/Hungarian_algorithm
class Hungarian:
    _original_matrix = None
    _working_matrix = None
    _assignments_overlay = None
    _total_assignments = None
    _assigned_cols = None
    _assigned_rows = None
    
    def __init__(self, matrix):
        # Keep the original somewhere safe.
        self._original_matrix = matrix
        self._working_matrix = [l[:] for l in matrix]
    
    # Bring all the stages together and perform the entire algorithm.
    def perform(self):
        # Reduction stage
        self._reduction()
        
        # Assignments stage
        self._assignments()
        
        # Until we get a complete assignment:
        while self._total_assignments < len(self._working_matrix):
            # Do the funky conditional addition and subtraction jazz.
            self._cover_zeroes()
            # Lather, rinse, repeat.
            self._assignments()
        
        return self._assignments_overlay
    
    # Perform the reduction stage of the algorithm on rows first, then columns.
    def _reduction(self):
        matrix = self._working_matrix
        # Rows
        for key, row in enumerate(matrix):
            row_min = min(row)
            if row_min == 0:
                continue
            matrix[key] = [n - row_min for n in row]
        
        # Columns
        for i in range(len(matrix[0])):
            col = []
            for j in range(len(matrix)):
                col.append(matrix[j][i])
            col_min = min(col)
            if col_min == 0:
                continue
            for j in range(len(matrix)):
                matrix[j][i] -= col_min
    
    def _assignments(self):
        # Try making all the assignments easily.
        self._easy_assignments()
        
        # If we couldn't do that, try it the hard way.
        if self._total_assignments < len(self._working_matrix):
            (
                self._assignments_overlay,
                self._total_assignments,
                self._assigned_cols,
                self._assigned_rows
            ) = self._hard_assignments(
                self._working_matrix,
                self._assignments_overlay,
                self._total_assignments,
                self._assigned_cols,
                self._assigned_rows
            )
    
    # Perform the assignments that are easily done (i.e. we have no choice but to assign them).
    def _easy_assignments(self):
        # Use a matrix of the same dimensions as the original to keep track of what's assigned where, 0 = no assignment, 1 = assignment.
        self._assignments_overlay = [[0 for n in row] for row in self._working_matrix]
        self._total_assignments = 0
        self._assigned_cols = []
        self._assigned_rows = []
        
        # Don't stop until we can't make any more assignments.
        keep_going = True
        while keep_going:
            keep_going = False
            
            # Try to find lone zeroes in rows.
            for key, row in enumerate(self._working_matrix):
                if key in self._assigned_rows:
                    continue
                
                temp_row = row[:]
                for col in self._assigned_cols:
                    temp_row[col] = -1
                if temp_row.count(0) == 1:
                    zeroindex = temp_row.index(0)
                    self._assignments_overlay[key][zeroindex] = 1
                    self._assigned_cols.append(zeroindex)
                    self._assigned_rows.append(key)
                    keep_going = True
                    self._total_assignments += 1
            
            # Try to find lone zeroes in columns.
            for i in range(len(self._working_matrix[0])):
                if i in self._assigned_cols:
                    continue
                zeroes = 0
                for j in range(len(self._working_matrix)):
                    if j in self._assigned_rows:
                        continue
                    if self._working_matrix[j][i] == 0:
                        zeroes += 1
                        if zeroes > 1:
                            break
                        zero_index = j
                if not zeroes == 1:
                    continue
                self._assignments_overlay[zero_index][i] = 1
                self._assigned_cols.append(i)
                self._assigned_rows.append(zero_index)
                keep_going = True
                self._total_assignments += 1
        
    # Perform the more difficult assignments, where we have to make a decision about which assignments to make. Nothing more sophisticated than a trial-and-error approach.
    def _hard_assignments(self, matrix, assignments_overlay, total_assignments, assigned_cols, assigned_rows):
        # Given a bipartite graph matrix and a partial matching consisting only of necessary pairs, find a maximal matching.
        for j in range(len(matrix)):
            if j in assigned_rows:
                continue
            for i in range(len(matrix[0])):
                if i in assigned_cols:
                    continue
                if matrix[j][i] == 0:
                    # We've got ourselves a live one!
                    # Make a load of temporary variables to explore this route with.
                    my_overlay = [row[:] for row in assignments_overlay]
                    my_overlay[j][i] = 1
                    
                    new_overlay, my_total_assignments, my_assigned_cols, my_assigned_rows = self._hard_assignments(matrix, my_overlay, total_assignments + 1, assigned_cols + [i], assigned_rows + [j])
                    # The above line takes our temporary variables and passes them into a new instance of this function so we can perform a depth-first recursive search for a solution.
                    
                    if my_total_assignments == len(matrix):
                        return new_overlay, my_total_assignments, my_assigned_cols, my_assigned_rows
        
        return assignments_overlay, total_assignments, assigned_cols, assigned_rows
    
    # Find which rows and columns to strike through for when we can't make enough assignments
    def _cover_zeroes(self):
        
        marked_rows = []
        marked_cols = []
        
        # Mark all rows without assignments.
        for key, row in enumerate(self._working_matrix):
            if not key in self._assigned_rows:
                marked_rows.append(key)
        
        # Don't stop until we can't mark any more.
        marked = True
        while marked:
            marked = False
            
            # Mark all columns containing zeroes in the marked rows.
            for row_key in marked_rows:
                for col_key, n in enumerate(self._working_matrix[row_key]):
                    if col_key in marked_cols:
                        continue
                    if n == 0:
                        marked_cols.append(col_key)
                        marked = True
            
            # Mark all rows containing assignments in the marked columns.
            for i in marked_cols:
                for j in range(len(self._working_matrix)):
                    if j in marked_rows:
                        continue
                    if self._assignments_overlay[j][i] == 1:
                        marked_rows.append(j)
                        marked = True
        
        # Contains all elements which are in marked rows but not in marked columns.
        remaining_elements = []
        for i in range(len(self._working_matrix[0])):
            for j in range(len(self._working_matrix)):
                if (not i in marked_cols) and (j in marked_rows):
                    remaining_elements.append(self._working_matrix[j][i])
        
        min_remaining = min(remaining_elements)
        
        for i in range(len(self._working_matrix[0])):
            for j in range(len(self._working_matrix)):
                if (i in marked_cols) and (not j in marked_rows):
                    self._working_matrix[j][i] += min_remaining
                elif (not i in marked_cols) and (j in marked_rows):
                    self._working_matrix[j][i] -= min_remaining
