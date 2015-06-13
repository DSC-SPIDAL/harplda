import sys

"""
extend the phi(.beta) file by wordmap from gibbslda output to gensim dictionary file
input format:
term_count
term id


"""

if len(sys.argv) != 5:
    print 'usage: extendphi <wordmap> <beta> <newbeta> <vocabSize>'
    sys.exit(0)

wordmap = open(sys.argv[1], 'r')
beta = open(sys.argv[2],'r')
newbeta = open(sys.argv[3], 'w')
V = int(sys.argv[4])

tm = dict()
term_cnt = 0
for line in wordmap:
    if term_cnt == 0:
        term_cnt = int(line.strip())
        continue
    tokens = line.strip().split(' ')
    # cur term id  -> map back to original word(true id)
    tm[int(tokens[1])] = int(tokens[0])


for line in beta:
    vals = line.strip().split(' ')
    trueval = ['0'] * V
    for i in range(len(vals)):
        if i in tm.keys():
            trueval[tm[i]] = vals[i]


    newbeta.write(' '.join(trueval))
    newbeta.write('\n')



