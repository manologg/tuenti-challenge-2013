import sys
def w(what):
    sys.stdout.write(what)

words_points = [(7, 'SH'), (11, 'SPA'), (13, 'SPAN'), (8, 'KA'), (11, 'DAK'), (12, 'DAP'), (14, 'DAPS'), (8, 'DAD'), (7, 'DAN'), (9, 'PA'), (12, 'PAD'), (14, 'PADS'), (12, 'PAD'), (11, 'PAN'), (11, 'DAK'), (8, 'DAD'), (10, 'DADS'), (12, 'DAP'), (14, 'DAPS'), (7, 'DAN'), (5, 'AD'), (7, 'ADS'), (8, 'ADD'), (5, 'AD'), (8, 'ADD'), (8, 'ADD'), (10, 'ADDS'), (4, 'AN'), (7, 'AND'), (9, 'ANDS'), (4, 'NA'), (11, 'NAP'), (13, 'NAPS')]
seconds = 50

#print 'words_points = ' + str(words_points)

def sort_words(words_points):
    sorted_words_points = []
    for (points, word) in words_points:
        sorted_words_points.append((points/float(len(word)+1), points, word))
    sorted_words_points.sort()
    sorted_words_points.reverse()
    return sorted_words_points
    

# SORT WORDS
words_points.sort()
words_points.reverse()
sorted_words_points = sort_words(words_points)

# PRINT
for (points, word) in words_points:
    print '\'' + word + '\' (' + str(len(word) +1) + 's) => ' + str(points)
print '---'
for (rate, points, word) in sorted_words_points:
    print '(' + str(rate) + ')\'' + word + '\' (' + str(len(word) +1) + 's) => ' + str(points)
print '________\n'

# SELECT WORDS
submitted_words = []
total_points = 0
i = 0
while seconds > 0 and i < len(sorted_words_points):
    w('seconds left: ' + str(seconds))
    (rate, points, word) = sorted_words_points[i]
    if word not in submitted_words:
        if seconds >= len(word) + 1:
            w(' -> ' + word + ' TAKE IT!')
            seconds -= (len(word) +1)
            submitted_words.append(word)
            total_points += points
        else:
            w(' -> ' + word + ' no time')
    else:
        w(' -> ' + word + ' already submitted')
    w('\n')
    i += 1
       

# PRINT
print 'words: ' + str(submitted_words)
print 'total points: ' + str(total_points)
print 'seconds left: ' + str(seconds)

print total_points
