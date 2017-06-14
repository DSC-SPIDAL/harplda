#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Calibrate the likelihood of subset result, such as lightlda or yahoolda.

Beacuse there are only a subset of words in each node under the ps model,
the final likelihood output by each node is under-estimated.
There is a nearly constant difference from these unseen words, which have
low frequency and their contributions to the likelihood are almost constant.
So, the calibration works.

input format:
    iternum likelihood ...

Usage: calibrate_likelihood.py <src file> <dst file>

"""
import sys,os,re
import datetime
import numpy as np
import logging

logger = logging.getLogger(__name__)

def calibrate(srcfile, dstfile):

    if os.path.exists(dstfile + '.sav'):
        logger.info('already calibrated, quit...')
        return

    src = np.loadtxt(srcfile)
    dst = np.loadtxt(dstfile)

    # check if it has been calibrated
    gap = dst[0,1] - src[0,1]
    logger.info('gap : %e', gap)
    if abs(gap) < 1e-4:
        logger.info('already calibrated, quit...')
        return

    #calibrate
    ndst = np.zeros(dst.shape)    
    np.copyto(ndst, dst)
    ndst[:,1:] -= gap

    #save result
    np.savetxt(dstfile, ndst,fmt='%e')
    np.savetxt(dstfile + '.sav', dst,fmt='%e')

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    calibrate(sys.argv[1], sys.argv[2])
 

