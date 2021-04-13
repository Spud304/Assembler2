import json
import sys, getopt
import os
import time
import re

os.system("")

# Copyright, 2021, Henry Price, All rights Reserved
# I did not create this, only using it for testing the times

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")


def asciiart():
  Spud = f'{style.GREENBG2}Spud{style.RESET}'
  TheError = f'{style.VIOLET}TheError07{style.RESET}'
  for i in range(4):
    print('')
  print(f"""           
           ___________________________________
          /                                   \                                          
          |A Creation By {Spud} and {TheError}  |
          \___________________________________/
  
  """)
  print(style.BLUE + """
          /$$       /$$$$$$ /$$       /$$
          | $$      |_  $$_/| $$$    /$$$
          | $$        | $$  | $$$$  /$$$$
          | $$        | $$  | $$ $$/$$ $$
          | $$        | $$  | $$  $$$| $$
          | $$        | $$  | $$\  $ | $$
          | $$$$$$$$ /$$$$$$| $$ \/  | $$
          |________/|______/|__/     |__/
""" + style.RESET)

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


def errorLogger(msg, line):
    print(f'{style.RED}{msg} on line: {line} caused a problem{style.RESET}')
    print('Killing process, fix your shit')
    input('Press enter to close... ')
    os.kill(os.getpid(), 9)


def checkDataType(msg: str, line):
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
    errorLogger(msg, line)


def dataType0(msg: str, line):
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
  except ValueError:
    errorLogger(msg, line)


def dataType1(msg: str, address: int, line):
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
    errorLogger(msg, line)

def dataType2(msg: str, value: int, line):
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
    errorLogger(msg, line)


def writeToHighLowFile(output):
  # print(len(output))
  if len(output.strip()) == 0:
    return
  dataHigh = output[0:8]
  dataLow = output[8:16]
  # print(data)
  try:
    DEBUG_FILE = 'debug.txt'
    # print(f'high {output[0:7]}')
    # print(f'low {output[8:15]}')
    HIGH_FILE = 'high.bin'
    LOW_FILE = 'low.bin'
    HF = openOrCreate(HIGH_FILE)
    # print(bytearray(output[0:8]))
    # print(type(output[8:16]))
    # HF.write(hex(int(output[0:8], 2)) + '\n')
    HF.write(dataHigh + '\n')
    # HF.write(bytes(output[0:8], encoding='ansi'))
    HF.close()
    LF = openOrCreate(LOW_FILE)
    LF.write(dataLow + '\n')
    # LF.write(hex(int(output[8:16], 2)) + '\n')
    # LF.write(bytes(output[8:16], encoding='ansi'))

    LF.close()
    if DEBUGGING == True:
      DF = openOrCreate(DEBUG_FILE)
      DF.write(output + '\n')
      DF.close()
  except:
    return

def createTempFile(FileName):
  if FileName == '':
    return
  temp_file = os.path.splitext(FileName)[0]+'_temp.asm'
  openOrCreate(temp_file)
  toCopy = open(FileName, 'r').read()
  openTemp = open(temp_file, 'w')
  openTemp.write(toCopy)
  openTemp.close()
  return temp_file

def removeAllComments(FileName):
  print(FileName)
  pattern = '(\/\*(\w|\D)+\*\/)|(\/\/(?:[^\r\n]|\r(?!\n))*)'
  file = open(FileName, 'r').read()
  nfile = re.sub(pattern, '', file)
  wfile = open(FileName, 'w')
  # print(wfile)
  wfile.write(nfile)
  wfile.close()
    

def symbolWrite(init_Table):
  #In charge of opening and writing the symbolTable
  Symbol_Table = open('symbolTable.json', 'w')
  jsonf = json.dumps(init_Table)
  Symbol_Table.write(jsonf)
  Symbol_Table.close()


