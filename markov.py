#Loads humorous quotes into a markov chain, then attempts to generate new ones
import random

#re-captilizes variations of 'I'
def filter(word):
    if word == 'i':
        return 'I'
    elif word == 'i\'ve':
        return 'I\'ve'
    elif word == 'i\'m':
        return 'I\'m'
    elif word == 'i\'d':
        return 'I\'d'
    else:
        return word

def main():
    print('loading quotes into a Markov chain...')

    #connects to quotes file
    handle = open('jokes.txt', 'r', encoding = 'utf8')


    #dictionaries of the first and second order (go too high and generation turns into regurgitation)
    first, second = dict(), dict()
    first_words = list()
    for line in handle:
        lin = line.split()
        length = len(lin)
        if length == 0: continue
        previous, previous2 = '', ''
        phrase_index = None
        for i, word in enumerate(lin):
            filtered_word = ''
            phrase_end = False
            #gets rid of unnecessary symbols by rebuilding each word, id's phrase conclusions
            for char in word:
                if char in '@#$%^&*()\'\"': continue
                elif char in '.,;:?!':
                    phrase_index = -1
                else: filtered_word += char.lower()

            #conditionals to determine if words should be chained together, and if so, how
            if i == 0 or phrase_index == 0:
                previous = filtered_word
                first_words.append(previous)
                continue
            elif i == 1 or phrase_index == 1:
                if first.get(previous, 0) != 0:
                    first[previous].append(filtered_word)
                else:
                    first[previous] = [filtered_word]
                previous2 = previous
                previous = filtered_word
                continue
            else:
                if second.get((previous2, previous), 0) != 0:
                    second[previous2, previous].append(filtered_word)
                else:
                    second[previous2, previous] = [filtered_word]
                if first.get(previous, 0) != 0:
                    first[previous].append(filtered_word)
                else:
                    first[previous] = [filtered_word]
                previous2 = previous
                previous = filtered_word
                continue
            try:
                phrase_index += 1
            except ValueError:
                continue

    while True:
#loop that gets input from user, always ensures that the input is usable by the program
        Qlen = input('How many quotes do you wish to generate? (enter an integer, or \'n\' if finished): ')
        #listed twice to prevent an error
        if Qlen == 'n' or Qlen == 'N': break
        while True:
            if Qlen == 'n' or Qlen == 'N': break
            try:
                Qlength = int(Qlen)
            except:
                Qlen = input('Please enter an integer or \'n\' to quit: ')
                continue
            break

    #generates the new quotes
    #possible word lengths of quote
        qlen = [20, 30]
        for j in range(Qlength):
            phraselen = random.choice(qlen)
            current, previous, previous2 = '', '', ''
            phrase_index = None
            for i in range(phraselen):
                if i == 0:
                    previous = random.choice(first_words)
                    print('\"' + previous.capitalize(), end = ' ')
                    continue
                elif i == 1 or phrase_index == 1:
                    current = filter(random.choice(first.get(previous.lower(), [0,0])))
                    print(current, end = ' ')
                    previous2 = previous
                    previous = current
                    try:
                        phrase_index += 1
                    except TypeError:
                        continue
                elif i == (phraselen - 1):
                    current = filter(random.choice(second.get((previous2.lower(), previous.lower()), [0, 0])))
                    if current == 0:
                        print('\b.\"', end = '\n\n')
                        break
                    else:
                        print(current + '.\"', end = '\n\n')
                        break
                else:
                    current = filter(random.choice(second.get((previous2.lower(), previous.lower()), [0, 0])))
                    if current == 0:
                        current = filter(random.choice(first.get(previous.lower(), [0,0])))
                        if current == 0:
                            print('\b.\"', end = '\n\n')
                            break
                        print(current, end = ' ')
                        previous2 = previous
                        previous = current
                    else:
                        print(current, end = ' ')
                        previous2 = previous
                        previous = current


if __name__ == '__main__':
    main()
