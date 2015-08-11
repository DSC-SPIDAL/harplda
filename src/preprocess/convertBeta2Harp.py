#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Load .beta model file, convert into raw count file

input:
    .beta file
    log(p(w|k))

    dict file
    id  trem    freq

output:
    harp raw count format
    wordid  topic#.....

Usage:
    convertBeta2Harp <.beta file> <dict> <beta>

"""

import sys, os, math,re
import numpy as np
from scipy import stats, linalg
from scipy.stats import entropy
import logging

logger = logging.getLogger(__name__)

def load_model(betafile, dictfile, beta):
    """
    input:
        .beta
        dict

    solv the raw count matrix

    return:
        model is a word-topic count matrix
    """
    logger.info('loading beta file from %s', betafile)
    modeldata = np.exp(np.loadtxt(betafile))
    K,V = modeldata.shape
    logger.info('load model data as %s', modeldata.shape)


    logger.info('loading dict file from %s', dictfile)
    sum_k = np.zeros((V, 1))
    freq = []
    logger.info('read harp dict from %s', dictfile)
    harp = open(dictfile, 'r')
    wordcnt = 0
    for line in harp:
        tokens = line.strip().split('\t')
        sum_k[int(tokens[0])] = int(tokens[2])
        freq.append((int(tokens[0]), int(tokens[2])))
        wordcnt += int(tokens[2])

    #freq is (id, freq) list
    freq = sorted(freq, key = lambda x: x[1], reverse = True)

    # solv the sum_w from eqution : p'*(sum_w + V*beta) = sum_k + K*beta
    P = np.transpose(modeldata)

    #useSolver = False
    useSolver = True
    if useSolver:
        #select K words, send P[K,K] matrix to solver
        logger.info('select K words as %s',freq[:K])
        P_K = np.zeros((K,K))
        sum_k_K = np.zeros((K,1))
        for k in range(K):
            P_K[k] = P[freq[k][0],:]
            sum_k_K[k] = sum_k[freq[k][0]]

        # goto solver
        logger.info('solve sum_w...., P=%s, sum_k=%s', P_K.shape, sum_k_K.shape)
        sum_w = linalg.solve(P_K, sum_k_K + K*beta)
        #sum_w = np.transpose(sum_w - V*beta)
        logger.info('solve sum_w....done!, sum_w = %s,sum_w=%s', sum_w.shape, sum_w)
    else:
        # use pinv instead
        # todo, it doest not work now, 'array too large' error
        P_inv = linalg.pinv(P)
        sum_w = np.dot(P_inv, (sum_k + K*beta))

    #check result
    wordcnt2 = int(np.sum(sum_w) - K*V*beta)
    logger.info('wordcnt = %d, solved wordcnt = %d', wordcnt, wordcnt2)

    # N is the raw count matrix, elem multiply
    sum_w = np.transpose(sum_w)
    N = P*sum_w - beta

    # add first column of wordid
    id = np.arange(V).reshape((V,1))
    model = np.hstack((id, N))

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
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    betafile = sys.argv[1]
    dictfile = sys.argv[2]
    beta = float(sys.argv[3])

    model = load_model(betafile, dictfile, beta)
    
    logger.info('saving model to .harp')
    harpfile = os.path.splitext(os.path.basename(betafile))[0] + '.harp'
    np.savetxt(harpfile, model,fmt="%i")
