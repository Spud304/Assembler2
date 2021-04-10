import json
import sys, getopt
from timer import Timer
import os
import time

os.system("")


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

# Class of different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    VIOLET = '\33[35m'
    GREENBG2  = '\33[92m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

DEBUGGING = True

t = Timer()

def generateZero(msg): #Makes binary numbers have the proper amount of 0's
  mLen = 16 - len(msg)
  out = ''
  for i in range(mLen):
    out += str(0)
  return out


def openOrCreate(file):
    try:
        hack = open(file, 'x')
    except FileExistsError: #Creates file if it does not exist, otherwise it overwrites it
        hack = open(file, 'a')
    return hack

def createTable():
  values = {}
  Symbol_Table = open('symbolTable.json', 'w')
  jsonf = json.dumps(values)
  Symbol_Table.write(jsonf)
  Symbol_Table.close()

def wipeFiles():
  createTable()
  open('high.bin', 'w').close()
  open('low.bin', 'w').close()
  if DEBUGGING == True:
    open('debug.txt', 'w').close()


def checkDataType(msg: str):
  command = {
    '#define' : 'typeVar',
    'LDX' : 'type1',
    'STX' : 'type1',
    'LDY' : 'type1',
    'STY' : 'type1',
    'LVX' : 'type2',
    'LVY' : 'type2',
    'INX' : 'type0',
    'DEX' : 'type0',
    'CMP' : 'type0',
    'JMP' : 'type1',
    'JXL' : 'type1',
    'JYL' : 'type1',
    'JEQ' : 'type1',
    'JNE' : 'type1',
    'JOF' : 'type1',
    'JUF' : 'type1',
    'JSR' : 'type1',
    'RSR' : 'type0',
    'NOP' : 'type0',
    'BRK' : 'type0'
  }
  try:
    # print(f'msg={msg}, type={command[msg]}')
    return command[msg]
  except KeyError:
    print(f'{style.RED}{msg} caused a problem{style.RESET}')
    print('Killing process, fix your shit')
    os.kill(os.getpid(), 9)


def dataType0(msg: str):
  command = {
    'INX' : 0x06,
    'DEX' : 0x07,
    'CMP' : 0x08,
    'RSR' : 0x11,
    'NOP' : 0x12,
    'BRK' : 0x13
  }
  try:
    out = f'{command[msg]:0>5b}'
    return generateZero(out) + out
  except KeyError:
    print(f'{style.RED}{msg} caused a problem{style.RESET}')


def dataType1(msg: str, address: int):
  command = {
    'LDX' : 0x00,
    'STX' : 0x01,
    'LDY' : 0x02,
    'STY' : 0x03,
    'JMP' : 0x09,
    'JXL' : 0x0A,
    'JYL' : 0x0B,
    'JEQ' : 0x0C,
    'JNE' : 0x0D,
    'JOF' : 0x0E,
    'JUF' : 0x0F,
    'JSR' : 0x10,
  }
  try:
    inst = f'{command[msg]:0>5b}'
    add = f'{address:0>11b}'
    return add + inst
  except ValueError:
    print(f'{style.RED}{msg} caused a problem{style.RESET}')

def dataType2(msg: str, value: int):
  command = {
    'LVX' : 0x04,
    'LVY' : 0x05,
  }
  try:
    inst = f'{command[msg]:0>5b}'
    val = f'{value:0>4b}'
    out = val + inst
    return generateZero(out) + out
  except ValueError:
    print(f'{style.RED}{msg} caused a problem{style.RESET}')


def writeToHighLowFile(output):
  DEBUG_FILE = 'debug.txt'
  # print(f'high {output[0:7]}')
  # print(f'low {output[8:15]}')
  HIGH_FILE = 'high.bin'
  LOW_FILE = 'low.bin'
  HF = openOrCreate(HIGH_FILE)
  HF.write(output[0:7] + '\n')
  HF.close()
  LF = openOrCreate(LOW_FILE)
  LF.write(output[8:15] + '\n')
  LF.close()
  if DEBUGGING == True:
    DF = openOrCreate(DEBUG_FILE)
    DF.write(output + '\n')
    DF.close()


