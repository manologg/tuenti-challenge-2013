#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 05/05/13
Tuenti Challenge - 11
@author: manolo
'''

import sys
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

ofile = open('./my.out', 'w')
def write(what):
    ofile.write(what + '\n')

def w(what):
    sys.stdout.write(what)

b_char = '█'
w_char = ' '
    

### PRINT ###

#def print_m(name, m):
#    w(name + ': ' + m[0])
#    for i in range(1, len(m), 4):
#        w(' ' + m[i:i+4])
#    w('\n')

#def print_m_array(name, m):
#    w(name + ': ' + str(m[0]))
#    for i in range(1, len(m), 4):
#        w(' ' + ''.join([str(x) for x in m[i:i+4]]))
#    w('\n')

#def print_tree(tree):
#    print_node(tree, 0)
#    
#def print_node(node, depth):
#    if type(node) == list:
#        print '  ' * depth + '`*'
#        for elem in node:
#            print_node(elem, depth + 1)
#    else:
#        print '  ' * depth + ' -' + node

def print_drawing(drawing):
    for row in drawing:
        w(' ' + ' '.join(row) + '\n')


### PREPROCESS ###

def preprocess(m):
    if m[0] != 'p':
        return m[0]
    else:
        next_i = 4
        new_m = [0]
        for char in m[1:]:
            if char == 'p':
                new_m.append(next_i)
                next_i += 4
            else:
                new_m.append(char)
        return new_m


### TREE ###

def get_tree(m, index, d):
    global max_d
    max_d = max(max_d, d)
#    print '    ' * d + 'm:', m[index:index+4]
#    print '    ' * d + 'index:', index
    tree = []
    for i in range(index, index+4):
        elem = m[i]
#        print '    ' * d + '[' + str(i) + '] -->', elem
#        print '    ' * d + 'tree:', tree
        if type(elem) == int:
#            print '    ' * d + 'elem is an int, go to', elem
            go_to = int(elem)
            tree.append(get_tree(m, go_to, d+1))
        else:
#            print '    ' * d + 'elem is an char'
            tree.append(elem)
#        print '    ' * d + 'tree:', tree
#        print '    ' * d + '-------------'
    return tree


def give_me_tree(m):
    if type(m[0]) == int:
        return get_tree(m[1:], 0, 1)
    else:
        return m[0]


### DRAW ###

def fill_square(drawing, x, y, width, elem):
#    print range(x, x + width)
#    print range(y, y + width)
    for i in range(x, x + width):
        for j in range(y, y + width):
            drawing[i][j] = elem

def draw_deep(tree, x, y, drawing, width, d):

    small_width = width / 2

#    print '    ' * d + 'we have to start painting from (' + str(x) + ',' + str(y) + ')'
#    print '    ' * d + 'we have a square of ' + str(width) + 'x' + str(width)
#    print '    ' * d + 'and we\'ll make 4 smaller squares of ' + str(small_width) + 'x' + str(small_width)
#    print '    ' * d + 'tree:', tree

    for i in range(4):
    
        if i == 0:
            (new_x, new_y) = (x, y + small_width)
        elif i == 1:
            (new_x, new_y) = (x, y)
        elif i == 2:
            (new_x, new_y) = (x + small_width, y)
        elif i == 3:
            (new_x, new_y) = (x + small_width, y + small_width)
            
#        print '    ' * d + 'this is element number ' + str(i) + ', we have to start painting from (' + str(new_x) + ',' + str(new_y) + ')'
#        print '    ' * d + 'we\'ll make a square of ' + str(small_width) + 'x' + str(small_width)
        
        elem = tree[i]
        
        if type(elem) == str:
            if elem == 'b':
                to_show = b_char
            else: #if elem == 'w':
                to_show = w_char
                
#            print '    ' * d + 'elem is a str: \'' + elem + '\' --> ' + to_show
            fill_square(drawing, new_x, new_y, small_width, to_show)

        else:
            draw_deep(elem, new_x, new_y, drawing, small_width, d+1)
                
def draw(tree, side):
    if tree == 'b':
        return [[b_char]]
    if tree == 'w':
        return [[w_char]]
    else:
        drawing = []
        for i in range(side):
            drawing.append(['▢'] * side)
#        print drawing
#        print_drawing(drawing)
        draw_deep(tree, 0, 0, drawing, len(drawing), 0)
        return drawing


### SUM ###

def sum_drawings(d1, d2):
    width = len(d1)
    if width != len(d2):
        raise Exception('d1 and d2 must have the same length!')
    
    d = []
    for i in range(width):
        d.append(['▢'] * width)
    for i in range(width):
        for j in range(width):
            if d1[i][j] == b_char or d2[i][j] == b_char:
                d[i][j] = b_char
            else:
                d[i][j] = w_char
    return d

def msg_to_matrix(m):

    global max_d
    max_d = 0
    
#    print 'm:', m
#    print '--------------'

#    print_m('m before', m)
    m_array = preprocess(m)
#    print_m_array(' m after', m_array)
    
#    print '--------------'
    
    tree = give_me_tree(m_array)
#    print 'tree:', tree
#    print_tree(tree)
#    print 'depth:', max_d
    width = 2 ** max_d
    
#    print '--------------'
    
    drawing = draw(tree, width)
    return drawing


### GENERATE QR #####
import Image
import ImageDraw
from qrtools import QR
import zbar

def get_data(file_name):
    code = QR(filename=file_name)
    if code.decode():
#        print 'data:', code.data
#        print 'data type:', code.data_type
#        print 'data to string:', code.data_to_string()
        return code.data
    else:
        return ''
#        print 'no data'

#def show_data_2(file_name):
#    scanner = zbar.ImageScanner()
#    scanner.parse_config('enable')
#    pil = Image.open(file_name).convert('L')
#    width, height = pil.size
#    raw = pil.tostring()
#    image = zbar.Image(width, height, 'Y800', raw)
#    num = scanner.scan(image)
#    if num == 0:
#        print 'no data'
#    else:
#        for symbol in image:
#            print 'type:', symbol.type
#            print 'data:', symbol.data
#    del(image)


coef = 10
black = (255, 255, 255)
white = (0, 0, 0)
border = 0
def generateQR(matrix, filename):

    width = len(matrix)
    size = ((width + border) * coef, (width + border) * coef)
    image = Image.new('RGB', size, black)
    draw = ImageDraw.Draw(image)
    
    for i in range(width):
        for j in range(width):
            if (matrix[j][i] == b_char):
                draw.rectangle([((i+border)*coef, (j+border)*coef), ((i+border)*coef + coef, (j+border)*coef + coef)], white)
            else:
                draw.rectangle([((i+border)*coef, (j+border)*coef), ((i+border)*coef + coef, (j+border)*coef + coef)], black)

    del draw 
    image.save(filename)
    
#    print 'case:', case
#    print '----------------'
#    show_data(filename)
#    print '----------------'
#    show_data_2(filename)
#    print '----------------'

### MAIN ###

T = int(r())
for case in range(1,T+1):
    messages = r().split(' ')
    max_d = 0
    
    m_total = messages[0]
    d_total = msg_to_matrix(m_total)
#    print_drawing(d_total)
    
    for m in messages[1:]:
        d = msg_to_matrix(m)
#        print '\n +\n'
#        print_drawing(d)
        d_total = sum_drawings(d_total, d)
#        print '\n =\n'
#        print_drawing(d_total)

#    print_drawing(d_total)
    filename = './qr_' + str(case) + '.png'
    generateQR(d_total, filename)
    hidden_message = get_data(filename)
    print hidden_message
    
#    print '_______________________________________________________________\n'
    
