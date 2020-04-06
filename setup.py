import sys

def progress_module():
    try:
        import progress
    except ModuleNotFoundError as error:
        try:
            choice = input('[*] Missing progress module, would you like to install it ? [yY/nN] ')
        except KeyboardInterrupt:
            print('[!] User keyboard interrupt !')
            raise SystemExit
        if choice.strip().lower()[0] == 'y':
            print('[*] Trying to install progress...')
            sys.stdout.flush()
            try:
                from pip._internal import main as pip
                pip(['install', '--user', 'progress'])
                print('[+] Installing progress...')
                from progress.bar import Bar
                print('[!] Successfully imported progress.bar')

            except Exception:
                print('[!] Failed to install progress.bar')
                raise SystemExit
        elif choice.strip().lower()[0] == 'n':
            print('[+] Canceled : progress.bar module will not be installed')
            raise SystemExit
        else:
            print('[!] Invalid user input')
            raise SystemExit


def install_modules():
    progress_module()


def main():
    install_modules()

if __name__ == "__main__":
    main()
