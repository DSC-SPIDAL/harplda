#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Analysis the model data.

The model data is dominated by the words with high freqency, is that right?

input:
    model data format:
    TxtModel
        wordid  wordfreq    topic:count ....
        type + " " + totalCount + " " + [" " + topic + ":" + count]*

    HarpModel
        wordid  topic#.....

analysis:

Usage:
    analysis_modeldata -txt|-harp <model file> 

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib import cm
import logging
from preprocess.LDAModelData import LDAModelData

logger = logging.getLogger(__name__)

def load_harpmodel(modelDir):
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

def load_txtmodel(modelfile):
    model = LDAModelData()
    model.load_from_txt(modelfile)
    logger.info('load model data as %s', model.model.shape)
    return model.model

def load_model(modelname, modeltype):
    """
    load model and return topiccnt vector
    """
    if modeltype == '-txt':
        model = load_txtmodel(modelname)
    elif modeltype == '-harp':
        model = load_harpmodel(modelname)

    # get the word, topiccnt matrix
    topiccnt = np.sum(model > 1, axis=1)

    return topiccnt


def draw_cdf(topiccnt, fig):

    vocabsize = topiccnt.shape[0]
    total = sum(topiccnt)
    cdf = np.zeros((vocabsize))
    rank = np.zeros((vocabsize))
    acc  = 0
    for w in xrange(vocabsize):
        acc += topiccnt[w]
        cdf[w] = acc * 1.0 / total
        rank[w] = w

    # draw cdf curve
    #xp = np.linspace(0, vocabsize, 100)
    #logger.debug('xp.shape=%s, cdf.shaep=%s', xp.shape, cdf.shape)

    plt.title('CDF Model Size of Word')
    plt.xlabel('Word Rank')
    plt.ylabel('Accumulate Percent of Model Size')
    plt.plot(rank, cdf, '.')
    plt.legend()
    plt.savefig(fig)
    plt.show()

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)


    modelType = sys.argv[1]
    modelDir = sys.argv[2]

    #1. load models
    model = load_model(modelDir,modelType)

    #2. run sampling
    draw_cdf(model, modelDir + '-cdf.png')
