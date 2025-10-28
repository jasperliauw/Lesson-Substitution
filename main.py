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

def write_output_for_acceptance(school_name, original_teacher, day, sub_lessons, nameofFile):
    # Header lines
    lines = []
    lines.append(f"Name of school: {school_name}")
    lines.append(f"Substitution for {original_teacher} on Day {int(day)}")
    lines.append("")
    # Table header
    col1 = "Lesson".ljust(8)
    col3 = "Substitute".ljust(9)
    sep = "  "
    lines.append(f"{col1}{sep}{col3}")
    lines.append(f"{'-'*8}{sep}{'-'*8}")

    # Build table rows
    for entry in sub_lessons:
        # Expect entry = [lesson_index, substitute_name]
        lesson_idx = int(entry[0])
        lesson_display = str(lesson_idx + 1).ljust(8)  # convert 0-based to 1-based for display
        substitute = str(entry[1]).ljust(9)
        lines.append(f"{lesson_display}{sep}{substitute}")
    if nameofFile == "":
        nameofFile = "Output"
    # Write to file (overwrite existing)
    with open(nameofFile, "w", encoding="utf-8") as f:
        for l in lines:
            f.write(l + "\n")
    print("Saved!")
    print("Would you like to return to the main menu?")
    choose = input("Y)es, N)o\n")
    if choose.upper() == "Y":
        print("Returning")
        chooseOption()
    elif choose.upper() == "N":
        print("Goodbye")
    else:
        print("Invalid Option, returning to main menu")


def AcceptOrNot(subLessons, teacherName, subNeedDay):
    backupSub = subLessons.copy()
    for i in range(len(subLessons)):
        print("Do you accept this substitution?")
        print("Lesson: " + str(subLessons[i][0] + 1))
        print("Teacher: "+ teacherName + " --> " + str(subLessons[i][1]))
        acceptOrNot = input("Y)es, N)o\n")
        if acceptOrNot.upper() == "Y":
            continue
        else:
            teacherValid = False
            while teacherValid == False:
                new = input("Which teacher would you like to substitute with: ")
                for j in range(0, len(teachers)):
                    if teachers[j] == new:
                        teacherValid = True
                        subLessons[i][1] = new
                        break
                if not teacherValid:
                    print("No teacher with that initial is found, please try again ")
    if not len(subLessons) == 0:
        print("Is this correct?")
        for i in range(len(subLessons)):
            print("Lesson: " + str(subLessons[i][0] + 1), ", Teacher: " + teacherName+ " --> "+str(subLessons[i][1]))
        confirm = input("Y)es, N)o\n")
        if confirm.upper() == "Y":
            name = input("What would you like the name of the file to be? (Default: Output):\n")
            write_output_for_acceptance(schoolName, teacherName, subNeedDay, subLessons, name)
        else:
            print("Please retry")
            AcceptOrNot(backupSub, teacherName)
    else:
        print("No substitution is needed, good day.")

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
            #print("Some of the teachers have the same amount of days debt")
            daysSame.append(daysDebt[i])
            daysSame.append(daysDebt[i+1])
    daysSame.sort(key=lambda x: str(x[1]))
    #print(daysSame)
    #print(daysDebt)
    #print(lessonsNeedSub)
    for j in range(0, len(lessonsNeedSub)): #Step 1 & 2
        for i in range(0, len(daysDebt)):
            if daysDebt[i][2][lessonsNeedSub[j]] == "#":
                temp = []
                temp.append(lessonsNeedSub[j])
                temp.append(daysDebt[i][1])
                subLessons.append(temp)
                #print(lessonsNeedSub[j], daysDebt[i][1])
                #print(subLessons)
                day = int(daysDebt[i][0])
                day += 1
                daysDebt[i][0] = str(day)
                #print(daysDebt)
                daysDebt.sort(key=lambda x: int(x[0]))
                break
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        os.system("clear")
    elif sys.platform.startswith("win"):
        os.system("cls")
    #print(lessonsNeedSub)
    found_indexes = [entry[0] for entry in subLessons]
    for lesson in lessonsNeedSub:
        if lesson not in found_indexes:
            print(f"No teacher available for lesson {lesson + 1}")

    AcceptOrNot(subLessons, subNeedTeacher,subNeedDay)




def chooseOption():
    if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
        os.system("clear")
    elif sys.platform.startswith("win"):
        os.system("cls")
    #modyfiytable()
    print("Welcome to Lesson Substitution\nWhat do you want to do?")
    choose = input("D)isplay timetable, S)ubstitute, C)hange Files, Q)uit\n")
    if choose.upper() == "D":
        for timetableLength in range (0,len(splitDataTimetable)):
            print(splitDataTimetable[timetableLength][0])
            for i in range (2,len(splitDataTimetable[timetableLength])):
                print("Day", str(i-1) + ":")
                print(splitDataTimetable[timetableLength][i])
                if i == len(splitDataTimetable[timetableLength]) - 1:
                    print()
        choice = input("R)eturn, E)xit:\n")
        if choice.upper() == "R":
            chooseOption()
        elif choice.upper == "E":
            print("Thank you and goodbye")
        else:
            print("Invalid Option, returning")
            chooseOption()
    elif choose.upper() == "S":
        ModifyTable()
    elif choose.upper() == "Q":
        print("Thank you and goodbye")
    elif choose.upper() == "C":
        start()
    else:
        print("Invalid option, please try again")
        chooseOption()
    


def DisplayInfoTimetable(): #Display all the info of the timetable and allow the user to check or not and then modify it
    print("Teachers code found: ", end="")
    for timetableLength in range (0,len(splitDataTimetable)):
        print(splitDataTimetable[timetableLength][0],end=" ")
        teachers.append(splitDataTimetable[timetableLength][0])
    print()
    isCorrect = input("Is the above information correct? (y/n) ")
    CheckQuit(isCorrect)
    if isCorrect.upper() == "Y":
        chooseOption()
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
def start():
    global fileSelected
    global splitData
    fileSelected = False
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        os.system("clear")
    elif sys.platform.startswith("win"):
        os.system("cls")
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




start()