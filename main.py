######################
#Imports

import os

#######################
#Global Variables

fileSelected = False
fileNameSC = ""
fileNameTimetable = ""
schoolCode = ""
schoolCodeID = 0
foundSchoolCode = False
schoolName = ""
lessonDays = 0
lessonAmount = 0

#######################


def DisplayInfoTimetable():
    for timetableLength in range (0,len(splitDataTimetable)):
        print(splitDataTimetable[timetableLength][0])
        for i in range (2,len(splitDataTimetable[timetableLength])):
            print(splitDataTimetable[timetableLength][i], end="")
            if i == len(splitDataTimetable[timetableLength]) - 1:
                print()


def checkFileExistence(fileName):
    if os.path.isfile(fileName):
        return True
    else:
        print("File does not exist, please try again")
        return False


def CheckTimetableValidity():
    daysValid = 0
    daysValidd = 0
    lessonsValid = 0
    lessonsValidd = 0
    passVerified = True
    for timetableLength in range (0, len(splitDataTimetable)):
        daysValidd +=1
        if len(splitDataTimetable[timetableLength]) - 2 == lessonDays:
            daysValid +=1
    for timetableLength in range(0, len(splitDataTimetable)):
        for i in range(3, len(splitDataTimetable[timetableLength])):
            lessonsValidd += 1
            if len(splitDataTimetable[timetableLength][i]) == lessonAmount:
                lessonsValid +=1


    if daysValid != daysValidd:
        passVerified = False
        print("Amount of days in SC.txt doesn't match with data in timetable")
        print("Program terminated")
    if lessonsValid != lessonsValidd:
        passVerified = False
        print("Amount of lessons in SC.txt doesn't match with data in timetable")
        print("Program terminated")
    if passVerified:
        print("All timetable data is valid")
        DisplayInfoTimetable()

def OpenTimetable():
    foundTimetable = False
    global fileNameTimetable
    while not foundTimetable:
        fileNameTimetable = input("Please enter the full directory of timetable\n")
        if checkFileExistence(fileNameTimetable):
            foundTimetable = True
    file = open(fileNameTimetable, mode='r')
    fileLines = file.read()
    lines = fileLines.splitlines()
    global splitDataTimetable
    splitDataTimetable = [line.split(';') for line in lines]
    CheckTimetableValidity()


def SchoolDetails():
    global schoolName
    global lessonDays
    global lessonAmount
    schoolName = splitData[schoolCodeID][1]
    lessonDays = int(splitData[schoolCodeID][2])
    lessonAmount = int(splitData[schoolCodeID][3])
    global fileNameTimetable
    print("Details:\nSchool Name:", schoolName, "\nAmount of days:", lessonDays, "\nAmount of lessons:", lessonAmount)
    isCorrect = input("Would you like to proceed? (y/n) ")
    if isCorrect.upper() == "Y":
        OpenTimetable()
    elif isCorrect.upper() == "N":
        isRetry = input("Would you like to retry? (y/n)")
        if isRetry.upper() == "Y":
            SchoolCodeCheck()
        elif isRetry.upper() == "N":
            print("Thank You for using this program, goodbye!")
        else:
            print("Please try again")
            SchoolDetails()
    else:
        print("Please try again")
        SchoolDetails()



def SchoolCodeCheck():
    userInputSchoolCode = input("Please enter your school code\n")
    foundSchoolCode = False
    global schoolCode
    global schoolCodeID
    for i in range(len(splitData)):
        if userInputSchoolCode == splitData[i][0]:
            schoolCode = splitData[i][0]
            schoolCodeID = i
            foundSchoolCode = True
    if foundSchoolCode:
        print("School code found.")
        print(schoolCode)
        SchoolDetails()
    else:
        print("School code not found, please try again")
        SchoolCodeCheck()



while not fileSelected:
    fileNameSC = input("Please enter the full directory of SC.txt\n")
    if checkFileExistence(fileNameSC):
        fileSelected = True

file = open(fileNameSC, mode='r')
fileLines = file.read()
lines = fileLines.splitlines()
splitData = [line.split(';') for line in lines]
SchoolCodeCheck()


