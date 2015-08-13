#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Load harp topic output , convert into mallet estimator input file

input:
    harp topic model output are servral files under one directory with the name '#iternum'
    wordid  topic#.....

output: binary format (java use bigendian)
    numTopics   int
    numWords    int
    alpha   double
    beta    double
    model Matrix[numWords][numTopics]   int

    if two result comes from different word-id, they should be aligned by dictionary matching.

Usage:
    convertHarp2Mallet <model dir> <alpha=0.5> <beta=0.1> <mallet dict> <harp dict>

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
        modelDir : model files inside are <wordid, topicCnt....>
        or
        modelfile

    return:
        model is a word-topic count matrix
    """
    model = None

    if os.path.isdir(modelDir):
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
    else:
        # assume it's a file name
        model = np.loadtxt(modelDir)

    # sort the matrix by the first column            
    model = model[model[:,0].argsort()]
    #model = np.sort(model, axis=0)

    model = model[:, 1:]
    logger.info('load model data as %s', model.shape)
    return model

def align_dict(model, malletDict, harpDict):
    """
    Align word id between two model system

    input:
        malletDict  <id term>
        harpDict    <id term freq>

    output:
        model       realigned

    """
    mallet = open(malletDict, 'r')
    harp = open(harpDict, 'r')

    # read in harpDict
    logger.info('read mallet dict from %s', malletDict)
    malletmap = dict()
    for line in mallet:
        tokens = line.strip().split('\t')
        malletmap[int(tokens[0])] = tokens[1]
    
    harpmap = dict()
    logger.info('read harp dict from %s', harpDict)
    for line in harp:
        tokens = line.strip().split('\t')
        harpmap[tokens[1]] = int(tokens[0])
    

    K,V = model.shape
    new_model = np.zeros((len(malletmap),V))
    for k in range(len(malletmap)):
        new_model[k] = model[harpmap[malletmap[k]]]

    # debug
    # 3161    christ  27
    #logger.debug('new: term = %s, id = 3137, topics count = %s', malletmap[3137], new_model[3137])
    #logger.debug('old: term = christ, id = %d, topics count = %s', harpmap['christ'], model[harpmap['christ']])


    logger.info('align model data as %s', new_model.shape)
    return new_model

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
    malletDict = ''
    harpDict = ''
    if len(sys.argv) > 5:
        malletDict = sys.argv[4]
        harpDict = sys.argv[5]

    model = load_model(modelDir, beta)

    if malletDict:
        model = align_dict(model, malletDict, harpDict)

    logger.info('saving to .mallet')
    if os.path.isdir(modelDir):
        save_model('model-'+modelDir+'.mallet', model, alpha, beta)
    else:
        basename = os.path.splitext(modelDir)[0]
        save_model(basename + '.mallet', model, alpha, beta)
        

