import sys
import os
from genderBender import bendFile, bendString, defaultOutputPath, defaultInputPath

# handles the command for converting a string
# INPUT: the command line inputs
# OUTPUT: nothing, prints the genderbent text
def handleStringCommand(inputs):
    
    # if there's only one additional parameter, send that as the text
    if(len(inputs) == 3):
        string = inputs[2]
    # if there are multiple parameters, concatenate them into a single string
    else:
        string = " ".join(inputs[2:])
    print(bendString(string)) 


# check that the filename and file path are valid
# INPUT: the name of the file, optionally its path
# OUTPUT: true if the file can be found and false otherwise
def validFileName(fileName, path = defaultInputPath):
    if(os.path.isfile(path+fileName)):
        return True
    else:
        return False

# check that the year is a valid number
# INPUT: a string representing the year
# OUTPUT: true if the string can be converted to an int and false otherwise
def validYear(year):
    try:
        int(year)
        return True
    except ValueError:
        return False

# handles the command for converting a string
# INPUT: the command line inputs
# OUTPUT: nothing, prints exit status and creates a new file if it was successful
def handleFileCommand(inputs):
    fileName = inputs[2]
    outputPath = defaultOutputPath

    # if only the file path was submitted
    if(len(inputs) == 3):
        # check that the file name is falid
        if(validFileName(fileName)):
            bendFile(fileName)
        else:
            print("ERROR: invalid file name")
            return

    # if one additional parameter was submitted
    elif(len(inputs) == 4):

        # check if it was a year
        if(validYear(inputs[3]) and validFileName(fileName)):
            year = inputs[3]
            bendFile(fileName, year = year)
        # check if it was a path
        elif(validFileName(fileName, inputs[3])):
            outputPath = inputs[3]
            inputPath = inputs[3]
            bendFile(fileName, inputFilePath = inputPath, 
                                outputFilePath = outputPath)
        # otherwise declare failure
        else:
            print("ERROR: invalid file name, path, or year")
            return

    # if two additionaly parameters were submitted
    elif(len(inputs) == 5):

        # check if the first was a year dn the the scond was a path
        if(validYear(inputs[3]) and validFileName(fileName,inputs[4])):
            year = inputs[3]
            inputPath = inputs[4]
            outputPath = inputs[4]
            bendFile(fileName, year=year, inputFilePath = inputPath, 
                                outputFilePath = outputPath)
        # check vice versa
        if(validYear(inputs[4]) and validFileName(fileName,inputs[3])):
            year = inputs[4]
            inputPath = inputs[3]
            outputPath = inputs[3]
            bendFile(fileName, year=year, inputFilePath = inputPath, 
                                outputFilePath = outputPath)
        # otherwise declare failure
        else:
            print("ERROR: invalid file name, path, or year")
            return

    print("File has been genderbent successfuly! It can be found at: " + outputPath)

# the main function
# INPUT: the command line inputs
# OUTPUT: nothing, prints exit status
def main():
    
    # stop if not enough arguments were submitted
    if(len(sys.argv) < 3):
        msg = """ERROR: You have not inputted enough arguments. 
        Please input the type of operation you'd like to perform 
        and then the text you'd like to peform it on."""
        print(msg.replace("    ", ""))
        return 

    # determine the type of procedure based on the command
    command = sys.argv[1]
    if(command == "string"):
        handleStringCommand(sys.argv)
    elif(command == "file"):
        handleFileCommand(sys.argv)
    else:
        msg = """ERROR: You have inputted an invalid command. 
                Please input 'string' as a first parameter if you'd like to bend a string and 
                'file' as a first parameter if you'd like to bend a file."""
        print(msg.replace("    ", ""))

if __name__ == "__main__":
    main()