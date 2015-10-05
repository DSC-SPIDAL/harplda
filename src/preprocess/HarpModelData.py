#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Model Data File: word-topic matrix harp output

input:
    harp topic model output are servral files under one directory with the name '#iternum'
    wordid  topic#.....
    or
    wordid  topic:coutn ...

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

class HarpModelData():
    def __init__(self):
        self.model = None
        self.num_topics = 0
        self.alpha = []
        self.beta = 0.
        self.fullload = True

    def load_model(self, modelDir):
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

        self.model = model

        return model

    def align_dict(self, malletDict, harpDict):
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
        
    
        K,V = self.model.shape
        new_model = np.zeros((len(malletmap),V))
        for k in range(len(malletmap)):
            # test dataset dict may be different with the traning set
            if malletmap[k] in harpmap:
                new_model[k] = self.model[harpmap[malletmap[k]]]
    
        # debug
        # 3161    christ  27
        #logger.debug('new: term = %s, id = 3137, topics count = %s', malletmap[3137], new_model[3137])
        #logger.debug('old: term = christ, id = %d, topics count = %s', harpmap['christ'], model[harpmap['christ']])
    
    
        logger.info('align model data as %s', new_model.shape)

        self.model = new_model
        return new_model
    
    def save_model(self, fname, alpha, beta):
        with open(fname, 'wb') as f:
            V, K = self.model.shape
            f.write(struct.pack('>i', K))
            f.write(struct.pack('>i', V))
            f.write(struct.pack('>d', alpha))
            f.write(struct.pack('>d', beta))
    
            for w in range(V):
                for k in range(K):
                    f.write(struct.pack('>i', self.model[w][k]))
    
    def save_model_sorted(self, fname, alpha, beta):
        """
        Save the topicCount[][] each line sorted by count descendently
        """
        with open(fname, 'wb') as f:
            V, K = self.model.shape
            f.write(struct.pack('>i', K))
            f.write(struct.pack('>i', V))
            f.write(struct.pack('>d', alpha))
            f.write(struct.pack('>d', beta))
    
            index = np.argsort(self.model)
            for w in range(V):
                for k in range(-1, -K-1, -1):
                    # sort in acscent order
                    col = index[w][k]
                    if (self.model[w][col] == 0):
                        # a row end by (0,0) pair
                        f.write(struct.pack('>i', 0))
                        f.write(struct.pack('>i', 0))
                        break
    
                    f.write(struct.pack('>i', self.model[w][col]))
                    f.write(struct.pack('>i', col))

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

    hda = HarpModelData()

    hda.load_model(modelDir)

    if malletDict:
        hda.align_dict(malletDict, harpDict)

    logger.info('saving to .mallet')
    if os.path.isdir(modelDir):
        hda.save_model_sorted('model-'+modelDir+'.mallet',  alpha, beta)
    else:
        basename = os.path.splitext(modelDir)[0]
        hda.save_model_sorted(basename + '.mallet', alpha, beta)
        

