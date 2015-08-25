import sys

o = open(sys.argv[1] + '.ylda', 'w')
f = open(sys.argv[1],'r')
linecnt = 0
for line in f:
    if line.strip() == '':
        continue
    idstr="%d %d "%(linecnt, linecnt)
    tokens = idstr + line
    o.write(tokens)
    linecnt += 1

print linecnt
