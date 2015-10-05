#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A general plot tool.

input:
    datafile:
        x y

    configure file:
        title:
        xlabel:
        ylabel:
        ...

Usage:
    plot <config> <figfile> <datafiles...>

"""

import sys, os, math,re
import numpy as np
import logging
try:
    import matplotlib.pyplot as plt
except:
    import matplotlib

logger = logging.getLogger(__name__)

def load_data(dir, pattern):
    """
    input:
        dir : model files inside are <wordid, topicCnt....>
        or
        modelfile

    return:
        model is a word-topic count matrix
    """
    datalist=[]
    
    logger.debug('load data files from %s with pattern = %s', dir, pattern)
    if os.path.isdir(dir):
        for dirpath, dnames, fnames in os.walk(dir):
            for f in fnames:
                if re.match(pattern,f):

                    logger.info('load data from %s ', f)
                    model = np.loadtxt(os.path.join(dirpath, f))
                    
                    # sort the matrix by the first column            
                    model = model[model[:,0].argsort()]

                    logger.debug('model = %s', model)

                    datalist.append((f, model))

    # try to sort
    datalist = sorted(datalist, key = lambda x :x[0])

    logger.info('load %d data files', len(datalist))

    return datalist

def load_config(configfile):
    """ 
    Configure file
    title : .....


    """
    basicname = ['title', 'xlable','ylabel']

    config = {}
    conf = open(configfile, 'r')
    for line in conf:
        tokens = line.strip().split(':')
        config[tokens[0]] = tokens[1]

    for name in basicname:
        if name not in config:
            config[name] = name

    return config

def print_stat(y, name):
    # basic statistics
    mean = int(np.mean(y))
    mod = np.sort(y)
    #logger.debug('mod=%s...%s', mod[:10], mod[-10:])
    mod = mod[y.shape[0]/2]
    logger.info('%s : mean= %d, mod = %d', name, mean, mod)

def plot(datalist, config, fig):

        plt.title(config['title'])
        plt.xlabel(config['xlabel'])
        plt.ylabel(config['ylabel'])

        ax = plt.subplot(111)

        for data in datalist:
            x = data[1][:,0]
            y = data[1][:,1]
            if 'xlog' in config:
                ax.set_xscale("log", nonposx='clip')

            if 'ylog' in config:
                ax.set_yscale("log", nonposy='clip')

            #plt.plot(data[1][:,0], data[1][:,1], label=data[0])
            plt.plot(x, y, label=data[0])

            print_stat(y, data[0]+'@0')
            print_stat(y[:3000], data[0] +'@3000')
            print_stat(y[:10000:], data[0] + '@10000')


        if 'loc' in config:
            loc = int(config['loc'])
        else:
            loc = 1

        plt.legend(loc = loc)
        plt.savefig(fig)
        plt.show()

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 5:
        print(globals()['__doc__'] % locals())
        sys.exit(1)


    configfile = sys.argv[1]
    figfile = sys.argv[2]
    dirname = sys.argv[3]
    datafile = sys.argv[4]

    config = load_config(configfile)

    model = load_data(dirname, datafile)

    plot(model, config, figfile)
