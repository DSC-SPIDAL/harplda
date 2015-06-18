#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Calculate the distance matrix bwteen two topic model
Each model is a V*K matrix with every element a log probability

The topics are reorder as best as possible using a greedy algorithm

Output the distance map

"""

import sys, os
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib import cm
import logging

logger = logging.getLogger(__name__)

def calc_distancematrix(topicA, topicB):
    """
    Distance is KL-Distance of two probability distributions
    input:
        np.array, K*V matrix, each row is term distribution of a topic
    return:
        np.array, distance matrix
    """
    if topicA.shape != topicB.shape:
        logger.error('topicA has different shape with topicB', topicA.shape, topicB.shape)
        return None

    K,V = topicA.shape

    # check the sum of probability
#    for row in range(K):
#        logger.debug('topicA row %d sum=%f', row, sum(topicA[row]))
#        logger.debug('topicB row %d sum=%f', row, sum(topicB[row]))

    distance_matrix = np.zeros((K,K))

    logger.debug('calculate the distance matrix, shape =(%d, %d) ', K, V)
    for i in range(K):
        for j in range(i, K):
            distance_matrix[i, j] = stats.entropy(topicA[i], topicB[j])*0.5 + \
                                    stats.entropy(topicB[j], topicA[i])*0.5
            distance_matrix[j, i] = distance_matrix[i, j]

    logger.debug('End of calculate, distance matrix=%s', distance_matrix)        
    return distance_matrix


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

def plot_matrix(distance_matrix, fig):
    """
    Input: a reordered distance matrix
    Output:
        graphic file 
    """
    logger.debug('plot the matrix')

    plt.imshow(distance_matrix, cmap=cm.bone)
    plt.colorbar()
    plt.savefig(fig)
    plt.show()

if __name__ == '__main__':
    # logging configure
    import logging.config
    logging.basicConfig(filename='debug_calcdistance.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    if len(sys.argv) != 3:
        print "Usage: calc_distancematrix <topic model A> <topic model B>"
        sys.exit(0)

    topicA = np.loadtxt(sys.argv[1])
    topicB = np.loadtxt(sys.argv[2])

    k , v = topicA.shape
    tA = np.exp(topicA)
    tB = np.exp(topicB)
    epsi = np.ones((k,v)) * (1e-12)
    A = tA + epsi
    B = tB + epsi
#    id = np.argmin( A )
#    print id, id/v, id%v, topicA[id/v, id%v], A[id/v, id%v ]
#    id = np.argmin( B )
#    print id, id/v, id%v, topicB[id/v, id%v], B[id/v, id%v ]

    dm = calc_distancematrix(A, B)
    match = match_topics(dm)
    matrix = reorder_matrix(dm, match)

    plot_matrix(matrix, 'distancemap.png')

