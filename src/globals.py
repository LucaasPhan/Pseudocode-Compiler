# importing configures from data_store.py as config
import src.datastore as datastore
import src.operators_handler as operator
import re

# creating a configure class for storage
configures = datastore.configures()
# stop code 
error = False

def is_comma(s): # Regex to match any string that only contains special characters 
    return bool(re.fullmatch(r',', s))

def detect_operators(s): # Detect operators 
    detected_operators = bool(re.findall(r'[+\-*/^%]', s))
    return detected_operators
