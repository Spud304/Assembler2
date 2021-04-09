#I feel like both things in here make sense by looking at them, but just incase. commandTyper returns the type of command. aInstruction converts decimals to binary.

def commandType(line):
  if '=' in line or ';' in line:
    return 'C_Command'
  if '@' in line:
    return 'A_Command'
  if ':' in line:
    return 'L_Command'
  else:
    return 'NaC' #Not a Command

def aInstruction(dest):
  dest = int(dest)
  out = bin(dest)[2:] #bin has the first 2 letters as 0b in binary, so this strips it
  return out