import sys,os

if len(sys.argv) != 2:
    print('Usage: ylda2mrlda.py <ylda input>')
    sys.exit(-1)

input = sys.argv[1]
fname = os.path.splitext(os.path.basename(input))[0] + '.mrlda'
print 'convert to %s\n'%fname

o = open(fname, 'w',1024*1024)
f = open(input,'r',1024*1024)
linecnt = 0
for line in f:
    index = line.find(' ')
    index2 = line[index+1:].find(' ')
    tokens = line[index+1+index2+1:]
    if tokens.strip() == '':
        continue
    #idstr="%d %d "%(linecnt, linecnt)
    #tokens = idstr + tokens
    o.write('%s\t%s'%(linecnt,tokens))
    linecnt += 1

print linecnt
