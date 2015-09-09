#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Create new wordid file from reided input file's docStat result
Be careful that the id in docstat can be non-continunous, for subsets of the train dataset can be 
used in experiments.

input format:
    docstat : docStat dictionary file <term freq>
    wordids : gensim dictionary file <id term freq>

output format:
    Save this Dictionary to a text file, in format: 
    id[TAB]word_utf8[TAB]word frequency[NEWLINE]. Sorted by word, or by decreasing word frequency.

Usage:
    dict2wordids <docstat dict> <wordid>

"""
import sys, os
import logging

logger = logging.getLogger(__name__)

def convert_dict(statdictfile, wordidsfile):
    statdict = open(statdictfile, 'r')
    wordids = open(wordidsfile, 'w')

    logger.info('loading dict file from %s', statdictfile)
    freqmap = {}
    idlist = []
    for line in statdict:
        tokens = line.strip().split('\t')
        idlist.append(int(tokens[0]))
        freqmap[tokens[0]] = tokens[1]

    # sort the idlist, create new id from the sorted ids
    idlist = sorted(idlist)

    term_cnt = 0
    for id in xrange(len(idlist)):
        wordids.write('%s\t%s\t%s\n'%(id, idlist[id], freqmap[str(idlist[id])]))

    wordids.close()

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    convert_dict(sys.argv[1], sys.argv[2])



