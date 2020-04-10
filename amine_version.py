#!/usr/bin/env python3
import socket
import sys
from optparse import OptionParser
import datetime
import time
import requests
import signal
import os
import classes
#import telegram



def keyboardInterruptHandler(signal, frame):
    print("\nShutdown says bye...")
    quit()

signal.signal(signal.SIGINT, keyboardInterruptHandler)




def options():
    global cibles
    global mtimeout
    global timeout
    global sleep
    global outfile
    global lines
    global notif
    parser = OptionParser()
    parser.add_option("-t", "--targets", action="append", dest="cibles", type="string", help="Select a taret in the format IP:PORT, IP:PORT1,PORT2, IP:PORT1-PORT3")
    parser.add_option("-s", "--sleep", dest="sleep", type="int", help="Time to sleep between each request batch", default=1)
    parser.add_option("-l", "--lines", dest="lines", type="int", help="Show X last requests in the \"buffer\".", default=10)
    parser.add_option("-T", "--timeout", dest="timeout", type="float", help="Timeout of each request", default=0.1)
    parser.add_option("-m", "--maxtimeout", dest="mtimeout", type="float", help="Max timeout (request kill) of each request", default=15.0)
    parser.add_option("-o", "--outfile", dest="outfile", type="string", help="Name of the file where logs have to be written", default='webservers-status.log')
    #parser.add_option("-n",  "--notigram", dest="notification", action="store_true", help="Activate telegram notification to the 'Alert!!!' group with the 'Status_bot'", default=False)
    (options, args) = parser.parse_args()
    if not options.cibles:
        parser.error('Target not given')

    cibles = options.cibles
    mtimeout = options.mtimeout
    timeout = options.timeout
    sleep = options.sleep
    outfile = options.outfile
    lines = options.lines
    notif = options.notification

def healthbar(a, b, c, d):
    A = bcolors.OKGREEN + '■' + bcolors.ENDC
    B = bcolors.WARNING  + '■' + bcolors.ENDC
    C = bcolors.MAGENTA + '■' + bcolors.ENDC
    D = bcolors.FAIL + '■' + bcolors.ENDC
    print(A * int(a/2) + B * int(b/2) + C * int(c/2) + D * int(d/2))

def banner():
    Total_reqs = OK_reqs + Timeout_reqs + KO_reqs + MTO_reqs
    os.system('clear')
    print_bold('Checking availability of web targets')
    print()
    print_bold('Settings')
    #print('   > URLs       : ' + str(urls))
    print('   > Timeout    : ' + str(timeout))
    print('   > Max timeout: ' + str(mtimeout))
    print('   > Outfile    : ' + str(outfile))
    print()
    if Total_reqs != 0:
        OK_reqs_perc = int(100 * OK_reqs / Total_reqs)
        Timeout_reqs_perc = int(100 * Timeout_reqs / Total_reqs)
        MTO_reqs_perc = int(100 * MTO_reqs / Total_reqs)
        KO_reqs_perc = int(100 * KO_reqs / Total_reqs)
        print_bold('Results')
        print('   > OK           : ' + str(OK_reqs_perc) + '% (' + str(OK_reqs) + ')')
        print('   > Timeouts     : ' + str(Timeout_reqs_perc) + '% (' + str(Timeout_reqs) + ')')
        print('   > Max timeouts : ' + str(MTO_reqs_perc) + '% (' + str(MTO_reqs) + ')')
        if KO_reqs != 0:
            print('   > ' + bcolors.BLINK + bcolors.REVERT + 'KO           : ' + str(KO_reqs_perc) + '% (' + str(KO_reqs) + ')' + bcolors.ENDC)
        else:
            print('   > KO           : ' + str(KO_reqs_perc) + '% (' + str(KO_reqs) + ')')
        print()
        print_bold('Health bar')
        if int(OK_reqs_perc/2) + int(Timeout_reqs_perc/2) + int(MTO_reqs_perc/2) + int(KO_reqs_perc/2) != 50:
            if KO_reqs_perc != 0:
                KO_reqs_perc += 1
            elif Timeout_reqs_perc != 0:
                Timeout_reqs_perc += 1
            elif MTO_reqs_perc != 0:
                MTO_reqs_perc += 1
        healthbar(OK_reqs_perc, Timeout_reqs_perc, MTO_reqs_perc, KO_reqs_perc)
        print()
    else:
        OK_reqs_perc = 0
        Timeout_reqs_perc = 0
        MTO_reqs_perc = 0
        KO_reqs_perc = 0
        print_bold('Results')
        print('   > OK         : ' + str(OK_reqs_perc) + '% (' + str(OK_reqs) + ')')
        print('   > Timeouts   : ' + str(Timeout_reqs_perc) + '% (' + str(Timeout_reqs) + ')')
        print('   > Max timeout: ' + str(MTO_reqs_perc) + '% (' + str(MTO_reqs) + ')')
        print('   > KO         : ' + str(KO_reqs_perc) + '% (' + str(KO_reqs) + ')')
        print()
        print_bold('Health bar')
        print('■' * 50)
        print()
    print_bold('Last ' + str(lines) + ' requests')

