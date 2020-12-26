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
ofile = open('./challenge1.out', 'w')

def r():
    return ifile.readline()[:-1]
    
def w(what):
    ofile.write(what + '\n')

T = int(r())
for case in range(1,T+1):
    money = int(r())
    rates = [int(c) for c in r().split(' ')]
#    print 'money: ' + str(money)
#    print 'rates: ' + str(rates) + ' - ' + str(type(rates))
    
    rates.append(1) # to avoid buying at the end
    
    old_rate = float('inf')
    tendence = 1
    for rate in rates:
#        print '--------------------------'
#        print 'old rate: ' + str(old_rate)
#        print 'rate: ' + str(rate)
        if rate < old_rate:
#            print '  rate < old_rate'
            if tendence == 1:
#                print '    tendence == 1'
#                print '    money = money / rate'
                money = Decimal(money) / Decimal(rate)
            elif tendence == -1:
#                print '    tendence == -1'
#                print '    money = (money * old_rate) / rate'
                money = Decimal(money * old_rate) / Decimal(rate)
            tendence = -1
        elif rate > old_rate:
#            print '  rate > old_rate'
            if tendence == -1:
#                print '    tendence == -1'
#                print '    money = money * rate'
                money = money * rate
            elif tendence == 1:
#                print '    tendence == 1'
#                print '    money = (money / old_rate) * rate'
                money = (Decimal(money) / Decimal(old_rate)) * rate
            tendence = 1
        old_rate = rate
#        print 'money: ' + str(int(money))
    
    print str(int(money))
#    print '__________________________________________________'
#    print ''


ofile.close

