from colorama import init, Fore, Back
# Init colorama
init(autoreset=True)

# Log messages
def warning(message):
    print(Back.YELLOW + Fore.BLACK + message)

def error(message):
    print(Back.RED + Fore.BLACK + message)