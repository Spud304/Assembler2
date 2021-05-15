import json
import sys
import os
import time
import re
import fnmatch
import distutils.util

os.system("")
VER = '1.0.2'
# DEBUGGING = False

# Copyright, 2021, Henry Price, All rights Reserved
# Discord: Spud#3639


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
    # Simple ASCII art generator
    Spud = f'{style.GREENBG2}Spud{style.RESET}'
    TheError = f'{style.VIOLET}TheError07{style.RESET}'
    for i in range(2):
        print('')

    print(f"""                                               
A Creation By {Spud} and {TheError}

  """)
    print(style.BLUE + """
/ $$      /$$$$$$ /$$       /$$
| $$      |_  $$_/| $$$    /$$$
| $$        | $$  | $$$$  /$$$$
| $$        | $$  | $$ $$/$$ $$
| $$        | $$  | $$  $$$| $$
| $$        | $$  | $$\  $ | $$
| $$$$$$$$ /$$$$$$| $$ \/  | $$
|________/|______/|__/     |__/
""" + style.RESET)
    print(f'Ver: {VER}')


# Progress bar, removed since it took too much time to display
def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

# Class of different styles
# For colors on the console


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
    GREENBG2 = '\33[92m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


t = Timer()


def generateZero(msg):  # Makes binary numbers have the proper amount of 0's
    mLen = 16 - len(msg)
    out = ''
    for i in range(mLen):
        out += str(0)
    return out


def openOrCreate(file):
    try:
        hack = open(file, 'xb')
    except FileExistsError:  # Creates file if it does not exist, otherwise it overwrites it
        hack = open(file, 'ab')
    return hack


def createTable():
    # Create the symbol table, which is responsible for vars and labels
    values = {}
    Symbol_Table = open('symbolTable.json', 'w')
    jsonf = json.dumps(values)
    Symbol_Table.write(jsonf)
    Symbol_Table.close()


def wipeFiles(DEBUGGING):
    # Since high and low .bin are always going to be the outputs they need to be wiped each run
    createTable()
    open('high.bin', 'wb').close()
    open('low.bin', 'wb').close()
    if DEBUGGING == True:
        open('debug.txt', 'w').close()
    else:
        try:
            os.remove('debug.txt')
        except:
            return


def find(pattern):
    # Simple pathfinding code for finding files in the dir
    path = os.getcwd()
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def errorLogger(msg, line, whereFrom):
    if msg == 'fileNotFound':
        # For the fileNotfound error, since it doesnt require any removals or line error logging
        print('Killing process, fix your code')
        os.kill(os.getpid(), 9)
    else:
        file = find('temp_file.txt')[0]
        print(
            f'{style.RED}{msg} on line: {line} caused a problem{style.RESET} {whereFrom}')
        # Remove extra files
        os.remove(file)
        os.remove('symbolTable.json')
        print('Killing process, fix your code')
        os.kill(os.getpid(), 9)


def checkDataType(msg: str, line):
    command = {
        '#define': 'typeVar',
        'LDX': 'type1',
        'STX': 'type1',
        'LDY': 'type1',
        'STY': 'type1',
        'LVX': 'type2',
        'LVY': 'type2',
        'INX': 'type0',
        'DEX': 'type0',
        'CMP': 'type0',
        'JMP': 'type1',
        'JXL': 'type1',
        'JYL': 'type1',
        'JEQ': 'type1',
        'JNE': 'type1',
        'JOF': 'type1',
        'JUF': 'type1',
        'JSR': 'type1',
        'RSR': 'type0',
        'NOP': 'type0',
        'BRK': 'type0'
    }
    try:
        return command[msg]
        # Dict of all valid commands, returns the command type so that they can be handled properly
    except KeyError:
        errorLogger(msg, line, 'Unknown Command')


def dataType0(msg: str, line):
    # Handles the datatype0 command, check data sheet for how they work
    command = {
        'INX': 0x06,
        'DEX': 0x07,
        'CMP': 0x08,
        'RSR': 0x11,
        'NOP': 0x12,
        'BRK': 0x13
    }
    try:
        out = f'{command[msg]:0>5b}'
        return generateZero(out) + out
    except ValueError:
        errorLogger(msg, line, 'datatype0 value error')


