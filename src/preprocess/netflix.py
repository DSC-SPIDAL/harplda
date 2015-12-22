#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Convert netflix dataset to simple MM format

Simple Matrix Market Format:
    #dataset.mm
    rowid   colid   val

    #dataset.rfreq
    rowid   freq

    #dataset.cfreq
    colid   freq

    #dataset.status
    rowcnt  colcnt  nonzerocnt

Usage:
    netflix.py  <datadir> <output>

"""

import sys, os, math,re
import numpy as np
import logging
import tarfile

logger = logging.getLogger(__name__)

class NetflixDataset():
    """
    netflix dataset 

    TRAINING DATASET FILE DESCRIPTION
    ================================================================================
    
    The file "training_set.tar" is a tar of a directory containing 17770 files, one
    per movie.  The first line of each file contains the movie id followed by a
    colon.  Each subsequent line in the file corresponds to a rating from a customer
    and its date in the following format:
    
    CustomerID,Rating,Date
    
    - MovieIDs range from 1 to 17770 sequentially.
    - CustomerIDs range from 1 to 2649429, with gaps. There are 480189 users.
    - Ratings are on a five star (integral) scale from 1 to 5.
    - Dates have the format YYYY-MM-DD.

    """
    def __init__(self, datadir):
        self.rowids = {}
        self.colids = {}
        self.nnz = 0
         
        self.tar = tarfile.open(datadir + '/training_set.tar')

        self.testf = open(datadir + '/qualifying.txt')
        self.judgef = open(datadir + '/judging.txt')

    def convert_test(self, mmfile):
        """
        convert test file to mm format
        """
        targetfile = mmfile + '.mm'
        if os.path.exists(targetfile):
            logger.info('%s file exist already, skip overwriting', targetfile)
            return

        mmf = open(mmfile + '.mm', 'w', 1024*1024)

        testset = []
        for line in self.testf:
            if line.find(':') > 0:
                movieid = line.split(':')[0]
            else:
                items = line.split(',')
                userid = items[0]

                testset.append((userid, movieid))

        idx = 0
        for line in self.judgef:
            if line.find(':') > 0:
                movieid = line.split(':')[0]
            else:
                items = line.split(',')
                val  = items[0]

                mmf.write('%s %s %s\n'%(testset[idx][0], testset[idx][1], val))
                idx += 1

        mmf.close()

        statusf = open(mmfile + '.status', 'w')
        statusf.write('%d\n'%(len(testset)))
        statusf.close()


    def convert(self, mmfile):
        """
        convert to mm format

        """
        targetfile = mmfile + '.mm'
        if os.path.exists(targetfile):
            logger.info('%s file exist already, skip overwriting', targetfile)
            return

        mmf = open(mmfile + '.mm', 'w', 1024*1024)

        for tar_info in self.tar:
            if not tar_info.isreg():
                continue
            file = self.tar.extractfile(tar_info)
            firstline = file.readline()
            movieid = firstline.split(':')[0]
            for line in file:
                items = line.split(',')
                userid = items[0]
                val = items[1]

                mmf.write('%s %s %s\n'%(userid, movieid, val))
                    
                # statistics
                self.nnz += 1
                if userid in self.rowids:
                    self.rowids[userid] += 1
                else:
                    self.rowids[userid] = 1

                if movieid in self.colids:
                    self.colids[movieid] += 1
                else:
                    self.colids[movieid] = 1

        mmf.close()

        # write freqfile
        freqf = open(mmfile + '.rfreq', 'w', 1024*1024)
        sort_rowids = sorted(self.rowids.items(), key = lambda tp : tp[1], reverse=True)
        for tp in sort_rowids:
            freqf.write('%s %d\n'%(tp[0], tp[1]))
        freqf.close()

        freqf = open(mmfile + '.cfreq', 'w', 1024*1024)
        sort_colids = sorted(self.colids.items(), key = lambda tp : tp[1], reverse = True)
        for tp in sort_colids:
            freqf.write('%s %d\n'%(tp[0], tp[1]))
        freqf.close()

        statusf = open(mmfile + '.status', 'w')
        statusf.write('%d %d %d\n'%(len(self.rowids), len(self.colids), self.nnz))
        statusf.close()


    def __str__(self):
        return 'netflix dataset: rowcnt=%d, colcnt=%d, nnz=%d'%(len(self.rowids), len(self.colids), self.nnz)

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

    datadir = sys.argv[1]
    mmfile = sys.argv[2]

    netflix = NetflixDataset(datadir)
    netflix.convert(mmfile)
    logger.info('%s', netflix)
    netflix.convert_test(mmfile + '-test')

