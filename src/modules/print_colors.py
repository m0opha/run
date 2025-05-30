from colorama import Fore, Style

def pSuccess(text:str):
    print(f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def pError(text:str):
    print(f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def pWarning(text:str):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}")