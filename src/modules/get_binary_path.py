import os

from .generic_fun import resolvePath

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