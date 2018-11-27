import string

def bendFullText(fileName, year = 2018):
    origText = open("../original_texts/" + fileName,"r")
    rawContents = origText.read()

    bentContents = bend(rawContents)

    bentText= open("../bent_texts/" + fileName + "_flipped.txt","w+")
    bentText.write(bentContents)
    bentText.close()

# def bendExcerpt(fileName, Title, Author, desiredLength= 30000, year = 2018):

# def bendManualInput(text, year = 2018):

####################################################################

def bend(rawContents):
    contents = processContents(rawContents)
    generalDict = getGeneralDict()
    nameDict = getNameDict(contents)

    replaceWords(contents, nameDict, generalDict)


    return "".join(contents)


def processContents(rawContents):
    contents = [""]
    letters = set(string.ascii_letters)
    for i in rawContents:
        if(i in letters):
            contents[-1] += i
        else:
            contents.append(i)
            contents.append("")
    return contents

def replaceWords(contents, nameDict, generalDict):
    for i in range(len(contents)):
        word = contents[i]
        if(word in generalDict):
            contents[i] = generalDict[word]
        if(word in nameDict):
            contents[i] = nameDict[i]







