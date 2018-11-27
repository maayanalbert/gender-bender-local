
import random
from random import shuffle
from os import listdir
from os.path import isfile, join
punctuations = ["","'s", ".", ":", ",", "!", "?", ";"]
quotations = ["'", '"', "(", ")", '“','”']
splitters = {"\n", "-"}


def makeNameSets(year = 2017):
    path = "names/"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    nameFile = getRightFile(year)
    contents = open("names/" + nameFile, "r")
    namesArr = contents.read().split("\n")
    femaleNames = dict()
    maleNames = dict()
    for namePkg in namesArr:
        sliced = namePkg.split(",")
        if(len(sliced) == 3):
            name, gender, pop = sliced
            if(gender == "F"):
                if(name[0] in femaleNames):
                    letterDict = femaleNames[name[0]]
                else:
                    letterDict = dict()
                    femaleNames[name[0]] = letterDict
            else:
                if(name[0] in maleNames):
                    letterDict = maleNames[name[0]]
                else:
                    letterDict = dict()
                    maleNames[name[0]] = letterDict
            letterDict[name] = int(pop)
    return(femaleNames, maleNames)  

def getRightFile(year):
    path = "/Users/Maayan/Google Drive/year 4.0 : senior fall/golan intermediate studio/07-book/gender flipper/names/"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files = sorted(files)
    return files[binSort(year, files, 1, len(files))]

def binSort(year, files, lowerInd, upperInd):
    midInd = (upperInd - lowerInd)//2 + lowerInd
    mid = int(files[midInd][3:7])

    if(mid == year):
        return midInd
    elif(mid < year):
        if(midInd == len(files)-1):
            return midInd
        else:
            return binSort(year, files, midInd, upperInd)
    else:
        if(midInd == 1):
            return midInd
        else:
            return binSort(year, files, lowerInd, midInd)

def getNamesInNovel(contents, femaleNames, maleNames):
    names = dict()
    for word in contents:
        wordIters = [word]
        nameFound = None
        gender = None
        for i in range(1, 4):
            if(len(word) >i):
                wordIters.append(word[:i*-1])
                wordIters.append(word[i:len(word)])
        for wordIter in wordIters:
            if(len(wordIter) != 0):
                firstLetter = wordIter[0]
            else:
                continue
            if firstLetter in femaleNames and wordIter in femaleNames[firstLetter].keys():
                curDict = femaleNames[firstLetter]
                if(curDict[wordIter] > 50):
                    nameFound = wordIter
                    gender = "f"
                    break
            if firstLetter in maleNames and wordIter in maleNames[firstLetter].keys():
                curDict = maleNames[firstLetter]
                if(curDict[wordIter] > 50):
                    nameFound = wordIter
                    gender = "m"
                    break
        if(nameFound != None):
            names[nameFound] = gender

    return names

def nameDictGenerator(contents, year):
    femaleNames, maleNames = makeNameSets(year)
    namesInNovel = getNamesInNovel(contents, femaleNames, maleNames)
    nameDict = dict()
    for name in namesInNovel.keys():
        if(namesInNovel[name] == "f"):
            nameSet = maleNames[name[0]]
            sameNameSet = femaleNames[name[0]]
        else:
            nameSet = femaleNames[name[0]]
            sameNameSet = maleNames[name[0]]
        closestName = findClosestName(name, nameSet, sameNameSet)
        if(name != "" and closestName != ""):
            addToDict(name, closestName, nameDict, True)
    return nameDict

def findClosestName(name, nameSet, sameNameSet):
    leastDist = None
    closestName = None
    closestNames = []
    maxDist = 3

    for otherName in nameSet:
        if(otherName in sameNameSet):
            continue
        if(len(name) > 0 and len(otherName) > 0 and name[0] != otherName[0]):
            continue
        dist = iterative_levenshtein(name, otherName)
        if(dist <= 3 and otherName):
            closestNames.append(otherName)
        elif(leastDist == None or leastDist > dist):
                leastDist = dist
                closestName = otherName

    if(len(closestNames) == 0):
        return closestName
    else:
        return findMostPopularName(closestNames, nameSet)

def findMostPopularName(closestNames, nameSet):
    mostPopName = None
    mostPopValue = None
    for name in closestNames:
        popValue = nameSet[name]
        if(mostPopValue == None or popValue > mostPopValue):
            mostPopValue = popValue
            mostPopName = name
    return mostPopName

def iterative_levenshtein(s, t, costs=(1, 1, 1)):
    """ 
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t
        
        costs: a tuple or a list with three integers (d, i, s)
               where d defines the costs for a deletion
                     i defines the costs for an insertion and
                     s defines the costs for a substitution
    """
    rows = len(s)+1
    cols = len(t)+1
    deletes, inserts, substitutes = costs
    
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = row * deletes
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = col * inserts
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + cost) # substitution

    return dist[rows-1][cols-1]

femaleNames, maleNames = makeNameSets()

def flipWholeText(textName):
    origText = open("texts/" + textName + ".txt","r")
    rawContents = origText.read()

    flippedContents = flip(rawContents)

    flippedText= open("flipped_texts/" + textName + "_flipped.txt","w+")
    flippedText.write(flippedContents)
    flippedText.close()

def flipExcerpt(textName, title, author, newName, year = 2018):
    origText = open("texts/" + textName + ".txt","r")
    rawContents = origText.read()
    excerptLen = 3000
    start = random.randint(0, len(rawContents) - excerptLen)
    end = start + excerptLen

    rawContents = title + "\nBy " + author + "\n" + rawContents[start:end]

    flippedContents = flip(rawContents)


    flippedText= open("../data/" + newName + ".txt","w+")
    flippedText.write(flippedContents)
    flippedText.close()

