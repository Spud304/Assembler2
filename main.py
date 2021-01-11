import SymbolTable as st
import code as cd
import json
from ps import commandType
import re
from timer import Timer
import sys
from gui import MyFrame, MyPanel
import wx

sys.path.append(".")

#So Much String manipulation.

t = Timer()

def symbolWrite(init_Table):
  #In charge of opening and writing the symbolTable
  Symbol_Table = open('symbolTable.json', 'w')
  jsonf = json.dumps(init_Table)
  Symbol_Table.write(jsonf)
  Symbol_Table.close()

def firstPass(init_Table, FileName):
  counter = 0 #Makes sure labels have right place in line
  pattern = r'(\/\*(\w|\D)+\*\/)|(\/\/(?:[^\r\n]|\r(?!\n))*)' #Regex for removing all kinds of comments. I hate regexs
  file = open(FileName, 'r').read() #open file
  file = file.replace(' ', '') #remove whitespace
  file = re.sub(pattern, '', file) #Apply Regex
  L_File = file.split('\n') #Make file array
  NL_File = [x for x in L_File if x] #remove empty indexes in array

  for i in range(0, len(NL_File)):
    if commandType(NL_File[i]) == 'L_Command':
      init_Table[NL_File[i].strip(')').strip('(')] = i - counter
      counter +=1
  #Find all labels and add to symbol table

  return NL_File
  #Return to main to allow for it to be written to symbol table


def secondPass(init_Table, fileName):
  n = 16 #Counter for variables
  pattern = r'(\/\*(\w|\D)+\*\/)|(\/\/(?:[^\r\n]|\r(?!\n))*)' #Regex for removing all kinds of comments. I hate regexs
  file = open(fileName, 'r').read()
  file = file.replace(' ', '')
  file = re.sub(pattern, '', file)
  L_File = file.split('\n')
  NL_File = [x for x in L_File if x]
  #This was all seen in the above function

  for i in range(0, len(NL_File)): #for loop through file
    if commandType(NL_File[i]) == 'A_Command': #Make sure only @ commands are taken
      if NL_File[i].strip('@') not in init_Table.keys(): #Makes sure it isn't a label
        try: #make sure it isnt an int like @1 or something
          thing = int(NL_File[i].strip('@'))
          thing += thing
        except (TypeError, ValueError): #Try except is a pretty lazy way to handle this, but meh
          init_Table[NL_File[i].strip('@')] = n
          n += 1
  
  return NL_File


def main(fileName):
  #main function

  init_Table = st.createTable()

  L_File = firstPass(init_Table, fileName)
  symbolWrite(init_Table)

  # First Pass aboce, Second Pass below

  L_File = secondPass(init_Table, fileName)
  symbolWrite(init_Table)

  try:
    hack = open('out.hack', 'x')
  except FileExistsError: #Creates file if it does not exist, otherwise it overwrites it
    hack = open('out.hack', 'w')

  #Amazing, you have finally reached the commmand parse loop. Only took 80 lines and god knows how many hours
  for i in range(len(L_File)):
    try:
      out = cd.parseCmd(L_File[i])
      if out != 'label':
        hack.write(out + '\n')
    except ValueError:
      print(i, L_File[i])

  hack.write('')

  hack.close()


t.start()

print('start')

#I like to time to see how long it takes
# main('rect.asm')
app = wx.App(False)
frm = MyFrame()
app.MainLoop()

print('stop')
t.stop()
