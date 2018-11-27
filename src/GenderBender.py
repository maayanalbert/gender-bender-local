import string

from PronounDictMaker import getPronounDict
from NameDictMaker import getNameDict


# genderbends a full text
# INPUT: the name of the file, optionally the year it was written, filepaths
# for input and output files
# OUTPUT: nothing, creates the genderbent text file in the desired filepath 
def bendFullText(fileName, year = 2018, 
    inputFilePath = "../original_texts/", 
    ouputFilePath = "../bent_texts/"):

    # get and read the original text
    origText = open(inputFilePath + fileName,"r")
    rawContents = origText.read()

    # bend the contents
    bentContents = bend(rawContents)

    # get rid of the type part of the file name
    fileName = fileName.split(".")[0]

    # create a new file and put the contents in there
    bentText= open(ouputFilePath + fileName + "_flipped.txt","w+")
    bentText.write(bentContents)
    bentText.close()

# def bendExcerpt(fileName, Title, Author, desiredLength= 30000, year = 2018):

# def bendManualInput(text, year = 2018):

####################################################################

# genderbends the text
# INPUT: original contents
# OUTPUT: genderbent contents
def bend(rawContents):
    
    # get the contents in a parseable form
    wordArr = seperateWords(rawContents)

    # get the dictionaries
    pronounDict = getPronounDict()
    nameDict = getNameDict(wordArr)

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
            (i<2 or rawContents[i-2:i] != "wo") and
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

    print(wordArr)
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

bendFullText("harry_potter.txt")





