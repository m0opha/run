def printUsage():
    usage = """
Usage:
  ./run [--target <filename>] [--help]

Options:
  --target <filename>    (optional) Specifies the target filename.
  --help, -h             Displays this help message and exits.

Examples:
  ./run --target run
  ./run -h"""
    print(usage)