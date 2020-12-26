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
    
def move(cave, (x,y)):
    positions = []
    
    #right
    new_y = y
    for i in range(y+1, width):
        if inside(x, i) and cave[x][i] != '#':
            new_y = i
        else:
            break
    positions.append((x, new_y, abs(new_y-y)))
    
    #left
    new_y = y
    for i in range(y-1, -1, -1):
        if inside(x, i) and cave[x][i] != '#':
            new_y = i
        else:
            break
    positions.append((x, new_y, abs(new_y-y)))
    
    #down
    new_x = x
    for i in range(x+1, height):
        if inside(i, y) and cave[i][y] != '#':
            new_x = i
        else:
            break
    positions.append((new_x, y, abs(new_x-x)))

    #up
    new_x = x
    for i in range(x-1, -1, -1):
        if inside(i, y) and cave[i][y] != '#':
            new_x = i
        else:
            break
    positions.append((new_x, y, abs(new_x-x)))
    
    return positions

# search path using branch and bound
def search_path(cave, (x, y), visited, seconds):

    global min_secs, start_stop

    # SOLUTION FOUND
    if cave[x][y] == 'O':
        min_secs = min(min_secs, seconds)
        return
    
    seconds += start_stop
    
    
    # TOO LONG
    if seconds > min_secs:
        return

    # LOOP ITSELT
    for (i, j, d) in move(cave, (x,y)):
        if (i, j) != (x, y) and (i,j) not in visited:
            visited2 = deepcopy(visited)
            visited2.append((x,y))
            search_path(cave, (i, j), visited2, seconds + (d/speed))



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
    
    
    speed = float(speed)
    
    min_secs = float('inf')
    
    search_path(cave, (x0, y0), [], 0)
    
    print int(round(min_secs))
    
    
