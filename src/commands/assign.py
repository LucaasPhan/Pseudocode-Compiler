import src.globals as globals 
import src.operators_handler as opHandler
import re

class command():
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
        detect_operators = globals.detect_operators
        configures = globals.configures

        # splitting the line by whitespace
        wordList = re.findall(r'\"[^\"]*\"|\S+', self.codeLine)
        # print(wordList)
        # taking in the variable name and the variable name and value
        if globals.error:
            return
        if len(wordList) > 3: 
            if detect_operators(wordList[3]):
                globals.error = True
                return print(f"ERROR: Compiler have not supported arithmetic operator for pseudocode yet -> {self.codeLine}")
            else: 
                globals.error = True 
                return print(f"ERROR: Unexpected character -> {self.codeLine}")
        try: 
            varName = wordList[0]
            value = wordList[2]
        except IndexError: 
            globals.error = True
            return print(f"ERROR: Variable is not defined -> {self.codeLine}")   
        if wordList[1] == '=':
            pass
        else: 
            operator = wordList[1] 
            if operator in opHandler.operators: 
                if varName in configures.variables:
                    return opHandler.operators[operator](varName, value)
                else: 
                    error = True
                    return print("?")
            else: 
                globals.error = True 
                return print(f"ERROR: Unexpected character or operator -> {self.codeLine}")             
        # Detect if the value is a string or not, and is it put in double quote or not
        if value[0] and value[-1] != '\"' and not value.isdigit():
            globals.error = True
            return print(f"ERROR: String datatype should be put inside double quote -> {self.codeLine}")
        elif value[0] and value[-1] == '\"':
            value = value[1:-1]
        # storing it in the dictionary
        configures.variables[varName] = value
        # print(str(configures.variables))