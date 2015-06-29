#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Validate the sparseness property in the topic model outputed by lda.
Each model is a V*K matrix with every element a log probability

prob(v=k | model) = (C(v,k) + beta ) /(sigma(C(v,k) + V*beta)
minval = argmin(model[k]) = 1/V

So, the sparseness can be represented by:
1. ratio of prob > minval
2. heat map

Output the sparseness map

"""

import sys, os
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
    minval = 1/V + 1e-12

    logger.debug('calculate the sparseness, shape =(%d, %d) ', K, V)
    for i in range(K):
        sparseness[i] = np.where(model[i] > minval)[0].shape[0] * 1.0 / V

    logger.debug('End of calculate, sparseness matrix=%s', sparseness)        
    return sparseness


def match_topics(distance_matrix):
    """
    return : 
        a list of index holding the indexes most match

    """
    if topicA.shape != topicB.shape:
        logger.error('topicA has different shape with topicB', topicA.shape, topicB.shape)
        return None
    
    copy = distance_matrix.copy()
    K,V = topicA.shape

    logger.debug('greedy search for most similar topics')
    match_ids = [] 
    for i in range(K):
        # search for the most similar
        idx = np.argmin(copy)
        row, col = idx/K, idx % K

        match_ids.append((row, col))

        copy[row].fill(10)
        copy[:,col].fill(10)
        
#        logger.debug('argmin found at row=%d, col=%d, fill copy matrix is:\n%s', row, col, copy)

    logger.debug('End of match, match_ids = %s', match_ids)
    return match_ids

def reorder_matrix(distance_matrix, match_ids):
    """
    Reorder the distance matrix, swap the rows according to the match_ids
    return a new reordered matrix
    """
    reorder_matrix = np.zeros(distance_matrix.shape)
    r_m = np.zeros(distance_matrix.shape)
    KA, KB = distance_matrix.shape
    for idx in range(KA):
        #reorder_matrix[match_ids[idx][1]]  = distance_matrix[match_ids[idx][0]]
        # match_ids[idx][0] --> idx row, [1] --> idx col
        r_m[idx] = distance_matrix[match_ids[idx][0]]
    for idx in range(KA):
        reorder_matrix[:, idx] = r_m[:, match_ids[idx][1]]

    logger.debug('End of reorder')
    return reorder_matrix

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
    topic = np.loadtxt(topicFile)

    k , v = topic.shape
    tA = np.exp(topic)
    epsi = np.ones((k,v)) * (1e-12)
    model = tA + epsi
    return model

if __name__ == '__main__':
    # logging configure
    import logging.config
    logging.basicConfig(filename='debug_testsparseness.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    if len(sys.argv) != 2:
        print "Usage: test_sparseness <model file>"
        sys.exit(0)

    model = load_model(sys.argv[1])

    sparse = calc_sparseness(model)
    
    plot_matrix(model, 'model.png')
