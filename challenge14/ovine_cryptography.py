#! /usr/bin/env python

'''
Created on 05/13
Tuenti Challenge - 
@author: manolo
'''

import sys
import binascii
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def w(what):
    sys.stdout.write(what)


for i in range(13):

    hex_str = r()
    print hex_str

    binary_str = binascii.a2b_hex(hex_str)
    hex_file = open('hex_file_' + str(i), 'wb')
    hex_file.write(binary_str)
    hex_file.close()
    







