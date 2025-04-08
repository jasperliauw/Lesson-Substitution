######################
#Imports

import os

#######################
#Global Variables

fileSelected = False
fileName = ""

#######################


print("Welcome to Lesson Substitution")



def checkFileExistence(fileName):
    if os.path.exists(fileName):
        return True
    else:
        print("File does not exist, please try again")
        return False



while not fileSelected:
    fileLocation = input("If the file is in the same folder as the program, please input (1)\nIf the file is not in the same folder as the program, please input (2)\n")
    if fileLocation == "1":
        fileName = input("Please input the name of the file: ")
        fileSelected = checkFileExistence(fileName)
    elif fileLocation == "2":
        fileName = input("Please input the FULL DIRECTORY of the file: ")
        fileSelected = checkFileExistence(fileName)

    else:
        print("Invalid option, please try again")




file = open(fileName, mode='r')
fileLines = file.read()
print(fileLines)