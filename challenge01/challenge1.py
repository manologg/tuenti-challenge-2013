#! /usr/bin/env python

'''
Created on 29/04/13
Tuenti Challenge - 1
@author: manolo
'''

import sys
import math
from decimal import Decimal
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

T = int(r())
for case in range(1,T+1):
    money = int(r())
    rates = [int(c) for c in r().split(' ')]
    
    rates.append(1) # to avoid buying at the end
    
    old_rate = float('inf')
    tendence = 1
    for rate in rates:
        if rate < old_rate:
            if tendence == 1:
                money = Decimal(money) / Decimal(rate)
            elif tendence == -1:
                money = Decimal(money * old_rate) / Decimal(rate)
            tendence = -1
        elif rate > old_rate:
            if tendence == -1:
                money = money * rate
            elif tendence == 1:
                money = (Decimal(money) / Decimal(old_rate)) * rate
            tendence = 1
        old_rate = rate
    
    print str(int(money))

