from progress.bar import Bar

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    MAGENTA = '\033[35m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BLINK = '\033[6m'
    REVERT = '\033[7m'
    UNDERLINE = '\033[4m'

class ChargingBar(Bar):
   suffix = '%(percent)d%%'
   bar_prefix = ' '
   bar_suffix = ' '
   empty_fill = '-'
   fill = '■'


class target:

   def __init__(self, name, value):
       self.name = name
       self.value = value
       self.ports = []

   def add_port(self, port):
       self.ports.append(port)

   def __repr__(self):
       return str(self.name) + ": " + str(self.value) + ": " + str(self.ports)
