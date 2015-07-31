#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Validate the sparseness property in the topic model outputed by lda.
Each model is a V*K matrix with every element a log probability

prob(v=k | model) = (C(v,k) + beta ) /(sigma(C(v,k) + V*beta)
minval = argmin(model[k]) ~ 1/V

So, the sparseness can be represented by:
1. ratio of prob > minval
2. heat map

Usage:
    test_sparseness -file <model file>
    Output the sparseness measure

    test_sparseness -dir <model dir>
    Output the sparseness changes on iterations

    test_sparseness -draw <fig file>
    Output the sparseness map

"""

import sys, os, re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib import cm
import logging

logger = logging.getLogger(__name__)

def calc_sparseness(model):
    """
    input:
        np.array, K*V matrix, each row is term distribution of a topic
    return:
        np.array, K*1 matrix, ratio of prob > minval
    """
    K,V = model.shape

    # check the sum of probability
#    for row in range(K):
#        logger.debug('topicA row %d sum=%f', row, sum(topicA[row]))
#        logger.debug('topicB row %d sum=%f', row, sum(topicB[row]))

    sparseness = np.zeros((K,1))
    # minval = 1/V + 1e-12

    logger.debug('calculate the sparseness, shape =(%d, %d) ', K, V)
    for i in range(K):
        minval = min(model[i])
        sparseness[i] = np.where(model[i] > minval)[0].shape[0] * 1.0 / V

    logger.debug('End of calculate, sparseness matrix=%s', sum(sparseness) / K )
    return sparseness

def plot_matrix(model, fig):
    """
    Input: a reordered model matrix
    Output:
        graphic file 
    """
    logger.debug('plot the matrix')
    K,V = model.shape
    
    plt.figure(figsize=(48, 12))
#plt.imshow(model, cmap=cm.bone, extent=[0, V, 0, K], aspect = V/K/3 )
    plt.imshow(model, cmap=cm.bone, interpolation='nearest', aspect='auto')


    plt.colorbar()
#    plt.ylim((0, K))
    plt.savefig(fig)
    plt.show()

def load_model(topicFile):
    """
    input:
        .beta model file, log(p(w|k))
    output:
        p(w|k) 
    """
    topic = np.loadtxt(topicFile)

    k , v = topic.shape
    tA = np.exp(topic)
    #epsi = np.ones((k,v)) * (1e-12)
    epsi = 1e-12
    model = tA + epsi
    return model


def calc_dir(modelDir, ext = '.beta'):
    """
    Calculate the sparseness change/decrease on iterations
    input:
        .beta files   xxx-###.beta
    output:
        .sparseness   matrix<iternum, sparseness>

    """
    # cache file
    cacheFile = modelDir + '.sparseness'
    if os.path.exists(cacheFile):
        logger.info('Cache file found at %s, loading sparseness', cacheFile)
        sparseness = np.loadtxt(cacheFile)
        return sparseness

    models = []
    for dirpath, dnames, fnames in os.walk(modelDir):
        for f in fnames:
            if f.endswith(ext):
                m = re.search('.*-([0-9]*)' + ext, f)
                if m:
                    iternum = int(m.group(1))

                    logger.info('load model from %s as iternum = %d', f, iternum)
                    model = load_model(os.path.join(dirpath, f))

                    models.append((iternum, model))

    models =  sorted(models, key = lambda modeltp : modeltp[0])
    if len(models) < 2:
        logger.error('ERROR: load too few model files')
        return None

    logger.debug('models iternum as %s', [s[0] for s in models])
    sparseness = np.zeros((len(models), 2))

    K, V = models[0][1].shape
    for idx in range( len(models) ):
        sp = calc_sparseness(models[idx][1])

        sparseness[idx][0] = models[idx][0]
        sparseness[idx][1] = sum(sp) / K
 
    # save result
    np.savetxt(cacheFile, sparseness)

    return sparseness

if __name__ == '__main__':
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
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    cmd = sys.argv[1]
    filename = sys.argv[2]

    if cmd == '-file':
        model = load_model(filename)
        sparse = calc_sparseness(model)
    elif cmd == '-dir':
        sparseness = calc_dir(filename)
    elif cmd == '-draw':
        model = load_model(filename)
        plot_matrix(model, filename + '-model.png')
    else:
        print(globals()['__doc__'] % locals())
        sys.exit(1)



    
