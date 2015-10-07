#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
convert mm file into MrLda input txt file with integer-id directly

mm format
%%MatrixMarket matrix coordinate real general
doccnt  wordcnt  positioncnt
docid  wordid   freq

mrlda low format
docid  wordlist....

idmap format
id  newid   freq

USAGE: mm2mrlda <mm file> <mrlda file> <skip headline cnt> <idmap>

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
    skipLines = 2
    idmap = {}

    if len(sys.argv) == 5:
        skipLines = int(sys.argv[3])
        idmapf = open(sys.argv[4], 'r')
        logger.info('use idmap from %s', sys.argv[4])
        # load dictionary
        for line in idmapf:
            tokens = line.strip().split('\t')
            idmap[tokens[0]] = tokens[1]

    mm = open(inp, 'r')
    mrlda = open(outp, 'w')

    for i in range(skipLines):
        line = mm.readline().strip()
        logger.info('skip:%s', line)

    lastdocid = '-1'
    wordlist = []
    for line in mm:
        tokens = line.strip().split(' ')
        docid = tokens[0]
        if idmap:
            if tokens[1] in idmap:
                wordid = idmap[tokens[1]]
            else:
                continue
        else:
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



