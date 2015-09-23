#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
WebCorpus, make corpus from web pages in html format

input:
    id \t   html content
output:
    id \t   tokens sorted

    dictionary file
usage:
    webcorpus <input> <output>

"""

import sys
import os
import logging
import lxml.html as lh
import cPickle as pickle
#from gensim import utils
from utils import simple_preprocess


logger = logging.getLogger(__name__)

class WebCorpus():
    def __init__(self):
        self.wordmap = {}
        self.docs = []

    def load(self, loadfile):
        logger.debug('load webcorpus from %s', loadfile)

        docf = open(loadfile, 'r')
        dictf = open(loadfile+'.dict', 'r')
        self.docs = pickle.load(self.docf)
        self.dicts = pickle.load(self.dictf)


    def save(self, savefile):
        logger.debug('save webcorpus to %s', savefile)

        docf = open(savefile, 'w')
        dictf = open(savefile+'.dict', 'w')
        pickle.dump(self.docs, docf, pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.wordmap, dictf, pickle.HIGHEST_PROTOCOL)


    def save_text(self, savefile):
        logger.debug('save webcorpus to text file %s', savefile)

        docf = open(savefile, 'w')
        dictf = open(savefile+'.dict', 'w')
        for doc in self.docs:
            id, tokens = doc
            #docf.write("%s\t%s\n"%(id, ' '.join(tokens).encode('utf-8')))
            docf.write("%s\t%s\n"%(id, tokens))

        for word in self.wordmap:
            dictf.write("%d\t%s\n"%(self.wordmap[word], word.encode('utf-8')))


    def add_page(self, id, content):
        logger.debug('add_page %s', id)

        #text = lh.document_fromstring(content).get_root().text_content()
        text = lh.document_fromstring(content).text_content()

        # puncs remove?, call utils in gensim
        tokens = simple_preprocess(text)

        # 
        tokens = sorted(tokens)

        ids = []
        wordcnt = len(self.wordmap)
        for token in tokens:
            if token in self.wordmap:
                ids.append(self.wordmap[token])
            else:
                self.wordmap[token] = wordcnt
                ids.append(wordcnt)
                wordcnt += 1

        self.docs.append((id, ids))

def make_webcorpus(input, output):
    """
    """
    webcorpus = WebCorpus()

    with open(input, 'r') as inputf:
        for line in inputf:
            pos = line.find('\t')
            if pos > 0:
                id = line[:pos]
                # search for the beginning of html code from "<" 
                pos2 = line.find('<')
                if pos2 > 0:
                    content = line[pos2:]
                else:
                    content = line[pos+1:]
            else:
                logger.error('input format error, \\t not found, quit...')
                return

            webcorpus.add_page(id, content)


    webcorpus.save(output)
    return webcorpus

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)

    # check and process input arguments
    if len(sys.argv) != 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    logger.info("running %s" % ' '.join(sys.argv))

    webcorpus = make_webcorpus(sys.argv[1], sys.argv[2])

    webcorpus.save_text(sys.argv[2] + '.mrlda')







