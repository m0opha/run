import subprocess
import os

from .generic_fun import getConfig
from .get_binary_path import getBinaryPath
from .print_colors import pError, pSuccess, pWarning

from ..vars.paths import _CONFIG_FILE_PATH


def executeByExtension(path:str, interpreters=None, arg=None):

    if not type(interpreters) == dict:
        interpreters = {}

    _ , extension = os.path.splitext(path)

    if extension[1:] not in interpreters.keys():
        pError(f"[-] Extension {extension} It is not configured")
        return 
    
    interpreter_path = getBinaryPath(interpreters[extension[1:]])

    pWarning(f"[*] running {os.path.basename(path)} with {os.path.basename(interpreter_path)}")
    subprocess.run([interpreter_path , path])
    pSuccess(f"[+]{os.path.basename(interpreter_path)} execution done.")