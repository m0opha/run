import os
import sys
import subprocess
import json

__CURRENT_DIR = os.getenv("PWD")
__TARGET_FILENAME = "run"

__CONFIG_PATH = os.path.join(os.getenv("HOME"), ".config", "run")
__CONFIG_FILE = os.path.join(__CONFIG_PATH, "config.json")

def createConfigDir():
    if os.path.exists(__CONFIG_PATH) == False:
        os.mkdir(__CONFIG_PATH)
        print("[+]Config directory has been created.")

        with open(__CONFIG_FILE, "w") as file:
            file.write('{\n"python3" : "py",\n"bash": "sh",\n"gcc" : "c"\n}')
            print("[+] Please setting up config.json")

createConfigDir()


def loadJson(path):
    with open(path , "r") as file:
        data = json.load(file)
    return data

def getPathBinary(binary:str):
    path = subprocess.run(["which", binary], capture_output=True, text=True)
    return path.stdout.strip()


def loadConfig():
    config = loadJson(__CONFIG_FILE)
    extension_interpreters = {}

    for _binary , _extension in config.items():
        extension_interpreters[_extension] = getPathBinary(_binary)
    
    return extension_interpreters
    
__EXTENSION_INTERPRETERS = loadConfig()


def splitFileAndExtension(content_dir:list):
    files = {}
    for _index, _item in enumerate(content_dir):
        if os.path.isfile(_item):
            full_name = _item.split(".")
            
            filename = full_name[0]
            extension = full_name[1]

            files[_index] = [filename, extension]
    
    return files

def main():
    content_dir = os.listdir(__CURRENT_DIR)    
    files_splited = splitFileAndExtension(content_dir)
    
    for _index , _content in files_splited.items():
        file_path = ""
        interpreter_path = ""
        if _content[0] != __TARGET_FILENAME:
            continue
       
        if _content[1] not in list(__EXTENSION_INTERPRETERS.keys()):
            continue
        
        
        interpreter_path = __EXTENSION_INTERPRETERS[_content[1]]
        file_path = os.path.join( __CURRENT_DIR ,".".join(_content))
    

        print(f"[*]Runing script with {os.path.basename(interpreter_path)}")
        subprocess.run([interpreter_path, file_path])
        sys.exit(0)

    print("[*]run file wasn't found.")

if __name__ == "__main__":
    main()
