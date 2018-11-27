from pronounDictMaker import createEntries

# creates a dictionary of names mapped to their opposite gendered equivalents
# INPUT: an array of all the words in the text, the year the text was written
# OUTPUT: the dictionary of mapped names
def getNameDict(wordArr, year):

    # get the file containing popular names from the year the text was written
    nameFile = getNameFile(year)
    rawContents = nameFile.read()

    # process the contents of this file into dictionaries of male and female names
    allMaleNames, allFemaleNames = processRawNames(rawContents)

    # get all of the names in the text
    namesInText = getNamesInText(wordArr, allMaleNames, allFemaleNames)

    nameDict = dict()

    # iterate through all of the names in the text and get the opposite gendered
    # equivalent
    for name in namesInText:
        gender = namesInText[name]
        if(gender == "F"):
            sameGenderNames = allFemaleNames
            oppGenderNames = allMaleNames
        else:
            sameGenderNames = allMaleNames
            oppGenderNames = allFemaleNames

        oppGenderName = getOppGenderName(name, sameGenderNames, oppGenderNames)
        createEntries(name, oppGenderName, nameDict)

    return nameDict

# finds the file with the most popular names from when the book was written
# INPUT: the year the book was written (defaults to 2017 if none was given)
# OUTPUT: the file for that year
def getNameFile(year):

    # we only have files between 1880 and 2017 so if the book was written outside
    # of that time frame round to one of those dates
    firstYear = 1880
    lastYear = 2017
    if(year < firstYear):
        year = firstYear
    elif( year > lastYear):
        year = lastYear

    return open("../name_corpus/" + "yob" + str(year) + ".txt", "r")

# formats the raw string from the name file into a dictionary
# INPUT: the contents of the name file in a string
# OUTPUT: Two dictionaries (one for male and one for female names) where the 
# keys are letters in the alphabet and the values are subdictionaries.
# These subdictionaries, called firstLetterDicts, whose keys are all of the names 
# that start with that letter and values are the names' popuarities (in number
# of newborns given that name in the US that year). This will
# speed up the opposite gender name search process because you only have to look
# at names that start with the same letter.
def processRawNames(rawContents):

    # splits each line into a namePackage containing the name, gender, 
    # and popularity
    namePackages = rawContents.split("\n")
    for i in range(len(namePackages)):
        newPkg = namePackages[i].split(',')
        if(len(newPkg) == 3):
            namePackages[i] = newPkg

    allMaleNames = dict()
    allFemaleNames = dict()

    # iterates through every name package and inserts the name into the 
    # correct subdictionary
    for namePackage in namePackages:
        # throw out the package if its has irregular contents
        if(len(namePackage) < 3):
            continue
        name, gender, popularity = namePackage
        firstLetter = name[0]
        
        # selece the correct gendered dictionary
        if(gender == "M"):
            d = allMaleNames
        else:
            d = allFemaleNames

        # select the correct subdictionary based on the first letter 
        if(firstLetter in d):
            firstLetterDict = d[firstLetter]
        else:
            d[firstLetter] = dict()
            firstLetterDict = d[firstLetter]

        # map the name to its popularity
        firstLetterDict[name] = int(popularity)

    return (allMaleNames, allFemaleNames)

# get all of the names that appear in the text
# INPUT: an array of all the words in the text, the male and female superdictionaries
# OUTPUT: a dictionary of all of the names in the text where the keys are the
# names and the values are their respective genders
def getNamesInText(wordArr, allMaleNames, allFemaleNames):
    
    # set a minimal popularity value in order to accept that name
    minPopularity = 50
    namesInText = dict()

    # iterate through every word in the array and add it to the return dictionary
    # if it's in one of the name dictionaries
    for word in wordArr:
        if(len(word) > 0):
            firstLetter = word[0]

            # see if the first letter matches any sub dictionaries
            if(firstLetter in allMaleNames):
                firstLetterDict = allMaleNames[firstLetter]

                # add it if its in the subdict and above the minimum popularity
                if(word in firstLetterDict and firstLetterDict[word] > minPopularity):
                    namesInText[word] = "M"
            if(firstLetter in allFemaleNames):
                firstLetterDict = allFemaleNames[firstLetter]
                if(word in firstLetterDict and firstLetterDict[word] > minPopularity):
                    namesInText[word] = "F"

    return namesInText

# get the opposite gendered equivalent of a given name
# INPUT: the original name, the superdictionary for the names of the same and 
# opposite genders
# OUTPUT: the opposite gendered equivalent to the name
def getOppGenderName(name, sameGenderNames, oppGenderNames):
    
    # set a boundary for how small the smallest acceptable distance can get
    acceptableDistBoundary = 4

    # get the correct subdictionaries
    firstLetter = name[0]
    firstLetterSame = sameGenderNames[firstLetter]
    if(firstLetter in oppGenderNames):
        firstLetterOpp = oppGenderNames[firstLetter]
    # if an opposite gendered subdictionary doesn't exist return the original name
    else:
        return name

    acceptableDist = None
    closestNames = []
    # iterate through all of the names in the opposite gendered subdictionary
    for otherName in firstLetterOpp:

        # get the distance between the original and opposite gendered name
        dist = getLevenshteinDist(name, otherName)

        # if the distance is small enough and the name isn't in the same
        # gendered dictionary, add it to the contendors
        closeEnough = (acceptableDist == None or dist <= acceptableDist)
        if(closeEnough and otherName not in firstLetterSame):
            closestNames.append((otherName, dist))

            # update the longest acceptable distance if it's larger than the
            # boundary
            acceptableDist = max(dist, acceptableDistBoundary)

    maxPop = None
    bestName = None

    # iterate through the closest names and select the most popular one
    for i in range(len(closestNames)):
        otherName, dist = closestNames[i]
        
        # throw out the name if its farther than the max acceptable dist
        if(dist > acceptableDist):
            continue
        pop = firstLetterOpp[otherName]
        if(maxPop == None or pop > maxPop):
            maxPop = pop
            bestName = otherName

    return bestName

# gets the distance between two words in number of different letters.
# based on Levenshtein's distance algorithm which can be found here: 
# https://people.cs.pitt.edu/~kirk/cs1501/Pruhs/Spring2006/assignments/editdistance/Levenshtein%20Distance.htm
# INPUT: the original name, the superdictionary for the names of the same and 
# opposite genders
# OUTPUT: the opposite gendered equivalent to the name
def getLevenshteinDist(name, otherName):
    name = "#" + name
    otherName = "#" + otherName
    matrix = []

    # create an empty matrix where the num cols is the length of one word and
    # the num rows is the length of the other
    for r in range(len(name)):
        row = []
        for c in range(len(otherName)):
            row.append(None)
        matrix.append(row)

    # fill in the matrix
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):

            # fill in the edges
            if(r == 0 and c == 0):
                matrix[r][c] = 0
            elif(r == 0):
                matrix[r][c] = matrix[r][c-1] + 1
            elif(c == 0):
                matrix[r][c] = matrix[r-1][c] + 1

            # fill in the middle cells
            else:
                # if the letters in both words are the same, set the cost to 0
                if(name[r] == otherName[c]):
                    cost = 0
                # otherwise set the cost to 1
                else:
                    cost = 1

                # set the value of the cell based on the preceding values
                up = matrix[r-1][c] + 1
                back = matrix[r][c-1] + 1
                diagonal = matrix[r-1][c-1] + cost
                matrix[r][c] = min(up, back, diagonal)

    # return the bottom left, or final value in the cell
    return matrix[len(matrix)-1][len(matrix[0])-1]
