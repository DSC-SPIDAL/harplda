#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Plot the performance firugres on performance data

input:
    trainer's performance data
    * likelihood
        .likelihood     ;   format as <iternum likelihood  perplexity>
    * timelog
        .computetime     ; computation time for each iteration
        .commtime        ; communication(synchronization) time for each iteration
        .runtime         ; running time, 
                   first two columns: app and train, 
                   the left are iternum columns: clock_time on each iteration
        .xxx-stat        ; 4 rows statistics of above files, min, max, mean, std

plotname:
    * overall_runtime    ;overall runtime
    * training_runtime   ;training runtime
    * accuracy_time     ;perplexity .vs. clock time
    * accuracy_iter     ;perlexity .cs. iternumber


Usage: 
    plot_perf <plot name> <datadir> <name file> <fig name> <title>


"""

import sys,os,re
import datetime
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class PlotConf():
    def __init__(self, configfile):
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

        self.config = config

    def __getitem__(self, name):
        if name in self.config:
            return self.config[name]
        else:
            return None

class PerfData():
    """
    Performance data loader

    {"name.ext" :  matrix}

    """
    data = {}
    support_exts = ['.likelihood', '.computetime', '.comput-stat', '.commtime', '.comm-stat', '.runtime', '.runtime-stat',
        '.itertime', '.iter-stat']

    def __init__(self, datadir):
        self.datadir = datadir

    def load(self, namelist):
        """
        Load data files with names in namelist
        """
        #self.data = {}
        for dirpath, dnames, fnames in os.walk(self.datadir):
            for f in fnames:
                #check .ext
                #basename = os.path.splitext(f)[0]
                if f in namelist:
                    if not f in self.data:
                        logger.debug('load data from %s', f)
                        matrix = np.loadtxt(dirpath + '/' + f)
                        self.data[f] = matrix

        #check all files ready?
        for name in namelist:
            if name not in self.data:
                logger.error('%s not found under %s, quit...', name, datadir)
                sys.exit(-1)

    def __getitem__(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

class PerfName():
    """
    This is a list of name pairs to determine the sequence of plots
    [(fname, label)]

    """
    def __init__(self, namefile):
        """
        read from namefile
        """
        perfname = []

        with open(namefile, 'r') as nf:
            for line in nf:
                tokens = line.strip().split('\t')
                perfname.append((tokens[0], tokens[1]))

        self.perfname = perfname
        self._pos = -1

    def __iter__(self):
        return self

    def next(self):
        self._pos += 1
        if self._pos == len(self.perfname):
            self._pos = -1
            raise StopIteration
        else:
            return self.perfname[self._pos]

class PlotEngine():

    def __init__(self):
        self.ploters = {
            "overall_runtime":self.plot_overall_app,
            "overall_traintime":self.plot_overall_train,
            "accuracy_iter":self.plot_accuracy_iter,
            "accuracy_runtime":self.plot_accuracy_runtime,
        }

        # init default subplot
        self.init_subplot(1,1)
        self.set_subplot(1,1)

    def init_data(self, datadir, perfname):
        """
        perfdata is PerfData object
        perfname is {"name":label} object
        """
        self.perfdata = PerfData(datadir)
        self.perfname = perfname

    def init_subplot(self,*args):
        """
        set up sub plot info

        """
        #f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
        self.fig, self.ax = plt.subplots(*args)
        logger.info('init_subplots as %s, axarr shape=%s', args, self.ax)
        #self.fig.set_size_inches(9.25*1.5, 5.25*1.5)

        x = args[0]
        y = args[1]
        if x == 1 and y == 1:
            self.axtype = 1
        elif y == 0:
            self.axtype = 2
        else:
            self.axtype = 3

    def set_subplot(self, x, y):
        if self.axtype == 1:
            self.curax = self.ax
        elif self.axtype == 2:
            self.curax = self.ax[x-1]
        else:
            self.curax = self.ax[x-1,y-1]
   
        logger.info('set_subplot curax = %s', self.curax)

    def savefig(self, figname):
        plt.savefig(figname)

    def plot(self, plotname, fig, conf):
        if plotname in self.ploters:
            return self.ploters[plotname](fig, conf)
        else:
            logger.error('plotname %s not support yet', plotname)

    def plot_overall_app(self, figname, conf):
        return self.plot_runtime_overall(0, figname, conf)

    def plot_overall_train(self, figname, conf):
        return self.plot_runtime_overall(1, figname, conf)

    def plot_runtime_overall(self, plottype, figname, conf):
        """
        get apptime max value from .runtime-stat

        plottype:
            0   apptime
            1   traintime
        """
        dataflist = []
        for name,label in self.perfname:
            fname = name + '.runtime-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist)

        overall_time = []
        for name,label in self.perfname:
            fname = name + '.runtime-stat'
            # get max apptime
            overall_time.append((self.perfdata[fname][1,plottype], label))
    
        #
        # data is two group, one in ib, other in eth
        #
        

        # draw a bar charta
        N = 2
        #ind = np.arange(N)  # the x locations for the groups
        ind = np.array([0,0.3])
        width = 0.05       # the width of the bars

        colors=['r','b','y','c']

        #fig, ax = plt.subplots()

        grp_size = len(overall_time)/2
        for idx in range(grp_size):
            logger.info('val=%d, label=%s', overall_time[idx][0], overall_time[idx][1])
            grp_data = ( overall_time[idx][0], overall_time[idx+grp_size][0] )
            logger.info('val = %s, label=%s', grp_data, overall_time[idx][1])
            # ax.bar(ind + width*idx, overall_time[idx][0], width, label = overall_time[idx][1])
            self.curax.bar(ind + width*idx, grp_data, width, color=colors[idx], label = overall_time[idx][1])

        self.curax.set_ylabel('runtime (ms)')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Overall Performance of LDA Trainers')
        self.curax.set_xticks(ind+width)
        self.curax.set_xticklabels( ('ib', 'eth') )

        #ax.set_ylim(0, overall_time[0][0] * 2)
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 4)
        if figname:
            plt.savefig(figname)

        #plt.show()


    #
    # accuracy plots
    #
    def plot_accuracy_iter(self, figname, conf):
        return self.plot_accuracy(0, figname, conf)

    def plot_accuracy_runtime(self, figname, conf):
        return self.plot_accuracy(1, figname, conf)

    def plot_accuracy(self, plottype, figname, conf):
        """
        get accuracy from .likelihood, and itertime from .runtime[3:]

        plottype:
            0   accuracy .vs. iternum
            1   accuracy .vs. traintime
        """
        dataflist = []
        for name,label in self.perfname:
            fname = name + '.likelihood'
            dataflist.append(fname)
            fname = name + '.runtime-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist)

        accuracy = []
        for name,label in self.perfname:
            lh_name = name + '.likelihood'
            runtime_name = name + '.runtime-stat'
            #
            # get (iternum, runttime-mean, perplexity, label)
            # 
            logger.debug('runtime_name=%s', runtime_name)
            accuracy.append((self.perfdata[lh_name][:,0], 
                        self.perfdata[runtime_name][2,2:],
                        self.perfdata[lh_name][:,1], label))

        colors=['r','b','y','c']

        #fig, ax = plt.subplots()

        #grp_size = len(accuracy)/2
        # data is two group, one in ib, other in eth
        colors = ['b','c','r','g','y']

        grp_size = len(accuracy)
        for idx in range(grp_size):
            if plottype == 0:
                x = accuracy[idx][0]
                self.curax.set_ylabel('iteration number')
            else:
                x = accuracy[idx][0]
                #convert iternum to runtime
                x_int = x.astype(int)
                x = accuracy[idx][1][x_int - 1 ]
                self.curax.set_ylabel('runtime (s)')

            self.curax.plot(x, accuracy[idx][2], colors[idx]+'.-', label = accuracy[idx][3])

        #self.curax.set_ylabel('Model Perplexity')
        self.curax.set_ylabel('Model Likelihood')
        if plottype == 0:
            self.curax.set_xlabel('Iteration Number')
        else:
            self.curax.set_xlabel('Training Time')

        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('LDA Trainer Accuracy')
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        
        if figname:
            #plt.savefig('full-'+figname)
            #self.curax.set_ylim(0, 350)
            #plt.savefig('tail-'+figname)
            plt.savefig(figname)

        #plt.show()


if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 5:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # check the path
    plotname = sys.argv[1]
    datadir = sys.argv[2]
    namefile = sys.argv[3]
    figname = sys.argv[4]

    #conffile = sys.argv[4]
    #conf = PlotConf(conffile).config
    conf = {}
    if len(sys.argv) > 5:
        conf['title'] = sys.argv[5]

    ploter = PlotEngine()
    perfname = PerfName(namefile)
    ploter.init_data(datadir, perfname)
    ploter.plot(plotname, figname, conf)

