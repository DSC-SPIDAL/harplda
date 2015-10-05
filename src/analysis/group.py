#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Group data to make histgram.

input:
    datafile:
        x y

Usage:
    group <groupcnt> <input> <output>

"""

import sys, os, math,re
import numpy as np
import logging

logger = logging.getLogger(__name__)

def group_data(groupcnt, input, output):
    """
    """
    data = np.loadtxt(input)

    row, col = data.shape

    out = np.zeros((int(row/groupcnt), col))
    for i in xrange(int(row/groupcnt)):
        out[i][0] = i
        endid = i*groupcnt+groupcnt
        if endid >= row:
            endid = row
        out[i][1] = np.sum(data[i*groupcnt:endid,1]) / groupcnt

    logger.debug('data[:10]=%s, out=%s, sum=%s', data[:10,1], out[0], np.sum(data[:10,1]))

    np.savetxt(output, out, fmt='%d')

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


    groupcnt = int(sys.argv[1])
    input = sys.argv[2]
    output = sys.argv[3]

    group_data(groupcnt, input, output)
