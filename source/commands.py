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
        wordList = self.codeLine.split()
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
        for index in range(len(wordList)):
            word = wordList[index]
            # print(string_flag, word)

            if is_comma(word):
                continue
            
            # if the start of the word is "... flag thats its a string
            if word.startswith('\"') and not string_flag:
                string_flag = True
                word = word[1:]

            if string_flag:
                if word.__contains__('\",'):
                    string_flag = False
                    continue
                elif word.__contains__('\"') and len(word) >= 2:
                    if word[-1] != '\"': 
                        error = True
                        return print(f"ERROR: Unexpected character after quotation -> {word} in line -> {self.codeLine}")
                    else: 
                        word = word[:-1]
                        printed += word  
                elif word == '' or word == ' ':
                    string_flag = True  
                elif word[-1] != ',' and word.__contains__('\"') and wordList[index + 1][0:-1] != '\"' and not wordList[index] == (len(wordList) - 1):
                    error = True
                    return print(f"ERROR: Missing expected comma after the output -> {self.codeLine}")
                else: 
                    printed += word + " "
            else: 
                word = word.rstrip(',')
                if word in configures.variables:
                    printed += configures.variables[word] + " "
                else:
                    error = True
                    return print(f"ERROR: Variable is not declared -> Variable: {word} in line -> {self.codeLine}")
        printed = printed.replace(',', '')
        print(printed)