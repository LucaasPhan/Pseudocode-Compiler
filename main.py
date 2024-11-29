import re
import src.handlers.commands_handler as deploy_command
import src.datastore as datastore
import src.handlers.operators_handler as opHandler

deploy = deploy_command.deployCommand
# this function extracts the name of the file from the filepath
def getFileName(filePath):
    # turning the file path into a raw string
    raw_filePath = repr(filePath)[1:-1]
    # instead of if elsing to select the the of slash in the text, just seperate the text by 2 delimiters 
    pattern = '|'.join(map(re.escape, "\\/"))
    # patern = r'\\|/'
    # pattern = r'[\\/]'
    extracted_filepath = re.split(pattern, raw_filePath)[-1]
    return extracted_filepath.split(".")[0]

# this function takes the entire code file and seperates it into different lines of code
def seperateIntoLines(text):
    lines = []
    #lineNumber = 0
    line = ''
    charCount = 0
    # reading each character from the code
    for char in text:
        # if its a new line the line is added to the lines list
        if char == '\n':
            lines.append(line)
            line = ''
        # if char is equal to the ending character and the character count also the same with the length of the text - 1 indicating the index of the last character, this line is also added
        elif char == text[-1] and charCount == len(text) - 1:
            # print("debug: ", text[-1], "-----", len(text) - 1, " charCount = ", charCount)
            line += char
            lines.append(line)
        # otherwise the char is added to the line
        else:
            line += char
        charCount += 1
    return lines

# remove white spaces from the code line
def removeWhitespace(lines):
    for line in range(len(lines)):
        # lstrip will remove all the white spaces in front of the line whether it is tab or whitespace 
        lines[line] = lines[line].lstrip() and lines[line].rstrip()
        # print(lines[line])
    return lines

# taking in file path
# fileInPath = input("Please enter the filepath where your pseudocode is stored: ")
fileInPath = "C:/Users/nhath/OneDrive/Documents/Pseudocode-Compiler/text.txt"

# reading the pseudocode text file 
with open(fileInPath, "r") as file:
    read = file.read()
    # print("read: ", read)

linesW = seperateIntoLines(read)
# print("LinesW: ", linesW)
linesNW = removeWhitespace(linesW)
# print("LinesNW: ", linesNW)

programObject = []

for index in range(len(linesNW)):
    splitedLine = linesNW[index].split()
    # print("splitted: ", splitedLine) # debug

    if linesNW[index][:6] == "OUTPUT" or linesNW[index][:5] == "PRINT":
        # print("OUTPUT detected")
        # print("OUTPUT DEBUG: ", linesW[index])
        programObject.append(deploy.create_command("OUTPUT", index, index, index, linesW[index]))
        
    elif splitedLine[1] in opHandler.operators or datastore.configures.operatorList:
        # print("ASSIGN detected")
        # print("ASSIGN DEBUG: ", linesW[index])
        programObject.append(deploy.create_command("ASSIGN", index, index, index, linesW[index]))
        
for obj in programObject:
    obj.run()
