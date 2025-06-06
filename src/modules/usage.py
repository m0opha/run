def printUsage():
    usage = f"""
Usage:
  ./run [--help] [--target <keyword>] [--path <path>] [--execute-all]

Options:
  --help, -h                 Show this help message and exit.
  --target, -T <keyword>     (Optional) Specify the target filename (without extension) to execute.
  --path, -p <path>          Specify the directory path to search for the script.
  --execute-all, -EA         Execute all scripts that match the target keyword.

Examples:
  ./run --target run
  ./run -h
  ./run --target myscript --path ~/projects
  ./run --target test --execute-all
"""
    print(usage)
