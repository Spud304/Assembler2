from ps import commandType, aInstruction
import json

def convertTuple(tup): 
  #joins strings instead of adding them
  str =  ''.join(tup) 
  return str

def generateZero(msg): #Makes binary numbers have the proper amount of 0's
  mLen = 16 - len(msg)
  out = ''
  for i in range(mLen):
    out += str(0)
  return out


def destCmd(msg):
  #Kind of proud for using the easy if instead of checking for each possibe combo
  d1 = 0 #A
  d2 = 0 #D
  d3 = 0 #M
  if 'A' in msg:
    d1 = 1
  if 'D' in msg:
    d2 = 1
  if 'M' in msg:
    d3 = 1
  
  #String Manipulation
  out = convertTuple((str(d1), str(d2), str(d3)))
  return out

#JumpCmd and compCmd work the same way, creates a dictionary/hash table for fast lookup, uses Try except to see if the value/key exists in the dict, if so return it, if not return whatever null is for the command

def jumpCmd(msg):
  jump = {
    'JGT' : '001',
    'JEQ' : '010',
    'JGE' : '011',
    'JLT' : '100',
    'JNE' : '101',
    'JLE' : '110',
    'JMP' : '111'
  }
  try:
    return jump[str(msg)]
  except KeyError:
    return '000'

def compCmd(msg):
  #The first bit in the number is a
  command = {
    '0'  : '0101010',
    '1'  : '0111111',
    '-1' : '0111010',
    'D'  : '0001100',
    'A'  : '0110000',
    '!D' : '0001101',
    '!A' : '0110001',
    '-D' : '0001111',
    '-A' : '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M'  : '1110000',
    '!M' : '1110001',
    '-M' : '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101'
  }
  try:
    return command[str(msg)]
  except KeyError:
    return '0101010'


#Dear god I hated writing this thing, its a mess and it shows. I'm done with the lab and do not have the energy to rewrite it. So instead enjoy my comments
def parseCmd(msg):
  f = open('symbolTable.json', 'r')
  sym_table = json.load(f)
  out = 'label' #standin, will be replaced no matter what
  if commandType(msg) == 'C_Command':
    dest = ''
    comp = ''
    jump = ''
    try: #C command can have a = or ; in it, so I need to work with both possibilities
      dest, comp = msg.split('=')
    except ValueError:
      pass
    try:
      comp, jump = msg.split(';')
    except ValueError:
      pass
    out = '111' + compCmd(comp) + destCmd(dest) + jumpCmd(jump) 
  if commandType(msg) == 'A_Command': #Removes the @ checks if its a label or not, it its just a plain int convert to binary, if not grab the value of the label in sym table then convert to binary
    trash, msg = msg.split('@')
    try:
      msg = sym_table[str(msg)]
    except KeyError:
        msg = int(msg)
    out = aInstruction(msg)
    add = generateZero(out)
    out = str(add) + out

  return(out)

