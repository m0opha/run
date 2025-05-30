import os

from .print_colors import pError

def resolvePath(path:str):

    decorator = path[0]
    abstract_path = path[2:]

    if decorator == "~":
        home_path = os.getenv("HOME")
        return os.path.join(home_path, abstract_path)

    return os.path.abspath(path)

def _printConfigErrors(error , position, line):        
    if not error: 
        return

    errors_config_file_messages = {
    "missing_value": "[!] Missing values in configuration:",
    "malformed_line": "[!] Malformed lines:"
    }

    pError(errors_config_file_messages[error])
    print( f"{position} | {line}")
    
    return True

def getConfig(path):
    config = {}
    errors = False
        
    with open(path, "r") as f:
        for i, line in enumerate(f):
            
            line = line.strip().replace(" ", "")
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                errors = _printConfigErrors("malformed_line", i, line)
                continue

            key, value = line.split("=", 1)

            if not value:
                errors = _printConfigErrors("missing_value", i, line)
                continue

            config[value] = key

    if errors:
        return None
    
    return config