#SVG label maker
#By Andrew Mulholland aka gbaman
#Based off previous Raspberry Jamboree 2014 badge generator https://github.com/gbaman/Raspberry-Jamboree-Badges

#Released under MIT Licence


# To use
# There are 2 ways to use this program
# 1. Simply run the program in interactive mode, it will ask for each required value for the badge, then spit out a filled in SVG file.
# 2. Run the program but include a number of parameters
# python3 Label-builder.py id hdl itemName owner notes
# There are also 2 optional parameters that can be used
# python3 Label-builder.py id hdl itemName owner notes templateFile newLabelFile


import sys

try:   #For Python 2 and Python 3 support.
    input = raw_input
except NameError:
    pass

#------------------------Constants------------------------
LabelTemplateFile = "../Label-templates/LabelTemplate.svg"
NewLabelFile = "NewBadge.svg"
#----------------------Constants-End----------------------

def getList(listFile):
    """
    Imports a text file line by line into a list.
    """
    file = open(listFile)
    svgFile = []
    while 1:
        line = file.readline()
        if not line:
            break
        svgFile.append(line)
    return svgFile

def writeTextFile(filelist, name):
    """
    Writes the final list to a text file.
    Adds a newline character (\n) to the end of every sublist in the file.
    Then writes the string to the text file.
    """
    file = open(name, 'w')
    mainstr = ""
    for i in range(0, len(filelist)):
        mainstr = mainstr + filelist[i] + "\n"
    file.write(mainstr)
    file.close()

def replacer(svgFile, toReplace, newData):
    """
    Searches through SVG file until it finds a toReplace, once found, replaces it with newData
    """
    for count in range(0,len(svgFile)):
        found = svgFile[count].find(toReplace) #Check if the current line in the SVG file has the required string
        if not (found == -1):
            location = (svgFile[count]).find(toReplace) #We know exact location on the line that Name and Twitter are
            partone = (str(svgFile[count])[:location]) #Grab part of line before the searched for string
            parttwo = (str(svgFile[count])[(location+len(toReplace)):]) #Grab part of line after the searched for string
            svgFile[count] = partone + newData + parttwo
            break
    return svgFile

def askQuestion(question, lengthLimit, allowBlank = False):
    while True:
        print(question)
        answer = input()
        if len(answer) == 0 and allowBlank == False:
            print("You must enter at least 1 character.")
        elif len(answer) > lengthLimit:
            print("You entered too many characters. You may only use " + str(lengthLimit) + " characters and you used " + str(len(answer)) + ".")
        else:
            #complete = True
            return answer




def interactiveLabelMaker():
    svgFile = getList(LabelTemplateFile)
    svgFile = replacer(svgFile, ",,ID,,", askQuestion("Enter ID", 4, False))
    svgFile = replacer(svgFile, ",,HDL,,", askQuestion("Enter HDL", 4, False))
    svgFile = replacer(svgFile, ",,ITEM,,", askQuestion("Enter item name", 25, False))
    svgFile = replacer(svgFile, ",,OWNER,,", askQuestion("Enter item owner", 25, False))
    svgFile = replacer(svgFile, ",,NOTES,,", askQuestion("Any additional notes?", 25, True))
    writeTextFile(svgFile, NewLabelFile)

#-----------------------------------Main program----------------------------------------

if len(sys.argv) == 1:
    interactiveLabelMaker()
else:
    try:
        if len(sys.argv) > 6:
            LabelTemplateFile = sys.argv[6]
            if len(sys.argv) > 7:
                NewLabelFile = sys.argv[7]
        svgFile = getList(LabelTemplateFile)
        svgFile = replacer(svgFile, ",,ID,,", sys.argv[1])
        svgFile = replacer(svgFile, ",,HDL,,", sys.argv[2])
        svgFile = replacer(svgFile, ",,ITEM,,", sys.argv[3])
        svgFile = replacer(svgFile, ",,OWNER,,", sys.argv[4])
        svgFile = replacer(svgFile, ",,NOTES,,", sys.argv[5])
        writeTextFile(svgFile, NewLabelFile)
    except IndexError:
        print("Incorrect number of parameters provided, expected 5.")
    except IOError:
        print("Unable to open file, are you sure the name/path is correct?")
