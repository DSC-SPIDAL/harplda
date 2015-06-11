#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
USAGE: 

convert Gensim bow.mm file to blei's blei.ldac
bow.mm in Corpus in the Matrix Market format
blei.ldac is Corpus in ldac format

refer to : http://radimrehurek.com/gensim/corpora/mmcorpus.html

Example: python -m lda-test.preprocess.mm2ldac bow.mm blei.ldac

"""

import logging
import os.path
import sys

from gensim.corpora import LowCorpus, BleiCorpus, Dictionary

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
 
    #let's convert the file
    dictionary = Dictionary.load_from_text('wordids.txt')
    low = LowCorpus(inp, dictionary)
    blei = BleiCorpus.serialize(outp, low , dictionary)



