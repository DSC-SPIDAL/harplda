#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Analysis the relationship between topic distribution between 
concentrate parameters alpha, beta and topic count K.

Generate a LDA z samples from input alpha and K
Gather statistics on the z samples, calculate the topicCount/K 
ratio for each document. 
Draw the error bar graph comparing the relationships.

output:
    

Usage:
    concentrate_param  <alpha> <K>

"""

import sys, os
import math
import numpy as np
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

class TopicModel():
    alpha = 1.0
    beta = 0.1
    K = 20
    V = 100
    phi = None

    def __init__(self, V, K = 20, alpha = 1.0 , beta = 0.1):
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.V = V

        self.phi = None

    def __str__(self):
        return 'Topic Model: VocabSize = %d, Topic Count K = %d, alpha = %f, beta = %f.'% \
                (self.V, self.K, self.alpha, self.beta) 

    def loadFromBleiModelFile(self, modelFile):
        """
        Load phi matrix from blei's lda output .beta and .other file
        .beta 
            Each line is a topic; in line k, each entry is log p(w | z=k)
        .other 
            num_topics 20
            num_terms 21774
            alpha 2.5
        """
        betaFile = modelFile + '.beta'
        otherFile = modelFile + '.other'

        if os.path.exists(betaFile) and os.path.exists(otherFile):
            
            self.phi = np.loadtxt(betaFile)
            self.K, self.V = self.phi.shape
            logger.debug('k = %d, v = %d', self.K, self.V)

            with open(otherFile, 'r') as of:
                for line in of:
                    tokens = line.strip().split()
                    if tokens[0] == 'alpha':
                        self.alpha = float(tokens[1])

                of.close()
            return True

        else:
            logger.error('blei model not exists as %s, %s', betaFile, otherFile)
            return False

    def getTopicModelFromImage(self, imageFile):
        """
        Every image is a topic vector
        """
        im = Image.open(imageFile)
        r_value = []
        topic = []
        if im:
            pixels = im.load()
            for y in xrange(im.size[0]):
                for x in xrange(im.size[1]):
                    # get R plane only, it's symatric
                    r_value.append( pixels[x, y][0] )

            # normalize
            
            total = sum(r_value) * 1.0
            # logger.debug('sum=%f, r_value=%s', total, r_value)

            topic = [ math.log(1e-12 + val / total) for val in r_value]

            #im.close()

        return topic
    
    def sampling(self, doccnt , doclen_mu, doclen_sigmma, sampleFile='sample.txt'):
        """
        Sampling from given topic model.

        Return documents

        """
        sf = open(sampleFile, 'w')

        # draw \theta for D documents
        alpha = tuple([ self.alpha for i in range(self.K) ])
        theta = np.random.dirichlet(alpha, doccnt)
        logger.debug('theta = %s', theta)    

        # draw doclen according to Guassian for D documents
        doclen = np.random.normal(doclen_mu, doclen_sigmma, doccnt)
        logger.debug('doclen = %s', doclen)

        # prepare the phi
        # phi = [math.exp(v) - 1e-12 for v in self.phi[k] ]
        phi = np.exp(self.phi) -  1e-12

        # draw every words for the documents
        sf.write('%d\n'%doccnt)

        for i in xrange(doccnt):
            wordcnt = int(doclen[i])
            z = np.random.multinomial(wordcnt, theta[i])
            # logger.debug('z = %s', z)    
            
            for k in range(self.K):
                if z[k] == 0:
                    continue

                #phi = [math.exp(v) - 1e-12 for v in self.phi[k] ]
                #logger.debug('sum phi = %f, %s', sum(phi), phi)    
            
                w = np.random.multinomial(z[k], phi[k])
                #logger.debug('w = %s', w)    

                # write to output file

                for j in xrange(self.V):
                    if w[j] == 0:
                        continue
                    sf.write( ('%d '% j) * w[j])
            sf.write('\n')    

        sf.close()

    def sampling_z(self, doccnt , doclen_mu, doclen_sigmma, sampleFile=''):
        """
        Sampling from given topic model.

        Return documents

        """
        if sampleFile:
            sf = open(sampleFile, 'w')

        # draw \theta for D documents
        alpha = tuple([ self.alpha for i in range(self.K) ])
        theta = np.random.dirichlet(alpha, doccnt)
        logger.debug('theta = %s', theta)    

        # draw doclen according to Guassian for D documents
        doclen = np.random.normal(doclen_mu, doclen_sigmma, doccnt)
        logger.debug('doclen = %s', doclen)

        # prepare the phi
        # phi = [math.exp(v) - 1e-12 for v in self.phi[k] ]
        #phi = np.exp(self.phi) -  1e-12

        # draw every words for the documents
        if sampleFile:
            sf.write('%d\n'%doccnt)

        z_all = np.zeros((doccnt, self.K))
        for i in xrange(doccnt):
            wordcnt = int(doclen[i])
            z = np.random.multinomial(wordcnt, theta[i])
            # logger.debug('z = %s', z)    
            z_all[i] = np.transpose(z)

            if sampleFile:
                for k in range(self.K):
                    if z[k] == 0:
                        continue
                    sf.write( '%d:%d'%(k,z[k]) )
                sf.write('\n')    
        
        return z_all
#
# Test Case
#
def test_sample(doccnt = 500, doclen_mu = 300, doclen_sigmma = 10):
    #alpha_list = [2.5, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    #K_list = [100, 200, 500, 1000, 10000, 100000]

    alpha_list = [2.5, 1.0, 0.5, 0.1, 0.05, 0.01]
    K_list = [100, 200, 500, 1000, 10000]

    # mean, std every K
    z_alpha = np.zeros((len(K_list), len(alpha_list), 4))

    # cache file
    cacheFile = 'z_alpha-%d-%d'%(doccnt, doclen_mu) 
    if os.path.exists(cacheFile + '.npy'):
        logger.info('Cache file found at %s, loading z_alpha', cacheFile)
        z_alpha = np.load(cacheFile + '.npy')
    else:
        for i in range(len(K_list)):
            K = K_list[i]
            for j in range(len(alpha_list)):
                alpha = alpha_list[j]
                model = TopicModel(0,K, alpha, 0)
                logger.info('%s', model)

                # dynamic doclen when doclen_mu is 0
                doclen = doclen_mu
                if doclen_mu == 0:
                    doclen = K * 5
                z = model.sampling_z(doccnt, doclen, doclen_sigmma)

                # z is [doccnt, K]
                z_count = np.zeros((doccnt,1))
                for d in range(doccnt):
                    z_count[d] = np.count_nonzero(z[d])

                z_alpha[i,j,0] = np.mean(z_count)
                z_alpha[i,j,1] = np.std(z_count)
                z_alpha[i,j,2] = np.mean(z_count / K)
                z_alpha[i,j,3] = np.std(z_count / K)

        np.save(cacheFile, z_alpha)

    # draw error bar 
    # x = np.log2(np.array(K_list))
    x = alpha_list
    plt.subplot(2, 1,1)
    if doclen_mu == 0:
        plt.title('concentrate parameters(doccnt=%d,doclen=K*5)'%(doccnt))
    else:
        plt.title('concentrate parameters(doccnt=%d,doclen=%d)'%(doccnt, doclen_mu))
    plt.xlabel('alpha')
    plt.ylabel('topic count every document')
    for i in range(len(K_list)):
        plt.errorbar(x, z_alpha[i,:,0], yerr = z_alpha[i,:,1],label='K=' + str(K_list[i]))
    plt.legend()

    plt.subplot(2, 1,2)
    plt.xlabel('alpha')
    plt.ylabel('TopicCount/K Ratio')
    for i in range(len(K_list)):
        plt.errorbar(x, z_alpha[i,:,2], yerr = z_alpha[i,:,3],label='K=' + str(K_list[i]))
    plt.legend()

    plt.savefig('concentrate-%d-%d.png'%(doccnt, doclen_mu))
    plt.show()

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    #logging.basicConfig(filename='debug_calcdistance.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                    level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) >= 1:
        doccnt = 500
        doclen_mu = 300
        if len(sys.argv) == 3:
            doccnt = int(sys.argv[1])
            doclen_mu = int(sys.argv[2])

        #test_sample(alpha, K)
        test_sample(doccnt, doclen_mu)

    else:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

