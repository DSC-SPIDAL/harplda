#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Convert wordmap from gibbslda output to gensim dictionary file

input format:
    term_count
    term id

output format:
    Save this Dictionary to a text file, in format: 
    id[TAB]word_utf8[TAB]word frequency[NEWLINE]. Sorted by word, or by decreasing word frequency.

Usage:
    wordmap2wordids <lowfile> <wordmap> <wordid>

"""


wordmap = open(sys.argv[1], 'r')
wordids = open(sys.argv[2], 'w')

term_cnt = 0
for line in wordmap:
    if term_cnt == 0:
        term_cnt = int(line.strip())
        continue
    tokens = line.strip().split(' ')
    wordids.write('%s\t%s\t1\n'%(tokens[1], tokens[0]))

wordids.close()
wordmap.close()


