import os
from .modules import (verifyConfigDir, 
                     searchTargetFile, 
                     pError,
                     pWarning, 
                     resolvePath,  
                     executeByExtension, 
                     ParserArguments, 
                     printUsage)

verifyConfigDir()

from .vars.config import _TARGET_FILENAME, _EXECUTE_ALL_FLAG
from .vars.paths import _CURRENT_DIR
from .vars.get_data import _CONFIG

def multiple_target_files(targets_filename):
    length_files_found = len(targets_filename)
    
    if not _EXECUTE_ALL_FLAG:
        pWarning(f"Which {_TARGET_FILENAME} file do you want execute.")
        for _index , _target in enumerate(targets_filename):
            print(f"[{_index}]  {os.path.basename(_target)}")
        
               
        print("[*] Enter to execute all.")
        op = input("> ")
    else :
        op = ""
    #execute all target file
    if op == "":
        for _path in targets_filename:
            executeByExtension(_path , _CONFIG)
        return 

    #some errors
    if not op.isdigit():
        pError("[-] Selection must be a digit or empty.")
        return
    
    if int(op) > length_files_found:
        pError(f"[-] {op} Not exits")
        return
    
    #excute specific target file
    executeByExtension(targets_filename[int(op)] , _CONFIG)

def run():
    targets_files = searchTargetFile(_TARGET_FILENAME, resolvePath(_CURRENT_DIR))
    
    if not targets_files:
        pError(f"[-] Target file {_TARGET_FILENAME} Not found.")        
        return

    if type(targets_files) == list :
        multiple_target_files(targets_files)
        return
    
    #if only one target file execute it.
    executeByExtension(targets_files, _CONFIG)
    
def main():
    parser_arguments = ParserArguments()    
    parser_arguments.add("--help", "-h")
    parser_arguments.add("--target" , "-T", length=2)
    parser_arguments.add("--path" , "-p", length=2)
    parser_arguments.add("--execute_all", "-EA")
    
    arg = parser_arguments.get()
    help = arg.help
    target = arg.target
    path = arg.path
    execute_all = arg.execute_all
    
    if help:
        printUsage()
        return
        
    if target:
        if type(target) == bool:
            pError("[-] Argument \"--target -T\" require keyword. ")
            return
        
        global _TARGET_FILENAME 
        _TARGET_FILENAME = target
    
    if path:
        if type(path) == bool:
            pError('[-] Arguments "--path, -p" require a path.')
            return
        
        global _CURRENT_DIR
        _CURRENT_DIR = path 
        
    if execute_all:
        global _EXECUTE_ALL_FLAG
        _EXECUTE_ALL_FLAG = True
        
         
    try:
        run()
        return
        
    except KeyboardInterrupt:
        pass

    except Exception:
        pass

    finally:
        return