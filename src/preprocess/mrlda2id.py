#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
USAGE: mrlda2id <mrlda file> <wordmap> <output>

convert MrLda input txt file to integer-id txt file
The word-id mapping input by wordmap.txt(gibbslda++)

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
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, idp, outp = sys.argv[1:4]

mrlda = open(inp, 'r')
wordmap = open(idp, 'r')
output = open(outp, 'w')

term_cnt = 0
wmap = dict()
for line in wordmap:
    if term_cnt == 0:
        term_cnt = int(line.strip())
        continue
    tokens = line.strip().split(' ')
    wmap[tokens[0]] = tokens[1]

for line in mrlda:
    tokens = line.split(' ')
    doc_token = tokens[0].split('\t')
    docid = doc_token[0]
    
    # logger.debug('split to : docid = %s, tokens = %s, %s'%(docid, doc_token,tokens))
    
    output.write('%s\t'%docid)

    if len(doc_token) > 1:
        tokens[0] = doc_token[1].strip()

        if tokens[0] != '':
            # last \n
            tokens[-1] = tokens[-1].strip()

            for word in tokens:
                if word in wmap:
                    output.write('%s '%wmap[word])

    else:
        logger.debug('doc_token=0, where docid=%s', docid)

    output.write('\n')


