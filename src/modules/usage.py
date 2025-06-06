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