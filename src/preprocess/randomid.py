#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Create a radom wordid file.
Ylda get better performance with no id sorted by word freq. When we get reid input file, we have
to convert it back to no no-reid version through a randomized id mapping.

output format:
    wordmap : gibbslda dictionary file <term id>

Usage:
    randomid <dictsize> <output>

"""
import sys, os
import logging
import numpy as np

logger = logging.getLogger(__name__)

def make_randomdict(dictsize, wordmapfile):

    logger.info('create random permutation of %d words', dictsize)
    rand_dict = np.random.permutation(dictsize)

    wordmap = open(wordmapfile, 'w')

    logger.info('save dict file to %s', wordmapfile)
    wordmap.write('%d\n'%dictsize)
    for id in xrange(dictsize):
        wordmap.write('%d %d\n'%(id, rand_dict[id]))

    wordmap.close()

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

    make_randomdict(int(sys.argv[1]), sys.argv[2])


