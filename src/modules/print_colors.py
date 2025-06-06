from colorama import Fore, Style, init

init(autoreset=True)

def pSuccess(text: str):
    print(f"{Fore.GREEN}{Style.BRIGHT}{text}")

def pError(text: str):
    print(f"{Fore.RED}{Style.BRIGHT}{text}")

def pWarning(text: str):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{text}")