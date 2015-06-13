#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Visualize topic models by image.
Every model is a K*V matrix, and is also an image.




"""

import sys, os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
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
        return 'Topic Model: VocabSize = %d, Topic Count K = %d, alpha = %f, beta = %f.\n'% \
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
            self.K, self.V = self.phi.shape()

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
            logger.debug('sum=%f, r_value=%s', total, r_value)

            topic = [ math.log(1e-6 + val / total) for val in r_value]

            #im.close()

        return topic
    
    def loadFromImageFiles(self, imageDir):
        """
        Load a topic model from .bmp files under the directory

        return: topic_cnt readed in

        """
        
        topic_cnt = 0
        topic_map = dict()
        topics = []
        topic_len = 0
        for f in os.listdir( imageDir):
            if f.endswith(".bmp"):
                topic = self.getTopicModelFromImage(f)
                
                if topic:
                    topic_map[topic_cnt] = f
                    topics.append(topic)
                    topic_cnt += 1

                    if topic_len != 0:
                        if topic_len != len(topic):
                            logger.error('topic length different error! topiclen=%d, f=%s, curlen=%d.', topic_len, f, len(topic))
                    else:
                        topic_len = len(topic)

        if topic_len:
            self.K = topic_cnt
            self.V = topic_len
            self.phi = np.array(topics)
            return topic_cnt

        return 0

    def saveToBetaFile(self, betaFile):
        pass

    def saveToImageFiles(self, imageDir):

        canvas_edge = int(math.sqrt(self.V))
        if canvas_edge * canvas_edge != self.V:
            logger.error('vocabulary size can not map to an square image, size=%d', self.V)
            return False

        canvas_rect = (canvas_edge, canvas_edge)
        template = Image.new('RGB', canvas_rect, 'black')

        for k in range(self.K):
            imageFile = imageDir + '/%d.bmp'%k

            # convert topic to 0-255 scale
            topic = [ math.exp(val) for val in self.phi[k]]
            max_val = max(topic)
            r_value = [ int(val/max_val * 255) for val in topic]

            cur_img = template.copy()
            pixels = cur_img.load()
            for y in xrange(cur_img.size[0]):
                for x in xrange(cur_img.size[1]):
                    val = r_value[y * cur_img.size[0] + x]
                    pixels[x, y] = (val, val, val)

            cur_img.save(imageFile)

    def similarity(self, other):
        """
        Calculate similarity between two models.
        Use KL distance or cos similarity.

        """
        


        pass

    def sampling(self, doccnt , doclen_mean, doclen_var):
        """
        Sampling from given topic model.

        Return documents

        """

        pass


class TopicModelImage():
    def createImagesByText(self, text, canvas_edge = 100):
        #canvas_edge = 100
        canvas_rect = (canvas_edge, canvas_edge)
        template = Image.new('RGB', canvas_rect, 'black')
        font = ImageFont.truetype('simhei.ttf', 90) # MicroSoft Ya Hei Bold
    
        i = 0
        for char in text:
            i = i + 1
            cur_img = template.copy()
            font_box = font.getsize(char)
            point = ((canvas_rect[0] - font_box[0]) / 2, (canvas_rect[1] - font_box[1]) / 2)
            point_adjusted = (point[0], point[1] - 8) # this line should be removed.
            draw =  ImageDraw.Draw(cur_img)
            draw.text(point_adjusted, char, font=font, fill='white')
            
    
            filename = char.encode('utf-8') + '.bmp'
            #filename = char.encode('utf-8') + '.bmp'
            cur_img.save(filename)
            print("The image has been saved as: {}".format(os.path.abspath(filename)))


if __name__ == '__main__':
    # logging configure
    import logging.config
    logging.basicConfig(filename='debug_generator.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)



    model = TopicModel(0)
    
    print 'load from blei model file: model-final'
    model.loadFromBleiModelFile('model-final')
    print model

    print 'load from images under directory img'
    model.loadFromImageFiles('img')
    print model

    print 'save model to images under new'
    model.saveToImageFiles('new')



