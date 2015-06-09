import sys

o = open(sys.argv[1] + '.low', 'w')
f = open(sys.argv[1],'r')
linecnt = 0
for line in f:
    index = line.find('\t')
    o.write(line[index+1:])
    linecnt += 1

print linecnt
