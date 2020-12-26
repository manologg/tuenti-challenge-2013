#! /usr/bin/env python

'''
Created on 04/05/13
Tuenti Challenge - 10
@author: manolo
'''

import sys
import hashlib
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def make_tree():
    return get_tree(0)

def get_tree(i):
    digits = ''
    node = []
    while i < len(line):
        char = line[i]
        if char.isdigit():
            digits += char
        elif char == '[':
            mult = int(digits)
            (tree, new_i) = get_tree(i+1)
            for i in range(mult):
                node.append(tree)
            digits = ''
            i = new_i
        elif char == ']':
            return (node, i)
        else:
            node.append(char)
        i += 1
    
    return (node, i)

# traverse the tree to add characters to md5_word
def traverse(node):
    global md5_processor
    for elem in node:
        if type(elem) == list:
            traverse(elem)
        else:
            md5_processor.update(elem)

line = r()
while (line != ''):

    (tree, i) = make_tree()
    
    md5_processor = hashlib.md5()
    traverse(tree)
    
    md5sum = md5_processor.hexdigest()
    print md5sum
    
    line = r()



