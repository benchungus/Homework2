import sys
import random
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

#preprocessor will comb through the text and return relevant processed data

def preprocessor(text):
    #tokenizes the text
    tokenList = word_tokenize(text.lower())

    #replaces the list with only alpha, not in stopwords, and length > 5 words.
    tokenList = [token for token in tokenList if token.isalpha() and token not in stopwords.words('english') and len(token) > 5]

    #lemmatizes the words, then puts them in a set.
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokenList]

    #pos tagging 
    tagged = nltk.pos_tag(lemmas)

    #print tagged lemmas
    print("First 20 tagged lemmas:")
    for lemma, pos in tagged[:20]:
        print(f"{lemma}: {pos}")

    #sort out nouns from lemma
    nouns = [lemma for lemma, pos in tagged if pos.startswith('N')]

    # print tokens and nouns counts
    print(f'Number of tokens: {len(tokenList)}')
    print(f'Number of nouns: {len(nouns)}')

    # return tokens and nouns
    return tokenList, nouns


#guessing game
def guessing_game(wordsList):
    #starting score of 5
    score = 5

    #terminates if score is negative
    while score > 0:
        word = random.choice(wordsList)
        wordLen = len(word)

        #creating word with all blanks
        currWord = ['_'] * wordLen
        print(' '.join(currWord))

        #keeps looping until all are guessed
        while '_' in currWord:
            letter = input("Guess a letter: ")

            #terminate if !
            if letter == '!':
                print('Game over!')
                return

            #if letter is correct increase score and fill in
            if letter in word:
                print('Right! ', end = '')
                for i in range(wordLen):
                    if word[i] == letter:
                        currWord[i] = letter + ' '
                score += 1

            #wrong letter deducts points and checks for termination
            else:
                score -= 1
                if score < 0:
                    print('Game over!')
                    return
                print('Sorry, guess again.', end = '')
            print(f'Score is {score}')
            print(' '.join(currWord))

        
        print(f'You solved it! \n Current score: {score}')

    print('Game over')

# load the textfile, exit if argument not given
if len(sys.argv) < 2:
    print("Error: pass in the filename as a system argument. Ending program.")
    quit()
filename = sys.argv[1]
text = ""
with open(filename, "r") as f:
    text = f.read()

#feed to preprocessor
tokens, nouns = preprocessor(text)

# create a dictionary of noun counts
freqDistNouns = FreqDist(nouns)
mostCommonNouns = freqDistNouns.most_common(50)
print(f'Top 50 most common nouns and their counts: {mostCommonNouns}')
mostCommonNouns = [seq[0] for seq in mostCommonNouns]

# calculate lexical diversity
lexical_diversity = len(set(tokens)) / len(tokens)
print(f'Lexical diversity: {lexical_diversity}')

#play the guessing game
guessing_game(mostCommonNouns)

