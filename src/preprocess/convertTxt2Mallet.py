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

logger = logging.getLogger(__name__)

def load_model(txtmodel):
    """
    input:
        modelfile

    return:
        model is a word-topic count matrix
    """
    model = None
    
    #load .hyper
    alpha = []
    beta = 0.
    numTopics, numTypes = 0, 0
    with open(txtmodel + '.hyper', 'r') as hyperf:
        line = hyperf.readline().strip()
#values = line[line.find(':') + 2:].split(' ')
#        print values
        alpha = [float(x) for x in line[line.find(':') + 2:].split(' ')]
        line = hyperf.readline().strip()
        beta = float(line[line.find(':') + 1:])
        line = hyperf.readline().strip()
        numTopics = int(line[line.find(':') + 1:])
        line = hyperf.readline().strip()
        numTypes = int(line[line.find(':') + 1:])

        logger.debug('load hyper as: numTopics=%d, numTypes=%d, alpha[0]=%f, beta=%f', numTopics, numTypes, alpha[0], beta)

    #load model data
    model = np.zeros((numTypes, numTopics))
    logger.debug('loading model data....')
    with open(txtmodel, 'r') as matf:
        linecnt = 0
        for line in matf:
            line = line.strip()
            word =  int(line[:line.find(' ')])
            line = line[line.find('  ') + 2:]
            tokens = line.split(' ')
            linecnt += 1
            for item in tokens:
                #print 'item=', item
                tp = item.split(':')
                #print tp[0], tp[1]
                model[word][int(tp[0])] = int(tp[1])

    # verify data format
    if linecnt != numTypes:
        logger.error('txtmodel file format error, linecnt=%d, numTypes=%d', linecnt, numTypes)

    # sort the matrix by the first column            
    #model = model[model[:,0].argsort()]
    #model = np.sort(model, axis=0)

    #model = model[:, 1:]
    logger.info('done, load model data as %s', model.shape)
    return model, alpha, beta

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
        # test dataset dict may be different with the traning set
        if malletmap[k] in harpmap:
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

def save_model_sorted(fname, model, alpha, beta):
    """
    Save the topicCount[][] each line sorted by count descendently
    """
    with open(fname, 'wb') as f:
        V, K = model.shape
        f.write(struct.pack('>i', K))
        f.write(struct.pack('>i', V))
        f.write(struct.pack('>d', alpha))
        f.write(struct.pack('>d', beta))

        index = np.argsort(model)
        for w in range(V):
            for k in range(-1, -K-1, -1):
                # sort in acscent order
                col = index[w][k]
                if (model[w][col] == 0):
                    # a row end by (0,0) pair
                    f.write(struct.pack('>i', 0))
                    f.write(struct.pack('>i', 0))
                    break

                f.write(struct.pack('>i', model[w][col]))
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
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    modelfile = sys.argv[1]
    malletDict = sys.argv[2]
    harpDict = sys.argv[3]

    model, alpha, beta = load_model(modelfile)

    model = align_dict(model, malletDict, harpDict)

    savefile = modelfile + '.mallet'
    logger.info('saving to %s', savefile)
    #basename = os.path.splitext(modelfile)[0]
    save_model_sorted(savefile, model, alpha[0], beta)