def dataType1(msg: str, address: int, line):
    # Handles the datatype1 command, check data sheet for how they work
    command = {
        'LDX': 0x00,
        'STX': 0x01,
        'LDY': 0x02,
        'STY': 0x03,
        'JMP': 0x09,
        'JXL': 0x0A,
        'JYL': 0x0B,
        'JEQ': 0x0C,
        'JNE': 0x0D,
        'JOF': 0x0E,
        'JUF': 0x0F,
        'JSR': 0x10,
    }
    try:
        inst = f'{command[msg]:0>5b}'
        add = f'{address:0>11b}'
        return add + inst
    except ValueError:
        errorLogger(msg, line, 'datatype1 value error')


def dataType2(msg: str, value: int, line):
    # Handles the datatype2 command, check data sheet for how they work
    command = {
        'LVX': 0x04,
        'LVY': 0x05,
    }
    try:
        inst = f'{command[msg]:0>5b}'
        val = f'{value:0>4b}'
        out = val + inst
        return generateZero(out) + out
    except ValueError:
        errorLogger(msg, line, 'datatype2 value error')


def fillFile():
    # Fills the remaining file with 0xFF bits, just how the cpu works
    fillBit = b'\xFF'
    HIGH_FILE = 'high.bin'
    LOW_FILE = 'low.bin'
    HF = openOrCreate(HIGH_FILE)
    LF = openOrCreate(LOW_FILE)
    while HF.tell() <= 0x7FF:
        HF.write(fillBit)
    while LF.tell() <= 0x7FF:
        LF.write(fillBit)


def writeToHighLowFile(output, DEBUGGING: bool):
    # this just writes to file
    DEBUG_FILE = 'debug.txt'
    HIGH_FILE = 'high.bin'
    LOW_FILE = 'low.bin'
    DEBUGGING = DEBUGGING
    HF = openOrCreate(HIGH_FILE)
    LF = openOrCreate(LOW_FILE)
    if DEBUGGING:
        try:
            DF = open(DEBUG_FILE, 'x')
        except FileExistsError:  # Creates file if it does not exist, otherwise it overwrites it
            DF = open(DEBUG_FILE, 'a')
        for line in output:
            DF.write(line + '\n')
            DF.close()
    for line in output:
        if len(line.strip()) == 0:
            # makes sure to not write empty lines
            return
        dataHigh = bytes([int(line[0:8], 2)])
        dataLow = bytes([int(line[8:16], 2)])
        HF.write(dataHigh)
        LF.write(dataLow)
    HF.close()
    LF.close()


def createTempFile(FileName):
    if FileName == '':
        # Make sure it isnt creating a blank file
        return
    temp_file = os.path.dirname(FileName) + '\\' + 'temp_file.txt'
    openOrCreate(temp_file)
    toCopy = open(FileName, 'r').read()
    openTemp = open(temp_file, 'w')
    openTemp.write(toCopy)  # Copy over the original file
    openTemp.close()
    return temp_file


def removeAllComments(FileName):
    # Strips all comments from temp file since they arent needed
    pattern = '(\/\*(\w|\D)+\*\/)|(\/\/(?:[^\r\n]|\r(?!\n))*)'
    file = open(FileName, 'r').read()
    nfile = re.sub(pattern, '', file)
    wfile = open(FileName, 'w')
    wfile.write(nfile)
    wfile.close()


def symbolWrite(init_Table):
    # In charge of opening and writing the symbolTable
    Symbol_Table = open('symbolTable.json', 'w')
    jsonf = json.dumps(init_Table)
    Symbol_Table.write(jsonf)
    Symbol_Table.close()


def firstPass(FileName, init_Table):
    # first pass doesnt do any translating, just adding to the symbol table and setting the file for translating
    removeAllComments(FileName)
    file = open(FileName, 'r').read()  # open file
    L_FILE = file.split('\n')
    LL_FILE = []
    for x in L_FILE:
        if x:
            LL_FILE.append(x)
    hex_line_Counter = 0
    error_line_Counter = 1
    pattern = ('\w+:')  # Label patter
    for line in LL_FILE:
        if len(line.strip()) == 0:
            error_line_Counter += 1
            continue
        temp_Line = line.split(' ')

        while("" in temp_Line):
            temp_Line.remove("")
        if re.search(pattern, line):
            # Since I dumb, when I split line it could be a couple different lengths meaning label will be in a diff spot, this is how I find it
            if len(temp_Line) == 1:
                init_Table[temp_Line[0].split(':')[0]] = hex(hex_line_Counter)
                hex_line_Counter += 1
                continue
            if len(temp_Line) == 2:
                init_Table[temp_Line[1].split(':')[0]] = hex(hex_line_Counter)
                hex_line_Counter += 1
                continue
            if len(temp_Line) == 3:
                init_Table[temp_Line[2].split(':')[0]] = hex(hex_line_Counter)
                hex_line_Counter += 1
                continue

        if '#define' in line:
            # Add definitions to the symbol table
            L_LINE = line.split(' ')
            var = L_LINE[1]
            address = L_LINE[2]
            try:
                if int(address, 16) > 0x7FF:
                    errorLogger(line, error_line_Counter, 'define mem overflow')
                init_Table[var] = address
                hex_line_Counter -= 1
            except:
                errorLogger(line, error_line_Counter, 'definition error')
        error_line_Counter += 1
        hex_line_Counter += 1
    symbolWrite(init_Table)


