#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Build a test collection 

input:
    lda input file in low format

output:
    input dataset split into traning set and test set 

Usage:
    build_testset <lowfile> <total doc number> <testset doc number>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib import cm
import logging

logger = logging.getLogger(__name__)

#global constant


def run_random_sample(lowfile, totalDocCnt, testsetDocCnt):
    logger.info('random_sample %d from %d documents', testsetDocCnt, totalDocCnt)
    
    # sample by random.randint, repeat sample is possible occur in the result
    testset = sorted(np.random.randint(0, totalDocCnt, testsetDocCnt*2))
    logger.debug('samples id = %s', testset)

    lf = open(lowfile, 'r')
    trainf = open(lowfile + '.train', 'w')
    testf = open(lowfile + '.test', 'w')

    id, idx, sampleCnt = 0, 0, 0
    for line in lf:
        if sampleCnt < testsetDocCnt and idx < testsetDocCnt*2 and id == testset[idx]:
            testf.write(line)
            sampleCnt += 1
            while  idx < testsetDocCnt*2 and id == testset[idx]:
                idx += 1
        else:
            trainf.write(line)
        id += 1

    lf.close()
    trainf.close()
    testf.close()
    logger.info('random_sample finished, write to %s,%s', lowfile+'.train', lowfile+'.test')


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
    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    lowfile = sys.argv[1]
    totalDocCnt = int(sys.argv[2])
    testsetDocCnt = int(totalDocCnt * 0.5)
    if len(sys.argv) > 3:
        testsetDocCnt = int(sys.argv[3])

    # sampling
    run_random_sample(lowfile, totalDocCnt, testsetDocCnt)

