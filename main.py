######################
#Imports

import os
import sys


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
teachers = []


#######################



def CheckQuit(inputString):
    if inputString == "quit()":
        print("Program terminated, good day.")
        sys.exit()


def ModifyTable():
    teacherAvailable = []
    lessonNeeded = 0
    try:
        subNeedDay = int(input("Please input the day that needs to be substituted: "))
    except ValueError:
        print("Please input a number.")
        ModifyTable()
        return False
    subNeedTeacher = input("Please input the name of the teacher that needs to be substituted: ")
    teacherValid = False
    teacherLocation = 0
    for i in range(0, len(teachers)):
        if teachers[i] == subNeedTeacher:
            teacherValid = True
            teacherLocation = i
    if not teacherValid:
        print("Please input a valid teacher.")
        ModifyTable()
        return False
    lessonSubTeacherNeeded = splitDataTimetable[teacherLocation][subNeedDay+1]
    lessonsNeedSub = []
    for i in range(0, len(lessonSubTeacherNeeded)):
        if not lessonSubTeacherNeeded[i] == "#":
            lessonNeeded += 1
            lessonsNeedSub.append(i)
    if lessonNeeded == 0:
        print("The teacher has no lesson that day, no need for substitution, please try again")
        ModifyTable()
        return False
#    print(splitDataTimetable)
#    print(splitDataTimetable[teacherLocation][subNeedDay+1])
    daysDebt = []
    temp = []
    subLessons = []
    daysSame = []
    for i in range(0, len(teachers)):
        if not splitDataTimetable[i][0] == subNeedTeacher:
            tempArray = []
            tempArray.append(splitDataTimetable[i][1])
            tempArray.append(splitDataTimetable[i][0])
            tempArray.append(splitDataTimetable[i][2])
            daysDebt.append(tempArray)
    daysDebt.sort(key=lambda x: int(x[0]))
    #We check if two teachers have the same days amount
    for i in range(len(daysDebt)-1):
        if daysDebt[i][0] == daysDebt[i+1][0]:
            print("Some of the teachers have the same amount of days debt")
            daysSame.append(daysDebt[i])
            daysSame.append(daysDebt[i+1])
    daysSame.sort(key=lambda x: str(x[1]))
    print(daysSame)
    print(daysDebt)
    print(lessonsNeedSub)
    for j in range(0, len(lessonsNeedSub)): #Step 1 & 2
        for i in range(0, len(daysDebt)):
            if daysDebt[i][2][lessonsNeedSub[j]] == "#":
                temp = []
                temp.append(lessonsNeedSub[j])
                temp.append(daysDebt[i][1])
                subLessons.append(temp)
                print(lessonsNeedSub[j], daysDebt[i][1])
                print(subLessons)
                break






def DisplayInfoTimetable(): #Display all the info of the timetable and allow the user to check or not and then modify it
    print("Teachers code found: ", end="")
    for timetableLength in range (0,len(splitDataTimetable)):
        print(splitDataTimetable[timetableLength][0],end=" ")
        teachers.append(splitDataTimetable[timetableLength][0])
    print()
    isCorrect = input("Is the above information correct? (y/n) ")
    CheckQuit(isCorrect)
    if isCorrect.upper() == "Y":
        ModifyTable()
    else:
        print("Program terminated")


def checkFileExistence(fileName): #Check file exists or not
    if os.path.isfile(fileName):
        return True
    else:
        print("File does not exist, please try again")
        return False


def CheckTimetableValidity(): #Check if the timetable is valid (day -> lesson amount)
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



def CheckSCValidity(): #Check if the SC file is valid or not
    isValid = True
    for i in range(len(splitData)):
        if len(splitData[i]) != 4:
            isValid = False
        for j in range(len(splitData[i])):
            if splitData[i][j] == '':
                isValid = False
    return isValid

def OpenTimetable(): #Open the file of the timetable and split the data so that it's in arrays that is readable
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


def SchoolDetails(): #Show school details
    global schoolName
    global lessonDays
    global lessonAmount
    schoolName = splitData[schoolCodeID][1]
    lessonDays = int(splitData[schoolCodeID][2])
    lessonAmount = int(splitData[schoolCodeID][3])
    global fileNameTimetable
    print("Details:\nSchool Name:", schoolName, "\nAmount of days:", lessonDays, "\nAmount of lessons:", lessonAmount)
    isCorrect = input("Would you like to proceed? (y/n) ")
    CheckQuit(isCorrect)
    if isCorrect.upper() == "Y":
        OpenTimetable()
    elif isCorrect.upper() == "N":
        isRetry = input("Would you like to retry? (y/n)")
        CheckQuit(isRetry)
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



def SchoolCodeCheck(): #Check school code valid or not
    userInputSchoolCode = input("Please enter your school code\n")
    CheckQuit(userInputSchoolCode)
    foundSchoolCode = False
    global schoolCode #Make it so that the variable is accessible everywhere, maybe needed later
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



#Start of application
if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
    os.system("clear")
elif sys.platform.startswith("win"):
    os.system("cls")
print("Welcome to Lesson Substitution.")
print("At any point if you would like to terminate the program, just type 'quit()'")
while not fileSelected:
    fileNameSC = input("Please enter the full directory of SC.txt\n")
    CheckQuit(fileNameSC)
    if checkFileExistence(fileNameSC):
        fileSelected = True

file = open(fileNameSC, mode='r')
fileLines = file.read()
lines = fileLines.splitlines()
splitData = [line.split(';') for line in lines]
if CheckSCValidity():
    SchoolCodeCheck()
else:
    print("SC.txt invalid")
    print("Program terminated")


