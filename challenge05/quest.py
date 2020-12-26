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

#    print 'secs = ' + str(sec)
    val = 0
    for i in range(x-sec, x+sec+1):
        for j in range(y-sec, y+sec+1):
            if (i,j) != (x,y) and inside(i,j):
                val += dungeon[i][j]
            
#    print 'val: ' + str(val)
    return val
            

def max_points_possible(sec, (t_1, t_2, t_5)):

#    print 'secs = ' + str(sec)
#    print 'sec*5: ' + str(sec*5)
    
    val = 0
    while sec > 0:
#        print 'secs = ' + str(sec)
        if t_5 > 0:
            t_5 -= 1
            val += 5
#            print '5 => val = ' + str(val)
        elif t_2 > 0:
            t_2 -= 1
            val += 2
#            print '2 => val = ' + str(val)
        elif t_1 > 0:
            t_1 -= 1
            val += 1
#            print '1 => val = ' + str(val)
        sec -=1
        
#    print 'val: ' + str(val)
    
    return val
    
def print_dungeon(dungeon, (x,y)):
    sys.stdout.write('     ')
    for i in range(len(dungeon[0])):
        sys.stdout.write('(' + str(i) + ') ')
    sys.stdout.write('\n\n')
    for i in range(len(dungeon)):
        sys.stdout.write('(' + str(i) + ')   ')
        for j in range(len(dungeon[0])):
            if i == x and j == y:
                sys.stdout.write('x')
            else:
                sys.stdout.write(str(dungeon[i][j]))
            if j != len(dungeon[0])-1:
                sys.stdout.write(' - ')
        sys.stdout.write('\n')
        sys.stdout.write('      ')
        if i != len(dungeon)-1:
            for j in range(len(dungeon[0])):
                sys.stdout.write('|   ')
            sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.flush()


# search path using branch and bound
def search_path(dungeon, (x, y), (last_x, last_y), seconds_left, points):#, (t_1, t_2, t_5)):

#    print '------------------------'
#    print 'dungeon:'
#    print_dungeon(dungeon, (x, y))
    
    # CALCULATE MAX
    global max_points
    max_points = max(max_points, points)
    if max_points == max_ammount_of_points:
#        print 'we got max! ' + str(max_ammount_of_points)
        return
    
#    tabs = ' - ' * (max_seconds - seconds_left)
    if seconds_left == 0:
#        print tabs + '(' + str(x) + ', ' + str(y) + ') [' + str(points) + ' points] (max = ' + str(max_points) + ')'
        return
#    else:
#        print tabs + '(' + str(x) + ', ' + str(y) + ') [' + str(points) + '] (max = ' + str(max_points) + ')'


    if seconds_left * 5 + points < max_points:
        return
#    if max_points_possible(seconds_left, (t_1, t_2, t_5)) + points < max_points:
##        print 'Ahhh!!!'
#        return
    if max_points_possible_2(seconds_left, dungeon, (x, y)) + points < max_points:
#        print 'Ahhh!!!2'
        return

        
    # LOOP ITSELT
    for (i,j) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if (i, j) != (last_x, last_y) and inside(i,j):
            old_v = dungeon[i][j]
            dungeon[i][j] = 0
#            d_1 = 0
#            d_2 = 0
#            d_5 = 0
#            if old_v == 1:
#                d_1 = 1
#            elif old_v == 2:
#                d_2 = 1
#            elif old_v == 5:
#                d_5 = 1
#            elif old_v != 0:
#                raise Exception('old_v = ' + str(old_v))
            search_path(dungeon, (i, j), (x, y), seconds_left - 1, points + old_v)#, (t_1 - d_1, t_2 - d_2, t_5 - d_5))
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
#        print 'gem in (' + str(i) + ', ' + str(j) + ') with value ' + str(k)
        dungeon[i][j] = k
    
    total_gems_1 = len([x for x in total_gems if x == 1])
    total_gems_2 = len([x for x in total_gems if x == 2])
    total_gems_5 = len([x for x in total_gems if x == 5])
#    print 'total 1s: ' + str(total_gems_1)
#    print 'total 2s: ' + str(total_gems_2)
#    print 'total 5s: ' + str(total_gems_5)

#    print 'we start in (' + str(x0) + ', ' + str(y0) + ')'
#    print 'we have ' + str(seconds) + ' seconds'
#    print 'there are ' + str(n_gems) + ' gems'
#    print 'dungeon:'
#    print_dungeon(dungeon, (x0, y0))

#    global max_points
    max_points = 0
    max_ammount_of_points = max_points_possible(seconds, (total_gems_1, total_gems_2, total_gems_5))
#    print 'max_ammount_of_points: ' + str(max_ammount_of_points)
    
    max_seconds = seconds  
      
    search_path(dungeon, (x0, y0), (None, None), seconds, 0)#, (total_gems_1, total_gems_2, total_gems_5))
    
#    print 'max_points: ' + str(max_points)
    print max_points
    
#    print '__________________________________________'
#    print ''








