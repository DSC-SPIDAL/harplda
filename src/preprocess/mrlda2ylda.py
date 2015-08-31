import sys

o = open(sys.argv[1] + '.ylda', 'w')
f = open(sys.argv[1],'r')
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
