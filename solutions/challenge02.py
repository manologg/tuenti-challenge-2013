#! /usr/bin/env python

'''
Created on 29/04/13
Tuenti Challenge - 2
@author: manolo
'''

import sys
from itertools import permutations
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]
    
def is_suggestion(word, dict_word):
    a = list(word)
    a.sort()
    b = list(dict_word)
    b.sort()
    return a == b

comment = r()
dictionary = r()
comment = r()
n_words = int(r())
comment = r()

# WORDS
words = []
suggestions = {}
for case in range(1, n_words+1):
    word = r()
    words.append(word)
    suggestions[word] = []

# DICTIONARY
dict_file = open('./' + dictionary, 'r')
dict_word = dict_file.readline()
while (dict_word != ''):
    dict_word = dict_word[:-1]
    for word in words:
        if is_suggestion(word, dict_word) and word != dict_word:
            suggestions[word].append(dict_word)
    dict_word = dict_file.readline()

for word in words:
    sys.stdout.write(word + ' -> ' + ' '.join(suggestions[word]) + '\n')
    
        
        
        