def checkValidMem(line, line_Counter):
    # Makes sure its a valid memory address
    if checkDataType(line[0], line_Counter) == 'type1' or 'type2':
        address = int(line[1], 16)
        if address > 0x7FF:
            errorLogger(hex(address), line_Counter, 'check valid mem')
    else:
        return


def makeBar():
    # code for progress bar, since been removed
    for i in progressbar(range(100), "Computing: ", 40):
        time.sleep(0.0001)  # ineffcient but looks cool as hell


def run(FileName, DEBUGGING):
    out = []
    wipeFiles(DEBUGGING)
    init_Table = {}
    address_Counter = 0
    debug_line_counter = 1
    firstPass(FileName, init_Table)  # Set up file
    file = open(FileName, 'r').read()  # open file
    L_FILE = file.split('\n')
    LL_FILE = []
    # really ugly for loop since I need to increment line counter
    for x in L_FILE:
        LL_FILE.append(x)
    for line in LL_FILE:
        if len(line.strip()) == 0:
            debug_line_counter += 1
            continue
        NL_FILE = line.split(' ')
        try:	
            if checkDataType(NL_FILE[0], debug_line_counter) == 'type0':	
                out.append(dataType0(NL_FILE[0], address_Counter))	
            if checkDataType(NL_FILE[0], debug_line_counter) == 'typeVar':	
                address_Counter -= 1	
            if len(NL_FILE) > 1:	
                if NL_FILE[1] in init_Table.keys() and NL_FILE[0] != '#define':	
                    NL_FILE[1] = init_Table[str(NL_FILE[1])]	
                if checkDataType(NL_FILE[0], debug_line_counter) == 'type1':	
                    checkValidMem(NL_FILE, address_Counter)	
                    out.append(dataType1(NL_FILE[0], int(	
                        NL_FILE[1], 16), debug_line_counter))	
                if checkDataType(NL_FILE[0], debug_line_counter) == 'type2':	
                    checkValidMem(NL_FILE, address_Counter)	
                    out.append(dataType2(NL_FILE[0], int(	
                        NL_FILE[1], 16), address_Counter))	
            debug_line_counter += 1	
            address_Counter += 1	
        except:	
            errorLogger(NL_FILE[0], debug_line_counter,	
                        'Probably a label error or something, consider this a SEGFAULT though, who knows why it broke, it just did')	
    writeToHighLowFile(out, DEBUGGING)	
    return address_Counter


def main():
    args = sys.argv
    os.system('cls' if os.name == 'nt' else 'clear')
    os.chdir(os.path.dirname(args[1]))
    asciiart()
    thing = args
    if len(thing) == 3:
        garb, file, DEBUGGING = thing
        if DEBUGGING:
            DEBUGGING = distutils.util.strtobool(DEBUGGING)
        else:
            DEBUGGING = False
    else:
        file = args[1]
        DEBUGGING = False
    t.start()
    try:
        open(file, 'r')
        file = createTempFile(file)
        lines = run(file, DEBUGGING) - 1
    except:
        print(
            f'{style.RED}Either file is not valid or you did not input a file path\nAssembler thinks the path is {style.RESET}[{file}]')
        print('You could also check to see if the file is in too large of a folder, blame to coder for a bad search function')
        errorLogger('fileNotFound', 0, 0)
    t.stop()
    os.remove(file)
    os.remove('symbolTable.json')
    fillFile()
    if lines >= 2012:
        print(f'{style.RED}Warning you have used over 2012 words of memory, \nin total you have used {lines} words of memory {style.RESET}')
    else:
        print(f'You have used {lines} words of memory out of 2012')



if __name__ == "__main__": 
    main()