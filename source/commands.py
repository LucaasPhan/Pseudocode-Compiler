# importing configures from data_store.py as config
import source.datastore as datastore
import re

# creating a configure class for storage
configures = datastore.configures()
# stop code 
error = False

def is_comma(s): # Regex to match any string that only contains special characters 
    return bool(re.fullmatch(r',', s))

def detect_operators(s): 
    pattern = r'[+\-*/^%]'
    detected_operators = bool(re.findall(pattern, s))
    return detected_operators

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
        self.codeLine = codeLine
        # print("ASSIGN: ", self.codeLine)

    def run(self):
        global error
        # splitting the line by whitespace
        wordList = re.findall(r'\"[^\"]*\"|\S+', self.codeLine)
        # print(wordList)
        # taking in the variable name and the variable name and value
        if not error:
            if len(wordList) > 3: 
                if detect_operators(wordList[3]):
                    error = True
                    return print(f"ERROR: Compiler have not supported arithmetic operator for pseudocode yet -> {self.codeLine}")
                else: 
                    error = True 
                    return print(f"ERROR: Unexpected character -> {self.codeLine}")
            try: 
                varName = wordList[0]
                value = wordList[2]
            except IndexError: 
                error = True
                return print(f"ERROR: Variable is not defined -> {self.codeLine}")
                    
            # Detect if the value is a string or not, and is it put in double quote or not
            if value[0] and value[-1] != '\"' and not value.isdigit():
                error = True
                return print(f"ERROR: String datatype should be put inside double quote -> {self.codeLine}")
            elif value[0] and value[-1] == '\"':
                value = value[1:-1]
            # storing it in the dictionary
            configures.variables[varName] = value
            # print(str(configures.variables)+"\n")
      
class OUTPUT(command) :
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

        global error
        if error: 
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
                error = True
                return print(f"ERROR: Compiler have not supported arithmetic operator for pseudocode yet -> {self.codeLine}")

            # Syntax error detection
            if index > 0 and not (word.startswith('\"') or word.startswith(',')): 
                if not wordList[index - 1].endswith(','): 
                    error = True 
                    return print(f"ERROR: Variable or component not separated by a comma -> {word} in line -> {self.codeLine}")

            # main process
            if word.startswith('\"') and word.endswith('\"'):   
                printed += word[1:-1]
            else: # process for variables
                word = word.rstrip(',')
                if word in configures.variables:
                    printed += configures.variables[word]
                else:
                    error = True
                    return print(f"ERROR: Variable is not declared -> Variable: {word} in line -> {self.codeLine}")
        print(printed)