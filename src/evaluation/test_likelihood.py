#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
compute the held-out likelihood by mallet evaluator

dependency:
mallet toolkit installed under $ROOT/tool/mallet

input:
    model file in mallet binary format (java use bigendian)
    numTopics   int
    numWords    int
    alpha   double
    beta    double
    model Matrix[numWords][numTopics]   int

    held-out text file

Usage: 
    * calculate likelihoods and perplexity
    test_likelihood <mallet path> <trainer> <model dir| model file> <held-out data> <held-out.ldac>

    * draw convergence fig from likelihoods result
    test_likelihood -draw fig-name

"""

import sys,os,re
import numpy as np
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

def run_mallet_evaluator(mallet, model, data, trainer):
    """
    Refer to mallet's manual
    for 3rd party topic model trainer results:
    run "mallet evaluate-topics --modeldata <model> --input data --output-prob probfile"

    for mallet results:
    run "mallet evaluate-topics --modelfile <model> --input data --output-prob probfile"

    return:
        0  on error
        likelihood  log likelihood sum

    """
    name = model
    l_file = model + '-mallet-lhood.dat'
    if os.path.exists(l_file):
        logger.info('%s exists, skip call mallet', l_file)
    else:
        if trainer == 'mallet':
            command = mallet + ' evaluate-topics --modelfile ' + model + ' --input ' + data +' --output-prob ' + l_file
        else:
            command = mallet + ' evaluate-topics --modeldata ' + model + ' --input ' + data +' --output-prob ' + l_file
        logger.info('call mallet evaluator: %s', command)
        ret = os.system(command)
        if ret:
            # something wrong
            return 0

    #calc the likelihood and perplexity 
    l_sum = 0.
    with open(l_file, 'r') as file:
        for line in file:
            l_sum+= float(line.rstrip())

    return l_sum


def calc_file(malletPath, modelfile, data, doccnt, wordcnt, trainer):
    """
    Calculate likelihood of one model output phi on testset

    input:
        modelfile   model file name
        wordcnt     total word counts of the collection
    return:
        doccnt, likelihood
        doccnt = 0 in error
    """

    mallet = malletPath + '/mallet'
    likelihood = 0 
    perplexity = 0

    if os.path.exists(mallet):
        if os.path.exists(modelfile):
            if os.path.exists(data):
                likelihood = run_mallet_evaluator(mallet, modelfile, data, trainer)

                if likelihood != 0:
                    perplexity = np.exp(- likelihood / wordcnt)
                    logger.info('doccnt = %d, wordcnt = %d, likelihood = %f, perplexity = %f\n'%(doccnt, wordcnt, likelihood, perplexity))
                else:
                    logger.error('Error: run command failed')
            else:
                logger.error('Error: data file not exists!')
        else:
            logger.error('Error: model file not found at %s.',modelfile)
    else:
        logger.error('Error: mallet not found at %s', mallet)
 
    return likelihood, perplexity

def calc_dir(malletPath, modelDir, data, doccnt, wordcnt, ext, trainer):
    """
    Calculate likelihood on models output of different iterations

    input:
        modelDir   directory name
    return:
        array [iternum, likelihood]
    """
    # cache file
    cacheFile = modelDir + '.likelihood'
    if os.path.exists(cacheFile):
        logger.info('Cache file found at %s, loading likelihoods', cacheFile)
        likelihoods = np.loadtxt(cacheFile)
        return likelihoods

    models = []
    for dirpath, dnames, fnames in os.walk(modelDir):
        for f in fnames:
            if f.endswith(ext):
                m = re.search('.*[\.-]([0-9]*)' + ext, f)
                if m:
                    iternum = int(m.group(1))

                    logger.info('load model from %s as iternum = %d', f, iternum)
                    basename = os.path.splitext(f)[0]
                    models.append((iternum, os.path.join(dirpath, basename)))
    
    models =  sorted(models, key = lambda modeltp : modeltp[0])
    if len(models) < 2:
        logger.error('ERROR: load too few model files')
        return None

    logger.debug('models iternum as %s', [s[0] for s in models])
    likelihoods = np.zeros((len(models), 3))

    for idx in range( len(models) ):
        likelihood, perplexity = calc_file(malletPath, models[idx][1] + ext, data, doccnt, wordcnt, trainer)

        likelihoods[idx][0] = models[idx][0]
        likelihoods[idx][1] = likelihood
        likelihoods[idx][2] = perplexity

    # save result
    np.savetxt(cacheFile, likelihoods)

    return likelihoods

def draw_likelihood(likelihoods, modelname, fig, show = False):
    logger.debug('plot the matrix')

    x = likelihoods[:,0]
    y = likelihoods[:,1]
    z = likelihoods[:,2]
    plt.title('Convergence of likelihood')
    plt.xlabel('Iteration Number')
    plt.ylabel('Perplexity')
    #plt.plot(x, y, 'b.-', label=modelname+' likelihood' )
    plt.plot(x, z, 'c.-', label=modelname+' perplexity' )
    plt.legend()

    plt.savefig(fig)
    if show:
        plt.show()

def draw_convergence(fig, show = False):
    """
    Draw convergence graph, load likelihood data from .likelihood data
    """
    plt.title('Convergence of LDA Topic Model')
    plt.xlabel('Iteration Number')
    plt.ylabel('Perplexity')

    colors = ['b','c','r','g','y']
    idx = 0

    for dirpath, dnames, fnames in os.walk("."):
        for f in fnames:
            if f.find('.likelihood') > 0:
                modelname =os.path.splitext(f)[0]
                filename = os.path.join(dirpath, f)
                logger.info('load likelihood data from %s', filename)
                likelihoods = np.loadtxt(filename)

                x = likelihoods[:,0]
                y = likelihoods[:,1]
                z = likelihoods[:,2]
                plt.plot(x, z, colors[idx] + '.-', label=modelname )
                idx += 1

    plt.legend()
    plt.savefig(fig)
    if show:
        plt.show()

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    #logging.basicConfig(filename='debug_calcdistance.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                    level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 6:
        if len(sys.argv) == 3 and sys.argv[1] == '-draw':
            draw_convergence(sys.argv[2] + '.png', True)
            sys.exit(0)
        else:
            logger.error(globals()['__doc__'] % locals())
            sys.exit(1)

    # check the path
    malletPath = sys.argv[1]
    trainer = sys.argv[2]
    modelname = sys.argv[3]
    data = sys.argv[4]

    # read doccnt and wordcnt from .ldac format test file
    ldac = sys.argv[5]
    # get wordnum in data
    num_docs, num_words = 0, 0
    with open(ldac, 'r') as ldacf:
        for line in ldacf:
            num_docs += 1
            # format: wordcnt word1:cnt1 word2:cnt2 .....
            num_words += int(line[:line.find(' ')])

    logger.info('test set %s has %d docs and %d words', data, num_docs, num_words)

    if os.path.exists(modelname):
        # if input a directory name
        likelihoods = calc_dir(malletPath, modelname, data, num_docs, num_words,'.mallet', trainer)

        #draw it
        draw_likelihood(likelihoods, modelname, modelname + '.png', True)

    else:
        calc_file(malletPath, modelname+'.mallet', data, num_docs, num_words, trainer)
    


