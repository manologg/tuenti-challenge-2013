#! /usr/bin/env python

'''
Created on 07/05/13
Tuenti Challenge - 13
@author: manolo
'''

import sys
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def w(what):
    sys.stdout.write(what)


T = int(r())
for case in range(1,T+1):
    
    print 'Test case #' + str(case)
    
    n, m = [int(c) for c in r().strip().split(' ')]
    generated_numbers = [int(c) for c in r().strip().split(' ')]
    intervals = []
    for i in range(m):
        s_m, e_m = [int(c) for c in r().strip().split(' ')]
        intervals.append((s_m, e_m))

    generated_numbers.sort()

    i = 0
    for (i_min, i_max) in intervals:

        from itertools import groupby
        print max([len(list(group)) for key, group in groupby(generated_numbers[i_min-1 : i_max])])



