#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Dump wikicorpus

input:
    enwiki dump file

output:
    mrlda format <docid, wordid....>
    dictionary file

usage:
    * make corpus, output .mrlda and .wordids
    wikicorpus -make <dumpfile> <output_prefix> <bigram>



"""


import logging
import os.path
import sys

from gensim.corpora import Dictionary, HashDictionary, MmCorpus, WikiCorpus
from gensim.models import TfidfModel


# Wiki is first scanned for all distinct word types (~7M). The types that
# appear in more than 10% of articles are removed and from the rest, the
# DEFAULT_DICT_SIZE most frequent types are kept.
DEFAULT_DICT_SIZE = 100000

class MyWikiCorpus():
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
                #dictf.write("%d\t%s\n"%(wordmap[id][1], wordmap[id][0].encode('utf-8','ignore')))
                dictf.write("%d\t%s\n"%(wordmap[id][1], wordmap[id][0]))

        if self.wordfreq:
            freqf = open(savefile+'.txt.freq', 'w')
            # output sorted by id
            wordmap = [(word, self.wordfreq[word]) for word in self.wordfreq]
            wordmap = sorted(wordmap, key = lambda s: s[1], reverse=True)
            for id in xrange(len(wordmap)):
                # freqf.write("%s\t%d\n"%( wordmap[id][0].encode('utf-8','ignore'), wordmap[id][1]))
                freqf.write("%s\t%d\n"%( wordmap[id][0], wordmap[id][1]))
                #freqf.write("%s\t%d\n"%( wordmap[id][0].encode('utf-8'), wordmap[id][1]))

    def add_page(self, id, tokens):
        logger.debug('add_page %s, %s', id, tokens[:10])

        # if bigram
        if self.bigram:
            grams = [ tokens[i]+'_'+tokens[i+1] for i in xrange(len(tokens)-1)]
        else:
            grams = tokens

        tokens = sorted(grams)
    

        #try:
        #    content = ' '.join(tokens).decode('utf-8','ignore')
        #except UnicodeDecodeError:
        #    logger.debug('exception UnicodeDecodeError')
        #    return -1

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
        return 0

def make_wikicorpus(input, output, bigram):
    """
    """
    wikicorpus = MyWikiCorpus(bigram=bigram)

    if os.path.exists(output):
        logger.info('%s exists already, skip convert', output)
        return wikicorpus
    
    wiki = WikiCorpus(input) # takes about 9h on a macbook pro, for 3.5m articles (june 2011)
    id = 0
    for tokens in wiki.get_texts():
        ret = wikicorpus.add_page(id, tokens)
        if ret == 0:
            id += 1

    wikicorpus.save(output)
    return wikicorpus

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)

    # check and process input arguments
    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)
    logger.info("running %s" % ' '.join(sys.argv))

    if sys.argv[1] == '-make':
        bigram = (sys.argv[4].lower() == 'true')
        wikicorpus = make_wikicorpus(sys.argv[2], sys.argv[3], bigram)
        #webcorpus.save_text(sys.argv[2] + '.mrlda')
    else:
        logger.error(globals()['__doc__'] % locals())

