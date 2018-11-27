from PronounDictMaker import createEntries

def getNameDict(wordArr, year):
    nameFile = getNameFile(year)
    rawContents = nameFile.read()
    allMaleNames, allFemaleNames = processRawNames(rawContents)

    namesInText = getNamesInText(wordArr, allMaleNames, allFemaleNames)

    nameDict = dict()
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

def getNameFile(year):
    firstYear = 1880
    lastYear = 2017

    if(year < firstYear):
        year = firstYear
    elif( year > lastYear):
        year = lastYear

    return open("../name_corpus/" + "yob" + str(year) + ".txt", "r")

def processRawNames(rawContents):
    namePackages = rawContents.split("\n")
    for i in range(len(namePackages)):
        newPkg = namePackages[i].split(',')
        if(len(newPkg) == 3):
            namePackages[i] = newPkg

    allMaleNames = dict()
    allFemaleNames = dict()
    for namePackage in namePackages:
        if(len(namePackage) < 3):
            continue
        name, gender, popularity = namePackage
        firstLetter = name[0]
        if(gender == "M"):
            d = allMaleNames
        else:
            d = allFemaleNames

        if(firstLetter in d):
            firstLetterDict = d[firstLetter]
        else:
            d[firstLetter] = dict()
            firstLetterDict = d[firstLetter]

        firstLetterDict[name] = int(popularity)

    return (allMaleNames, allFemaleNames)

def getNamesInText(wordArr, allMaleNames, allFemaleNames):
    minPopularity = 50
    namesInText = dict()
    for word in wordArr:
        if(len(word) > 0):
            firstLetter = word[0]
            if(firstLetter in allMaleNames):
                firstLetterDict = allMaleNames[firstLetter]
                if(word in firstLetterDict and firstLetterDict[word] > minPopularity):
                    namesInText[word] = "M"
            if(firstLetter in allFemaleNames):
                firstLetterDict = allFemaleNames[firstLetter]
                if(word in firstLetterDict and firstLetterDict[word] > minPopularity):
                    namesInText[word] = "F"

    return namesInText

def getOppGenderName(name, sameGenderNames, oppGenderNames):
    acceptableDistBoundary = 4
    firstLetter = name[0]
    firstLetterSame = sameGenderNames[firstLetter]
    firstLetterOpp = oppGenderNames[firstLetter]

    acceptableDist = None
    closestNames = []
    for otherName in firstLetterOpp:
        dist = getLevenshteinDist(name, otherName)
        if((acceptableDist == None or dist <= acceptableDist) and otherName not in firstLetterSame):
            closestNames.append((otherName, dist))
            acceptableDist = max(dist, acceptableDistBoundary)

    maxPop = None
    bestName = None

    for i in range(len(closestNames)):
        otherName, dist = closestNames[i]
        if(dist > acceptableDist):
            continue
        pop = firstLetterOpp[otherName]
        if(maxPop == None or pop > maxPop):
            maxPop = pop
            bestName = otherName

    return bestName

def getLevenshteinDist(name, otherName):
    name = "#" + name
    otherName = "#" + otherName
    matrix = []
    for r in range(len(name)):
        row = []
        for c in range(len(otherName)):
            row.append(None)

        matrix.append(row)

    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if(r == 0 and c == 0):
                matrix[r][c] = 0
            elif(r == 0):
                matrix[r][c] = matrix[r][c-1] + 1
            elif(c == 0):
                matrix[r][c] = matrix[r-1][c] + 1
            else:
                if(name[r] == otherName[c]):
                    cost = 0
                else:
                    cost = 1
                up = matrix[r-1][c] + 1
                back = matrix[r][c-1] + 1
                diagonal = matrix[r-1][c-1] + cost
                matrix[r][c] = min(up, back, diagonal)

    return matrix[len(matrix)-1][len(matrix[0])-1]
