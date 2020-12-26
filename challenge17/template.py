#! /usr/bin/env python

'''
Created on 05/13
Tuenti Challenge - 
@author: manolo
'''

import sys
import math
from decimal import Decimal
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def w(what):
    sys.stdout.write(what)


T = int(r())
for case in range(1,T+1):
    money = int(r())
    rates = [int(c) for c in r().split(' ')]
