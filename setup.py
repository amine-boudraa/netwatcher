from pip._internal import main as pip
import argparse
import json

def setup():


      parser = argparse.ArgumentParser(description="Configuration")
      parser.add_argument('-tbn', '--telegramBotToken', help="Telegram bot token")
      parser.add_argument('-tcid', '--telegramChatID' , help="Telegram chat ID")
      parser.add_argument('-r', '--requirements',action='store_true',help="Requirements")

      args = parser.parse_args()

      if args.telegramBotToken and args.telegramChatID:
          generateTelegramConfiguration(args.telegramBotToken,args.telegramChatID)

      if args.requirements:
          pip(['install', '-r', 'requirements.txt'])


def generateTelegramConfiguration(telegramBotToken,telegramChatID):
      data = {}
      data['telegram_configuration'] = []
      data['telegram_configuration'].append({
           'telegramBotToken': telegramBotToken,
           'telegramChatID': telegramChatID,
        })

      with open('configuration.json', 'w') as outfile:
         json.dump(data, outfile)

def main():
    setup()

if __name__ == "__main__":
    main()
