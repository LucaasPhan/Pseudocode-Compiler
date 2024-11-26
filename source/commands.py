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
        print(wordList)
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
            print(string_flag, word)
            # if the start of the word is "... flag thats its a string
            if word.startswith('\"') and not string_flag:
                string_flag = True
                word = word[1:]

            if string_flag:
                if word.endswith('\"') or word.endswith('\",'):
                    string_flag = False
                    word.rstrip('",')
                    printed += word + " "
                else: 
                    printed += word + " "
            else: 
                word = word.rstrip(',')
                print(word)
                if word in configures.variables:
                    printed += configures.variables[word] + " "
                else:
                    return print("ERROR")
        printed = printed.replace(',', '')
        print(printed)