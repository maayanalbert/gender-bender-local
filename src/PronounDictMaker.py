
# creates a dictionary of pronouns
# INPUT: 
# OUTPUT: a dictionary where the keys are gendered pronouns and the values
# are the opposite gendered equivalent
def getPronounDict():

    # open and read the file that contains all of the pronouns
    pronounFile = open("../pronoun_corpus/" + "pronouns.txt","r")
    rawContents = pronounFile.read()

    # process the raw contents into pairs of pronouns
    pairs = processCorpus(rawContents)

    # add every pair to the dictionary
    pronounDict = dict()
    for pair in pairs:
        addPairToDict(pair, pronounDict)

    return pronounDict

# processes the raw contents into ann array of pairs
# INPUT: a string all the pronouns
# OUTPUT: and nested array of pronoun pairs
def processCorpus(rawContents):

    # split the pairs by line
    unprocessedPairs = rawContents.split("\n")

    # split each word in pairs by commas
    pairs = []
    for pair in unprocessedPairs:
        pairs.append(pair.split(","))

    return pairs 

# add a pair of pronouns to the dictionary
# INPUT: an array of two pronouns, the pronoun dictionary
# OUTPUT: 
def addPairToDict(pair, pronounDict):
    bothWays = True

    # check to see if there's an extra element denoting the pair should only 
    # be inputted one way
    if(len(pair) == 2):
        word1, word2 = pair
    elif(len(pair) == 3):
        word1, word2, holder = pair
        bothWays = False
    else:
        return

    # create dictionary entries one or both ways
    createEntries(word1, word2, pronounDict)
    if(bothWays):
        createEntries(word2, word1, pronounDict)

# get the plural of a word
# INPUT: a word
# OUTPUT: the plural of that word
def getPlural(word):

    #if the word is a mr, mrs, etc, skip it
    if(word ==  "mr" or word == "ms" or word == "mrs"):
        return word

    # if the word ends in "ss", as in "countess", add "es"
    if(len(word) > 2 and word[-2:] == "ss"):
        return word + "es"

    # otherwise just add "s"
    else:
        return word + "s"

# enter different permutations of the word into the dictionary
# INPUT: the word, its opposite gendered equivalent, the pronoun dictionary
# OUTPUT: 
def createEntries(word, oppword, pronounDict):

    
    # account for the word in different capitalizations
    words = [word, word.capitalize(), word.upper()]
    oppWords = [oppword, oppword.capitalize(), oppword.upper()]


    for i in range(len(words)):
        word = words[i]
        oppword = oppWords[i]
        pronounDict[word] = oppword

        # add the plural version of the word as well
        # make sure its uppercase if the rest of the word is
        if(i == len(words)-1):
            pronounDict[getPlural(word).upper()] = getPlural(oppword).upper()
        else:
            pronounDict[getPlural(word)] = getPlural(oppword)
