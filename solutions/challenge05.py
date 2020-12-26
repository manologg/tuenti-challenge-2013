#! /usr/bin/env python

'''
Created on 30/04/13
Tuenti Challenge - 5
@author: manolo
'''

import sys
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def inside(i, j):
    return i > -1 and j > -1 and i < height and j < width

def max_points_possible_2(sec, dungeon, (x, y)):

    val = 0
    for i in range(x-sec, x+sec+1):
        for j in range(y-sec, y+sec+1):
            if (i,j) != (x,y) and inside(i,j):
                val += dungeon[i][j]
            
    return val


def max_points_possible(sec, (t_1, t_2, t_5)):

    val = 0
    while sec > 0:
        if t_5 > 0:
            t_5 -= 1
            val += 5
        elif t_2 > 0:
            t_2 -= 1
            val += 2
        elif t_1 > 0:
            t_1 -= 1
            val += 1
        sec -=1
        
    return val
            

# search path using branch and bound
def search_path(dungeon, (x, y), (last_x, last_y), seconds_left, points):

    # CALCULATE MAX
    global max_points
    max_points = max(max_points, points)
    if max_points == max_ammount_of_points:
        return
    
    if seconds_left == 0:
        return

    if seconds_left * 5 + points < max_points:
        return
    if max_points_possible_2(seconds_left, dungeon, (x, y)) + points < max_points:
        return

    # LOOP ITSELT
    for (i,j) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if (i, j) != (last_x, last_y) and inside(i,j):
            old_v = dungeon[i][j]
            dungeon[i][j] = 0
            search_path(dungeon, (i, j), (x, y), seconds_left - 1, points + old_v)
            dungeon[i][j] = old_v


T = int(r())
for case in range(1,T+1):

    (width, height) = [int(x) for x in r().split(',')]
    dungeon = []
    for i in range(height):
        row = [0] * width
        dungeon.append(row)
    
        
    (x0, y0) = [int(x) for x in r().split(',')]
    
    seconds = int(r())
    
    n_gems = int(r())
    
    g_poss = r().split('#')
    if len(g_poss) != n_gems:
        raise 'len(g_poss) != n_gems (' + str(len(g_poss)) + ' != ' + str(n_gems) + ')'
    
    total_gems = []
    for gem_pos in g_poss:
        (i, j, k) = [int(x) for x in gem_pos.split(',')]
        total_gems.append(k)
        dungeon[i][j] = k
    
    total_gems_1 = len([x for x in total_gems if x == 1])
    total_gems_2 = len([x for x in total_gems if x == 2])
    total_gems_5 = len([x for x in total_gems if x == 5])
    max_ammount_of_points = max_points_possible(seconds, (total_gems_1, total_gems_2, total_gems_5))

    max_points = 0    
    max_seconds = seconds  
      
    search_path(dungeon, (x0, y0), (None, None), seconds, 0)
    
    print max_points
    






