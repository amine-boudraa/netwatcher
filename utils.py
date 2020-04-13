from classes import *
from optparse import OptionParser
import time


def print_bold(content):
    print(bcolors.BOLD + content + bcolors.ENDC)

def print_ok(url, port):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = bcolors.OKGREEN + '[OK]' + bcolors.ENDC + ' [' + date + '] ' + url + ':' + port
    treatment(log, outfile)

def print_timeout(url, timeout, port):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = bcolors.WARNING + '[Timeout ' + str(timeout)[:5] + ']' + bcolors.ENDC + ' [' + date + '] ' + url + ':' + port
    treatment(log, outfile)

def print_ko(url, port):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = bcolors.FAIL + '[KO]' + bcolors.ENDC + ' [' + date + '] ' + url + ':' + port
    treatment(log, outfile)

def logtofile(data, file):
    with open(file, 'a+') as f:
        f.write(data + "\n")
        f.close()

def treatment(data, file):
    queue(data)
    logtofile(data, file)
    print(data)

def queue(data):
    global requests_results
    if len(requests_results) == (lines):
        requests_results.pop(0)
    requests_results.append(data)

def keyboardInterruptHandler(signal, frame):
    print("\nShutdown says bye...")
    quit()

def healthbar(a, b, c, d):
    A = bcolors.OKGREEN + '■' + bcolors.ENDC
    B = bcolors.WARNING  + '■' + bcolors.ENDC
    C = bcolors.MAGENTA + '■' + bcolors.ENDC
    D = bcolors.FAIL + '■' + bcolors.ENDC
    print(A * int(a/2) + B * int(b/2) + C * int(c/2) + D * int(d/2))

def progressbar(sleeptime):
    print()
    with ChargingBar('Sleeping...') as bar:
        for i in range(100):
            time.sleep(sleeptime / 100)
            bar.next()

def telegram_notif(url, port):
    with open('configuration.json') as json_file:
        data = json.load(json_file)
        for field in data['telegram_configuration']:
            telegramBotToken = field['telegramBotToken']
            telegramChatID   = field['telegramChatID']
            bot = telegram.Bot(token=telegramBotToken)
            bot.send_message(telegramChatID, text="Le domaine ou l'IP " + str(url) +':' + str(port) + " est Down - Retourne bosser!")
