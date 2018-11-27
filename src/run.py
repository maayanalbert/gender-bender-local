import sys
import os
from genderBender import bendFile, bendString, defaultOutputPath, defaultInputPath

# handles a string command
# INPUT: the comman line inputs
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

def validYear(year):
    try:
        int(year)
        return True
    except ValueError:
        return False

def validOutputPath(outputPath):
    if(os.path.isdir(outputPath)):
        return True
    else:
        print("Invalid output path")
        return False

def handleFileCommand(inputs):
    fileName = inputs[2]
    outputPath = defaultOutputPath
    if(len(inputs) == 3):
        if(validFileName(fileName)):
            bendFile(fileName)
        else:
            return
    elif(len(inputs) == 4):
        if(validYear(inputs[3]) and validFileName(fileName)):
            year = inputs[3]
            bendFile(fileName, year = year)
        elif(validFileName(fileName, inputs[3])):
            outputPath = inputs[3]
            inputPath = inputs[3]
            bendFile(fileName, inputFilePath = inputPath, 
                                outputFilePath = outputPath)
        else:
            print("Invalid file name, path, or year")
            return

    elif(len(inputs) == 5):
        if(validYear(inputs[3]) and validFileName(fileName,inputs[4])):
            year = inputs[3]
            inputPath = inputs[4]
            outputPath = inputs[4]
            bendFile(fileName, year=year, inputFilePath = inputPath, 
                                outputFilePath = outputPath)
        if(validYear(inputs[4]) and validFileName(fileName,inputs[3])):
            year = inputs[4]
            inputPath = inputs[3]
            outputPath = inputs[3]
            bendFile(fileName, year=year, inputFilePath = inputPath, 
                                outputFilePath = outputPath)
        else:
            print("Invalid file name, path, or year")
            return

    print("File has been genderbent successfuly! It can be found at: " + outputPath)

def main():
    if(len(sys.argv) < 3):
        msg = """You have not inputted enough arguments. 
        Please input the type of operation you'd like to perform 
        and then the text you'd like to peform it on."""
        print(msg.replace("    ", ""))
        return 

    command = sys.argv[1]
    if(command == "string"):
        handleStringCommand(sys.argv)
    elif(command == "file"):
        handleFileCommand(sys.argv)
    else:
        msg = """You have inputted an invalid command. 
                Please input 'string' as a first parameter if you'd like to bend a string and 
                'file' as a first parameter if you'd like to bend a file."""
        print(msg.replace("    ", ""))

if __name__ == "__main__":
    main()