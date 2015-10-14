#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Load harp topic output , convert into txt LDA model file
(new version model output, old version use convertHarp2Mallet)

input:
    harp topic model output are servral files under one directory with the name '#iternum'
    wordid  topic#.....
    type + " " + [" " + topic + ":" + count]*

Txt Format:
    matrix file
    wordid  wordfreq    topic:count ....
    type + " " + totalCount + " " + [" " + topic + ":" + count]*

    matrix hyper file
    #alpha :
    #beta : 
    #numTopics :
    #numTypes : 

Usage:
    convertHarp2Txt <model dir> <alpha=0.5> <beta=0.1> <numTopics> <numTypes>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import struct
import logging

logger = logging.getLogger(__name__)

def load_model(modelDir):
    """
    input:
        modelDir : model files inside are <wordid, topicCnt....>
        or
        modelfile

    return:
        model is a word-topic count matrix
    """
    mdata = []
    if os.path.isdir(modelDir):
        for dirpath, dnames, fnames in os.walk(modelDir):
            for f in fnames:
                #modeldata = np.loadtxt(os.path.join(dirpath, f))
                #new version harp model is : type  wordid:cnt ...
                harpf = open(os.path.join(dirpath, f), 'r')
                for line in harpf:
                    tokens = line.strip().split('  ')
                    wordid = int(tokens[0])
                    mdata.append((wordid,tokens[1]))
                harpf.close()

                # first column is wordid
                # modeldata = modeldata[:,1:]
                logger.info('load model from %s', f)
        
        # sort the matrix by the first column            
        mdata = sorted(mdata, key=lambda x:x[0])

    logger.info('load model data len=%d', len(mdata))
    return mdata


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    modelDir = sys.argv[1]
    alpha = float(sys.argv[2])
    beta = float(sys.argv[3])
    numTopics = int(sys.argv[4])
    numTypes = int(sys.argv[5])

    if os.path.isdir(modelDir):
        model = load_model(modelDir)

        numTypes = len(model)
        #save to .hyper
        basename = os.path.basename(modelDir) + '.harp'
        with open(basename + '.hyper', 'w') as hyperf:
            hyperf.write("#alpha : %f\n"%alpha)
            hyperf.write("#beta : %f\n"%beta)
            hyperf.write("#numTopics : %d\n"%numTopics)
            hyperf.write("#numTypes : %d\n"%numTypes)

        #save to 
        with open(basename , 'w') as txtf:
            for d in model:
                txtf.write("%d 0  %s\n"%d)

        logger.info('write txt model to %s', basename)
    else:
        logger.error('%s should be a directory', modelDir)

