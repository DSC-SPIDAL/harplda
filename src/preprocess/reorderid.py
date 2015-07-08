import sys

"""
reorder the id of the low dictionary, using a trick here by changing the term to new id
then the result file is still a low dictionary file, which can support mm2low.py

input format:
id\tterm\tfreq


output format:
Save this Dictionary to a text file, in format: id[TAB]word_utf8[TAB]document frequency[NEWLINE]. 

"""

if len(sys.argv) != 4:
    print('uasage: reorderid <wordids in> <wordids out>')
    sys.exit(-1)

wordid_in = open(sys.argv[1], 'r')
wordid_out = open(sys.argv[2], 'w')
newmap = open(sys.argv[3], 'w')

newid = 0
for line in wordid_in:
    tokens = line.strip().split('\t')
    wordid_out.write('%s\t%d\t%s\n'%(tokens[0], newid, tokens[2]))
    newmap.write('%d\t%s\t%s\n'%(newid, tokens[1], tokens[2]))

    newid += 1

wordid_in.close()
wordid_out.close()
newmap.close()