def print_bold(content):
    print(bcolors.BOLD + content + bcolors.ENDC)

def queue(data):
    global requests_results
    if len(requests_results) == (lines):
        requests_results.pop(0)
    requests_results.append(data)

def logtofile(data, file):
    with open(file, 'a+') as f:
        f.write(data + "\n")
        f.close()

def treatment(data, file):
    queue(data)
    logtofile(data, file)
    print(data)

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

def progressbar(sleeptime):
    print()
    with ChargingBar('Sleeping...') as bar:
        for i in range(100):
            time.sleep(sleeptime / 100)
            bar.next()

#def telegram_notif(url, port):
#        bot = telegram.Bot(token='1093736486:AAH4hKrx81zD_7dq7VQMMVNSOlnHiUV0wNo')
#        bot.send_message('-378188970', text="Le domaine ou l'IP " + url +':' + port + " est Down - Retourne bosser!")


def parseCibles():
	target_list = []
	i = 1
	for cible in cibles:
		name = 'target' + str(i)
		i = i + 1
		if 'http' in cible:
			ip = cible.split('/')[-1]
			object = target(name,ip)
			target_list.append(object)
			object.add_port(80)
			if 'https' in cible:
				print('   > Sleep      : ' + str(sleep))
				object.add_port(443)
		else:
			ip, ports_arg = cible.split(':')
			object = target(name,ip)
			target_list.append(object)
			if ',' in ports_arg :
				ports_list = ports_arg.split(',')
				for port in ports_list:
					object.add_port(port)
			elif '-' in ports_arg:
				portA, portB = ports_arg.split('-')
				for y in range(int(portB)+1):
					if y >= int(portA):
						object.add_port(y)
	return target_list

def test_connection(ip, port):
    global KO_reqs
    global Timeout_reqs
    global OK_reqs
    global requests_results
    global MTO_reqs
    global timeout_time

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(mtimeout)
        sock.connect((ip, port))
        OK_reqs += 1
        print_ok(ip, str(port))
        sock.shutdown(socket.SHUT_WR)

    except socket.timeout:
        Timeout_reqs += 1
        print_timeout(ip, request_time, str(port))
        sock.shutdown(socket.SHUT_WR)

    except:
        KO_reqs += 1
        print_ko(ip, str(port))
        if notif == True:
            telegram_notif(ip, str(port))

def main():
    options()
    global KO_reqs
    global Timeout_reqs
    global OK_reqs
    global requests_results
    global MTO_reqs
    global timeout_time
    requests_results = []
    KO_reqs = 0
    Timeout_reqs = 0
    MTO_reqs = 0
    OK_reqs = 0
    target_list = parseCibles()

    while True:
        banner()
        for res in requests_results:
            print(res)
        for target in target_list:
            timeout_time = time.time()
            for port in target.ports:
                test_connection(target.value, int(port))
        progressbar(sleep)

if __name__ == '__main__':
    main()
