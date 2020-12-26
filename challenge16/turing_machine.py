#! /usr/bin/env python

'''
Created on 07/05/13
Tuenti Challenge - 16
@author: manolo
'''

import sys
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]

def w(what):
    sys.stdout.write(what)


script_file = open('./script', 'r')
line = script_file.readline()[:-1]
commands = []
while line != '':
    state, old_new_chr, movement, new_state = line.split(',')
    old_chr, new_chr = old_new_chr.split(':')
    commands.append((state, old_chr, new_chr, movement, new_state))
    line = script_file.readline()[:-1]


# COMMAND: state,character:character_to_write,movement,new_state
def process(tape, pos, state):

    while state != 'end':
    
        current_chr = tape[pos]
        
        command = filter(lambda c : c[0] == state and c[1] == current_chr, commands)
        if len(command) > 1:
            raise Exception('more than one command possible!!!')
        else:
            command = command[0]
        
        state, old_chr, new_chr, movement, new_state = command
        
        if pos < len(tape):
            tape[pos] = new_chr
        else:
            tape.append(new_chr)
        
        if movement == 'R':
            pos += 1
            if pos >= len(tape):
                tape.append('_')
        elif movement == 'L':
            pos -= 1
            if pos < 0:
                pos = 0
        elif movement != 'S':
            raise Exception('movement must be R, L or S')
        
        state = new_state

line = r()
while line != '':

    tape = list(line)
    process(tape, 0, 'start')
    new_line = ''.join(tape)
    print new_line.rstrip('_')
    
    line = r()

