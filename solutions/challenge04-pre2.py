#! /usr/bin/env python

'''
Created on 29/04/13
Tuenti Challenge - 4
@author: manolo
'''

import sys
from struct import *
from time import sleep
from itertools import takewhile, dropwhile
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

numbers = []
integers = open('./less_integers', 'r')
read_str = integers.read(4)

while read_str != '':
    read_int = unpack('i', read_str)[0]
    if read_int != -1:
        numbers.append(read_int)
    read_str = integers.read(4)

print 'numbers: (' + str(len(numbers)) + ')'

special = (100000, 2147383647)

numbers.sort()
i = 0
missing = []
for number in takewhile(lambda x: x < special[0], numbers):
    if number > i:
        while i < number:
            sys.stdout.write('.')
            sys.stdout.flush()
            missing.append(i)
            i += 1
        sleep(0.2)
    elif number == i:
        pass
    else:
        raise 'impossible: ' + str(number) + ' < ' + str(i)
    i += 1
    
sys.stdout.write('\n')

i = special[1]
for number in dropwhile(lambda x: x < special[1], numbers):
    if number > i:
        while i < number:
            sys.stdout.write('.')
            sys.stdout.flush()
            missing.append(i)
            i += 1
        sleep(0.2)
    elif number == i:
        pass
    else:
        raise 'impossible: ' + str(number) + ' < ' + str(i)
    i += 1

sys.stdout.write('\n')

print str(len(missing)) + ' numbers missing'
print 'missing  = ' + str(missing)


integers.close()


