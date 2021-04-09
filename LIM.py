import json

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


def wipeFiles():
  open('high.bin', 'w').close()
  open('low.bin', 'w').close()


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
    return command[msg]
  except KeyError:
    print('Uh oh invalid command')


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
    print('huh')


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
    print('oingo boingo')

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
    print('ouch')


def writeToHighLowFile(output):
  print(f'high {output[0:7]}')
  print(f'low {output[8:15]}')
  HIGH_FILE = 'high.bin'
  LOW_FILE = 'low.bin'
  HF = openOrCreate(HIGH_FILE)
  HF.write(output[0:7] + '\n')
  HF.close()
  LF = openOrCreate(LOW_FILE)
  LF.write(output[8:15] + '\n')
  LF.close()


def symbolWrite(init_Table):
  #In charge of opening and writing the symbolTable
  Symbol_Table = open('symbolTable.json', 'w')
  jsonf = json.dumps(init_Table)
  Symbol_Table.write(jsonf)
  Symbol_Table.close()


def firstPass(FileName):
  file = open(FileName, 'r').read() #open file
  L_FILE = file.split('\n')
  LL_FILE  = [x for x in L_FILE if x]
  init_Table = {}
  line_Counter = 0
  for line in L_FILE:
    #line[0] = instruction, line[1] = label, assuming not subroutine
    #line[0] = JSR, line[1] = Subroutine, line[2] = label
    #init_Table[name] = number
    temp_Line = line.split(' ')
    if ':' in line and temp_Line[0] != 'JSR':
      init_Table[temp_Line[1]] = line_Counter - 2
    if ':' in line and temp_Line[0] == 'JSR':
      init_Table[temp_Line[2]] = line_Counter - 2
    if '#define' in line:
      define, var, address = line.split(' ')
      init_Table[var] = address
    line_Counter += 1
  symbolWrite(init_Table)


def main(FileName):
    firstPass(FileName)
    file = open(FileName, 'r').read() #open file
    L_FILE = file.split('\n')
    LL_FILE  = [x for x in L_FILE if x]
    print(LL_FILE)
    wipeFiles()
    for line in LL_FILE:
        # print(line)
        NL_FILE = line.split(' ')
        out = ''
        if checkDataType(NL_FILE[0]) == 'type0':
            out = dataType0(NL_FILE[0])
        if checkDataType(NL_FILE[0]) == 'type1':
            out = dataType1(NL_FILE[0], int(NL_FILE[1], 16))
        if checkDataType(NL_FILE[0]) == 'type2':
            out = dataType2(NL_FILE[0], int(NL_FILE[1], 16))
        if checkDataType(NL_FILE[0]) == 'typeVar':
            out = ''
        try:
            writeToHighLowFile(out)
        except:
            print(f'something went wrong, tried to write {out}')


main('test.asm')

## TODO: Labels, output high and low
#colon is where it jumps to
#first 5 bits instruction
#3 diff data formats, some don't take extra args, inc, dec

#datatype 1; 4bit value
#11 bits for address
#mem is between 0000, 2047. all unused words are 0x
# xxxxxxxxxxxIIIII

# xxxxxxxxxxxIIIII 0
# xxxxxxxDDDDIIIII 1
# AAAAAAAAAAAIIIII 2

# 0xC
# 1100
# 8421

# 0000
# 2047FF