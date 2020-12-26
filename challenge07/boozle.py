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

#def w(what):
#    sys.stdout.write(what)
    
def sort_words(words_points):
    sorted_words_points = []
    for (points, word) in words_points:
        sorted_words_points.append((points/float(len(word)+1), points, word))
    sorted_words_points.sort()
    sorted_words_points.reverse()
    return sorted_words_points
    
# returns (valid, continue, current_i)
def valid(word, start_i):
#    count = 0
    global count
    for i in range(start_i, len_valid_word):
        count += 1
        dict_word = valid_words[i]
        if dict_word == word:
#            print dict_word + ' == ' + word
#            print '                                                                ' + str(count) + ' words were compared'
            return (True, True, i)
        elif dict_word > word:
#            sys.stdout.write(dict_word + ' > ' + word)
            if dict_word.startswith(word):
#                print ' -> ' + dict_word + ' starts with ' + word
#                print '                                                                ' + str(count) + ' words were compared'
                return (False, True, i)
            else:
#                print ' -> ' + dict_word + ' DOES NOT start with ' + word
#                print '                                                                ' + str(count) + ' words were compared'
                return (False, False, None)
#        else:
#            print dict_word + ' < ' + word
#    print '                                                                ' + str(count) + ' words were compared'
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


#def print_board(board):
#    sys.stdout.write('\n     ')
#    for i in range(len(board[0])):
#        sys.stdout.write('(' + str(i) + ')        ')
#    sys.stdout.write('\n\n')
#    for i in range(len(board)):
#        sys.stdout.write('(' + str(i) + ')   ')
#        for j in range(len(board[0])):
#            sys.stdout.write(board[i][j][0] + ' <' + str(board[i][j][1]) + ', ' + str(board[i][j][2]) + '>   ')
#        sys.stdout.write('\n\n')


# get words using branch and bound
def get_words((x, y), visited, word, start_i):


    global board, valid_words, found_words, seconds

    new_word = word + board[x][y][0]
    
    # PRINT
#    print '\n------------------------------'
#    print_board(board)
#    print 'we\'re in (' + str(x) + ', ' + str(y) + ') - visited = ' + str(visited)
#    print 'new word: \'' + new_word + '\''

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
    


    # PRINT
#    w('adjacents:')
#    for (i, j) in adjacents(x, y):
#        w(' (' + str(i) + ', ' + str(j) + ')')
#    w('\n')

    # LOOP ITSELT
    for (i,j) in adjacents(x, y):
#        sys.stdout.write('trying: (' + str(i) + ', ' + str(j) + ')')
        if inside(i,j) and (i,j) not in visited:
#            print ' --> good one!'
            get_words((i, j), visited2, new_word, current_i)
#        else:
#            if not inside(i,j):
#                print ' --> not possible'
#            else:
#                print ' --> already visited'


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

#print 'max len: ' + str(max_len)

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
    
    # PRINT    
#    print 'char values: ' + str(char_values)
#    print 'you have ' + str(seconds) + ' seconds'
#    print 'board (' + str(n_rows) + 'x' + str(n_cols) + '):'
#    print_board(board)
#    print '-----'
#    print board
    
    # INIT
    count = 0
    found_words = []
    
#    total_cells = n_rows * n_cols
#    cells = 0
    # DO
    for i in range(n_rows):
        for j in range(n_cols):
            get_words((i, j), [], '', 0)
#            cells += 1
#            print str(cells/float(total_cells) * 100) + '% done'
    
    # PRINT
#    print 'count: ' + str(count)
#    print 'words found (' + str(len(found_words)) + ')'
#    for word in found_words:
#        print ' * ' + str(word)
   
#    print 'char values: ' + str(char_values)
#    print 'board (' + str(n_rows) + 'x' + str(n_cols) + '):'
#    print_board(board)
    
    # CALCULATE POINTS
    #    board[i][j][1] - multiplier type (1 => CM, 2 => WM)
    #    board[i][j][1] - multiplier type (1 => CM, 2 => WM)
    #    board[i][j][2] - multiplier value in [1..3]
    words_points = []
    for word, positions in found_words:
        base_points = 0
        word_mults = [1]
#        w('word: \'' + word + '\':\t')
        for (i, j) in positions:
            if board[i][j][1] == 1:
#                w('(' + str(char_values[board[i][j][0]]) + ' * ' + str(board[i][j][2]) + ')')
                base_points += char_values[board[i][j][0]] * board[i][j][2]
            else:
#                w('(' + str(char_values[board[i][j][0]]) + ' * 1)')
                base_points += char_values[board[i][j][0]]
                word_mults.append(board[i][j][2])
#            w(' + ')
        
#        w(' WM + lw\t= ' + str(base_points) + ' * ' + str(max(word_mults)) + ' + ' + str(len(word)))
        points = base_points * max(word_mults) + len(word)
#        w(' = ' + str(points) + '\n')
        words_points.append((points, word))
        
    # SORT WORDS
    sorted_words_points = sort_words(words_points)

    # PRINT
#    for (rate, points, word) in sorted_words_points:
#        print '(' + str(rate) + ')\'' + word + '\' (' + str(len(word) +1) + 's) => ' + str(points)
#    print '________\n'

    # SELECT WORDS
    submitted_words = []
    total_points = 0
    i = 0
    while seconds > 0 and i < len(sorted_words_points):
#        w('seconds left: ' + str(seconds))
        (rate, points, word) = sorted_words_points[i]
        if word not in submitted_words:
            if seconds >= len(word) + 1:
#                w(' -> ' + word + ' TAKE IT!')
                seconds -= (len(word) +1)
                submitted_words.append(word)
                total_points += points
#            else:
#                w(' -> ' + word + ' no time')
#        else:
#            w(' -> ' + word + ' already submitted')
#        w('\n')
        i += 1
           

    # PRINT
#    print 'words: ' + str(submitted_words)
#    print 'total points: ' + str(total_points)
#    print 'seconds left: ' + str(seconds)

    print total_points

#    print '__________________________________________'
#    print ''








