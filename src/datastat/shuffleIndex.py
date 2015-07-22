#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Analysis the word distribution on sharding the text document collection.
Design a metric: shuffle index
ShuffleIndex of a word is the count of shards where the word is distributed to.

input:
    text documents, in mrlda/low format

analysis:
    nodes: [1, 2, 4, 8, 16, 32, 64, 128, ..., 2^K] as N
    ShuffleIndex matrix for every sharding configuration, which is NxN

Usage:
    ShuffleIndex <lowfile> <K=8>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib import cm
import logging

import docStat
import wordStat

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    #logging.basicConfig(filename='debug_calcdistance.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                    level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    lowfile = sys.argv[1]
    K = 10
    if len(sys.argv) > 2:
        K = int(sys.argv[2])
    logger_level = ''
    splitType = 'HASH'

    # first, load the collection
    collection = docStat.load_lowfile(lowfile)

    # run experiments
    splitCnt = [2**(x+1) for x in range(K)]

    for cnt in splitCnt:
        split_dir = 'split%d'%cnt
        if os.path.exists(split_dir):
            logger.info('Skip existed split on splitCnt=%d', cnt)
        else:
            splits_col = docStat.split_collection(collection, cnt, splitType)

