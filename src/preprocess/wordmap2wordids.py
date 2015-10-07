#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Convert wordmap from gibbslda output to gensim dictionary file

input format:
    wordmap : gibbslda dictionary file <term id>
    docstat : docStat dictionary file <term freq>
    wordids : gensim dictionary file <id term freq>

output format:
    Save this Dictionary to a text file, in format: 
    id[TAB]word_utf8[TAB]word frequency[NEWLINE]. Sorted by word, or by decreasing word frequency.

Usage:
    wordmap2wordids <wordmap> <docstat dict> <wordid>

"""
import sys, os
import logging

logger = logging.getLogger(__name__)

def convert_dict(wordmapfile, statdictfile, wordidsfile):
    wordmap = open(wordmapfile, 'r')
    statdict = open(statdictfile, 'r')
    wordids = open(wordidsfile, 'w')

    logger.info('loading dict file from %s', statdictfile)
    freqmap = {}
    for line in statdict:
        tokens = line.strip().split('\t')
        freqmap[tokens[0]] = tokens[1]

    term_cnt = 0
    for line in wordmap:
        if term_cnt == 0:
            term_cnt = int(line.strip())
            continue
        tokens = line.strip().split(' ')
        
        if tokens[0] in freqmap:
            wordids.write('%s\t%s\t%s\n'%(tokens[1], tokens[0], freqmap[tokens[0]]))

    wordids.close()
    wordmap.close()

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    convert_dict(sys.argv[1], sys.argv[2], sys.argv[3])



