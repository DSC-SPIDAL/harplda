#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Power Law data are everywhere

Analysis input dictionary data with <term, freq>, draw the CDF.
This may give some hints to cache performance.

Usage:
    powerlaw  <dict file>

"""

import sys, os, re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib import cm
import logging

logger = logging.getLogger(__name__)

def load_model(dictfile):
    """
    input:
        dictioinary file, <term, freq>
    output:
    """
    data = np.loadtxt(dictfile)

    model = data[:,1]

    return model

def draw_distribution(model, modelname, sampleCnt = 200):
    """
    input:
        freq array
    """
    M = model.shape[0]

    # sort the freqs 
    #model = np.sort(model)

    #sample 200 points
    sumv = 0
    spansize = int(M / (sampleCnt-1) )
    total = sum(model)
    cdf = np.zeros((sampleCnt, 2))
    for i in range(sampleCnt -1):
        cdf[i][0] = i*spansize
        if i>=1:
            sumv += sum(model[(i-1)*spansize:i*spansize])
        else:
            sumv = 0

        cdf[i][1] = sumv /total
        #cdf[i][1] = sum(model[:i*spansize]) /total

    cdf[sampleCnt-1][0] = M
    cdf[sampleCnt-1][1] = 1

    #save cdf on samples
    np.savetxt(modelname + '-cdf.txt', cdf)


    #draw the distribution
    x = cdf[:,0]
    y = cdf[:,1]

    plt.subplot(2, 1,1)
    plt.title('Distribution of Probability Values')
    plt.xlabel('Rank')
    plt.ylabel('CDF')
    plt.plot(x, y, 'c.-', label=modelname)
    plt.legend()

    ax = plt.subplot(2, 1,2)
    #ax.set_xscale("log", nonposx = 'clip')
    plt.xlabel('Rank')
    plt.ylabel('CDF')
    #ax.set_xlim(xmin=-10)
    #plt.plot(x, y, 'b.-', label=modelname)
    plt.semilogx(x+1, y, 'b.-', label=modelname)
    

    plt.savefig(modelname + '-distribution.png')
    plt.show()


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

    filename = sys.argv[1]

    model = load_model(filename)
    draw_distribution(model,filename)

