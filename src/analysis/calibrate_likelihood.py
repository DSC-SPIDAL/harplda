#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Calibrate the likelihood of subset result, such as lightlda or yahoolda.

Beacuse there are only a subset of words in each node under the ps model,
the final likelihood output by each node is under-estimated.
There is a nearly constant difference from these unseen words, which have
low frequency and their contributions to the likelihood are almost constant.
So, the calibration works.

update: 07042017
likelihood calc on the base of node, single node no need to calibrate
let's calibrate to the harp's initial value for each distributed experiment setting

input format:
    iternum likelihood ...

Usage: calibrate_likelihood.py <src file> [restore]

"""
import sys,os,re
import datetime
import numpy as np
import logging

logger = logging.getLogger(__name__)


#
# harp iter0 as lower bound
# harp notimer iter1 as upper bound
#
init_lh_table={
    'enwiki':{
        '1000':(-1.1510770005329836E10,-1.113608457877022E10 ),
        '10000':(-12134290299,-1.121802667659592E10 ),
    },
    'clueweb30b':{
        '5000':(-2.937724421012109E11,-2.8910496187401874E11 )
    },
    'bigram':{
        '500': (-2.4805234740583996E10,-2.295583805893956E10 )
    }
    }

def calibrate(dstfile, use_upperbound = False):
    """
    input: .likelihood file
        lightlda_enwiki_t1000_4x16_i300_.05000000_0.01_4_0613-noreid.likelihood
    

    """

    if os.path.exists(dstfile + '.sav'):
        logger.info('already calibrated, quit...')
        return
    
    dst = np.loadtxt(dstfile)
    #get dataset and K
    for dataset in init_lh_table:
        if dstfile.find(dataset) > 0:
            m = re.search("lightlda_.*_t(\d+)_", dstfile)
            if m:
                K = m.group(1)
                
                logger.info('Dataset = %s, K = %s', dataset, K)

                if K in init_lh_table[dataset]:
                    
                    #
                    # here, use first line to calculate the gap
                    # it's not true, should get the lightlda's initial
                    # likelihood, then calculate the gap
                    # but, it seems that the initial one and the first 
                    # iteration one is similar?????
                    # there is a lightlda.initlh to get the initial value
                    #
                    idx = 1 if  use_upperbound else 0
                    gap = dst[0,1] - init_lh_table[dataset][K][idx]
                    logger.info('gap : %e', gap)

                    # check if it has been calibrated
                    #if abs(gap) < 1e-4:
                    #    logger.info('gap too small, already calibrated, quit...')
                    #    return

                    #calibrate
                    ndst = np.zeros(dst.shape)    
                    np.copyto(ndst, dst)
                    ndst[:,1:] -= gap

                    #save result
                    np.savetxt(dstfile, ndst,fmt='%e')
                    np.savetxt(dstfile + '.sav', dst,fmt='%e')

                    return

def restore(dstfile):
    """
    """
    if os.path.exists(dstfile + '.sav'):
        # copy .sav back
        logger.info('mv %s %s'%(dstfile + '.sav', dstfile))
        os.system('mv %s %s'%(dstfile + '.sav', dstfile))

    else:
        logger.info('.sav not exist, quit...')

def calibrate_byfile(srcfile, dstfile):
    """
    Use the source file's first line as the reference
    """
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
    if len(sys.argv) < 2:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    if len(sys.argv)>2 and sys.argv[2] == 'restore':
        restore(sys.argv[1])
    else:
        #calibrate(sys.argv[1], sys.argv[2])
        calibrate(sys.argv[1])
 

