# True  => add the word and continue
# False => DON'T add the word and continue
# None  => DON'T add the word and DON'T continue

# returns (valid, continue, current_i)
def c(word, start_i):
    for i in range(start_i, len_d):
        dict_word = d[i]
        if dict_word == word:
            print dict_word + ' == ' + word
            return (True, True, i)
        elif dict_word > word:
            sys.stdout.write(dict_word + ' > ' + word)
            if dict_word.startswith(word):
                print ' -> ' + dict_word + ' starts with ' + word
                return (False, True, i)
            else:
                print ' -> ' + dict_word + ' DOES NOT start with ' + word
                return (False, False, None)
        else:
            print dict_word + ' < ' + word
    return (False, False, None)

