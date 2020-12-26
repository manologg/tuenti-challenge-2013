#! /usr/bin/env python

'''
Created on 02/05/13
Tuenti Challenge - 9
@author: manolo
'''

import sys
ifile = sys.stdin
from time import sleep

def r():
    return ifile.readline()[:-1]

def simulate(width, length, soldiers, crematoriums):

    max_zorglings = width * length
    zorglings_per_sec = width - soldiers

    seconds = int((max_zorglings-width)/zorglings_per_sec) + 1

    return seconds * (crematoriums + 1)
        

T = int(r())
for case in range(1,T+1):
    
    (width, length, soldier_price, crematorium_price, gold) = [int(c) for c in r().split(' ')]
    
    if gold/soldier_price >= width:
        print -1
    else:
        time = []
        max_crematoriums = (gold/crematorium_price) + 1
        for crematoriums in range(max_crematoriums):
            
            gold_left = gold - (crematoriums * crematorium_price)
            soldiers = gold_left/soldier_price
            seconds = simulate(width, length, soldiers, crematoriums)
            time.append(seconds)
        print max(time)
    
    
