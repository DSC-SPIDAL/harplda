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
    analysis_modeldata -txt|-harp <model file> <dictfile> <sample>

"""

import sys, os, math,re
import numpy as np
import logging
from preprocess.LDAModelData import LDAModelData
try:
    import matplotlib.pyplot as plt
except:
    import matplotlib

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
    
    # get the word, topiccnt matrix
    topiccnt = np.sum(model > 1, axis=1)

    return topiccnt

def load_txtmodel_full(modelfile):
    model = LDAModelData()
    model.load_from_txt(modelfile, fullload=True)
    logger.info('load model data as %s', model.model.shape)

    topiccnt = np.sum(model.model > 0, axis=1)
    return topiccnt


def load_txtmodel(modelfile):
    model = LDAModelData()
    model.load_from_txt(modelfile, fullload=False)
    logger.info('load model data as %s', model.model.shape)

    wordcnt = model.model.shape[0]
    topiccnt = np.zeros((wordcnt))
    for w in xrange(wordcnt):
        topiccnt[w] = model.model[w][0].count(":")

    return topiccnt

def load_model(modelname, modeltype):
    """
    load model and return topiccnt vector
    """
    if modeltype == '-txt':
        #topiccnt = load_txtmodel_full(modelname)
        topiccnt = load_txtmodel(modelname)
        
    elif modeltype == '-harp':
        topiccnt = load_harpmodel(modelname)
    
    logger.debug('topiccnt is %s', topiccnt[:10])

    return topiccnt

def align_model(topiccnt, dictfile):
    """
    align the model matrix by word freq

    id term freq
    """
    logger.info('read dict from %s', dictfile)
    idlist = []
    dictf = open(dictfile, 'r')
    for line in dictf:
        tokens = line.strip().split('\t')
        idlist.append((int(tokens[0]), int(tokens[2])))

    idlist = sorted(idlist, key= lambda x:x[1], reverse = True)
    
    logger.debug('sorted id list: %s', idlist[:10])

    index = np.array([x[0] for x in idlist])
    
    logger.debug('topiccnt list: %s, %s', topiccnt[347], topiccnt[85])


    topiccnt = topiccnt[index]
    logger.debug('sorted topiccnt list: %s', topiccnt[:10])

    return topiccnt

def calc_cdf(topiccnt):
    """
    calc cdf
    return rank, cdf
    """
    vocabsize = topiccnt.shape[0]
    total = sum(topiccnt)
    cdf = np.zeros((vocabsize))
    rank = np.zeros((vocabsize))
    acc  = 0
    for w in xrange(vocabsize):
        acc += topiccnt[w]
        cdf[w] = acc * 1.0 / total
        rank[w] = w

    return rank, cdf

def draw_cdf(topiccnt, fig):

    rank,cdf = calc_cdf(topiccnt)

    # draw cdf curve
    #xp = np.linspace(0, vocabsize, 100)
    #logger.debug('xp.shape=%s, cdf.shaep=%s', xp.shape, cdf.shape)
    if fig:
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
    dictfile = ''
    sample = ''
    if len(sys.argv) > 3:
        dictfile = sys.argv[3]
    if len(sys.argv) > 4:
        sample = sys.argv[4]


    #1. load models
    model = load_model(modelDir,modelType)

    if dictfile:
        model = align_model(model, dictfile)

    if sample:
        #get sample from cdf only
        rank, cdf = calc_cdf(model)
        w = int(sample)

        cdffile= open('cdf-'+sample, 'a')
        cdffile.write('%s %.4f\n'%(modelDir, cdf[w]))
        cdffile.close()

    else:
        draw_cdf(model, modelDir + '-cdf.png')
