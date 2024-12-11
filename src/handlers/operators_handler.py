import src.datastore as datastore
import src.globals as globals

configures = datastore.configures()

def handle_add(varName, v):
    configures.variables[varName] = str(sum(v))
    return True

def handle_subtract(varName, v):
    configures.variables[varName] = str(v[0] - v[1])
    return True

    
operators = { 
            '+': handle_add, 
            '-': handle_subtract, 
            }