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
    * make corpus
    webcorpus -make <input> <output>

    * merge freq dicts
    webcorpus -mergefreq <workdir> <output>

    * reid


"""

import sys
import os
import logging
import lxml.html as lh
import cPickle as pickle
#from gensim import utils
from utils import simple_preprocess
import re
import htmlentitydefs

logger = logging.getLogger(__name__)


####################
def convertentity(m):
    if m.group(1)=='#':
        try:
            return unichr(int(m.group(2)))
        except ValueError:
            return '&#%s;' % m.group(2)
        try:
            return htmlentitydefs.entitydefs[m.group(2)]
        except KeyError:
            return '&%s;' % m.group(2)

class SimpleHtml():

    def __init__(self):
        self.script_pattern = re.compile(r"(?is)<script[^>]*>(.*?)</script>")
        self.tag_pattern = re.compile(r'<[^>]+>')
        self.entity_pattern = re.compile(r'&(#?)(.+?);')

    def clean(self, s):
        html = self.script_pattern.sub('', s)
        html = self.tag_pattern.sub('', html)

        html = self.entity_pattern.sub(convertentity,html)
        html.replace("&nbsp;", " ")
        return html

##################
class WebCorpus():
    def __init__(self, uselxml = False):
        self.wordmap = {}
        self.wordfreq = {}
        self.docs = []
        self.simplehtml = SimpleHtml()
        self.USE_LXML = uselxml

    def load(self, loadfile):
        logger.debug('load webcorpus from %s', loadfile)

        docf = open(loadfile, 'r')
        dictf = open(loadfile+'.dict', 'r')
        freqf = open(loadfile+'.freq', 'r')

        self.docs = pickle.load(docf)
        self.wordmap = pickle.load(dictf)
        self.wordfreq = pickle.load(freqf)

    def save(self, savefile):
        logger.debug('save webcorpus to %s', savefile)

        docf = open(savefile, 'w')
        dictf = open(savefile+'.dict', 'w')
        freqf = open(savefile+'.freq', 'w')

        pickle.dump(self.docs, docf, pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.wordmap, dictf, pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.wordfreq, freqf, pickle.HIGHEST_PROTOCOL)


    def save_text(self, savefile):
        logger.debug('save webcorpus to text file %s', savefile)

        docf = open(savefile+'.txt', 'w')
        dictf = open(savefile+'.txt.dict', 'w')
        freqf = open(savefile+'.txt.freq', 'w')
        for doc in self.docs:
            id, tokens = doc
            #docf.write("%s\t%s\n"%(id, ' '.join(tokens).encode('utf-8')))
            #docf.write("%s\t%s\n"%(id, tokens))
            tokenstr = [str(token) for token in tokens]
            docf.write("%s\t%s\n"%(id, ' '.join(tokenstr).encode('utf-8')))

        # output sorted by id
        wordmap = [(word, self.wordmap[word]) for word in self.wordmap]
        wordmap = sorted(wordmap, key = lambda s: s[1])
        for id in xrange(len(wordmap)):
            dictf.write("%d\t%s\n"%(wordmap[id][1], wordmap[id][0].encode('utf-8')))

        # output sorted by id
        wordmap = [(word, self.wordfreq[word]) for word in self.wordfreq]
        wordmap = sorted(wordmap, key = lambda s: s[1], reverse=True)
        for id in xrange(len(wordmap)):
            freqf.write("%s\t%d\n"%( wordmap[id][0].encode('utf-8'), wordmap[id][1]))

    def add_page(self, id, content):
        logger.debug('add_page %s, %s', id, content[:10])

        try:
            content = content.decode('utf-8','ignore')

            if self.USE_LXML:
                #text = lh.document_fromstring(content).get_root().text_content()
                text = lh.document_fromstring(content).text_content()
            else:
                text = self.simplehtml.clean(content)

            # puncs remove?, call utils in gensim
            tokens = simple_preprocess(text)

            # 
            tokens = sorted(tokens)
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

    def add_wordfreq(self, loadfile):
        """
        load wordfreq and merge into current dict
        """
        freqf = open(loadfile, 'r')
        wordfreq = pickle.load(freqf)

        for word in wordfreq:
            if word in self.wordfreq:
                self.wordfreq[word] += wordfreq[word]
            else:
                self.wordfreq[word] = wordfreq[word]

    def makedict_byfreq(self):
        """
        build dict sorted by freq
        """
        wordmap = [(word, self.wordfreq[word]) for word in self.wordfreq]

        wordmap = sorted(wordmap, key = lambda s: s[1], reverse=True)

        # build a new dict
        for id in xrange(len(wordmap)):
            self.wordmap[wordmap[id][0]] = id



###################
def dump(input):
    webcorpus = WebCorpus()

    webcorpus.load(input)

    webcorpus.save_text(input)


def merge_wordfreq(workdir, savefile):
    webcorpus = WebCorpus()

    for dirpath, dnames, fnames in os.walk(workdir):
        for f in fnames:
            if f.endswith(".freq"):
                #basename = os.path.splitext(f)[0]
                webcorpus.add_wordfreq(os.path.join(dirpath, f))

    webcorpus.makedict_byfreq()
    webcorpus.save_text(savefile)

def make_webcorpus(input, output):
    """
    """
    webcorpus = WebCorpus()

    if os.path.exists(output):
        logger.info('%s exists already, skip convert', output)
        return webcorpus

    with open(input, 'r') as inputf:
        for line in inputf:
            pos = line.find('\t')
            if pos > 0:
                id = line[:pos]
                # search for the beginning of html code from "<" 
                pos2 = line.find('<html')
                if pos2 < 0:
                    pos2 = line.find('<HTML')
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
    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)
    logger.info("running %s" % ' '.join(sys.argv))

    if sys.argv[1] == '-make':
        webcorpus = make_webcorpus(sys.argv[2], sys.argv[3])
        #webcorpus.save_text(sys.argv[2] + '.mrlda')
    elif sys.argv[1] == '-mergefreq':
        webcorpus = merge_wordfreq(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == '-dump':
        dump(sys.argv[2])
    else:
        logger.error(globals()['__doc__'] % locals())







