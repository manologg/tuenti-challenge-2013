
# True  => add the word and continue
# False => DON'T add the word and continue
# None  => DON'T add the word and DON'T continue
def valid(word):
    global valid_words
    for dict_word in valid_words:
        if dict_word == word:
            return True
        elif dict_word > word:
            if dict_word.startswith(word):
                return False
            else:
                return None
    return None
    

valid_words = []

dictionary = open('./boozzle-dict.txt', 'r')
word = dictionary.readline()[:-1]
while word != '':
    valid_words.append(word)
    word = dictionary.readline()[:-1]
valid_words.sort()

print 'valid words: ' + str(len(valid_words))
print valid_words
my_words = ['NONFOOD', 'ASIA', 'HELLO', 'COAT', 'SAMPLE', 'ASD', 'YELL']
import random
for i in range(1000):
    word = valid_words[random.randint(1, len(valid_words))]
    rand_100 = random.randint(1, 100)
    if rand_100 < 33:
        word += 'j'
    elif rand_100 > 33 and rand_100 < 66:
        word = word[0:len(word)/2]
    my_words.append(word)
c = 0
for word in my_words:
#    if word in valid_words:
    if valid(word):
#        print word + ' exists!'
        c += 1
#    else:
#        print word + ' does not exists...'
print str(c) + ' words out of ' + str(len(my_words)) + ' exist'
