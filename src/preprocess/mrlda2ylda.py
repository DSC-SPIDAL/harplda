import sys,os

if len(sys.argv) != 2:
    print('Usage: mrlda2ylda.py <mrlda input>')
    sys.exit(-1)

input = sys.argv[1]
fname = os.path.splitext(os.path.basename(input))[0] + '.ylda'
print 'convert to %s\n'%fname

o = open(fname, 'w',1024*1024)
f = open(input,'r',1024*1024)
linecnt = 0
for line in f:
    index = line.find('\t')
    tokens = line[index+1:]
    if tokens.strip() == '':
        continue
    idstr="%d %d "%(linecnt, linecnt)
    tokens = idstr + tokens
    o.write(tokens)
    linecnt += 1

print linecnt
