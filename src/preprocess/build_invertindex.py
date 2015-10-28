#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Build a inverted file

input: mrlda format
    docid   wordid....
output: mrlda format
    wordid  docid....

Usage:
    build_invertedfile   <intput> <output>

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import struct
import logging
from LDAModelData import LDAModelData

logger = logging.getLogger(__name__)

def build_inv(input, output, format='ylda'):
    outf = open(output, 'w', 1024*1024)
    inf = open(input,'r',1024*1024)
    linecnt = 0
    
    # word -> [docid ,  ]

    wordmap={}
    for line in inf:
        tokens = line.strip().split(' ')
        #doc_token = tokens[0].split('\t')
        #docid = doc_token[0]
        docid = str(linecnt)
        
        # logger.debug('split to : docid = %s, tokens = %s, %s'%(docid, doc_token,tokens))
    
        #if len(doc_token) > 1:
        #    tokens[0] = doc_token[1].strip()
    
        #    if tokens[0] != '':
                # last \n
        #        tokens[-1] = tokens[-1].strip()
        
        for wordid in xrange(2,len(tokens)):
            word = tokens[wordid]
            if word in wordmap:
                wordmap[word].append(docid)
            else:
                wordmap[word] = [docid]
        
        linecnt += 1
    
    # outout inv file
    for word in wordmap:
        postlist = ' '.join(wordmap[word])
        outf.write('%s 0 %s\n'%(word,postlist))


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

    input = sys.argv[1]
    output = sys.argv[2]
    
    build_inv(input, output)
