#! /usr/bin/env python

'''
Created on 05/13
Tuenti Challenge - 
@author: manolo
'''

import sys

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
    

encodings = [(open('./encoding_CCITT-' + c, 'r'), './encoding_CCITT-' + c) for c in ['1', '2', '2_alt']]
encodings_chars = []

for (enc, name) in encodings:
    cod = {'name' : name, 'LTRS': [], 'FIGS': []}
    encodings_chars.append(cod)
    char = enc.readline()[:-1]
    read = 0
    while char != '':
        cod['LTRS' if read < 32 else 'FIGS'].append(char)
        char = enc.readline()[:-1]
        read += 1

changing_chars = ['LTRS', 'FIGS']
no_idea_chars = ['BELL', 'STOP']

print 'encodings:\n'
for enc in encodings_chars:
    for reverse in [True, False]:

        print 'encoding:', enc['name']    
        print 'reverse:', reverse
        print 'LTRS: (' + str(len(enc['LTRS'])) + ')' + str(enc['LTRS'])
        print 'FIGS: (' + str(len(enc['FIGS'])) + ')' + str(enc['FIGS'])

        ifile = open('./web.in', 'r')
        
        result_str = ''
        current_enc = enc['LTRS']
        no_idea = 0
            
        line = r()
        print 'line length:', len(line)

        while line != '':
            
            for char in line:
                c_bin = bin(ord(char))
                code = get_code(c_bin, reverse)
                int_code = int(code, 2)
#                w('\'' + char + '\' - ' + c_bin + ' - ' + code + ' - ' + str(int_code) + '\n')
                decoded_char = current_enc[int_code]
                if decoded_char in changing_chars:
                    current_enc = enc[decoded_char]
                elif decoded_char in no_idea_chars:
                    no_idea += 1
                else:
                    result_str += decoded_char
                            
            line = r()
        
        ifile.close()
        
        print '----------------'
        print 'don\' know what to do with', no_idea, 'chars'
        
        print result_str
        
        print '_________________________________________\n'









