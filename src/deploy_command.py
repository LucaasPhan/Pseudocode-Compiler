import src.commands.assign as assign
import src.commands.output as output

class command():
    def __init__(self, startingLine=0, endingLine=0, currentLine=0):
        self.start = startingLine
        self.end = endingLine
        self.current = currentLine

class CommandFactory:
    @staticmethod
    def create_command(command_type, startingLine, endingLine, currentLine, codeLine):
        if command_type == "ASSIGN":
            return assign.ASSIGN(startingLine, endingLine, currentLine, codeLine)
        elif command_type == "OUTPUT":
            return output.OUTPUT(startingLine, endingLine, currentLine, codeLine)
        else:
            raise ValueError(f"Unknown command type: {command_type}")