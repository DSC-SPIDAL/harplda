#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
In distributed YLDA, each node output it's modeldata locally, which should merged togather into a global one.
Naive tool loads multiple word-topic-output matrix txt files , merge them into one global modeldata file.
And this one load only dictionaries, merge them into selected-dict files, which are extract plans for each node.

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

        dict.wordids.$HOSTNAME (local dictionary)
            id \t term \t freq

    global_dict.wordids (global dictionary)

output:
    global directory:
        matrix file
        matrix hyper file

Usage:
    * merge the modeldata dictionary files from input dir
    mergeTxtModelData -mergedict <local dir> <output dir> <global dict file>

    * select the selected words from local modeldata txt files
    mergeTxtModelData -extract <local dir> <output dir> <selected dict file>

    * merge the modeldata txt files from input dir
    mergeTxtModelData -mergetxt <local dir> <output dir>

"""

import sys, os, math,re
import numpy as np
import struct
import logging
from LDAModelData import LDAModelData

logger = logging.getLogger(__name__)


def load_dict(dfile):
    dictf = open(dfile, 'r')
    oldmap = dict()
    logger.info('read dict from %s', dfile)
    for line in dictf:
        tokens = line.strip().split('\t')
        oldmap[tokens[1]] = int(tokens[0])
    return oldmap

def load_dict_seq(dfile):
    dictf = open(dfile, 'r')
    oldmap = dict()
    logger.info('read dict from %s', dfile)
    for line in dictf:
        tokens = line.strip().split('\t')
        oldmap[int(tokens[0])] = tokens[1]
    return oldmap


def make_select_dicts(localdictdir, globaldict, outputdir, reverse_order):
    """
    input:
        local dict dir:
            dict.wordids.$HOSTNAME
        output dir
            dict.wordids.$HOSTNAME
        global dict file
    """
    # init
    dict_fs = []
    for dirpath, dnames, fnames in os.walk(localdictdir):
        dict_fs = [ f for f in fnames if f.startswith('dict.wordids')]
        break

    #
    # here the sequence of models are determined by sort()
    #
    dict_fs = sorted(dict_fs, reverse = reverse_order)
    logger.debug('found dict files under %s:%s, reverse=%s', localdictdir, dict_fs, reverse_order)

    dict_maps = []
    output_fs = []
    for f in dict_fs:
        dict_maps.append(load_dict(localdictdir + '/' + f))
        output_fs.append(open(outputdir + '/' + f, 'w'))
 
    gdict = load_dict_seq(globaldict)

    # run merge
    logger.info('merge begins, num_words=%d.................',len(gdict))

    num_words = len(gdict)
    for id in xrange(num_words):
            term = gdict[id]
            found = False
            for m in range(len(dict_maps)):
                if term in dict_maps[m]:
                    # assign word id to dict m
                    output_fs[m].write('%s\t%s\n'%(dict_maps[m][term], id))
                    found = True
                    break
            if found == False:
                logger.error('no model data for word id=%d', id)
                break

    # close
    for f in output_fs:
        f.close()

def extract_by_select_dicts(local_work_dir, select_dict, output_dir):
    """
    input:
        local_work_dir
            *.hyper     ; model data files
        select_dir      ; select dict file created by coordinator
        output_dir      ; 
            *.hyper     ; output selected model data files

    """
    # init
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # walk through each node dir, run merge
    mfs = []
    for dirpath, dnames, fnames in os.walk(local_work_dir):
        
        #for fname in fnames:
        #if fname.endwith('.hyper'):
        #    mfs.append(fname)
        mfs = [ os.path.splitext(f)[0] for f in fnames if f.endswith('.hyper')]
        break

    logger.debug('found model files: %s', mfs)
    
    # run merge
    for f in mfs:
        # f is the model file name
        model = LDAModelData()
        model.load_from_txt(local_work_dir + '/' + f, fullload=False)
        model.align_dict('', select_dict, 1000000)
        
        model.save_to_txt(outputdir + '/' + f)


def merge_one_model(dirlist, modelfile, outputdir):
    """
    concatenate the model files works
    """
    modeldata = None
    for dir in dirlist:
        cmd = "cat " + dir + '/' +modelfile + ' >>_dest'
        os.system(cmd)
    os.system('cp '+ dirlist[0] + '/' + modelfile + '.hyper _dest.hyper')
        

    model = LDAModelData()
    model.load_from_txt('_dest', fullload=False)
    model.save_to_txt(outputdir + '/' + modelfile)

    os.system("rm _dest*")


def merge_local_models(modelDir, outputdir):
    """
    input:
        modelDir    ; local/host1, host2, ....
            *.hyper ; model files
        outputdir   ; 

    """
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
        merge_one_model(dirlist, f, outputdir)


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

    cmd = sys.argv[1]
    if cmd == '-mergedict':
        localdir = sys.argv[2]
        outputdir = sys.argv[3]
        globalDict = sys.argv[4]
        reverse_order = False
        if len(sys.argv) > 5:
            reverse_order = (sys.argv[5].lower() == 'true')

        make_select_dicts(localdir, globalDict, outputdir, reverse_order)

    elif cmd == '-extract':
        localdir = sys.argv[2]
        outputdir = sys.argv[3]
        selectDict = sys.argv[4]

        extract_by_select_dicts(localdir, selectDict , outputdir)

    elif cmd == '-mergetxt':
        localdir = sys.argv[2]
        outputdir = sys.argv[3]
 
        merge_local_models(localdir, outputdir)




