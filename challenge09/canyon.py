#! /usr/bin/env python

'''
Created on 02/05/13
Tuenti Challenge - 9
@author: manolo
'''

import sys
ifile = sys.stdin
from time import sleep

def r():
    return ifile.readline()[:-1]

def w(what):
    sys.stdout.write(what)

def print_canyon(canyon):
    for row in canyon:
        w('# ')
        for cell in row:
            w(cell + ' ')
        w('#\n')

def safe(canyon):
    return not any([x == 'v' for x in canyon[-1]])

def zorglings_appear(canyon):
    # last row
    for i in range(len(canyon[-2])):
        if canyon[-2][i] == 'v':
            canyon[-1][i] = canyon[-2][i]
    # iterate
    for i in range(len(canyon)-2, 0, -1):
        canyon[i] = canyon[i-1]
    # first row
    canyon[0] = new_row = ['v'] * width

def the_end_is_close(canyon):
    return any([x == 'v' for x in canyon[-2]])
    
def use_crematorium():
    canyon = [['.'] * width] * length
    canyon.append(['O'] * width)
    return canyon

def attack(canyon, soldiers):
    for i in range(len(canyon)-2, -1, -1):
        row = canyon[i]
        for j in range(len(row)):
            if row[j] == 'v':
                row[j] = '.'
                soldiers -= 1
#                print 'one soldier attacks'
                if soldiers == 0:
                    return
            

def simulate(width, length, soldiers, crematoriums):

    canyon = [['.'] * width] * length
    canyon.append(['O'] * width)
    
    seconds = 0
    zorglings = 0
    while safe(canyon):

        seconds += 1
        
        # zorglings appear
#        sleep(0.1)
        zorglings_appear(canyon)
        zorglings += width
#        print_canyon(canyon)
#        print '\nzorglings appear: ' + str(zorglings)+ ' zorglings - t = ' + str(seconds) + 's\n'
        
        # we attack
        if soldiers > 0:
#            sleep(0.1)
            attack(canyon, soldiers)
            zorglings -= soldiers
#            print_canyon(canyon)
#            print '\nwe attack: ' + str(zorglings)+ ' zorglings - t = ' + str(seconds) + 's\n'
        
        if crematoriums > 0 and the_end_is_close(canyon):
#            sleep(0.5)
            canyon = use_crematorium()
            zorglings = 0
            crematoriums -= 1
#            print_canyon(canyon)
#            print '\nwe use the crematorium: ' + str(zorglings)+ ' zorglings - t = ' + str(seconds) + 's\n'
#            sleep(1)

#        print '------------------------------------------'        
#        sleep(1)
    
    return seconds-1

def simulate2(width, length, soldiers, crematoriums):

    zorglings = 0
    seconds = 0
    max_zorglings = width * length
    while True:

        seconds += 1
        
        # zorglings appear
        zorglings += width
#        print 'zorglings appear: ' + str(zorglings)+ ' zorglings - t = ' + str(seconds) + 's'

        if zorglings > max_zorglings:
            break
        
        # we attack
        if soldiers > 0:
            zorglings -= soldiers
#            print 'we attack: ' + str(zorglings)+ ' zorglings - t = ' + str(seconds) + 's'
        
        if crematoriums > 0 and zorglings > (max_zorglings - width):
            zorglings = 0
            crematoriums -= 1
#            print 'we use the crematorium: ' + str(zorglings)+ ' zorglings - t = ' + str(seconds) + 's'
    
    return seconds-1
    
def simulate3(width, length, soldiers, crematoriums):

    zorglings = 0
    
    max_zorglings = width * length
    print 'max_zorglings: ' + str(max_zorglings)
    zorglings_per_sec = width - soldiers
    print 'zorglings: ' + str(zorglings)
    print 'width: ' + str(width)
    print 'zorglings_per_sec: ' + str(zorglings_per_sec)
    zorglings += width
    seconds = 1
    while zorglings <= max_zorglings:
        zorglings += zorglings_per_sec
        seconds += 1
    
    print 'seconds: ' + str(seconds)
    print '----'

    if crematoriums == 0:
        return seconds - 1
    else:
        return (seconds - 1) * (crematoriums + 1)

def simulate4(width, length, soldiers, crematoriums):

    max_zorglings = width * length
    zorglings_per_sec = width - soldiers

#    print 'max_zorglings: ' + str(max_zorglings)
#    print 'zorglings_per_sec: ' + str(zorglings_per_sec)
#    print 'width: ' + str(width)

    seconds = int((max_zorglings-width)/zorglings_per_sec) + 1

#    print 'seconds: ' + str(seconds)
#    print '----'

    return seconds * (crematoriums + 1)
        

T = int(r())
for case in range(1,T+1):
    
    (width, length, soldier_price, crematorium_price, gold) = [int(c) for c in r().split(' ')]
    
#    print "Canyon is " + str(width) + ' m wide and ' + str(length) + ' m long'
#    print 'A soldier costs ' + str(soldier_price) + ' gold pieces'
#    print 'The crematorium costs ' + str(crematorium_price) + ' gold pieces'
#    print 'You have ' + str(gold) + ' pieces of gold\n'
    
#    print_canyon(canyon)
#    print '\ncanyon: t=0s\n'
#    print canyon

    if gold/soldier_price >= width:
        print -1
    else:
#        time2 = []
        time3 = []
        max_crematoriums = (gold/crematorium_price) + 1
        for crematoriums in range(max_crematoriums):
            
#            print str(crematoriums) + ' crematoriums'
            gold_left = gold - (crematoriums * crematorium_price)
#            print 'gold left: ' + str(gold_left)
            soldiers = gold_left/soldier_price
#            print str(soldiers) + ' soldiers'
#            seconds2 = simulate2(width, length, soldiers, crematoriums)
            seconds3 = simulate4(width, length, soldiers, crematoriums)
#            print str(seconds2) + ' - ' + str(seconds3) + ' => ' + ('OK' if seconds2 == seconds3 else '!!!!!!!!!!!!!')
#            print '---' 
#            time.append((seconds, crematoriums))
#            time2.append(seconds2)
            time3.append(seconds3)
#        time.sort()
#        time.reverse()
#        print str(time[0][0]) + ' - ' + str(time[0][1])
#        print str(max(time2)) + ' - ' + str(max(time3))
        print max(time3)
#    print '________________________________________\n'
    
    
