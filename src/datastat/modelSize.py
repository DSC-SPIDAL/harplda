#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Analysis the relation between model size and document partition
hypothesis:  
     +  model size nonlinear related to document partition
     +  follows some power function, with k>2, the bigger k the worse of the nonlinear property

input data from docStat.split_collection
collect the splits with <mean, var> of following statisics
nodes/partitionCnt,   docCnt,   vocabularySize,      totalWordCnt

Usage:
    ModelSize <lowfile>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib import cm
import logging
import cPickle as pickle

import docStat
import wordStat

logger = logging.getLogger(__name__)

def load_splits(lowfile):
    cachefile = lowfile + '.pickle'
    if os.path.exists(cachefile):
        f = open(cachefile, 'rb')
        obj = pickle.load(f)
        f.close()
        return obj

    # first, load the collection
    collection = docStat.LowDocumentCollection()
    collection.load(lowfile)

    # walk on current directory, find directory named with 'split###' 
    data_collect = []
    for dirpath, dnames, fnames in os.walk('.'):
        for d in dnames:
            m = re.search('split([0-9]*)', d)
            if m:
                splitCnt = int(m.group(1))
                splits_col = collection.load_splits(splitCnt)
                #nodes/partitionCnt,   docCnt,   vocabularySize,      totalWordCnt
                split_stat = np.zeros((3,splitCnt))
                for i in range(len(splits_col)):
                    logger.debug('split = %s', splits_col[i])

                    split_stat[0][i] = splits_col[i].get_doc_number()
                    split_stat[1][i] = splits_col[i].get_vocab_size()
                    split_stat[2][i] = splits_col[i].get_wordcnt()

                # calc mean,var
                logger.debug('split_stat = %s', split_stat)

                split_mean = np.mean(split_stat, axis = 1)
                split_var = np.std(split_stat, axis = 1)
    
                logger.debug('mean = %s, var = %s', split_mean, split_var)


                # save this
                data_collect.append((splitCnt, split_mean, split_var))

    #save the data to cache file
    f = open(cachefile, 'wb')
    pickle.dump(data_collect, f)
    f.close()

    return data_collect

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    #logging.basicConfig(filename='debug_calcdistance.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                    level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    lowfile = sys.argv[1]
    K = 10
    if len(sys.argv) > 2:
        K = int(sys.argv[2])
    logger_level = ''
    splitType = 'HASH'

    data_collect = load_splits(lowfile)

    # sort oder by splitCnt
    data_collect = sorted(data_collect, key = lambda x: x[0])
    totalRunCnt = len(data_collect)

    # model_stat
    x = np.log2(np.array([x[0] for x in data_collect]))
    # mean/var, run, docNumber/vocab/wordCnt
    model_stat = np.zeros((2,totalRunCnt,3))
    for i in range(totalRunCnt):
        model_stat[0][i] = data_collect[i][1]
        model_stat[1][i] = data_collect[i][2]

    logger.debug('model stat: %s', model_stat)

    # draw the result
    # doccnt
    plt.errorbar(x, model_stat[0,:,0], yerr = model_stat[1,:,0])
    plt.savefig('doccnt.png')
    # vocab
    plt.close('all')
    plt.errorbar(x, model_stat[0,:,1], yerr = model_stat[1,:,1])
    plt.savefig('vocab.png')
    # wordcnt
    plt.close('all')
    plt.errorbar(x, model_stat[0,:,2], yerr = model_stat[1,:,2])
    plt.savefig('wordcnt.png')

    #fit the vocab function
    plt.close('all')
    y = model_stat[0, :, 1] 

    y = y / 1000000

    z = np.polyfit(x, y, 1)
    logger.info('polyfit z = %s, ratio=%f', z, z[0]/z[1])
    p1 = np.poly1d(z)

    z2 = np.polyfit(x[3:8], y[3:8],1)
    p2 = np.poly1d(z2)
    logger.info('polyfit 3..8, z = %s, ratio=%f', z2, z2[0]/z2[1])

    z3 = np.polyfit(x[6:], y[6:],1)
    p3 = np.poly1d(z3)
    logger.info('polyfit 6.., z = %s, ratio=%f', z3, z3[0]/z3[1])

#    z2 = np.polyfit(x, y, 2)
#    p2 = np.poly1d(z2)

    xp = np.linspace(0, 11, 100)
    plt.title('Model Size Nonlinear Decrease')
    plt.xlabel('Document Partition Count 2^x')
    plt.ylabel('Model Size')
    #plt.plot(x, y, '.', xp, p1(xp), '-')
    plt.plot(x, y, '.', xp, p1(xp), '-', xp, p2(xp), '--',xp, p3(xp), '+')
    plt.legend()
    plt.savefig('modelSize.png')
    plt.show()




