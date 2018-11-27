import string

from pronounDictMaker import getPronounDict
from nameDictMaker import getNameDict

defaultInputPath = "../original_texts/"
defaultOutputPath = "../bent_texts/"

# genderbends the contents of a txt file
# INPUT: the name of the file, optionally the year it was written, filepaths
# for input and output files
# OUTPUT: nothing, creates the genderbent text file in the desired filepath 
def bendFile(fileName, year = 2018, 
    inputFilePath = defaultInputPath, 
    outputFilePath = defaultOutputPath):

    # get and read the original text
    origFile = open(inputFilePath + fileName,"r")
    rawContents = origFile.read()

    # bend the contents
    bentContents = bend(rawContents, year)

    # get rid of the type part of the file name
    fileName = fileName.split(".")[0]

    # create a new file and put the contents in there
    bentFile= open(outputFilePath + fileName + "_genderbent.txt","w+")
    bentFile.write(bentContents)
    bentFile.close()

# genderbends a string input and returns the results
# INPUT: a string of the original text
# OUTPUT: the genderbent text
def bendString(originalText, year = 2018):
    bentText = bend(originalText, year)
    return bentText

# genderbends the text
# INPUT: original string of contents, the year it was written
# OUTPUT: a string of genderbent contents
def bend(rawContents, year):
    
    # get the contents in a parseable form
    wordArr = seperateWords(rawContents)

    # get the dictionaries
    print("Getting pronoun dictionary...")
    pronounDict = getPronounDict()
    print("Getting name dictionary...")
    nameDict = getNameDict(wordArr, year)
    print("Replacing words...")

    # replace the words
    replaceWords(wordArr, nameDict, pronounDict)

    # return the contents in its original format
    return "".join(wordArr)

# parses the raw contents
# INPUT: raw contents
# OUTPUT: an array of words
def seperateWords(rawContents):
    wordArr = [""]
    letters = set(string.ascii_letters)

    # iterate thrugh every character in the text
    for i in range(len(rawContents)):
        char = rawContents[i]
        
        # isolate man and woman when it appears at the end of a word
        manLen = len("man")
        womanLen = len("woman")
        if(i < len(rawContents)-manLen and 
            (i<2 or rawContents[i-2:i] != "wo" and rawContents[i-2:i] != "hu") and
            (rawContents[i:i+manLen] == "man" or rawContents[i:i+manLen] == "men")):
                wordArr.append(char)

        elif(i < len(rawContents)-womanLen and 
            (rawContents[i:i+womanLen] == "woman" or rawContents[i:i+womanLen] == "women")):
                wordArr.append(char)

        # if it's a letter add it to the most recent word
        elif(char in letters):
            wordArr[-1] += char
        
        # if it isn't append it as an individual item 
        else:
            wordArr.append(char)
            wordArr.append("")

    return wordArr

# replaces every male word with a female one and vice versa
# INPUT: original word array, dictionary of names and pronouns
# OUTPUT: genderbent word array
def replaceWords(wordArr, nameDict, pronounDict):
    # iterate through every word 
    for i in range(len(wordArr)):
        word = wordArr[i]

        # if its a gendered pronoun or name switch it
        if(word in pronounDict):
            wordArr[i] = pronounDict[word]
        if(word in nameDict):
            wordArr[i] = nameDict[word]
