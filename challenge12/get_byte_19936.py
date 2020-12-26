#! /usr/bin/env python

import sys

ifile = sys.stdin
def r():
    return ifile.readline()[:-1]

def w(what):
    sys.stdout.write(what)


bytes = []
line = r()
byte_num = 0
while line != '':
    for char in line:
        bytes.append(char)
#        print 'byte num:', byte_num
        byte_num += 1
    line = r()

my_byte = 19936

print 'number of characters:', byte_num
    
#print 'byte[' + str(my_byte) + '-1]:', bytes[my_byte-1]
#print 'byte[' + str(my_byte) + ']:', bytes[my_byte]

print '_________________________________________\n'









