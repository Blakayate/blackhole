from colorama import init, Fore
# Init colorama
init()

# Log messages
def info(message):
    symbol = '[' + (Fore.GREEN + '+' + Fore.RESET) + '] '

    print(symbol + message)

def warning(message):
    symbol = '[' + (Fore.YELLOW + '-' + Fore.RESET) + '] '

    print(symbol + message)

def error(message):
    symbol = '[' + (Fore.RED + '!' + Fore.RESET) + '] '

    print(symbol + message)