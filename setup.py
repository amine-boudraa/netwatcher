from pip._internal import main as pip

def main():
    pip(['install', '-r', 'requirements.txt'])

if __name__ == "__main__":
    main()