def customSplit(fullWord):
    minLen = None
    maxLen = None
    wordArr = [""]
    for char in fullWord:
        if(char in splitters):
            wordArr.append(char)
            wordArr.append("")
        else:
            curSubstring = wordArr[-1]
            curSubstring = curSubstring + char
            wordArr[-1] = curSubstring            

    return wordArr


def customCombine(wordArr):
    word = ""
    for substring in wordArr:
        word = word + substring
    return word

def flip(rawContents, year = 2018): 

    contents = rawContents.split(" ")

    genDict = makeGeneralDict()
    nameDict = nameDictGenerator(contents, year)
    # print(nameDict)

    # replace any words
    for i in range(len(contents)):
        word = contents[i]
        wordArr = customSplit(word)
        for j in range(len(wordArr)):
            if(wordArr[j] != "" and wordArr[j] in genDict):
                wordArr[j] = genDict[wordArr[j]]
            if(wordArr[j] != "" and wordArr[j] in nameDict):
                wordArr[j] = nameDict[wordArr[j]]
        word = wordArr[0]
        word = customCombine(wordArr)

        contents[i] = word


    output = " ".join(contents)    
    return output 


def dictInsert(word1, word2, d):
    words = []
    
    # add singular
    words.append(word1)
    d[word1] = word2

    # add plural
    words.append(word1 + "s")
    d[word1 + "s"] = word2 + "s"

    # add capitals of those two
    for i in range(0, 2):
        word = words[i]
        word1 = word
        word2 = d[word1]

        words.append(word1.capitalize())
        d[word1.capitalize()] = word2.capitalize()

    # add punctuation
    for word in words:
        for punctuation in punctuations:
            word1 = word + punctuation
            word2 = d[word] + punctuation

            d[word1] = word2

            for quotation in quotations:
                if(quotation == '“'):
                    d[word1 + '”'] = word2 + '”'
                    d[quotation + word1] = quotation + word2
                    d[quotation + word1 + '”'] = quotation + word2 + '”'
                else:
                    d[word1 + quotation] = word2 + quotation
                    d[quotation + word1] = quotation + word2
                    d[quotation + word1 + quotation] = quotation + word2 + quotation





def addToDict(word1, word2, d, oneWay = False):
    dictInsert(word1, word2, d)
    if(oneWay == False):
        dictInsert(word2, word1, d)             

def makeGeneralDict():
    d = dict()

    addToDict("he", "she", d)
    addToDict("him", "her", d)
    addToDict("his", "hers", d)
    addToDict("his", "her's", d)
    addToDict("madam", "mister", d)
    addToDict("mr", "mrs", d)
    addToDict("mr", "ms", d)
    addToDict("brother", "sister", d)
    addToDict("aunt", "uncle", d)
    addToDict("mother", "father", d)
    addToDict("mom", "dad", d)
    addToDict("ma", "pa", d)
    addToDict("husband", "wife", d)
    addToDict("king", "queen", d)
    addToDict("gentleman", "lady", d)
    addToDict("gentlemen", "ladies", d)
    addToDict("prince", "pricess", d)
    addToDict("lord", "lady", d, True)
    addToDict("baron", "baroness", d)
    addToDict("miss", "mister", d)
    addToDict("daughter", "son", d)
    addToDict("man", "woman", d)
    addToDict("men", "women", d)
    addToDict("boy", "girl", d)
    addToDict("grandmother", "grandfather", d)
    addToDict("sir", "dame", d)
    addToDict("stepmother", "stepfather", d)
    addToDict("godmother", "godfather", d)
    addToDict("himself", "herself", d)
    addToDict("mss", "mister", d, True)
    addToDict("horseman", "horsewoman", d)
    addToDict("horsemen", "horsewomen", d)
    addToDict("wizard", "witch", d)
    addToDict("warlock", "witch", d, True)
    addToDict("businessman", "businesswoman", d)
    addToDict("businessmen", "businesswomen", d)
    # addToDict("warlock", "witch", d, True)


    return d

books = [("harry_potter", "Harry Potter", "J. K. Rowling"),
        ("alice_in_wonderland", "Alice's Adventures in Wonderland", "Lewis Carrol"),
        ("great_expectations", "Great Expectations", "Charles Dickens"),
        ("huckleberry_finn", "Adventures of Huckleberry Finn", "Mark Twain"),
        ("jane_eyre", "Jane Eyre", "Charlotte Bronte"),
        ("jekyll_hyde", "The Strange Case of Dr. Jekyll and Mr. Hyde", "Robert Louis Stevenson"),
        ("mary_poppins", "Mary Poppins", "P. L. Travers"),
        ("oliver_twist", "Oliver Twist", "Charles Dickens"),
        ("frankenstein", "Frankenstein", "Mary Shelley"),
        ("peter_pan", "Peter Pan", "J. M. Barrie"),
        ("pride_and_prejudice", "Pride and Prejudice", "Jane Austen"),
        ("sherlock_holmes", "The Adventures of Sherlock Holmes", "Sir Arthur Conan Doyle"),
        ("the_great_gatsby", "The Great Gatsby", "F. Scott Fitzgerald"),
        ("anna_karenina", "Anna Karenina", "Leo Tolstoy")]

def generateExcerpts(books):
    shuffle(books)
    for i in range(14):
        corpus, title, author = books[i]
        flipExcerpt(corpus, title, author, str(i))

# generateExcerpts(books)