def firstPass(FileName, init_Table):
  removeAllComments(FileName)
  file = open(FileName, 'r').read() #open file
  L_FILE = file.split('\n')
  LL_FILE  = [x for x in L_FILE if x]
  line_Counter = 0
  pattern = ('\w+:')
  for line in LL_FILE:
    # print('test')
    #line[0] = instruction, line[1] = label, assuming not subroutine
    #line[0] = JSR, line[1] = Subroutine, line[2] = label
    #init_Table[name] = number
    print(line)
    temp_Line = line.split(' ')
    
    while("" in temp_Line) :
      temp_Line.remove("")
    # print(line)
    # print(re.search(pattern, line))
    # print(temp_Line)
    if re.search(pattern, line):
      # print(temp_Line)
      if len(temp_Line) == 1:
        init_Table[temp_Line[0].split(':')[0]] = hex(line_Counter)
        # print('len 1')
        continue
      if len(temp_Line) == 2:
        init_Table[temp_Line[1].split(':')[0]] = hex(line_Counter)
        # print('len 2')
        continue
      if len(temp_Line) == 3:
        init_Table[temp_Line[2].split(':')[0]] = hex(line_Counter)
        # print('len 3')
        continue
    # if ':' in line and temp_Line[0] != 'JSR':
    #   init_Table[temp_Line[2].split(':')[0]] = hex(line_Counter)
    # if ':' in line and temp_Line[0] == 'JSR':
    #   init_Table[temp_Line[2].split(':')[0]] = hex(line_Counter)
    if '#define' in line:
      define, var, address = line.split(' ')
      init_Table[var] = address
      line_Counter -= 1
    line_Counter += 1
  symbolWrite(init_Table)


def run(FileName):
  wipeFiles()
  init_Table = {}
  line_Counter = 1
  firstPass(FileName, init_Table)
  file = open(FileName, 'r').read() #open file
  L_FILE = file.split('\n')
  LL_FILE = []
  # LL_FILE  = [x for x in L_FILE if x]
  # really ugly for loop since I need to increment line counter
  for x in L_FILE:
    if x != '':
      LL_FILE.append(x.split(';', 1)[0])
    else:
      LL_FILE.append(x)

  # print(LL_FILE)
  for line in LL_FILE:
    if len(line.strip()) == 0:
      line_Counter += 1
      continue
    NL_FILE = line.split(' ')
    out = ''
    try:
      if checkDataType(NL_FILE[0], line_Counter) == 'type0':
        out = dataType0(NL_FILE[0], line_Counter)
      if checkDataType(NL_FILE[0], line_Counter) == 'typeVar':
        out = ''
      if len(NL_FILE) > 1:
        if NL_FILE[1] in init_Table.keys() and NL_FILE[0] != '#define': 
          NL_FILE[1] = init_Table[str(NL_FILE[1])]
      if checkDataType(NL_FILE[0], line_Counter) == 'type1':
        out = dataType1(NL_FILE[0], int(NL_FILE[1], 16), line_Counter)
      if checkDataType(NL_FILE[0], line_Counter) == 'type2':
        out = dataType2(NL_FILE[0], int(NL_FILE[1], 16), line_Counter)
    except:
      errorLogger(NL_FILE[0], line_Counter)
    # try:
    # print(bytes(out, encoding='ansi'))
    writeToHighLowFile(out)
    # except:
      # print(f'something went wrong, tried to write {out}')
    line_Counter += 1


def main(argv):
  # options = "hd:"
  # long_options = ["Help", "debug"]
  # try:
  #   # Parsing argument
  #   arguments, values = getopt.getopt(argv, options, long_options)
  #   # checking each argument
  #   ##TODO: GET THIS TO WORK
  #   for currentArgument, currentValue in arguments:
  #     print(1)
  #     # print(currentArgument, currentValue)
  #     if currentArgument in ("-h", "--Help"):
  #       print ("LIM.py <filename> <debug>")
  #       print ("With the debug flag a txt dump of the output will be created")      
  #     elif currentArgument in ("-d", "--debug"):
  #       DEBUGGING = TRUE
  #       print ("debug mode")
    
    run(argv)

  # except getopt.error as err:
  #   # output error, and return with an error code
  #   print (str(err))


if __name__ == "__main__":
  os.system('cls' if os.name == 'nt' else 'clear')
  asciiart()
  #1st arg is script name
  file = input('Input full path to .asm file here: ')
  t.start()
  file = createTempFile(file)
  # print(file)
  main(file)
  num_lines = sum(1 for line in open(file))
  for i in progressbar(range(100), "Computing: ", 40):
    time.sleep(0.0001) # ineffcient but looks cool as hell
  t.stop()
  os.remove(file)
  print(f'You have used {num_lines} words of memory out of 2012')
  input('Press enter to close... ')

