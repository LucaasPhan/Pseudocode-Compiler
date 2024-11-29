import src.datastore as datastore
import src.globals as globals

configures = datastore.configures()

def handle_add(varName, value):
    if value.isdigit():
        configures.variables[varName] = str(int(configures.variables[varName]) + int(value))
        return True
    else: 
        globals.error = True
        return print("?")

def handle_subtract(varName, value):
    if value.isdigit():
        configures.variables[varName] = str(int(configures.variables[varName]) - int(value))
        return True
    else: 
        globals.error = True
        return print("?")
    
operators = { 
                '+=': handle_add, 
                '-=': handle_subtract, 
                }