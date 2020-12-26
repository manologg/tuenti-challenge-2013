#! /usr/bin/env python

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


##### ENCODINGS #####

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


##### MAIN #####

line = r()
string = ''
while line != '':
    for char in line:
        string += char
    line = r()

lens = len(string)
print 'lens:', lens
lenx = lens - (lens % 4 if lens % 4 else 4)
print 'lenx:', lenx
#padding = 4 - (lens-lenx)
#print 'padding:', padding


##### BASE 64 #####

import base64

decoded_string = base64.b64decode(string[:lenx])# + '=' * padding)
#print 'decoded_string:', decoded_string
print 'size:', len(decoded_string)

filename = 'audio'
print 'file:', filename
audio_file = open(filename, 'w')
audio_file.write(decoded_string)


##### WAV #####

import os
import scikits.audiolab

def get_bit(s):
    if s > 0:
        return 1
    else:
        return 0

os.system('ffmpeg -y -i audio audio.wav >/dev/null 2>&1')
signal, sample_frequency, encoding = scikits.audiolab.wavread(filename + '.wav')
print 'len(signal):', len(signal)
#print 'sample_frequency:', sample_frequency
#print 'encoding:', encoding

seconds = len(signal) / float(sample_frequency)
#print seconds, 'seconds'

bits = []
for s in signal:
    bit = get_bit(s)
#    print s, '-', bit
    bits.append(bit)


#print 'bits = ', bits
#print 'len:', len(bits)

frecs = [170, 850, 2125, 2295, 200, 1955]

#exit()

print '_________________________________________\n'


##### FRECUENCY #####

#group_by = 8
#for frec in frecs:
#    
#    print 'frec:', frec
#    rate = sample_frequency / frec
#    print 'rate:', rate
#    
#    bits_simple = [bits[i] for i in range(0, len(bits), rate)]
#    bits_simple_str = [str(x) for x in bits_simple]
##    print 'bits_simple_str:', bits_simple_str
#    
#    words = [''.join(bits_simple_str[i:i+group_by]) for i in range(0,len(bits_simple), group_by)]
##    print 'words:', words
#    
##    print 'encodings:\n'
#    
#    print '----------------'
#    for enc in encodings_chars:
#    
#        print 'encoding:', enc['name']
#        print '----------------'  
#        for reverse in [True, False]:

#            print 'reverse:', reverse
##            print 'LTRS: (' + str(len(enc['LTRS'])) + ')' + str(enc['LTRS'])
##            print 'FIGS: (' + str(len(enc['FIGS'])) + ')' + str(enc['FIGS'])

#            result_str = ''
#            current_enc = enc['LTRS']
#            no_idea = 0
#                
#            for word in words:
#                
#                c_bin = get_code(word, reverse)
#                if c_bin != '':
#                    int_code = int(c_bin, 2)
##                    w('\'' + word + '\' - ' + c_bin + str(int_code) + '\n')
#                    decoded_char = current_enc[int_code]
#                    if decoded_char in changing_chars:
#                        current_enc = enc[decoded_char]
#                    elif decoded_char in no_idea_chars:
#                        no_idea += 1
#                    else:
#                        result_str += decoded_char
#                                
##            print 'don\' know what to do with', no_idea, 'chars'
#            
#            print result_str
#            print '----------------'
#            
#    print '_________________________________________\n'













