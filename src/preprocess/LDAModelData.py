#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Model Data File: word-topic-output matrix txt file

Txt Format:
    matrix file
    wordid  wordfreq    topic:count ....
    type + " " + totalCount + " " + [" " + topic + ":" + count]*

    matrix hyper file
    #alpha :
    #beta : 
    #numTopics :
    #numTypes : 

Binary Format: (java use bigendian)
    numTopics   int
    numWords    int
    alpha   double
    beta    double
    model Matrix[numWords][numTopics]   int

    if two result comes from different word-id, they should be aligned by dictionary matching.
"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import struct
import logging

logger = logging.getLogger(__name__)


class LDAModelData():
    def __init__(self):
        self.model = None
        self.num_topics = 0
        self.alpha = []
        self.beta = 0.
        self.fullload = True

    def load_from_txt(self, txtmodel, fullload = True):
        """
        input:
            model data in txt format

            fullload: 
                True when load each cell of the model matrix
                False, only load id, and row data string,it'll be much faster
    
        return:
            model is a word-topic count matrix
        """
        model = None
        
        #load .hyper
        alpha = []
        beta = 0.
        numTopics, numTypes = 0, 0
        with open(txtmodel + '.hyper', 'r') as hyperf:
            line = hyperf.readline().strip()
    #values = line[line.find(':') + 2:].split(' ')
    #        print values
            alpha = [float(x) for x in line[line.find(':') + 2:].split(' ')]
            line = hyperf.readline().strip()
            beta = float(line[line.find(':') + 1:])
            line = hyperf.readline().strip()
            numTopics = int(line[line.find(':') + 1:])
            line = hyperf.readline().strip()
            numTypes = int(line[line.find(':') + 1:])
    
            logger.debug('load hyper %s as: numTopics=%d, numTypes=%d, alpha[0]=%f, beta=%f', txtmodel, numTopics, numTypes, alpha[0], beta)
    
        #load model data
        if fullload:
            model = np.zeros((numTypes, numTopics))
        else:
            # save the whole row string
            model = np.zeros((numTypes, 1), dtype=np.object)
        logger.debug('loading model data....,model.shape=%s', model.shape)
        with open(txtmodel, 'r') as matf:
            linecnt = 0
            for line in matf:
                line = line.strip()
                idx = line.find('  ')
                line = line[idx + 2:]

                # hacks
                #idx = line.find(' 0 ')
                #line = line[idx + 3:]
                if (idx <= 0):
                    logger.error('txt model file format error')
                    return
    
                # word id should be first number in the begining,
                # but it's always start from 0, to num_words for mallet's output
                # and it's local number for ylda Merge_Topics_Counts output
                # so, we just use lineno as the word id, which is always correct.
                # word =  int(line[:line.find(' ')])
                word = linecnt
    
                if fullload:
                    # parse each cell
                    tokens = line.split(' ')
                    for item in tokens:
                        #print 'item=', item
                        tp = item.split(':')
                        #print tp[0], tp[1]
                        model[word][int(tp[0])] = int(tp[1])
                else:
                    model[word][0] = line
                    #logger.debug('read ine [%d]=%s', word,  model[word][0])

                linecnt += 1
    
        # verify data format
        if linecnt != numTypes:
            logger.error('txtmodel file format error, linecnt=%d, numTypes=%d', linecnt, numTypes)
    
        # sort the matrix by the first column            
        #model = model[model[:,0].argsort()]
        #model = np.sort(model, axis=0)
        # for w in range(5):
        #    logger.debug('new model[%d]=%s', w, model[w][0])
    
        #model = model[:, 1:]
        logger.info('done, load model data as %s, alpha=%s, beta=%s', model.shape, alpha, beta)

        self.model = model
        self.alpha = alpha
        self.beta = beta
        self.num_topics = numTopics
        self.fullload = fullload

        return model, alpha, beta

    def save_to_txt(self, txtmodel):
        """
        Refer to :ylda/src/Unigram_Models/Topicsxxx/TypeTopicCounts.cpp:savemodel
        """
        logger.info('save model to txt as %s', txtmodel)
        num_words, num_topics = self.model.shape
        # if not fullload, num_topics is 1 always
        num_topics = self.num_topics
        with open(txtmodel, 'w') as mf:
            for i in xrange(num_words):
                prefix = str(i) + ' 0 '

                if self.fullload:
                    line = []
                    for t in xrange(num_topics):
                        if self.model[i][t] != 0:
                            line.append(str(t)+':'+str(self.model[i][t]))
                    content = ' '.join(line)    
                    # a litter different to ylda model data, here content is not sorted
                    mf.write(prefix + content + '\n')
                else:
                    mf.write(prefix + ' ' + str(self.model[i][0]) + '\n')

        with open(txtmodel+'.hyper', 'w') as hf:
            content = ','.join([str(alpha) for alpha in self.alpha])
            hf.write("#alpha : " + content + "\n")
            hf.write("#beta : " + str(self.beta) + "\n")
            hf.write("#numTopics : " + str(num_topics) +"\n")
            hf.write("#numTypes : " + str(num_words) + "\n")

    def align_dict(self, newDict, oldDict):
        """
        Align word id between two model system
    
        input:
            newDict  <id term>
            oldDict    <id term freq>
    
        output:
            model       realigned
    
        """
        new = open(newDict, 'r')
        old = open(oldDict, 'r')
    
        # read in oldDict
        logger.info('read new dict from %s', newDict)
        newmap = dict()
        for line in new:
            tokens = line.strip().split('\t')
            newmap[int(tokens[0])] = tokens[1]
        
        oldmap = dict()
        logger.info('read old dict from %s', oldDict)
        for line in old:
            tokens = line.strip().split('\t')
            oldmap[tokens[1]] = int(tokens[0])
        
    
        K,V = self.model.shape
        if self.fullload:
            new_model = np.zeros((len(newmap),V))
        else:
            new_model = np.zeros((len(newmap),V), dtype=np.object)

        for k in range(len(newmap)):
            # test dataset dict may be different with the traning set
            if newmap[k] in oldmap:
                new_model[k] = self.model[oldmap[newmap[k]]]
    
        # debug
        # 3161    christ  27
        #logger.debug('new: term = %s, id = 3137, topics count = %s', newmap[3137], new_model[3137])
        #logger.debug('old: term = christ, id = %d, topics count = %s', oldmap['christ'], model[oldmap['christ']])
    

        #for w in range(5):
        #    logger.debug('new model[%d]=%s', w, new_model[w])
        #    logger.debug('old model[%d]=%s', w, self.model[w])
    
        logger.info('align model data as %s', new_model.shape)
        self.model = new_model
        return new_model

    def save_to_binary_full(self, fname):
        with open(fname, 'wb') as f:
            V, K = self.model.shape
            K = self.num_topics
            f.write(struct.pack('>i', K))
            f.write(struct.pack('>i', V))
            f.write(struct.pack('>d', self.alpha[0]))
            f.write(struct.pack('>d', self.beta))
    
            for w in range(V):
                for k in range(K):
                    f.write(struct.pack('>i', self.model[w][k]))
    
    def save_to_binary(self, fname):
        """
        Save the topicCount[][] each line sorted by count descendently
        """
        with open(fname, 'wb') as f:
            V, K = self.model.shape
            if K != self.num_topics:
                logger.error(' model data(%d,%d) mismatch with .hyper(k=%d)', V,K, self.num_topics)
                return

            f.write(struct.pack('>i', K))
            f.write(struct.pack('>i', V))
            f.write(struct.pack('>d', self.alpha[0]))
            f.write(struct.pack('>d', self.beta))

            #todo, here is the only fullload mode save
            index = np.argsort(self.model)
            for w in range(V):
                for k in range(-1, -K-1, -1):
                    # sort in acscent order
                    col = index[w][k]
                    if (self.model[w][col] == 0):
                        # a row end by (0,0) pair
                        f.write(struct.pack('>i', 0))
                        f.write(struct.pack('>i', 0))
                        break
    
                    f.write(struct.pack('>i', self.model[w][col]))
                    f.write(struct.pack('>i', col))

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

    modelfile = sys.argv[1]
    malletDict = sys.argv[2]
    harpDict = sys.argv[3]

    model = LDAModelData()
    model.load_from_txt(modelfile)
    model.align_dict(malletDict, harpDict)
    logger.info('model is: %s, alpha=%s, beta=%s', model.model.shape, model.alpha, model.beta)


    savefile = modelfile + '.mallet'
    logger.info('saving to %s', savefile)
    #basename = os.path.splitext(modelfile)[0]
    model.save_to_binary(savefile)


