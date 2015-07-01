#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
USAGE: mm2mrlda <bow.mm> <mrlda file>

convert bow.mm into MrLda input txt file with integer-id directly
bow.mm in mm format
%%MatrixMarket matrix coordinate real general
doccnt  wordcnt  positioncnt
docid  wordid   freq

"""

import logging
import os.path
import sys

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, outp = sys.argv[1:3]

    mm = open(inp, 'r')
    mrlda = open(outp, 'w')
    
    mm.readline()
    #read meta
    line = mm.readline().strip()
    line = mm.readline().strip()
    
    lastdocid = '-1'
    wordlist = []
    for line in mm:
        tokens = line.strip().split(' ')
        docid = tokens[0]
        wordid = tokens[1]
        freq = int(tokens[2])

        if docid != lastdocid:
            if lastdocid != '-1':
                #write the last line
                wordstring = ' '.join(wordlist)
                mrlda.write('%s\t%s\n'%(lastdocid, wordstring))
            wordlist = []
            wordlist.extend([wordid for x in range(freq)])
            lastdocid = docid
        else:
            wordlist.extend([wordid for x in range(freq)])

    # write the last line
    wordstring = ' '.join(wordlist)
    mrlda.write('%s\t%s\n'%(lastdocid, wordstring))
        
    
    