def symbolWrite(init_Table):
  #In charge of opening and writing the symbolTable
  Symbol_Table = open('symbolTable.json', 'w')
  jsonf = json.dumps(init_Table)
  Symbol_Table.write(jsonf)
  Symbol_Table.close()


def firstPass(FileName, init_Table):
  file = open(FileName, 'r').read() #open file
  L_FILE = file.split('\n')
  LL_FILE  = [x for x in L_FILE if x]
  line_Counter = 0
  for line in LL_FILE:
    #line[0] = instruction, line[1] = label, assuming not subroutine
    #line[0] = JSR, line[1] = Subroutine, line[2] = label
    #init_Table[name] = number
    temp_Line = line.split(' ')
    if ':' in line and temp_Line[0] != 'JSR':
      init_Table[temp_Line[2].split(':')[0]] = hex(line_Counter)
    if ':' in line and temp_Line[0] == 'JSR':
      init_Table[temp_Line[2].split(':')[0]] = hex(line_Counter)
    if '#define' in line:
      define, var, address = line.split(' ')
      init_Table[var] = address
      line_Counter -= 1
    line_Counter += 1
  symbolWrite(init_Table)


def run(FileName):
  wipeFiles()
  init_Table = {}
  firstPass(FileName, init_Table)
  file = open(FileName, 'r').read() #open file
  L_FILE = file.split('\n')
  LL_FILE  = [x.split(';', 1)[0] for x in L_FILE if x]
  for line in LL_FILE:
    NL_FILE = line.split(' ')
    out = ''
    if checkDataType(NL_FILE[0]) == 'type0':
      out = dataType0(NL_FILE[0])
    if checkDataType(NL_FILE[0]) == 'typeVar':
      out = ''
    if len(NL_FILE) > 1:
      if NL_FILE[1] in init_Table.keys() and NL_FILE[0] != '#define': 
        NL_FILE[1] = init_Table[str(NL_FILE[1])]
    if checkDataType(NL_FILE[0]) == 'type1':
      out = dataType1(NL_FILE[0], int(NL_FILE[1], 16))
    if checkDataType(NL_FILE[0]) == 'type2':
      out = dataType2(NL_FILE[0], int(NL_FILE[1], 16))
    try:
      writeToHighLowFile(out)
    except:
      print(f'something went wrong, tried to write {out}')


def main(argv):
  options = "hd:"
  long_options = ["Help", "debug"]
  try:
    # Parsing argument
    arguments, values = getopt.getopt(argv, options, long_options)
    # checking each argument
    ##TODO: GET THIS TO WORK
    for currentArgument, currentValue in arguments:
      print(1)
      # print(currentArgument, currentValue)
      if currentArgument in ("-h", "--Help"):
        print ("LIM.py <filename> <debug>")
        print ("With the debug flag a txt dump of the output will be created")      
      elif currentArgument in ("-d", "--debug"):
        DEBUGGING = TRUE
        print ("debug mode")
    
    run(argv[0])

  except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

t.start()

# run("music1.asm")

if __name__ == "__main__" and len(sys.argv) >= 2:
  os.system('cls' if os.name == 'nt' else 'clear')
  for i in range(4):
    print('')
  print(f"""           
           ___________________________________
          /                                   \                                          
          |  A Creation By {style.GREENBG2}Spud{style.RESET} and {style.VIOLET}TheError07{style.RESET}|
          \___________________________________/
  
  """)
  print(style.BLUE + """
          /$$       /$$$$$$ /$$      /$$
          | $$      |_  $$_/| $$$    /$$$
          | $$        | $$  | $$$$  /$$$$
          | $$        | $$  | $$ $$/$$ $$
          | $$        | $$  | $$  $$$| $$
          | $$        | $$  | $$\  $ | $$
          | $$$$$$$$ /$$$$$$| $$ \/  | $$
          |________/|______/|__/     |__/
""" + style.RESET)
  #1st arg is script name
  main(sys.argv[1:])
  file = open(sys.argv[1], 'r').read()
  for i in progressbar(range(100), "Computing: ", 40):
    time.sleep(0.0001) # ineffcient but looks cool as hell

t.stop()