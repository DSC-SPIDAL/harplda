#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
USAGE: idmapping <new wordids> <old wordids> <output wordmap>

combine two wordids dictionary, and output the wordmap file for mrlda2id
wordids dictionary are <id word freq> file with "\t" as seperator

"""

import logging
import os.path
import sys


def idmapping(newmap, oldmap, output):
    #load wordmap
    wordmapf = open(newmap, 'r')
    newwordmap = {}
    for line in wordmapf:
        data = line.strip().split('\t')
        word = data[1].decode('utf-8','ignore')
        newwordmap[word] = data[0]

    logger.debug('newwordmap size =%d', len(newwordmap))

    wordmapf = open(oldmap, 'r')
    idmap={}
    for line in wordmapf:
        data = line.strip().split('\t')
        word = data[1].decode('utf-8','ignore')
        if word in newwordmap:
            idmap[data[0]] = newwordmap[word]
    logger.debug('idmap size =%d', len(idmap))

    wordmapf = open(output, 'w')
    wordmapf.write("%d\n"%len(idmap))

    for id in idmap:
        wordmapf.write("%s %s\n"%(id, idmap[id]))


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, idp, outp = sys.argv[1:4]

    idmapping(inp, idp, outp)

