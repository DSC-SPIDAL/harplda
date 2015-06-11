import sys

o = open(sys.argv[1] + '.low', 'w')
f = open(sys.argv[1],'r')
linecnt = 0
for line in f:
    index = line.find('\t')
    tokens = line[index+1:]
    if tokens.strip() == '':
        continue
    o.write(tokens)
    linecnt += 1

print linecnt
