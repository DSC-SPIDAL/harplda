#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
USAGE: low2mrlda <low file> <mrlda file>

convert GibbsLDA++ low input file to MrLda input txt file 

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

lowfile = open(inp, 'r')
output = open(outp, 'w')

docid = -1
for line in lowfile:
    if docid == -1:
        docid += 1
        continue
    output.write('doc%d\t%s'%(docid, line))
    docid += 1


