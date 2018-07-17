import random
import sys


def readFile(filename):
    f = open(filename, 'r')
    contents = f.read().replace('\n','').replace('\t', '')
    return cleanContents(contents)


# replace unneeded punctuation from the text
def cleanContents(contents):
    for k in "()[]{}:;'\"\\//-_=+*&^%$#@`~<>|":
        if k in contents:
            contents = contents.replace(k, '')
    return contents


def buildChain(contents, chain = {}):
    contents = contents.split(' ') # get rid of spaces
    punctuation = ['.', '!', '?']

    i = 1 # start at the second word
    for word in contents[i:]:
        # make list of words that follow the current word
        current = contents[i-1]
        if current in chain:
            chain[current].append(word)
        else:
            chain[current] = [word]
        i += 1

    return chain


def generate(chain, count = 100):
    word = random.choice(chain[getStartingWord(list(chain.keys()))])
    message = word.capitalize()
    
    while (len(message.split(' ')) < count):
        temp = random.choice(chain[word])
        if containsPunct(word): # if previous word was an end word
            temp.capitalize();
        word = temp
        message += ' ' + temp
    #end the rest of the sentence after desired length has been reached
    while (not containsPunct(word)):
        temp = random.choice(chain[word])
        word = temp
        message += ' ' + temp
    return message


def getStartingWord(words):
    # only words that follow punctuation are starter words
    starters = []
    for word in words:
        if containsPunct(word):
            starters.append(word)
    return random.choice(starters)


def containsPunct(word):
    for p in ['.', '!', '?']:
        if p in word:
            return True
    return False


def printMessage(message):
    try:
        print(message)
    except:
        print('Not enough word data')

        

def main():
    printMessage(generate(buildChain(readFile('sample.txt'))))

    
if __name__ == "__main__":
    main()
    
