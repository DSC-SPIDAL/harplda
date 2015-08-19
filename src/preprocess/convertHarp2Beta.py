#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Load harp topic output , convert into .beta file

input:
    harp topic model output are servral files under one directory with the name '#iternum'
    wordid  topic#.....

Usage:
    convertHarp2Beta <model dir> <beta=0.1>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
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
    # transpose from N(w,k) -> N(k,w)
    model = np.transpose(model)
    logger.info('load model data as %s', model.shape)

    # convert to probility
    model = np.matrix(model)
    sum_w = model.sum(axis = 1)

    #logger.debug('sum_w is %s', sum_w)
    K, V = model.shape
    model = (model + beta) / ( sum_w + beta * V)
    model = np.log(model)

    return model

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
    beta = 0.1
    if len(sys.argv) > 2:
        beta = float(sys.argv[2])

    model = load_model(modelDir, beta)
    
    logger.info('saving to .beta')
    np.savetxt('harp-'+modelDir+'.beta', model, fmt="%.8f")