#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Data partition for lda trainer

input:
    text file
    nodes number    ; split input file to # files
    strategy        ; line by line round robin by default

Usage:
    split <input txt> <nodes number> <strategy>

"""

import sys, os
import logging

logger = logging.getLogger(__name__)

def split(input, nodenum):
    # open write files
    outf=[]
    for i in range(nodenum):
        outf.append(open('%s.%d'%(input,i), 'w', 64*1024))

    with open(input, 'r', 1024*1024) as inf:
        linenum = 0
        for line in inf:
            id = linenum % nodenum
            outf[id].write(line)
            linenum += 1

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

    input = sys.argv[1]
    nodenum = int(sys.argv[2])
    #strategy = sys.argv[3]

    split(input, nodenum)
