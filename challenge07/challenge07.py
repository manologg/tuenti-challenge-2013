#! /usr/bin/env python

'''
Created on 02/05/13
Tuenti Challenge - 7
@author: manolo
'''

import sys
from copy import deepcopy
import json
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def sort_words(words_points):
    sorted_words_points = []
    for (points, word) in words_points:
        sorted_words_points.append((points/float(len(word)+1), points, word))
    sorted_words_points.sort()
    sorted_words_points.reverse()
    return sorted_words_points
    
# returns (valid, continue, current_i)
def valid(word, start_i):
    global count
    for i in range(start_i, len_valid_word):
        count += 1
        dict_word = valid_words[i]
        if dict_word == word:
            return (True, True, i)
        elif dict_word > word:
            if dict_word.startswith(word):
                return (False, True, i)
            else:
                return (False, False, None)
    return (False, False, None)


def adjacents(x, y):
    res = []
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if (i,j) != (x,y):
                res.append((i,j))
    return res


def inside(i, j):
    return i > -1 and j > -1 and i < n_rows and j < n_cols


# get words using branch and bound
def get_words((x, y), visited, word, start_i):


    global board, valid_words, found_words, seconds

    new_word = word + board[x][y][0]
    
    # TOO LONG WORD
    if (len(new_word) + 1) > seconds:
        return
    
    # VISITED - DEEP COPY
    visited2 = deepcopy(visited)
    visited2.append((x,y))
    
    # VALID WORD --> ADD IT
    (valid_word, shall_continue, current_i) = valid(new_word, start_i);
    if valid_word:
        found_words.append((new_word, visited2))
    if not shall_continue:
        return
    else:
        pass
    
    # LOOP ITSELT
    for (i,j) in adjacents(x, y):
        if inside(i,j) and (i,j) not in visited:
            get_words((i, j), visited2, new_word, current_i)


# GET VALID WORDS
valid_words = []
dictionary = open('./boozzle-dict.txt', 'r')
word = dictionary.readline()[:-1]
max_len = 0
while word != '':
    max_len = max(max_len, len(word))
    valid_words.append(word)
    word = dictionary.readline()[:-1]
valid_words.sort()
len_valid_word = len(valid_words)

T = int(r())
for case in range(1,T+1):
    
    # READ ALL
    char_values = json.loads(r().replace('\'', '\"'))
    min_char_value = min(char_values.values())
    seconds = int(r())
    n_rows = int(r())
    n_cols = int(r())
    board = []
    for i in range(n_rows):
        line = r().split(' ')
        row = []
        for i in range(n_cols):
            elem = line[i]
            row.append((elem[0], int(elem[1]), int(elem[2])))
        board.append(row)
    
    # INIT
    count = 0
    found_words = []
    
    # DO
    for i in range(n_rows):
        for j in range(n_cols):
            get_words((i, j), [], '', 0)
    
    # CALCULATE POINTS
    #    board[i][j][1] - multiplier type (1 => CM, 2 => WM)
    #    board[i][j][1] - multiplier type (1 => CM, 2 => WM)
    #    board[i][j][2] - multiplier value in [1..3]
    words_points = []
    for word, positions in found_words:
        base_points = 0
        word_mults = [1]
        for (i, j) in positions:
            if board[i][j][1] == 1:
                base_points += char_values[board[i][j][0]] * board[i][j][2]
            else:
                base_points += char_values[board[i][j][0]]
                word_mults.append(board[i][j][2])
        
        points = base_points * max(word_mults) + len(word)
        words_points.append((points, word))
        
    # SORT WORDS
    sorted_words_points = sort_words(words_points)

    # SELECT WORDS
    submitted_words = []
    total_points = 0
    i = 0
    while seconds > 0 and i < len(sorted_words_points):
        (rate, points, word) = sorted_words_points[i]
        if word not in submitted_words:
            if seconds >= len(word) + 1:
                seconds -= (len(word) +1)
                submitted_words.append(word)
                total_points += points
        i += 1

    print total_points








