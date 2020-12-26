#! /usr/bin/env python

'''
Created on 05/13
Tuenti Challenge - 
@author: manolo
'''

import sys

ifile = sys.stdin
def r():
    return ifile.readline()[:-1]

def w(what):
    sys.stdout.write(what)


def get_code(c_bin, reverse):

    if reverse:
        if len(c_bin) == 9:
            return c_bin[3:-1][::-1]
        else:
            return c_bin[2:-1][::-1]
    else:
        if len(c_bin) == 9:
            return c_bin[2:-2]
        else:
            return '0' + c_bin[2:-2]
    
encoding_name = './encoding_CCITT-1'
reverse = False

encoding_file = open(encoding_name, 'r')
enc = {'LTRS': [], 'FIGS': []}
char = encoding_file.readline()[:-1]
read = 0
while char != '':
    enc['LTRS' if read < 32 else 'FIGS'].append(char)
    char = encoding_file.readline()[:-1]
    read += 1
encoding_file.close()

changing_chars = ['LTRS', 'FIGS']



#print 'encoding:', encoding_name   
#print 'reverse:', reverse
#print 'LTRS: (' + str(len(enc['LTRS'])) + ')' + str(enc['LTRS'])
#print 'FIGS: (' + str(len(enc['FIGS'])) + ')' + str(enc['FIGS'])

    
result_str = ''
line = r()
while line != '':
    
    current_enc = enc['LTRS']
    for char in line:
        c_bin = bin(ord(char))
        code = get_code(c_bin, reverse)
        int_code = int(code, 2)
#        w('\'' + char + '\' - ' + c_bin + ' - ' + code + ' - ' + str(int_code) + '\n')
        decoded_char = current_enc[int_code]
        if decoded_char in changing_chars:
            current_enc = enc[decoded_char]
        else:
            result_str += decoded_char
                    
    line = r()

ifile.close()
print result_str

chars = {}
for c in result_str:
    if c in chars.keys():
        chars[c] += 1
    else:
        chars[c] = 1

#for k in sorted(chars.keys()):
#    print ' ' + k + ' -->', chars[k]
 
#print '_________________________________________\n'









