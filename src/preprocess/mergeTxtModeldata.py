#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
In distributed YLDA, each node output it's modeldata locally, which should merged togather into a global one.
This tool load multiple word-topic-output matrix txt files , merge them into one global modeldata file.

input:
    node m directory:
        matrix file
            wordid  wordfreq    topic:count ....
            type + " " + totalCount + " " + [" " + topic + ":" + count]*

        matrix hyper file
            #alpha :
            #beta : 
            #numTopics :
            #numTypes : 

        dict.wordids (local dictionary)
            id \t term \t freq

    global_dict.wordids (global dictionary)

output:
    global directory:
        matrix file
        matrix hyper file

Usage:
    * merge the modeldata txt files from input dir
    mergeTxtModeldata <node dir> <global dir> <global dict file>

"""

import sys, os, math,re
import numpy as np
import struct
import logging
from LDAModelData import LDAModelData

logger = logging.getLogger(__name__)

def merge_one_model(dirlist, modelfile, modeldict, globaldict, outputdir, fullload = False):
    
    logger.info('merge_one_model for modelfile=%s, globaldir=%s, outputdir=%s', modelfile, globaldict, outputdir)
    #load modles

    models = []
    for dir in dirlist:
        model = LDAModelData()
        model.load_from_txt(dir + '/' + modelfile, fullload=fullload)
        model.align_dict(globaldict, dir + '/' + modeldict)
        models.append(model)

    # run merge
    logger.info('merge begins.................')

    #logger.debug('nonzero cnt = %d', np.count_nonzero(models[0].model))
    #models[0].save_to_txt('test/debug')

    num_words, num_topics = models[0].model.shape
    for id in xrange(num_words):
        if fullload:
            nonzero = np.count_nonzero(models[0].model[id]) 
        else:
            nonzero = (models[0].model[id][0] != 0)
        if nonzero == 0:
            #logger.debug('word %d missed', id)
            # try to find a none zero row
            found = False
            for m in range(1, len(models)):
                if fullload:
                    nonzero = np.count_nonzero(models[m].model[id]) 
                else:
                    nonzero = (models[m].model[id][0] != 0)

                if nonzero != 0:
                    models[0].model[id] = models[m].model[id]
                    #if id == 126589:
                    #    logger.info('debug: found missed word %d at id=%d, =>%s', id, m, models[m].model[id])
                    found = True
                    break
            if found == False:
                logger.error('no model data for word id=%d', id)
                #output current models
                for m in range(len(models)):
                    logger.error('%d model[%d]=%s', m , id, models[m].model[id])
    
                break

    # save model
    models[0].alpha = [0.05]
    models[0].save_to_txt(outputdir + '/' + modelfile)

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

    modelDir = sys.argv[1]
    outputdir = sys.argv[2]
    globalDict = sys.argv[3]

    # walk through the model dir, get the first level dirs
    dirlist = []
    for dirpath, dnames, fnames in os.walk(modelDir):
        dirlist = [modelDir + '/' + d for d in dnames]
        break
    dirlist = sorted(dirlist)
    logger.debug('found nodes: %s', dirlist)

    # walk through each node dir, run merge
    mfs = []
    for dirpath, dnames, fnames in os.walk(dirlist[0]):
        
        #for fname in fnames:
        #if fname.endwith('.hyper'):
        #    mfs.append(fname)
        mfs = [ os.path.splitext(f)[0] for f in fnames if f.endswith('.hyper')]
        break

    logger.debug('found model files: %s', mfs)
    
    # run merge
    for f in mfs:
        merge_one_model(dirlist, f, 'dict.wordids', globalDict, outputdir)
        #break




