# importing configures from data_store.py as config
import source.datastore as datastore
import re

# creating a configure class for storage
configures = datastore.configures()

class command():
    # constructing the class with a startingLine, endingLine, currentLine, this will be the parent class for child classes --> commands
    def __init__(self, startingLine=0, endingLine=0, currentLine=0):
        self.start = startingLine
        self.end = endingLine
        self.current = currentLine

class ASSIGN(command):
    def __init__(self, startingLine, endingLine, currentLine, codeLine):
        # super allows to access all parenting classes
        super().__init__(startingLine, endingLine, currentLine)
        self.codeLine = repr(codeLine)

    def run(self):
        # splitting the line by whitespace
        wordList = self.codeLine.split()
        # taking in the variable name and the variable name and value
        varName = wordList[0]
        value = wordList[2]

        # storing it in the dictionary
        configures.variables[varName] = value
        print(str(configures.variables)+"\n")
      
class OUTPUT(command) :
    def __init__(self, startingLine, endingLine, currentLine, codeLine):
        # super allows to access all parenting classes
        super().__init__(startingLine, endingLine, currentLine)
        self.codeLine = repr(codeLine)

    def run(self):
        # splitting up the string by whitespace
        wordList = self.codeLine.split()
        # we delete the first piece which is either PRINT or OUTPUT
        del wordList[0]
        # the ending string that will be printed
        printed = ""
        # using a string flag to keep track of whether it is a string or not
        string_flag = False

        print(wordList)

        # looping through the list of words 
        for index in range(len(wordList)):
            word = wordList[index]
            # if the start of the word is "... flag thats its a string
            if word[0] == '\"':
                # marking the beginning that this aint a variable
                string_flag = True
                # if the end of the word is a ..." flag that string has stopped so that it could continue checking the next item(variable or string)
                if word[-1] == '\"':
                    string_flag = False
                    # procede to add the string but excludes the "" into the printed string
                    printed += word[1:-1]
                    continue
                else:
                    # if the end of the word isnt a ..." meaning that the string isnt complete so we add the entire string excluding the initial "...
                    printed += word[1:]
                    # we splited the words by white space so we have to add it back
                    printed += " "
                
            # continuing from the previous word, if this word is still in the previous string that has this ..." part which means the string is ending
            elif word[-1] == '\"':
                # string has ended, so flag to check next item(variable or string)
                string_flag = False
                # print the remaining part excluding the ending ..."
                printed += word[:-1]

            # if the end of the word is ...", for example World", Name the phrase: World",
            elif word[-2:] == '",':
                # string has ended, so flag to check next item(variable or string) 
                string_flag = False
                # print the string excluding ...",
                printed += word[:-2]

            # in case string is flagged meaning that this word is in the middle of the string that hasnt ended
            elif string_flag:
                # word[:] basically creates a shallow copy of the string
                # prints the string only
                printed += word[:]
                printed += " "

            # if its a variable
            if not string_flag:
                word = word.strip(",")
                if word in configures.variables:  # this checks if it is a variable and if the variable exists
                    printed += str(configures.variables[word])
                    continue
                # elif "[" in word:
                #     printed += str(fetch_value(word))
                elif word == ",":
                    printed += " "
        print(printed+"\n")