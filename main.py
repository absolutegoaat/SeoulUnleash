import os
import sys
import platform
import subprocess
from colorama import Fore, Style
from builder import main as build_loader

if platform.system() == "Windows":
    os.system('cls')
else:
    os.system('clear')

banner = '''
  █████████                               ████  █████  █████            ████                             █████     
 ███▒▒▒▒▒███                             ▒▒███ ▒▒███  ▒▒███            ▒▒███                            ▒▒███      
▒███    ▒▒▒   ██████   ██████  █████ ████ ▒███  ▒███   ▒███  ████████   ▒███   ██████   ██████    █████  ▒███████  
▒▒█████████  ███▒▒███ ███▒▒███▒▒███ ▒███  ▒███  ▒███   ▒███ ▒▒███▒▒███  ▒███  ███▒▒███ ▒▒▒▒▒███  ███▒▒   ▒███▒▒███ 
 ▒▒▒▒▒▒▒▒███▒███████ ▒███ ▒███ ▒███ ▒███  ▒███  ▒███   ▒███  ▒███ ▒███  ▒███ ▒███████   ███████ ▒▒█████  ▒███ ▒███ 
 ███    ▒███▒███▒▒▒  ▒███ ▒███ ▒███ ▒███  ▒███  ▒███   ▒███  ▒███ ▒███  ▒███ ▒███▒▒▒   ███▒▒███  ▒▒▒▒███ ▒███ ▒███ 
▒▒█████████ ▒▒██████ ▒▒██████  ▒▒████████ █████ ▒▒████████   ████ █████ █████▒▒██████ ▒▒████████ ██████  ████ █████
 ▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒   ▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒ ▒▒▒▒▒   ▒▒▒▒▒▒▒▒   ▒▒▒▒ ▒▒▒▒▒ ▒▒▒▒▒  ▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒  ▒▒▒▒ ▒▒▒▒▒ 
                                                                                                                   
            Created by: absolutegoaat
            run "help" for commands and information
'''

print(Fore.MAGENTA + banner + Style.RESET_ALL)

def check_py_version():
    if sys.version_info >= (3, 6):
        print(Fore.GREEN + "Python Version is A-OK!" + Style.RESET_ALL + "\n")
    else:
        print(Fore.RED + "Python Version is not supported! Please use Python 3.6 or higher." + Style.RESET_ALL)
        sys.exit(0)
def main():
    check_py_version()
    userinput = input("SEOUL >> ").lower()
    if userinput == "exit":
        print(Fore.YELLOW + "[-] Exiting SeoulUnleash..." + Style.RESET_ALL)
        sys.exit(0)
    elif userinput == "start":
        print(Fore.GREEN + "[+] Starting SeoulUnleash..." + Style.RESET_ALL)
        build_loader()
    elif userinput == "startserver":
        print(Fore.YELLOW + "[*] Starting the server..." + Style.RESET_ALL)
        directory = input('Enter the directory to serve the zip file: ')
        if platform.system() == "Windows":
            subprocess.run(["python", "-m", "http.server", "8080", "--directory", directory])
            print(Fore.GREEN + '[*] Server started at port 8080' + Style.RESET_ALL)
            print(Fore.BLUE + '[*] Its Recommended to open another terminal and make the executable' + Style.RESET_ALL)
        else:
            subprocess.run(["python3", "-m", "http.server", "8080", "--directory", directory])
            print(Fore.GREEN + '[*] Server started at port 8080' + Style.RESET_ALL)
            print(Fore.BLUE + '[*] Its Recommended to open another terminal and make the executable' + Style.RESET_ALL)
    elif userinput == "help":
        print(Fore.MAGENTA + """
Available commands:
- start: Build the loader and create the executable.
- startserver: Start a simple HTTP server to serve the zip file.
- exit: Exit SeoulUnleash.
- help: Show this help message.
- about: Show information about SeoulUnleash.
        """ + Style.RESET_ALL)
        main()
    elif userinput == "about":
        print(Fore.CYAN + """
SeoulUnleash is a Python-based tool designed to create a loader executables.
It is intended for educational purposes and should not be used for malicious activities.
Created by: absolutegoaat
        """ + Style.RESET_ALL)
        main()
    else:
        print(Fore.RED + "[-] Unknown command. Please type 'start' to begin or 'exit' to quit." + Style.RESET_ALL)
        main() 

if __name__ == "__main__":
    main()