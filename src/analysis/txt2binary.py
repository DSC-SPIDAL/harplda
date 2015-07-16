#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
->np.loadtxt is too slow? 3 mininutes for 392MB model file
http://stackoverflow.com/questions/18259393/numpy-loading-csv-too-slow-compared-to-matlab
Numpy loading csv TOO slow compared to Matlab

Answers:
     use pandas for IO
     Warren Weckesser's textreader library
     read a numpy array its much better to save it as a binary or compressed binary

Usage: txt2binary <txt matrix> <compress = True>     

"""

import sys, os, math,re
import numpy as np
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    txtfile = sys.argv[1]
    compressmode = True
    if len(sys.argv) > 2:
        compressmode = (sys.argv[2] == "True")

    #get filename
    npfile = os.path.splitext(os.path.basename(txtfile))[0]

    #do it
    logger.info('loading txt data from %s', txtfile)
    matrix = np.loadtxt(txtfile)

    logger.info('saving into %s', npfile)
    if compressmode:
        np.savez(npfile, matrix)
    else:
        np.save(npfile, matrix)

    


