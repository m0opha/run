import os

from .generic_fun import resolvePath

def getBinaryPath(binary:str):
    binarys_found = []
    put = binarys_found.append    
    environment_paths = os.getenv("PATH").split(":")
    
    #found all binarys in the system path.
    for _path in environment_paths:
        absolute_path = resolvePath(_path)

        for _item in os.listdir(absolute_path):
            if os.path.isdir(_item):
                continue
        
            binary_path = os.path.join(absolute_path, _item)
            put(binary_path)

    #search for specific binary if not found return none.
    for _binary_path in binarys_found:
        
        if binary == os.path.basename(_binary_path):
            return _binary_path
    
    return None