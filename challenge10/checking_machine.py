#! /usr/bin/env python

'''
Created on 03/05/13
Tuenti Challenge - 10
@author: manolo
'''

import sys
import hashlib
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

#def w(what):
#    sys.stdout.write(what)

#def print_tree(tree):
#    print_node(tree, 0)
    
#def print_node(node, depth):
#    for elem in node:
#        if type(elem) == list:
#            print '  ' * depth + '`'
#            print_node(elem, depth + 1)
#        else:
#            print '  ' * depth + '-' + elem

# a2[b3[c]]
# md5.new("a" + 2 * ("b" + 3 * "c")).hexdigest()

def make_tree():
    return get_tree(0, 0)

def get_tree(i, depth):
    nums = 0
#    print '    ' * depth + 'line: ' + line[i:]
    digits = ''
    node = []
    while i < len(line):
        char = line[i]
#        print '    ' * depth + '[' + str(i) + '] --> ' + char
        if char.isdigit():
            digits += char
#            print '    ' * depth + 'digit --> digits = ' + digits
        elif char == '[':
            mult = int(digits)
            (tree, new_i, new_nums) = get_tree(i+1, depth+1)
            for i in range(mult):
                node.append(tree)
#            print '    ' * depth + 'append ' + str(mult) + ' times the tree'
#            print '    ' * depth + 'node: ' + str(node)
#            print '    ' * depth + 'new_i: ' + str(new_i)
#            print '  ' * depth + 'new_nums: ' + str(new_nums)
            nums += (mult * new_nums)
#            print '  ' * depth + 'nums: ' + str(nums)
            digits = ''
            i = new_i
        elif char == ']':
#            print '    ' * depth + 'return node: ' + str(node)
#            print_tree(node)
            return (node, i, nums)
        else:
            node.append(char)
            nums += 1
#            print '    ' * depth + 'char --> node: ' + str(node)
        i += 1
    
#    print '    ' * depth + 'RETURN node: ' + str(node)
#    print_tree(node)
    return (node, i, nums)

# traverse the tree to add characters to md5_word
def traverse(node):
    global md5_processor, md5_word
    for elem in node:
        if type(elem) == list:
            traverse(elem)
        else:
#            md5_word += elem
            md5_processor.update(elem)

line = r()
while (line != ''):
    (tree, analized, nums) = make_tree()
#    print line
#    print nums
    
#    print 'analized...'
#    print '**********************'
#    print 'len(line): ' + str(len(line))
#    print 'alanlized: ' + str(analized)
#    print '**********************'
#    print '------------------------------'
#    print tree
#    print_tree(tree)
#    print '------------------------------'
    md5_processor = hashlib.md5()
#    md5_word = ''
    traverse(tree)
#    print 'tree traversed'
    md5sum = md5_processor.hexdigest()

#    print line + ':'
#    print md5_word + '\t-->\t' + md5sum
#    print '_______________________________________________________________\n'
    print md5sum

#    print md5sum_alt

    line = r()



