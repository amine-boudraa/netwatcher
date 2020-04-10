from pip._internal import main as pip
import argparse

def setup():


      parser = argparse.ArgumentParser(description="Configuration")
      parser.add_argument('-u', '--telegramUserToken',type=int, help="Telegram user token")
      parser.add_argument('-gid', '--telegramGroupID',type=int, help="Telegram group ID")
      parser.add_argument('-r', '--requirements',action='store_true',help="Requirements")

      args = parser.parse_args()

      if args.telegramUserToken and args.telegramGroupID:
          generateTelegramConfiguration(args.telegramUserToken,args.telegramGroupID)

      if args.requirements:
             pip(['install', '-r', 'requirements.txt'])


def generateTelegramConfiguration(telegramUserToken,telegramGroupID):
    print("TODO : Generer fichier de configuration avec les bons fields")

def main():
    setup()

if __name__ == "__main__":
    main()
