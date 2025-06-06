from colorama import Fore, Style, init
from types import SimpleNamespace
import os
import re
import subprocess
import sys


RUN = "run"
PWD = "PWD"
HOME = "HOME"
CONFIG = ".config"
PATH = "PATH"
TILDE = "~"
DOT = "."
COLON = ":"

_TARGET_FILENAME = RUN
_EXECUTE_ALL_FLAG = False

content = ["#basic conficuration\n"
           "#binary and extension\n"
           "python3 = py\n",
           "bash = sh\n",
           "gcc = c\n",
           "ruby = rb"]

_APP_NAME = RUN
_TARGET_FILENAME = RUN
_CURRENT_DIR = os.getenv(PWD)

if os.name == "posix":
    _CONFIG_PATH = os.path.join(os.getenv(HOME), CONFIG, _APP_NAME)

if os.name == "nt":
    _CONFIG_PATH = os.path.join(os.getenv('APPDATA'), _APP_NAME)

_CONFIG_FILE_PATH = os.path.join(_CONFIG_PATH, "config.txt")

CONFIG_DIRECTORY_CREATED_TEXT = "[+] Config directory has been created."
PLEASE_SETTING_UP_CONFIG_FILE_TEXT = "[+] Please setting up config file"

def verifyConfigDir():

    if not os.path.exists(_CONFIG_PATH):
        os.mkdir(_CONFIG_PATH)
        pSuccess(CONFIG_DIRECTORY_CREATED_TEXT)

    if not os.path.exists(_CONFIG_FILE_PATH):
        with open(_CONFIG_FILE_PATH, "w") as file:
            file.writelines(content)
            print(PLEASE_SETTING_UP_CONFIG_FILE_TEXT)
            
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

_CONFIG = getConfig(_CONFIG_FILE_PATH)

def getBinaryPath(binary: str):
    binarys_found = []
    put = binarys_found.append

    environment_paths = os.getenv("PATH", "").split(os.pathsep)

    # Agregar extensiones en Windows si es necesario
    if os.name == "nt":
        pathext = os.getenv("PATHEXT", ".EXE;.BAT;.CMD").split(os.pathsep)
        possible_names = [binary.lower() + ext.lower() for ext in pathext]
    else:
        possible_names = [binary]

    for _path in environment_paths:
        absolute_path = resolvePath(_path)

        if not os.path.exists(absolute_path):
            continue

        try:
            for _item in os.listdir(absolute_path):
                binary_path = os.path.join(absolute_path, _item)

                if os.path.isdir(binary_path):
                    continue

                filename = os.path.basename(binary_path).lower()

                if os.name == "nt":
                    if filename in possible_names:
                        return binary_path
                else:
                    if filename == binary.lower():
                        return binary_path
        except Exception:
            continue

    return None

def argumentsTree(argv: list):
    arguments_struct = {}

    unparsed_arguments = " ".join(argv)
    splited_unparsed_arguments = re.split(r" -{1,2}", unparsed_arguments)

    for _argv in splited_unparsed_arguments:
        content_argument = _argv.strip().split(" ")

        if not content_argument or content_argument[0] == "":
            continue

        # Transformar --argumento-to en argumento_to
        argument_name = content_argument[0].replace("-", "_")

        if len(content_argument) == 1:
            value = None
        elif len(content_argument) == 2:
            value = content_argument[1]
        else:
            value = content_argument[1:]

        arguments_struct[argument_name] = value

    return arguments_struct

class ParserArguments:
    def __init__(self):
        self.system_arguments = sys.argv
        self.filename = self.system_arguments[0]
        self.parsed_arguments = argumentsTree(self.system_arguments)

        self.arguments_added = {}
        self.arguments_allowed = []

    def add(self, *arg, text_help=None, length=1):
        arguments_allowed_forms = sorted(
            [a.lstrip('-').replace('-', '_') for a in arg],
            reverse=True
        )

        canonical_name = arguments_allowed_forms[0]

        self.arguments_added[canonical_name] = {
            "arguments": arguments_allowed_forms,
            "text_help": text_help,
            "length": length,
        }
    def get(self):
        arguments_allowed = [arg for data in self.arguments_added.values() for arg in data["arguments"]]
        ns = SimpleNamespace()

        for arg, _values in self.parsed_arguments.items():

            if arg not in arguments_allowed and arg != self.filename:
                print(f"[-] Argument {arg} not recognized.")
                continue

            if arg == self.filename:
                setattr(ns, "free_values", _values)
                continue


            variable_name, options = self._getVarName(arg)
            length = options["length"]

            # Si no se pasa ningún valor (None o vacío), se asume booleano
            if _values is None or (_values == [] or _values == ""):
                setattr(ns, variable_name, True)
                continue

            if length > len(_values):
                print(f"[-] Maximun values for this {arg} is {length}.")
                continue

            setattr(ns, variable_name, _values)

        for arg in arguments_allowed:
            if not hasattr(ns, arg):
                setattr(ns, arg, None)

        return ns

    def _getVarName(self, argument):
        for _variable_name, _values in self.arguments_added.items():
            if argument in _values["arguments"]:
                return _variable_name , self.arguments_added[_variable_name]


init(autoreset=True)

def pSuccess(text: str):
    print(f"{Fore.GREEN}{Style.BRIGHT}{text}")

def pError(text: str):
    print(f"{Fore.RED}{Style.BRIGHT}{text}")

def pWarning(text: str):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{text}")



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

def printUsage():
    usage = """
Usage:
  ./run [--help] [--target <keyword>] [--path <path>]

Options:
  --help, -h                  Displays this help message and exits.
  --target, -T <keyword>      (optional) Specifies the target keyword.
  --path, -p <path>           Specifies the path to scan a run it!.
  --execute-all, -EA          Execute all script with the target keyword

Examples:
  ./run --target run
  ./run -h"""
    print(usage)
    return

verifyConfigDir()


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

from src.main import main

if __name__ == "__main__":
    main()