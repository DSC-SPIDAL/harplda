#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
USAGE: 

convert Gensim bow.mm file to GibbsLDA++ gibbs.mm
bow.mm in Corpus in the Matrix Market format
gibbs.mm in Corpus in GibbsLda++ format of List-Of-Words

refer to : http://radimrehurek.com/gensim/corpora/mmcorpus.html

Example: python -m lda-test.preprocess.mm2low bow.mm gibbs.low

"""

import logging
import os.path
import sys

from gensim.corpora import MmCorpus, LowCorpus, Dictionary

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
    inp, outp,dictfile = sys.argv[1:4]
 
    #let's convert the file
    mm = MmCorpus(inp)
    dictionary = Dictionary.load_from_text(dictfile)
    low = LowCorpus.serialize(outp, mm, dictionary)


