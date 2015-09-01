#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
measure the performance of lda trainer
analysis the log file

input:
    lda trainer's log file
format:
    mallet  ^[0-9]+ms
    ylda    
    harp    


Usage: 
    analy_timelog <trainer> <logfile> <figname>

"""

import sys,os,re
import numpy as np
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class LDATrainerLog():
    name =''
    pattern={
        "mallet":"^([0-9]+)ms",
        "harp":"*Iter"
    }

    def __init__(self,name):
        if name not in self.pattern:
            raise NameError('no %s trainer support yet, quit.'%name)
        self.name = name

    def load_timelog(self, logfile):
        """
        load elapsed millis of each iteration from logfile
    
        return:
            nparray
        """
        logf = open(logfile,'r')
        elapsed=[]
        for line in logf:
            m = re.search(self.pattern[self.name], line)
            if m:
                elapsed.append(int(m.group(1)))
    
        return elapsed


def draw_time(elapsed, trainer, fig, show = False):
    logger.debug('plot the elapsed time fig')

    x = np.arange(1, len(elapsed) + 1 )
    y = np.array(elapsed)
    plt.title('Performance of LDA Trainers')
    plt.xlabel('Iteration Number')
    plt.ylabel('Elapsed Millis')
    #plt.plot(x, y, 'b.-', label=modelname+' likelihood' )
    plt.plot(x, y, 'c.-', label=trainer )
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
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # check the path
    trainer = sys.argv[1]
    logfile = sys.argv[2]
    figname = 'runtime.png'
    if len(sys.argv) > 3:
        figname = sys.argv[3]

    logAnalizer = LDATrainerLog(trainer)
    
    draw_time(logAnalizer.load_timelog(logfile), trainer, figname)



