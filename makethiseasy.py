import struct

data = open("music1.txt", "r").read()
L_FILE = data.split('\n')
LL_FILE  = [x for x in L_FILE if x]
out = open('out.txt', 'w')

for line in LL_FILE:
    temp_line = line.split(' ')
    tt_line = [x for x in temp_line if x]
    print(tt_line)
    empty = ''
    out.write(empty.join(tt_line[0:2]) + '\n')


out.close()