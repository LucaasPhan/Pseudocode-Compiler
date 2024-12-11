import src.globals as globals 
import src.handlers.operators_handler as operator
import re
import math

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
        try: 
            varName = wordList[0]
            if len(wordList) > 3: 
                if detect_operators(wordList[3]):
                    op = wordList[3]
                    v = []
                    for i in range(2, len(wordList)):
                        if wordList[i].isdigit():
                            v.append(int(wordList[i]))
                        else:
                            continue
                    if op in operator.operators:
                        return operator.operators[op](varName, v)
                else: 
                    globals.error = True 
                    return print(f"ERROR: Unexpected character -> {self.codeLine}")
            value = wordList[2]
        except IndexError: 
            globals.error = True
            return print(f"ERROR: Variable is not defined -> {self.codeLine}")   
        if wordList[1] == '=':
            pass
        else: 
            globals.error = True 
            return print(f"ERROR: Unexpected character or operator -> {self.codeLine}")             
        # Detect if the value is a string or not, and is it put in double quote or not
        if value[0] and value[-1] != '\"':
            globals.error = True
            return print(f"ERROR: String datatype should be put inside double quote -> {self.codeLine}")
        elif value[0] and value[-1] == '\"':
            value = value[1:-1]
        # storing it in the dictionary
        configures.variables[varName] = value
        # print(str(configures.variables))