#! /usr/bin/env python

'''
Created on 29/04/13
Tuenti Challenge - 6
@author: manolo
'''

import sys
from copy import deepcopy
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def inside(i, j):
    return i > -1 and j > -1 and i < height and j < width
    
def print_cave(cave, (x,y)):
    sys.stdout.write('\n     ')
    for i in range(len(cave[0])):
        sys.stdout.write('(' + str(i) + ') ')
    sys.stdout.write('\n\n')
    for i in range(len(cave)):
        sys.stdout.write('(' + str(i) + ')   ')
        for j in range(len(cave[0])):
            if (i,j) == (x,y):
                sys.stdout.write('X   ')
            else:
                sys.stdout.write(cave[i][j] + '   ')
        sys.stdout.write('\n\n')

def move(cave, (x,y)):
    positions = []
    
#    print 'we\'re in (' + str(x) + ', ' + str(y) + ')'
    
    #right
#    print '* go right'
    new_y = y
    for i in range(y+1, width):
#        sys.stdout.write('    try to go to (' + str(x) + ', ' + str(i) + ')')
        if inside(x, i) and cave[x][i] != '#':
            new_y = i
#            print ' -> good, go on'
        else:
#            print ' -> stop'
            break
#    print '    add (' + str(x) + ', ' + str(new_y) + ')'
    positions.append((x, new_y, abs(new_y-y)))
    
    #left
#    print '* go left'
    new_y = y
    for i in range(y-1, -1, -1):
#        sys.stdout.write('    try to go to (' + str(x) + ', ' + str(i) + ')')
        if inside(x, i) and cave[x][i] != '#':
            new_y = i
#            print ' -> good, go on'
        else:
#            print ' -> stop'
            break
#    print '    add (' + str(x) + ', ' + str(new_y) + ')'
    positions.append((x, new_y, abs(new_y-y)))
    
    #down
#    print '* go down'
    new_x = x
    for i in range(x+1, height):
#        sys.stdout.write('    try to go to (' + str(i) + ', ' + str(y) + ')')
        if inside(i, y) and cave[i][y] != '#':
            new_x = i
#            print ' -> good, go on'
        else:
#            print ' -> stop'
            break
#    print '    add (' + str(new_x) + ', ' + str(y) + ')'
    positions.append((new_x, y, abs(new_x-x)))

    #up
#    print '* go up'
    new_x = x
    for i in range(x-1, -1, -1):
#        sys.stdout.write('     try to go to (' + str(i) + ', ' + str(y) + ')')
        if inside(i, y) and cave[i][y] != '#':
            new_x = i
#            print ' -> good, go on'
        else:
#            print ' -> stop'
            break
#    print '    add (' + str(new_x) + ', ' + str(y) + ')'
    positions.append((new_x, y, abs(new_x-x)))
    
    return positions

from time import sleep
# search path using branch and bound
def search_path(cave, (x, y), visited, seconds):

    global min_secs, start_stop

    # PRINT
    sleep(1)
    print 'cave:'
    print_cave(cave, (x,y))
#    print '(' + str(x) + ', ' + str(y) + ') [' + str(seconds) + ' seconds] (min = ' + str(min_secs) + ')'
    

    # SOLUTION FOUND
    if cave[x][y] == 'O':
        min_secs = min(min_secs, seconds)
#        print 'EXIT FOUND!!! (' + str(x) + ', ' + str(y) + ') [' + str(seconds) + ' seconds]'
        return
    
    seconds += start_stop
    
    
    # TOO LONG
    if seconds > min_secs:
        return

    # LOOP ITSELT
    for (i, j, d) in move(cave, (x,y)):
#        sys.stdout.write('trying: (' + str(i) + ', ' + str(j) + ')')
        if (i, j) != (x, y) and (i,j) not in visited:
#            print ' --> good one!'
            visited2 = deepcopy(visited)
            visited2.append((x,y))
            search_path(cave, (i, j), visited2, seconds + (d/speed))
#        else:
#            if (i,j) in visited:
#                print ' --> already visited'
#            else:
#                print ' --> the same as (' + str(x) + ', ' + str(y) + ')'



T = int(r())
for case in range(1,T+1):

    (width, height, speed, start_stop) = [int(x) for x in r().split(' ')]
    cave = []
    for i in range(height):
        row = ''
        for x in r():
            if x == '#' or x == 'O' or x == 'X':
                row += x
            else:
                row += '.'
        cave.append([c for c in row.replace('..', '_')])
    
    for i in range(len(cave)):
        for j in range(len(cave[i])):
            if cave[i][j] == 'X':
                cave[i][j] = '_'
                (x0, y0) = (i,j)
                break
    
#    print 'cave:'
#    print_cave(cave, (x0,y0))
    
    speed = float(speed)
#    print 'dimensions: ' + str(width) + 'x' + str(height)
#    print 'you slide at ' + str(speed) + ' m/s'
#    print 'you have to wait ' + str(start_stop) + ' seconds before starting after a move'
#    print 'you are at (' + str(x0) + ', ' + str(y0) + ')'
    
    min_secs = float('inf')
    
    search_path(cave, (x0, y0), [], 0)
    
#    print '\nmin seconds: ' + str(round(min_secs))
    print int(round(min_secs))
    
#    print '__________________________________________'
#    print ''

    
