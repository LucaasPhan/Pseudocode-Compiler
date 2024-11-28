import src.globals as globals 
import re

class command():
    def __init__(self, startingLine=0, endingLine=0, currentLine=0):
        self.start = startingLine
        self.end = endingLine
        self.current = currentLine

class OUTPUT(command):
    def __init__(self, startingLine, endingLine, currentLine, codeLine):
        # super allows to access all parenting classes
        super().__init__(startingLine, endingLine, currentLine)
        self.codeLine = codeLine

    def run(self):
        # splitting up the string by whitespace
        wordList = re.findall(r'\"[^\"]*\"|[^\s]+', self.codeLine)
        # print("Word List:", wordList)
        # we delete the first piece which is either PRINT or OUTPUT
        del wordList[0]
        # the ending string that will be printed
        printed = ""
        # using a string flag to keep track of whether it is a string or not
        string_flag = False
        # init imported vars
        configures = globals.configures
        is_comma = globals.is_comma
        detect_operators = globals.detect_operators

        # error => stop
        if globals.error: 
            return
        # looping through the list of words 
        for index, word in enumerate(wordList):
            word = wordList[index]
            # print(string_flag, word)

            # comma only => skip
            if is_comma(word): 
                continue
            
            # detect operators within the line (arithmetic operators not supported yet)
            if detect_operators(word):
                globals.error = True
                return print(f"ERROR: Compiler have not supported arithmetic operator for pseudocode yet -> {self.codeLine}")

            # Syntax error detection
            if index > 0 and not (word.startswith('\"') or word.startswith(',')): 
                if not wordList[index - 1].endswith(','): 
                    globals.error = True 
                    return print(f"ERROR: Variable or component not separated by a comma -> {word} in line -> {self.codeLine}")

            # main process
            if word.startswith('\"') and word.endswith('\"'):   
                printed += word[1:-1]
            else: # process for variables
                word = word.rstrip(',')
                if word in configures.variables:
                    printed += configures.variables[word]
                else:
                    globals.error = True
                    return print(f"ERROR: Variable is not declared -> Variable: {word} in line -> {self.codeLine}")
        print(printed)