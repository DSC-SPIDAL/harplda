#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
compute the held-out likelihood by blei's lda implementation.

dependency:
blei's lda-c-dist installed under $ROOT/tool/blei

input:
1. model beta file
    .beta contains the log of the topic distributions.
    Each line is a topic; in line k, each entry is log p(w | z=k)
2. model alpha file
    .other contains alpha.

    For example:
    num_topics 20
    num_terms 21774
    alpha 0.015
3. held-out text file

output:
    doccnt, likelihood

Usage: test_likelihood <lda-install-path> <model-name> <data>
"""

import sys,os,re
import numpy as np
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)



def run_lda_inference(lda, settings, model, data):
    """
    Refer to blei's lda readme
    run "lda inf [settings] [model] [data] [name]"
    """
    name = model
    if os.path.exists(name + '-lda-lhood.dat'):
        logger.info('%s exists, skip call lda', name)
    else:
        command = lda + ' inf ' + settings + ' ' + model + ' ' + data + ' ' + name
        logger.info('call lda inference: %s', command)
        ret = os.system(command)
        if ret:
            # something wrong
            return 0, ret

    #calc the likelihood and perplexity 
    l_file = model + '-lda-lhood.dat'
    num_docs, num_words =0, 0
    l_sum = 0.
    with open(l_file, 'r') as file:
        for line in file:
            num_docs+=1
            l_sum+= float(line.rstrip())

    with open(data, 'r') as ldacf:
        for line in ldacf:
            # format: wordcnt word1:cnt1 word2:cnt2 .....
            num_words += int(line[:line.find(' ')])

    perplexity = np.exp(-l_sum / num_words)

    return num_docs, l_sum, num_words, perplexity


def calc_file(ldaPath, modelname, data, ext = '.beta'):
    """
    Calculate likelihood of one model output phi on testset

    input:
        modelname   model file name, '.beta', '.other' should exist
    return:
        doccnt, likelihood
        doccnt = 0 in error
    """

    lda = ldaPath + '/lda'
    settings = ldaPath + '/inf-settings.txt'
    local_settings = '.inf-settings.txt'
    beta = modelname + ext
    other = modelname + '.other'
    
    doccnt, likelihood = 0,0 
    wordcnt, perplexity = 0,0

    if os.path.exists(lda) and os.path.exists(settings):
        if os.path.exists(beta) and os.path.exists(other):
            if os.path.exists(data):
                if os.path.exists(local_settings):
                    doccnt, likelihood, wordcnt, perplexity = run_lda_inference(lda, local_settings, modelname, data)
                else:
                    doccnt, likelihood, wordcnt, perplexity = run_lda_inference(lda, settings, modelname, data)
                if doccnt:
                    logger.info('doccnt = %d, wordcnt = %d, likelihood = %f, perplexity = %f\n'%(doccnt, wordcnt, likelihood, perplexity))
                else:
                    logger.error('Error: run command failed\n')
            else:
                logger.error('Error: data file not exists!\n')
        else:
            logger.error('Error: %s or .other file not found at %s, %s\n'%(ext, beta, other))
    else:
        logger.error('Error: lda not found at %s\n'%lda)
    
    return doccnt, likelihood, wordcnt, perplexity

def calc_dir(ldaPath, modelDir, data, ext = '.beta'):
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
                m = re.search('.*-([0-9]*)' + ext, f)
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
        doccnt, likelihood, wordcnt, perplexity = calc_file(ldaPath, models[idx][1], data, ext)

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
                plt.plot(x, z, colors[idx] + '.-', label=modelname+' perplexity' )
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
    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # check the path
    ldaPath = sys.argv[1]
    modelname = sys.argv[2]
    data = sys.argv[3]

    if ldaPath == '-draw':
        draw_convergence(modelname + '.png', True)
        sys.exit(0)

    if os.path.exists(modelname):
        # if input a directory name
        likelihoods = calc_dir(ldaPath, modelname, data)

        #draw it
        draw_likelihood(likelihoods, modelname, modelname + '.png', True)

    else:
        calc_file(ldaPath, modelname, data)
    


