#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Filtering input text stream by a input dictionary, removing all words not appeared in 
the dict file.

input:
    input file  : low format (wordlist...)
    output file : low format 
    dict file   : id  trem

Usage:
    txtfilter <inputfile> <output file> <dict file>

"""

import sys, os, math,re
import numpy as np
from scipy import stats, linalg
from scipy.stats import entropy
import logging

logger = logging.getLogger(__name__)

def run_filter(inputfile, outputfile, dictfile):
    """
    """
    logger.info('loading dict file from %s', dictfile)
    mallet = open(dictfile, 'r')
    wordmap = {}
    for line in mallet:
        tokens = line.strip().split('\t')
        wordmap[tokens[1]] = int(tokens[0])

    inf = open(inputfile, 'r')
    outf = open(outputfile, 'w')
    logger.info('run filtering...')
    for line in inf:
        outline = []
        tokens = line.strip().split(' ')
        for word in tokens:
            if word in wordmap:
                outline.append(word)
        outf.write(' '.join(outline) + '\n')

    logger.info('done!')

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

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    dictfile = sys.argv[3]

    run_filter(inputfile, outputfile, dictfile)
