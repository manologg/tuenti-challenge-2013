#! /usr/bin/env python

'''
Created on 29/04/13
Tuenti Chall_sentenge - 3
@author: manolo
'''

import sys
ifile = sys.stdin

def r():
    return ifile.readline()[:-1]
    
def search_prev_dot(delims, i):
    for n in reversed(range(i)):
        if delims[n] == '.':
            return n
    
    raise 'ahhhhh! no \'.\' before!'

T = int(r())
for case in range(1,T+1):
    all_sent = r();
#    print all_sent
#    print "------"
    
    delims = []
    sentences = []
    
    pos = {}
#    equiv = {}
#    equiv_num = 0
    
    min_i = min([x for x in [all_sent.find('.'), all_sent.find('<'), all_sent.find('>')] if x != -1])
    delims.append(all_sent[min_i])
    all_sent = all_sent[min_i+1:]

    while all_sent != '':
        array_i = [x for x in [all_sent.find('.'), all_sent.find('<'), all_sent.find('>')] if x != -1]
        if len(array_i) != 0:
            min_i = min(array_i)
            delims.append(all_sent[min_i])
            new_sent = all_sent[:min_i]
            sentences.append(new_sent)
            pos[new_sent] = None
#            if not new_sent in equiv:
#                equiv[new_sent] = equiv_num
#                equiv_num += 1
            all_sent = all_sent[min_i+1:]
        else:
            sentences.append(all_sent)
            pos[all_sent] = None
#            if not all_sent in equiv:
#                equiv[all_sent] = equiv_num
#                equiv_num += 1
            all_sent = ''

#    num = 0
#    for i in range(len(delims)):
#        print '(' + str(num) + ') ' + delims[i] + ' : ' + sentences[i]
#        num += 1
    
    for i in range(len(delims)):
      
        if delims[i] == '.':
            array = [i]
        elif delims[i] == '<':
            array = []
            prev_dot_i = search_prev_dot(delims, i)
            for j in range(-1, prev_dot_i):
                array.append(j)
        elif delims[i] == '>':
            array = []
            prev_dot_i = search_prev_dot(delims, i)
            for j in range(prev_dot_i+1,len(delims)+1):
                array.append(j)

        if pos[sentences[i]] == None:
            pos[sentences[i]] = set(array)
        else:
            pos[sentences[i]] = pos[sentences[i]].intersection(set(array))
        
#    print "--------------"
#    
#    for poss in pos.keys():
#        print poss + ': ' + str(pos[poss])

#    print "--------------"

    positions = [pos[x] for x in pos.keys()]
    
    if any([len(x) == 0 for x in positions]):
        print 'invalid'
#        print str([len(x) == 0 for x in positions])
    elif len([x for x in positions if -1 in x]) > 1:
        print 'invalid'
#        print str([x for x in positions if -1 in x])
    elif len([x for x in positions if len(positions) in x]) > 1:
        print 'invalid'
#        print str([x for x in positions if len(positions) in x])
    else:
        all_pos = []
        for x in positions:
            all_pos.extend(list(x))
#        print 'list: ' + str(sorted(all_pos))
#        print 'set:  ' + str(sorted(list(set(all_pos))))
        if len(all_pos) != len(set(all_pos)):
            print 'valid'
        else:
#            print 'BLA BLA BLA BLA'
            pos_tuples = [(x,pos[x]) for x in pos.keys()]
#            print pos_tuples
#            print ':::::::::::::::::::'
            pos_tuples.sort(key=lambda x: min(x[1]))
#            print pos_tuples
            story = [x[0] for x in pos_tuples]
#            print '>>>>>>>>>>>>>>>>>>>'
            print ','.join(story)
    
#    print "__________________________________________________________"
#    print ''
    
    





