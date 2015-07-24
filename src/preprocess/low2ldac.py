#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Convert list-Of-Words file to blei's blei.ldac
bow.mm in Corpus in the list of Words format
blei.ldac is Corpus in ldac format

refer to : http://radimrehurek.com/gensim/corpora/mmcorpus.html

Usage:
    low2ldac gibbs.low blei.ldac wordids.txt

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
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp, outp, wordids = sys.argv[1:4]
 
    #let's convert the file
    dictionary = Dictionary.load_from_text(wordids)
    low = LowCorpus(inp, dictionary)
    blei = BleiCorpus.serialize(outp, low , dictionary)



