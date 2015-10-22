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
    plot_perf <plot name> <datadir> <name file> <fig name>


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

    def __init__(self, datadir, perfname):
        """
        perfdata is PerfData object
        perfname is {"name":label} object
        """
        self.perfdata = PerfData(datadir)
        self.perfname = perfname
        self.ploters = {
            "overall_runtime":self.plot_overall_app,
            "overall_traintime":self.plot_overall_train
        }

    def plot(self, plotname, fig):
        if plotname in self.ploters:
            return self.ploters[plotname](fig)
        else:
            logger.error('plotname %s not support yet', plotname)

    def plot_overall_app(self, figname):
        return self.plot_runtime_overall(0, figname)

    def plot_overall_train(self, figname):
        return self.plot_runtime_overall(1, figname)

    def plot_runtime_overall(self, plottype, figname):
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
        fig, ax = plt.subplots()
        grp_size = len(overall_time)/2
        for idx in range(grp_size):
            logger.info('val=%d, label=%s', overall_time[idx][0], overall_time[idx][1])
            grp_data = ( overall_time[idx][0], overall_time[idx+grp_size][0] )
            logger.info('val = %s, label=%s', grp_data, overall_time[idx][1])
            # ax.bar(ind + width*idx, overall_time[idx][0], width, label = overall_time[idx][1])
            ax.bar(ind + width*idx, grp_data, width, color=colors[idx], label = overall_time[idx][1])

        ax.set_ylabel('runtime (ms)')
        ax.set_title('Overall Performance of LDA Trainers')
        ax.set_xticks(ind+width)
        ax.set_xticklabels( ('ib', 'eth') )

        ax.set_ylim(0, overall_time[0][0] * 2)
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        ax.legend()
        plt.savefig(figname)

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
    if len(sys.argv) < 5:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # check the path
    plotname = sys.argv[1]
    datadir = sys.argv[2]
    namefile = sys.argv[3]
    figname = sys.argv[4]

    perfname = PerfName(namefile)

    ploter = PlotEngine(datadir, perfname)

    ploter.plot(plotname, figname)



