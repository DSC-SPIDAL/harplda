#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Load mallet word-topic-output matrix txt file , convert into mallet estimator input file

input:
    matrix file
    wordid  wordfreq    topic:count ....
    type + " " + totalCount + " " + [" " + topic + ":" + count]*

    matrix hyper file
    #alpha :
    #beta : 
    #numTopics :
    #numTypes : 

output: binary format (java use bigendian)
    numTopics   int
    numWords    int
    alpha   double
    beta    double
    model Matrix[numWords][numTopics]   int

    if two result comes from different word-id, they should be aligned by dictionary matching.

Usage:
    convertTxt2Mallet <txt model file> <mallet dict> <harp dict>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import struct
import logging
from LDAModelData import LDAModelData

logger = logging.getLogger(__name__)

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

    modelfile = sys.argv[1]
    newdict = sys.argv[2]
    traindict = sys.argv[3]

    fullload = True
    build_wordid = True
    if len(sys.argv) > 4:
        fullload = (sys.argv[4].lower() != 'false')
    if len(sys.argv) > 5:
        build_wordid = (sys.argv[5].lower() != 'false')


    model = LDAModelData()
    model.load_from_txt(modelfile, fullload, build_wordid)

    # logger.debug('model=%s', model.model)

    # try calc likelihood on learned model directly
    #model.align_dict(newdict, traindict)
    # logger.debug('model=%s', model.model)


    savefile = modelfile + '.mallet'
    logger.info('saving to %s', savefile)
    #basename = os.path.splitext(modelfile)[0]

    totalTokens = model.save_to_binary(savefile)
    logger.info('total tokens count=%d', totalTokens)

    model.print_model()

