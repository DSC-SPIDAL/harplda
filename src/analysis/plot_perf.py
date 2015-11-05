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
    * accuracy_runtime     ;perplexity .vs. clock time
    * accuracy_iter     ;perlexity .cs. iternumber
    * overhead          ;overhead=itertime-computetime, overhead comparision between two result
    * comm_breakdown    ; time breakdown on communication and commputation time


Usage: 
    * draw figures on plotname
    plot_perf <plot name> <datadir> <name file> <fig name> <title>
    
    * make namefile
    plot_perf namefile <workfile> <namefile> <features>

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
                logger.error('%s not found under %s, quit...', name, self.datadir)
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
    def __init__(self, namefile = ''):
        """
        read from namefile
        format:
        datafile    label   groupname

        """
        perfname = []

        if namefile:
            with open(namefile, 'r') as nf:
                content = nf.read()
                deli = '\t'
                if not content.find(deli) > 0:
                    deli = ' '
                nf.seek(0,0)

                for line in nf:
                    tokens = line.strip().split(deli)
                    #perfname.append((tokens[0], tokens[1]))
                    perfname.append(tokens)

        self.perfname = perfname
        self.worklist = None
        self._pos = -1

    def load_worklist(self, workfile):
        """
        workfile is a text file of features meta data for experiments
        format:
        name    trainer cluster dataset network sampler iternum

        """
        worklist = np.loadtxt(workfile, dtype=np.object)
        row, col = worklist.shape
        if col != 7:
            logger.error('worklist file format error, assert(col==7), fiel=%s, col=%s', workfile, col)
            return 
        
        logger.info('worklist file =%s, row =%s, col= %s', workfile, row, col)
        self.worklist = worklist

    def make_namefile(self, namefile, features):
        """
        search names by features, and output to namefile
        features is a tuple:
            (cluster, dataset, network, sampler)
            value 0 means *

        return: matched <name, trainer> pairs
        """
        if self.worklist == None:
            return 
    
        logger.info('start make namefile from features=%s', features)
        row, col = self.worklist.shape
        result = []
        for idx in range(row):
            if features[0] != '0' and features[0] != self.worklist[idx][2]:
                continue

            if features[1] != '0' and features[1] != self.worklist[idx][3]:
                continue

            if features[2] != '0' and features[2] != self.worklist[idx][4]:
               continue

            if features[3] != '0' and features[3] != self.worklist[idx][5]:
               continue

            #ok, match one
            result.append((self.worklist[idx][0], self.worklist[idx][1]))

        logger.info('%d match records found', len(result))
        # save result
        if len(result) > 0:
            with open(namefile, 'w') as nf:
                for tp in result:
                    nf.write("%s %s\n"%(tp[0],tp[1]))


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
            "accuracy_overalltime":self.plot_accuracy_overalltime,
            "overhead":self.plot_overhead,
            "comm_breakdown":self.plot_comm_breakdown
        }

        # init default subplot
        self.init_subplot(1,1)
        self.set_subplot(1,1)

        self.colors=['m', 'r','b','g','c','k','y']

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
        elif x == 1 or y == 1:
            self.axtype = 2
        else:
            self.axtype = 3

    def set_subplot(self, x, y):
        if self.axtype == 1:
            self.curax = self.ax
        elif self.axtype == 2:
            x = max(x, y)
            self.curax = self.ax[x-1]
        else:
            self.curax = self.ax[x-1,y-1]
   
        logger.info('set_subplot curax = %s', self.curax)

    def savefig(self, figname):
        plt.savefig(figname)


    def autolabel(self, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            self.curax.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%d'%int(height),
                ha='center', va='bottom')


    ######################3
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
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            fname = name + '.runtime-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist)

        overall_time = []

        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            gname = tp[2]
 
            fname = name + '.runtime-stat'
            # get max apptime
            overall_time.append((self.perfdata[fname][1,plottype], label, gname))
    
        #
        # data is two group, one in ib, other in eth
        #
        

        # draw a bar charta
        N = 2
        #ind = np.arange(N)  # the x locations for the groups
        ind = np.array([0,0.3])
        width = 0.05       # the width of the bars

        #fig, ax = plt.subplots()

        # perf configure file format
        # datafile  label   groupname
        #grp_size = len(overall_time)/2
        groupname = []
        for id in range(len(overall_time)):
            if not overall_time[id][2] in groupname:
                groupname.append( overall_time[id][2] )

        grp_size = len(groupname)
        rects = []
        for idx in range(grp_size):
            logger.info('val=%d, label=%s', overall_time[idx][0], overall_time[idx][1])
            grp_data = ( overall_time[idx][0], overall_time[idx+grp_size][0] )
            logger.info('val = %s, label=%s', grp_data, overall_time[idx][1])
            # ax.bar(ind + width*idx, overall_time[idx][0], width, label = overall_time[idx][1])
            rects.append(self.curax.bar(ind + width*idx, grp_data, width, color=self.colors[idx], label = overall_time[idx][1]))

        self.curax.set_ylabel('runtime (s)')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Overall Performance of LDA Trainers')
        self.curax.set_xticks(ind+width)
        #self.curax.set_xticklabels( ('ib', 'eth') )
        self.curax.set_xticklabels( groupname )


        for rect in rects:
            self.autolabel(rect)

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

    def plot_accuracy_overalltime(self, figname, conf):
        return self.plot_accuracy(2, figname, conf)


    def plot_accuracy(self, plottype, figname, conf):
        """
        get accuracy from .likelihood, and itertime from .runtime[3:]

        plottype:
            0   accuracy .vs. iternum
            1   accuracy .vs. traintime
            2   accuracy .vs. excution time
        """
        dataflist = []
        #for name,label in self.perfname:
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            fname = name + '.likelihood'
            dataflist.append(fname)
            fname = name + '.runtime-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist)

        accuracy = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
 
            lh_name = name + '.likelihood'
            runtime_name = name + '.runtime-stat'
            #
            # get (iternum, runttime-mean, perplexity, label)
            # 
            #
            logger.debug('runtime_name=%s', runtime_name)
            # start overhead = apptime - traintime 
            if plottype == 2:
                # use overall time
                offset = self.perfdata[runtime_name][2,0] - self.perfdata[runtime_name][2,1] 
            else:
                offset = 0
            accuracy.append((self.perfdata[lh_name][:,0], 
                        self.perfdata[runtime_name][2,2:] + offset,
                        self.perfdata[lh_name][:,1], label))


        #fig, ax = plt.subplots()

        #grp_size = len(accuracy)/2
        # data is two group, one in ib, other in eth

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

            self.curax.plot(x, accuracy[idx][2], self.colors[idx]+'.-', label = accuracy[idx][3])

        #self.curax.set_ylabel('Model Perplexity')
        self.curax.set_ylabel('Model Likelihood')
        if plottype == 0:
            self.curax.set_xlabel('Iteration Number')
        elif plottype == 1:
            self.curax.set_xlabel('Training Time (s)')
        elif plottype == 2:
            self.curax.set_xlabel('Excution Time (s)')


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

    def plot_overhead(self, figname, conf):
        """
        get overhead value from .iter-stat and .comput-stat
        """
        dataflist = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            dataflist.append(name + '.iter-stat')
            dataflist.append(name + '.comput-stat')

        self.perfdata.load(dataflist)

        iter_time = []
        compute_time = []

        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            gname = tp[2]
 
            fname = name + '.iter-stat'
            # get max apptime
            iter_time.append((self.perfdata[fname], label, gname))
            fname = name + '.comput-stat'
            # get max apptime
            compute_time.append((self.perfdata[fname], label, gname))
    
        #
        # data is in groups
        #
        

        # draw a bar stacked
        #ind = np.arange(N)  # the x locations for the groups
        #ind = np.array([0,0.3])
        #width = 0.05       # the width of the bars

        #fig, ax = plt.subplots()

        # perf configure file format
        # datafile  label   groupname
        #grp_size = len(overall_time)/2
        groupname = []
        for id in range(len(iter_time)):
            if not iter_time[id][2] in groupname:
                groupname.append( iter_time[id][2] )

        grp_size = len(groupname)
        rects = []

        N = compute_time[0][0][2][:10].shape[0]
        logger.info('N=%s', N)
        ind = np.arange(N)
        width = 0.5       # the width of the bars

        for idx in range(grp_size):

            #grp_data = ( compute_time[idx][0], compute_time[idx+grp_size][0] )
            grp_data = compute_time[idx][0][2]
            grp_data_err = compute_time[idx][0][3]
            grp_data = grp_data[:10]
            grp_data_err = grp_data_err[:10]
            logger.info('grp_data = %s', grp_data)

            p1 = self.curax.bar(ind + width*idx, grp_data, width, color=self.colors[idx*2], yerr= grp_data_err, label = compute_time[idx][1] +'-compute')

            grp_data2 = iter_time[idx][0][2] - compute_time[idx][0][2]
            grp_data2_err = iter_time[idx][0][3] - compute_time[idx][0][3]
            grp_data2 = grp_data2[:10]
            grp_data2_err = grp_data2_err[:10]

            p2 = self.curax.bar(ind + width*idx, grp_data2, width, bottom = grp_data, color=self.colors[idx*2+1], yerr= grp_data2_err, label = compute_time[idx][1]+'-overhead')

            rects.append(p1)
            rects.append(p2)

            #logger.info('val = %s, label=%s', grp_data, compute_time[idx][1])
            # ax.bar(ind + width*idx, compute_time[idx][0], width, label = compute_time[idx][1])
            #rects.append(self.curax.bar(ind + width*idx, grp_data, width, color=self.colors[idx], label = compute_time[idx][1]))

        self.curax.set_ylabel('elapsed time (s)')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Overhead of LDA Trainers')
        self.curax.set_xticks(ind+width)
        #self.curax.set_xticklabels( ('ib', 'eth') )
        #self.curax.set_xticklabels( groupname )
        self.curax.set_xlabel('iteration')


        for rect in rects:
            self.autolabel(rect)

        #ax.set_ylim(0, overall_time[0][0] * 2)
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        if figname:
            plt.savefig(figname)

        #plt.show()

    def plot_comm_breakdown(self, figname, conf):
        """
        get comm and compute value from .comm-stat and .comput-stat

        """
        dataflist = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            dataflist.append(name + '.comm-stat')
            dataflist.append(name + '.comput-stat')

        self.perfdata.load(dataflist)

        comm_time = []
        compute_time = []

        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            gname = tp[1]
 
            fname = name + '.comm-stat'
            # get max apptime
            comm_time.append((self.perfdata[fname]/1000, label, gname))
            fname = name + '.comput-stat'
            # get max apptime
            compute_time.append((self.perfdata[fname]/1000, label, gname))
    
        #
        # data is in groups
        #
        

        # draw a bar stacked
        groupname = []
        for id in range(len(comm_time)):
            if not comm_time[id][2] in groupname:
                groupname.append( comm_time[id][2] )

        grp_size = len(groupname)
        rects = []

        N = compute_time[0][0][2][:10].shape[0]
        logger.info('N=%s', N)
        ind = np.arange(N)
        width = 0.45       # the width of the bars

        for idx in range(grp_size):

            #grp_data = ( compute_time[idx][0], compute_time[idx+grp_size][0] )
            # get mean , std
            grp_data = compute_time[idx][0][2]
            grp_data_err = compute_time[idx][0][3]
            grp_data = grp_data[:10]
            grp_data_err = grp_data_err[:10]
            logger.info('grp_data = %s', grp_data)

            p1 = self.curax.bar(ind + width*idx, grp_data, width, color=self.colors[idx*2], yerr= grp_data_err, label = compute_time[idx][1] +'-compute')

            grp_data2 = comm_time[idx][0][2]
            grp_data2_err = comm_time[idx][0][3]
            grp_data2 = grp_data2[:10]
            grp_data2_err = grp_data2_err[:10]

            p2 = self.curax.bar(ind + width*idx, grp_data2, width, bottom = grp_data, color=self.colors[idx*2+1], yerr= grp_data2_err, label = compute_time[idx][1]+'-comm')

            rects.append(p1)
            rects.append(p2)

            #logger.info('val = %s, label=%s', grp_data, compute_time[idx][1])
            # ax.bar(ind + width*idx, compute_time[idx][0], width, label = compute_time[idx][1])
            #rects.append(self.curax.bar(ind + width*idx, grp_data, width, color=self.colors[idx], label = compute_time[idx][1]))

        self.curax.set_ylabel('elapsed time (s)')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Communication and Computation time breakdown of LDA Trainers')
        self.curax.set_xticks(ind+width)
        self.curax.set_xticklabels([x+1 for x in range(N)])
        #self.curax.set_xticklabels( ('ib', 'eth') )
        #self.curax.set_xticklabels( groupname )
        self.curax.set_xlabel('iteration')


        #for rect in rects:
        #    self.autolabel(rect)

        #ax.set_ylim(0, overall_time[0][0] * 2)
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        if figname:
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
    
    if plotname == 'namefile':
        #make_namefile(sys.argv)
        workfile = sys.argv[2]
        namefile = sys.argv[3]
        features=[0,0,0,0]
        if len(sys.argv) > 4:
            cluster = sys.argv[4]
            features[0] = cluster
        if len(sys.argv) > 5:
            dataset = sys.argv[5]
            features[1] = dataset
        if len(sys.argv) > 6:
            network = sys.argv[6]
            features[2] = network
        if len(sys.argv) > 7:
            sampler = sys.argv[7]
            features[3] = sampler

        perfname = PerfName()
        perfname.load_worklist(workfile)
        perfname.make_namefile(namefile, features)

    else:
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

