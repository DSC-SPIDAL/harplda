#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Analysis the converge property of the lda inference algorithm.

Is there any differences between words with high frequency and low in their 
speed of convergence?

input:
    saved phi word-topic count matrixes every M iteration. (M = 50 by default)
    word id sorted descendently already, start from 0 for the word with highest freqency.
    a dictionary file, with <wordid word frequency> information inside

analysis:
    sample L words evenly according to their power law frequency distribution. (L= 100)
    generate word-iteration# distance matrix
    draw a heat map to visualize the distance matrix

Usage:
    analysis_converge <model dir> <dictfile> <sample_size=100> 

"""

import sys, os, math,re
import numpy as np
from scipy import stats
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib import cm
import logging

logger = logging.getLogger(__name__)

#global constant
SAMPLETYPE_EVEN = 1
SAMPLETYPE_RANDOM = 2
MODELTYPE_GIBBS = 'gibbs'
MODELTYPE_BLEI = 'blei'
MODELTYPE_RAW = 'raw'


class Dictionary():
    """
        lda input data format
        dictfile: "id\tword\tfreq\n" each line

    """
    dictfile = ''
    # freqmap := <k = freq> <v = id list>
    freqmap = {}
    freqlist = []
    minfreq, maxfreq = 0, 0

    #
    wordmap = {}

    def __init__(self, dictfile=''):
        self.dictfile = dictfile
        pass

    def load_by_freq(self, dictfile=''):
        """
        load the dictionary as a freq map
        """
        if dictfile:
            self.dictfile = dictfile
        self.freqmap = {}
        with open(self.dictfile, 'r') as df:
            for line in df:
                tokens = line.strip().split('\t')
                #wordids format: id, word,freq  
                #by gensim make_wiki.py
                freq = int(tokens[2])
                id = int(tokens[0])
                if freq in self.freqmap.keys():
                    self.freqmap[freq].append(id)
                else:
                    self.freqmap[freq] = [id]

        self.freqlist = sorted(self.freqmap.keys())
        logger.debug('freqlist = %s', self.freqlist[:10])
        self.minfreq = min(self.freqlist)
        self.maxfreq = max(self.freqlist)

        logger.info('load_by_freq: %s, minfreq = %d, maxfreq = %d', self.dictfile, self.minfreq, self.maxfreq)


    def _try_sample(self, id_samples, freq_samples, idx):
        """
        try draw a sample from idx, and which is not in samples

        return:
            False, not found 
            True, yes found and added to samples
        """
        freq = self.freqlist[idx]
        idlist = self.freqmap[freq]
        
        candidate = idlist[np.random.randint(len(idlist), size = 1)[0]]
        if candidate in id_samples:
            # check if the sample already in the id_samples list, if yes then try it's neighbour
            if len(idlist) == 1:
                return False

            # first, try in the same freq
            maxTryCnt = len(idlist) * 2
            tryCnt = 0
            while tryCnt < maxTryCnt:
                candidate = idlist[np.random.randint(len(idlist), size = 1)[0]]

                if candidate in id_samples:
                    tryCnt += 1
                else:
                    break
            if tryCnt >= maxTryCnt:
                return False

        # found in the same freq
        id_samples.append(candidate)
        freq_samples.append(freq)
        return True

    def sampling(self, sample_size, sample_type = SAMPLETYPE_RANDOM):
        """
        sampling words by their frequency

        input:
            dictfile: "id\tword\tfreq\n" each line

        method:
            sampling evenly in [log(minfreq), log(maxfreq)] 
            or
            sampling randomly in [log(minfreq), log(maxfreq)]

        return:
            sampled word list

        """
        #uniform random sampling on log scale freq
        freqsamples = np.random.uniform(math.log(self.minfreq), math.log(self.maxfreq), sample_size)
        logger.info('uniform samples as %s', freqsamples[:min(20,sample_size)])

        #search for sampled freqs
        source = np.sort(freqsamples)
        target = np.log(np.array(self.freqlist))
        freq_samples_idx = []
        i, j = 0, 0
        while i < source.shape[0]:
            if source[i] > target[j]:
                j += 1
            else:
                freq_samples_idx.append(j)
                i += 1

        # sort the samples freq
        #freq_samples = sorted(freq_samples)
        logger.info('draw samples freq as %s', [self.freqlist[idx] for idx in freq_samples_idx[:min(20, sample_size)]] )

        #sample the words for each freq
        id_samples = []
        freq_samples = []
        for idx in freq_samples_idx:
            foundflag = self._try_sample(id_samples, freq_samples, idx)
            
            neighbour = idx
            while foundflag == False:
                # second, try it's neighbours
                neighbour -= 1
                if neighbour < 10:
                    logger.error('ERROR: sampling failure, it can not draw samples even in low freq range(freq<=10)')
                    return [], []

                foundflag = self._try_sample(id_samples, freq_samples, neighbour)

        logger.info('draw id samples as %s', id_samples[:min(20, sample_size)])
        return id_samples, freq_samples


def load_models(modelDir, modeltype = MODELTYPE_RAW):
    """
    phi file name:
        prefix_#iter#.phi

    return:
        list of (iternum, model)
        model is a word-topic count matrix

    """
    models = []
    for dirpath, dnames, fnames in os.walk(modelDir):
        for f in fnames:
            if f.endswith(".phi"):
                m = re.search('.*-([0-9]*).phi', f)
                if m:
                    iternum = int(m.group(1))
                    # TODO, assume the id order here
                    modeldata = np.loadtxt(os.path.join(dirpath, f))
                    if modeltype != MODELTYPE_RAW:
                        # transpose K*V matrix to V*K
                        modeldata = np.transpose(modeldata)

                    models.append((iternum, modeldata))
                    logger.info('load model from %s as iternum = %d', f, iternum)
    
    models =  sorted(models, key = lambda modeltp : modeltp[0])
    logger.debug('models iternum as %s', [s[0] for s in models])

    return models

def calc_distance(models, sample_ids, modeltype = MODELTYPE_RAW):
    """
    calculate the distance matrix for each samples

    return:
        distance_matrix: sample_ids * iternum KL distance

    """
    M = len(sample_ids)
    N = len (models)
    distance_matrix = np.zeros((M,N))

    logger.debug('calculate the distance matrix, shape =(%d, %d) ', M, N)
    for i in range(M):
        endDist = models[N -1][1][sample_ids[i]]
        if modeltype == MODELTYPE_RAW:
            endDist = endDist / (1.0 * sum(endDist))
        elif modeltype == MODELTYPE_BLEI:
            k, v = endDist.shape
            endDist = np.exp(endDist) + np.ones((k,v)) * (1e-12)  


        for j in range(N):
            curDist = models[j][1][sample_ids[i]]
            if modeltype == MODELTYPE_RAW:
                curDist = curDist / (1.0 * sum(curDist))
            elif modeltype == MODELTYPE_BLEI:
                k, v = endDist.shape
                curDist = np.exp(curDist) + np.ones((k,v)) * (1e-12)  


            distance_matrix[i, j] = stats.entropy(curDist, endDist)*0.5 + \
                                    stats.entropy(endDist, curDist)*0.5

    logger.debug('End of calculate, distance matrix=%s', distance_matrix)        
    return distance_matrix


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


def run_word_sampling(dictfile, sample_size, sample_type = SAMPLETYPE_EVEN):
    dt = Dictionary()
    dt.load_by_freq(dictfile)
    id_samples = dt.sampling(sample_size)

    return id_samples

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

    modelDir = sys.argv[1]
    dictfile = sys.argv[2]
    sample_size = 100
    if len(sys.argv) > 3:
        sample_size = int(sys.argv[3])

    id_samples, freq_samples = run_word_sampling(dictfile, sample_size)
    np.savetxt(modelDir + '.ids', np.array(id_samples), fmt='%d')
    np.savetxt(modelDir + '.freqs', np.array(freq_samples), fmt='%d')

    models = load_models(modelDir,modeltype = 'gibbs')

    distance_matrix = calc_distance(models, id_samples, modeltype = 'gibbs')
    np.savetxt(modelDir + '.distance', distance_matrix)

    plot_matrix(distance_matrix, 'converge_map.png')

