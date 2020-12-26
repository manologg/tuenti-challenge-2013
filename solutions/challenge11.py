#! /usr/bin/env python

'''
Created on 05/05/13
Tuenti Challenge - 11
@author: manolo
'''

import sys
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def w(what):
    sys.stdout.write(what)

b_char = 'b'
w_char = 'w'
    

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
    tree = []
    for i in range(index, index+4):
        elem = m[i]
        if type(elem) == int:
            go_to = int(elem)
            tree.append(get_tree(m, go_to, d+1))
        else:
            tree.append(elem)
    return tree


def give_me_tree(m):
    if type(m[0]) == int:
        return get_tree(m[1:], 0, 1)
    else:
        return m[0]


### DRAW ###

def fill_square(drawing, x, y, width, elem):
    for i in range(x, x + width):
        for j in range(y, y + width):
            drawing[i][j] = elem

def draw_deep(tree, x, y, drawing, width, d):

    small_width = width / 2

    for i in range(4):
    
        if i == 0:
            (new_x, new_y) = (x, y + small_width)
        elif i == 1:
            (new_x, new_y) = (x, y)
        elif i == 2:
            (new_x, new_y) = (x + small_width, y)
        elif i == 3:
            (new_x, new_y) = (x + small_width, y + small_width)
            
        elem = tree[i]
        
        if type(elem) == str:
            if elem == 'b':
                to_show = b_char
            else: #if elem == 'w':
                to_show = w_char
                
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
            drawing.append([' '] * side)
        draw_deep(tree, 0, 0, drawing, len(drawing), 0)
        return drawing


### SUM ###

def sum_drawings(d1, d2):
    width = len(d1)
    if width != len(d2):
        raise Exception('d1 and d2 must have the same length!')
    
    d = []
    for i in range(width):
        d.append([' '] * width)
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
    
    m_array = preprocess(m)
    
    tree = give_me_tree(m_array)
    
    width = 2 ** max_d
    
    drawing = draw(tree, width)
    return drawing


### GENERATE QR #####
import Image
import ImageDraw
from qrtools import QR

def get_data(file_name):
    code = QR(filename=file_name)
    if code.decode():
        return code.data
    else:
        return ''

coef = 10
black = (255, 255, 255)
white = (0, 0, 0)
def generateQR(matrix, filename):

    width = len(matrix)
    size = (width * coef, width * coef)
    image = Image.new('RGB', size, black)
    draw = ImageDraw.Draw(image)
    
    for i in range(width):
        for j in range(width):
            if (matrix[j][i] == b_char):
                draw.rectangle([(i*coef, j*coef), (i*coef + coef, j*coef + coef)], white)
            else:
                draw.rectangle([(i*coef, j*coef), (i*coef + coef, j*coef + coef)], black)

    del draw 
    image.save(filename)


### MAIN ###

T = int(r())
for case in range(1,T+1):
    messages = r().split(' ')
    max_d = 0
    
    m_total = messages[0]
    d_total = msg_to_matrix(m_total)
    
    for m in messages[1:]:
        d = msg_to_matrix(m)
        d_total = sum_drawings(d_total, d)

    filename = './qr_' + str(case) + '.png'
    generateQR(d_total, filename)
    hidden_message = get_data(filename)
    print hidden_message
    
