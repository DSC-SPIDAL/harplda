#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TxtCorpus, make corpus from txt documents
  http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project
  http://web.eecs.umich.edu/~lahiri/gutenberg_dataset.html

input:
    txt files

output:
    mrlda format <docid, wordid....>
    dictionary file

usage:
    * make corpus, output .mrlda and .wordids
    txtcorpus -make <dir> <output_prefix> <bigram>

"""

import sys
import os
import logging
#from gensim import utils
from utils import simple_preprocess
import re

logger = logging.getLogger(__name__)


##################
VOCABSIZE=8000000
class TxtCorpus():
    def __init__(self, uselxml = False, bigram = False):
        # term, id
        self.wordmap = {}
        # term, freq
        self.wordfreq = {}
        #self.wordmap = dict.fromkeys(xrange(VOCABSIZE))
        #self.wordfreq =  dict.fromkeys(xrange(VOCABSIZE))
        # id, wordlist
        self.docs = []
        self.bigram = bigram
        logger.info('init TxtCorpus use bigram=%s', self.bigram)

    def save(self, savefile):
        logger.debug('save txtcorpus to text file %s', savefile)

        if self.docs:
            docf = open(savefile+'.txt', 'w')
            for doc in self.docs:
                id, tokens = doc
                #docf.write("%s\t%s\n"%(id, ' '.join(tokens).encode('utf-8')))
                #docf.write("%s\t%s\n"%(id, tokens))
                tokenstr = [str(token) for token in tokens]
                docf.write("%s\t%s\n"%(id, ' '.join(tokenstr).encode('utf-8')))


        if self.wordmap:
            dictf = open(savefile+'.txt.dict', 'w')
                   # output sorted by id
            wordmap = [(word, self.wordmap[word]) for word in self.wordmap]
            wordmap = sorted(wordmap, key = lambda s: s[1])
            for id in xrange(len(wordmap)):
                dictf.write("%d\t%s\n"%(wordmap[id][1], wordmap[id][0].encode('utf-8')))

        if self.wordfreq:
            freqf = open(savefile+'.txt.freq', 'w')
            # output sorted by id
            wordmap = [(word, self.wordfreq[word]) for word in self.wordfreq]
            wordmap = sorted(wordmap, key = lambda s: s[1], reverse=True)
            for id in xrange(len(wordmap)):
                freqf.write("%s\t%d\n"%( wordmap[id][0].encode('utf-8','ignore'), wordmap[id][1]))
                #freqf.write("%s\t%d\n"%( wordmap[id][0].encode('utf-8'), wordmap[id][1]))

    def add_page(self, id, content):
        logger.debug('add_page %s, %s', id, content[:10])

        try:
            content = content.decode('utf-8','ignore')

            # puncs remove?, call utils in gensim
            tokens = simple_preprocess(content)

            # if bigram
            if self.bigram:
                grams = [ tokens[i]+'_'+tokens[i+1] for i in xrange(len(tokens)-1)]
            else:
                grams = tokens

            tokens = sorted(grams)
        except UnicodeDecodeError:
            logger.debug('exception UnicodeDecodeError')
            return
        
        ids = []
        wordcnt = len(self.wordmap)
        for token in tokens:
            if token in self.wordmap:
                self.wordfreq[token] += 1
                ids.append(self.wordmap[token])
            else:
                self.wordfreq[token] = 1
                self.wordmap[token] = wordcnt
                ids.append(wordcnt)
                wordcnt += 1

        self.docs.append((id, ids))

def make_txtcorpus(inputdir, output, bigram):
    """
    """
    txtcorpus = TxtCorpus(bigram=bigram)

    if os.path.exists(output):
        logger.info('%s exists already, skip convert', output)
        return txtcorpus
    
    id = 0
    for dirpath, dnames, fnames in os.walk(inputdir):
        for f in fnames:
            input = os.path.join(dirpath, f)
            with open(input, 'r') as inputf:

                content = inputf.read()
                txtcorpus.add_page(id, content)
                id += 1

    txtcorpus.save(output)
    return txtcorpus

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)

    # check and process input arguments
    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)
    logger.info("running %s" % ' '.join(sys.argv))

    if sys.argv[1] == '-make':
        bigram = (sys.argv[4].lower() == 'true')
        txtcorpus = make_txtcorpus(sys.argv[2], sys.argv[3], bigram)
        #webcorpus.save_text(sys.argv[2] + '.mrlda')
    else:
        logger.error(globals()['__doc__'] % locals())







