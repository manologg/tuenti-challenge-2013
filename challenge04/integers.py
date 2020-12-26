#! /usr/bin/env python

'''
Created on 29/04/13
Tuenti Challenge - 4
@author: manolo
'''

import sys
from struct import *
from time import sleep
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

numbers = []
integers = open('./integers', 'r')
read_str = integers.read(4)
last_int = 0
go_go = False
already = 0

try:
    while read_str != '':
        read_int = unpack('I', read_str)[0]
        
    #    numbers.append(read_int)
        
        if last_int == (read_int -1):
            if not go_go:
                numbers.append(-1)
                go_go = True
    #        else:
    #            pass
        else:
            if go_go:
                numbers.append(last_int)
            numbers.append(read_int)
            go_go = False
        last_int = read_int
        
    #    print str(read_int) + ' (' + str(len(numbers)) + ')'
        read_str = integers.read(4)
        already += 1
        if already % 20000000 == 0:
            print 'done: ' + str(already/20000000) + '% - numbers: (' + str(len(numbers)) + ')'
            sys.stdout.flush()

    print 'numbers: (' + str(len(numbers)) + ')'
    print numbers

except KeyboardInterrupt:
    less_integers = open('./less_integers', 'w')
    for number in numbers:
        byte = pack('i', number)
        less_integers.write(byte)
    less_integers.close()
    integers.close()

less_integers = open('./less_integers', 'w')
for number in numbers:
    byte = pack('i', number)
    less_integers.write(byte)
less_integers.close()
integers.close()


