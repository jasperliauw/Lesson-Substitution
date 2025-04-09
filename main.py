######################
#Imports

import os

#######################
#Global Variables

fileSelected = False
fileNameSC = ""
schoolCode = []
lessonVar = []
lessonDays = 0
lessonAmount = 0



#######################


print("Welcome to Lesson Substitution")



def checkFileExistence(fileName):
    if os.path.exists(fileName):
        return True
    else:
        print("File does not exist, please try again")
        return False



while not fileSelected:
    fileNameSC = input("Please enter the full directory of SC.txt\n")
    if checkFileExistence(fileNameSC):
        fileSelected = True



file = open(fileNameSC, mode='r')
fileLines = file.read()
lines = fileLines.splitlines()
splitData = [line.split(';') for line in lines]
