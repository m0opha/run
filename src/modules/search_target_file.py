import os

from .generic_fun import resolvePath

def searchTargetFile(target_filename:str , path:str):

    file_found = []
    put = file_found.append

    for _content in os.listdir(path):
        absolute_path = os.path.join(resolvePath(path), _content)

        if os.path.isdir(absolute_path):
            continue

        possible_target_filename , _ = os.path.splitext(os.path.basename(absolute_path))
        
        if target_filename == possible_target_filename:
            put(absolute_path)
        
    if len(file_found) == 1:
        return file_found[0]
    
    return file_found if file_found != [] else None