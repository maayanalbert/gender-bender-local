
def getPronounDict():
    pronounFile = open("../pronoun_corpus/" + "pronouns.txt","r")
    rawContents = pronounFile.read()

    pairs = processCorpus(rawContents)

    pronounDict = dict()

    for pair in pairs:
        addPairToDict(pair, pronounDict)

    return pronounDict

def processCorpus(rawContents):
    unprocessedPairs = rawContents.split("\n")

    pairs = []
    for pair in unprocessedPairs:
        pairs.append(pair.split(","))

    return pairs 

def addPairToDict(pair, pronounDict):
    bothWays = True
    if(len(pair) == 2):
        word1, word2 = pair
    elif(len(pair) == 3):
        word1, word2, holder = pair
        bothWays = False
    else:
        return

    createEntries(word1, word2, pronounDict)
    if(bothWays):
        createEntries(word2, word1, pronounDict)


def getPlural(word):
    if(len(word) > 2 and word[-2:] == "ss"):
        return word + "es"
    else:
        return word + "s"


def createEntries(word1, word2, pronounDict):
    pronounDict[word1] = word2
    pronounDict[word1.capitalize()] = word2.capitalize()

    plural1 = getPlural(word1)
    plural2 = getPlural(word2)

    pronounDict[plural1] = plural2
    pronounDict[plural1.capitalize()] = plural2.capitalize()


