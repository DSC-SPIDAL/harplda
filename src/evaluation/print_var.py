#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Print mean, variance for experiments result

input:
    .likelihood <runid, likelihood, perplexity> matrix text file

Usage: 
    print_var <dir>

"""

import sys,os,re
import numpy as np
import logging
try:
    import matplotlib.pyplot as plt
    matplotlib_available = True
except ImportError:
    matplotlib_available = False

logger = logging.getLogger(__name__)

def calc_mean_var(inputdir, ext):
    """
    Calculate mean , var 

    input:
        modelDir   directory name
    return:
        array [iternum, ]
    """
    data = []
    for dirpath, dnames, fnames in os.walk(inputdir):
        for f in fnames:
            if f.endswith(ext):
                cacheFile = os.path.join(dirpath, f)
                logger.info('data file found at %s, loading likelihoods', cacheFile)
                likelihoods = np.loadtxt(cacheFile)
                data.append(likelihoods)

    #
    row, col = data[0].shape
    mv = np.zeros((row, len(data)))

    for idx in range( len(data) ):
        #  
        mv[:, idx] = data[idx][:,2]

    std = np.std(mv, axis = 1)
    mean = np.mean(mv, axis = 1)

    # save result

    return mean, std


if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # check the path
    inputdir = sys.argv[1]

    mean, std = calc_mean_var(inputdir, '.likelihood')
    #logger.info('mean:%s', mean)
    #logger.info('std :%s', std)
    print('mean:\n%s'%mean)
    print('std:\n%s'%std)


