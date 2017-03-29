#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Validate the zipf law on text dataset.
According to zipf law, freq(i) = C0 / i, i is the rank of a word.

hypothesis:  
     +  word freqency follows zipf law

input data:
    dictionary file, "word\tfreq"

Usage:
    zipf <lowfile> <dataset name>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib
matplotlib.use('Svg')
import matplotlib.pyplot as plt
from matplotlib import cm
import logging
import cPickle as pickle

import docStat
import wordStat

logger = logging.getLogger(__name__)


def draw1(freq, rank, savefile):
    lfreq = np.log(np.array(freq))
    lrank = np.log(np.array(rank))
    logger.debug('freq=%s, log(freq)=%s', freq[:10], lfreq[:10])

    # fit the zipf law curve?
    z = np.polyfit(lrank, lfreq, 1)
    p = np.poly1d(z)
    logger.info('polyfit all, z = %s, ratio=%f', z, z[0]/z[1])

    idx=np.where(lrank<8)
    z2 = np.polyfit(lrank[idx], lfreq[idx], 1)
    p2 = np.poly1d(z2)
    logger.info('polyfit 3..8, z = %s, ratio=%f', z2, z2[0]/z2[1])


    xp = np.linspace(0, lrank[-1], 100)
    plt.title('Zipf Distribution of Text Data')
    plt.xlabel('Word Rank')
    plt.ylabel('Word Frequency')
    #plt.plot(x, y, '.', xp, p1(xp), '-')
    plt.plot(lrank, lfreq, '.', xp, p2(xp),'+', xp, p(xp), '-')
    plt.legend()
    plt.savefig(savefile)
    plt.show()

def draw2(freq, rank, savefile,description):
    lfreq = np.log10(np.array(freq))
    lrank = np.log10(np.array(rank))
    logger.debug('freq=%s, log(freq)=%s', freq[:10], lfreq[:10])

    # fit the zipf law curve?
    z = np.polyfit(lrank, lfreq, 1)
    p = np.poly1d(z)
    logger.info('polyfit all, z = %s, ratio=%f', z, z[0]/z[1])

    idx=np.where(lrank<np.log10(3000))
    z2 = np.polyfit(lrank[idx], lfreq[idx], 1)
    p2 = np.poly1d(z2)
    logger.info('polyfit 3..8, z = %s, ratio=%f', z2, z2[0]/z2[1])

    xp = np.linspace(0, lrank[-1], 100)
    ax = plt.subplot(111)
    ax.set_xscale("log", nonposx='clip')
    ax.set_yscale("log", nonposy='clip')

    plt.title('Zipf Distribution of ' + description)
    plt.xlabel('Word Rank')
    plt.ylabel('Word Frequency')
    #plt.plot(x, y, '.', xp, p1(xp), '-')
    #plt.plot(rank, freq, '.', np.exp(xp), np.exp(p2(xp)),'+', np.exp(xp), np.exp(p(xp)), '-')
    #plt.plot(rank, freq, '.', 10**xp, 10**p2(xp),'+', 10**xp, 10**p(xp), '-')
    plt.plot(rank, freq, '.')
    label=r'$y=10^{%.1f}x^{%.1f}$'%(z2[1], z2[0])
    plt.plot(10**xp, 10**p2(xp),'+', label=label)
    label=r'$y=10^{%.1f}x^{%.1f}$'%(z[1], z[0])
    plt.plot(10**xp, 10**p(xp), '-',label=label)
    plt.legend()

    plt.savefig(savefile)
    plt.show()

def zipf(dictfile, description):

    vocabulary = dict.fromkeys(xrange(8000000))
    
    # load vocabulary
    vocab=[]
    dictf = open(dictfile,'r')
    logger.info('load from dict file %s', dictfile)
    #detect deli
    #line = dictf.readline()

    for line in dictf:
        data = line.strip().split()
        #data = line.strip().split('\t')
        #vocabulary[data[1]] = int(data[1])
        vocab.append((data[0], int(data[1])))

    dictf.close()

    vocab =sorted(vocab, key=lambda s: s[1], reverse = True)
    
    freq = [s[1] for s in vocab]
    rank = [x for x in xrange(1, len(freq)+1)]

    #draw1(freq, rank, dictfile + '-zipf.png')
    draw2(freq, rank, dictfile + '-zipf.png',description)

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

    lowfile = sys.argv[1]
    #description ='Text Data'
    description =lowfile[:lowfile.find('.')]

    if len(sys.argv)>2:
        description =sys.argv[2]
    zipf(lowfile, description)



