#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Load harp topic output , convert into mallet estimator input file

input:
    harp topic model output are servral files under one directory with the name '#iternum'
    wordid  topic#.....

output: binary format
    numTopics   int
    numWords    int
    alpha   double
    beta    double
    model Matrix[numWords][numTopics]   int


Usage:
    convertHarp2Mallet <model dir> <alpha=0.5> <beta=0.1>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import struct
import logging

logger = logging.getLogger(__name__)

def load_model(modelDir, beta):
    """
    input:
        modelDir model file are <wordid, topicCnt....>

    return:
        model is a word-topic count matrix
    """
    model = None
    for dirpath, dnames, fnames in os.walk(modelDir):
        for f in fnames:
            modeldata = np.loadtxt(os.path.join(dirpath, f))
            # first column is wordid
            # modeldata = modeldata[:,1:]
            logger.info('load model from %s , modelmatrix as %s', 
                    f, modeldata.shape)
            if model != None:
                model = np.concatenate((model, modeldata), axis=0)
            else:
                model = modeldata

    # sort the matrix by the first column            
    model = model[model[:,0].argsort()]
    #model = np.sort(model, axis=0)

    model = model[:, 1:]
    logger.info('load model data as %s', model.shape)
    return model

def save_model(fname, model, alpha, beta):
    with open(fname, 'wb') as f:
        V, K = model.shape
        f.write(struct.pack('>i', K))
        f.write(struct.pack('>i', V))
        f.write(struct.pack('>d', alpha))
        f.write(struct.pack('>d', beta))

        for w in range(V):
            for k in range(K):
                f.write(struct.pack('>i', model[w][k]))


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
    alpha = 0.5
    if len(sys.argv) > 2:
        alpha = float(sys.argv[2])
    beta = 0.1
    if len(sys.argv) > 3:
        beta = float(sys.argv[3])


    model = load_model(modelDir, beta)
    
    logger.info('saving to .mallet')
    save_model('harp-'+modelDir+'.mallet', model, alpha, beta)

