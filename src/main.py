import os
import sys

from .modules import (verifyConfigDir, 
                     searchTargetFile, 
                     pError,
                     pWarning, 
                     resolvePath, 
                     getConfig, 
                     executeByExtension, 
                     ParserArguments, 
                     printUsage)

from .vars.config import _TARGET_FILENAME
from .vars.paths import _CURRENT_DIR, _CONFIG_FILE_PATH

verifyConfigDir()

_CONFIG = getConfig(_CONFIG_FILE_PATH)
if _CONFIG == None:
    sys.exit(1)

def multiple_target_files(targets_filename):
    length_files_found = len(targets_filename)

    pWarning(f"Which {_TARGET_FILENAME} file do you want execute.")
    for _index , _target in enumerate(targets_filename):
        print(f"[{_index}]  {os.path.basename(_target)}")
    
    print("[*] Enter to execute all.")

    op = input("> ")

    #execute all target file
    if op == "":
        for _path in targets_filename:
            executeByExtension(_path , _CONFIG)
        sys.exit(0)

    #some errors
    if not op.isdigit():
        pError("[-] Selection must be a digit or empty.")
        sys.exit(1)

    if int(op) > length_files_found:
        pError(f"[-] {op} Not exits")
        sys.exit(1)
    
    #excute specific target file
    executeByExtension(targets_filename[int(op)] , _CONFIG)
    sys.exit(0)
    
def run():
    targets_filename = searchTargetFile(_TARGET_FILENAME, resolvePath(_CURRENT_DIR))
    
    if not targets_filename:
        pError(f"[-] Target file {_TARGET_FILENAME} Not found.")        
        return

    if type(targets_filename) == list :
        multiple_target_files(targets_filename)
    
    #if only one target file execute it.
    executeByExtension(targets_filename, _CONFIG)
    
def main():
    parser_arguments = ParserArguments()    
    parser_arguments.add("--help", "-h")
    parser_arguments.add("--target" , "-T", length=2)
    
    arg = parser_arguments.get()
  
    target = arg.target
    help = arg.help

    if help:
        printUsage()
        return
        
    if target:
        global _TARGET_FILENAME 
        _TARGET_FILENAME = target
    
    try:
        run()
    
    except KeyboardInterrupt:
        pass

    except Exception:
        pass

    finally:
        pass