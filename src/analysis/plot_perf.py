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
    * accuracy_overalltime     ;perplexity .vs. clock app time
    * accuracy_runtime     ;perplexity .vs. clock training time
    * accuracy_iter     ;perlexity .cs. iternumber
    * overhead          ;(,_end,_all) overhead=itertime-computetime, overhead comparision between two result
    * comm_breakdown    ;(,_end,_all) time breakdown on communication and commputation time
    * iter              ;(,_end,_all) iter time 
    * network,freemem, cpu            ; system monitor logs, network in/out, memory, cpu utilization
    * model_zipf, _split;model size analysis, zipf and model split 



Usage: 
    * draw figures on plotname
    plot_perf <plot name> <datadir> <name file> <fig name> <title>
    
    * make namefile by features(0 means *)
    plot_perf namefile <workfile> <cluster> <dataset> <network> <sampler>

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

    def load(self, namelist, quit_on_fail=True):
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
                if quit_on_fail:
                    logger.error('%s not found under %s, quit...', name, self.datadir)
                    sys.exit(-1)
                else:
                    logger.error('%s not found under %s, .....', name, self.datadir)

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
                    if line.strip().replace(' ','') == '':
                        break
                    tokens = line.strip().split(deli)
                    #perfname.append((tokens[0], tokens[1]))
                    if tokens[0][0] == '#':
                        continue
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


class DataSampler():
    """
    sample from np.array data
    """
    def __init__(self):
        pass

    def sample_max(self, vector, span):
        """
        sample the point with max value from vector every span data points
        """
        cnt = vector.shape[0]
        logger.debug('sample_max on vector cnt =%d, span=%d,shape=%s', cnt, span, vector.shape)

        new_vec = np.zeros((cnt/span))
        idmax = cnt/span * span
        for idx in range(0, idmax , span):
            new_vec[idx/span] = np.max(vector[idx:idx+span])

        return new_vec

class PlotEngine():

    def __init__(self, use_shortest_x = True):
        self.ploters = {
            "converge_level":self.plot_converge_level,
            "overall_runtime":self.plot_overall_app,
            "overall_traintime":self.plot_overall_train,
            "accuracy_iter":self.plot_accuracy_iter,
            "accuracy_itertime":self.plot_accuracy_itertime,
            "accuracy_runtime":self.plot_accuracy_runtime,
            "accuracy_overalltime":self.plot_accuracy_overalltime,
            "loadbalance_runtime":self.plot_loadbalance_runtime,
            "throughput_runtime":self.plot_throughput_runtime,
            "accthroughput_runtime":self.plot_accthroughput_runtime,
            "scalability":self.plot_scalability,
            "overhead":self.plot_overhead_top,
            "overhead_end":self.plot_overhead_end,
            "overhead_all":self.plot_overhead_all,
            "comm_breakdown":self.plot_comm_breakdown_top,
            "comm_breakdown_end":self.plot_comm_breakdown_end,
            "comm_breakdown_all":self.plot_comm_breakdown_all,
            "comm_iter":self.plot_comm_iter,
            "iter_trend":self.plot_iter_trend_top,
            "iter_trend_end":self.plot_iter_trend_end,
            "iter_trend_all":self.plot_iter_trend_all,
            "network":self.plot_network,
            "freemem":self.plot_freemem,
            "cpu":self.plot_cpu,
            "model_zipf":self.plot_model_zipf,
            "model_split":self.plot_model_split
        }

        # init default subplot
        self.init_subplot(1,1)
        self.set_subplot(1,1)

        self.colors_orig=['r','b','g', 'm','c','y','k','r','b','m','g','c','y','k']
        self.colors_orig_shade=['#ff8080','#8080ff','#80ff80', 'm','c','y','k','r','b','m','g','c','y','k']
        #self.colors=[(name, hex) for name, hex in matplotlib.colors.cnames.iteritems()]
        #self.colors=[hex for name, hex in matplotlib.colors.cnames.iteritems()]
        self.colors_stackbar=['r','y','b','g', 'm','c','y','k','r','y','b','g','m','c','y','k']
        self.linestyle=['-','--','-.',':']
        self.marker=['.','o','^','s','*','3']
        #default setting
        self.colors = self.colors_orig
        self.lines = ['.-'] * 10
        self.lines2 = ['--'] * 10

        self.use_shortest_x = use_shortest_x

        self.dataset={
            'clueweb30':29911407874,
            'enwiki':1107903672
        }

    def getTrainsetSize(self,fname):
        for name in self.dataset.keys():
            if fname.find(name) > 0:
                return self.dataset[name]
        logger.error('getTrainsetSize(%s) failed', fname)
        return 0

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
        # plt.savefig(figname, dpi=300)
        self.fig.tight_layout()
        self.fig.savefig(figname)

    def autolabel(self, rects, realnum = False):
        """
        input:
            bar
        """
        for rect in rects:
            height = rect.get_height()
            self.curax.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%.1e'%float(height) if realnum==False else '%.0f'%float(height),
                        ha='center', va='bottom')

    def autolabel_stack(self, rects):
        """
        input:
            (bar1, bar2)
        """
        old_height = []
        for rect in rects[0]:
            height = rect.get_height()
            self.curax.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%d'%int(height),
                        ha='center', va='bottom')
            old_height.append(height)

        # stack the next one
        idx = 0
        for rect in rects[1]:
            height2 = rect.get_height()
            self.curax.text(rect.get_x()+rect.get_width()/2., 1.01*(old_height[idx]+height2), '%d'%int(height2),
                        ha='center', va='bottom')
            idx += 1
 
    ######################3
    def analysis(self, analy_type, data):
        """
            data := [(label, x,y) ] 
        """
        if analy_type == 'convergelevel':
            logger.info('Begin analysis %s', analy_type)
            
            #1. curve fit on the first line
        pass



    ######################
    def plot_converge_level(self, figname, conf):
        """
        .convege file input
            level traintime

        """
        dataflist = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            fname = name + '.converge'
            dataflist.append(fname)

        self.perfdata.load(dataflist)

        overall_time = []
        groupname = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            fname = name + '.converge'
            overall_time.append(self.perfdata[fname])
            groupname.append(label)

        grp_size = len(groupname)
        rects = []
        N = overall_time[0].shape[0]
        ind = np.arange(N) + 0.10
        width = 1. / grp_size - 0.20

        for idx in range(grp_size):
            #get trainingtime from <level, trainingtime>
            grp_data = overall_time[idx][:,1]
            logger.info('val = %s, label=%s', grp_data, groupname[idx])
            # ax.bar(ind + width*idx, overall_time[idx][0], width, label = overall_time[idx][1])
            rects.append(self.curax.bar(ind + width*idx, grp_data, width, color=self.colors[idx], label = groupname[idx]))

        if 'xlabel' in conf:
            self.curax.set_xlabel(conf['xlabel'])
        else:
            self.curax.set_xlabel('Model Log-Likelihood')
        self.curax.set_ylabel('Training Time (s)')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('LDA Trainer Convergence')
        self.curax.set_xticks(ind+width)
        #set xticklabel to levels
        if 'xticks' in conf:
            xticks = conf['xticks']
        else:
            xticks = ['%.2e'%x for x in overall_time[0][:,0]]
        self.curax.set_xticklabels( xticks)

        for rect in rects:
            self.autolabel(rect, realnum=True)

        if 'loc' in conf:
            self.curax.legend(loc = conf['loc'])
        else:
            self.curax.legend(loc = 2)
        if figname:
            self.savefig(figname)


    def plot_converge_levelEx(self, figname, figdata ):
        """
        input: figdata <label, name, time, ratio>

        """
        logger.info('figdata=%s, shape=%s', figdata, figdata.shape)
        labels = figdata[:,0]
        grp_size = len(figdata)
        rects = []
        N = len(figdata)
        ind = np.arange(N) + 0.10
        width = 1. / grp_size - 0.20

        for idx in range(grp_size):
            grp_data = figdata[:,2].astype(np.float)
            # ax.bar(ind + width*idx, overall_time[idx][0], width, label = overall_time[idx][1])
            rects.append(self.curax.bar(ind + width*idx, grp_data, width, color=self.colors[idx], label = labels))

        self.curax.set_ylabel('Training Time (s)')
        self.curax.set_title('LDA Trainer Convergence')
        self.curax.set_xticks(ind+width)
        #self.curax.set_xticklabels( ('ib', 'eth') )
        self.curax.set_xticklabels(labels)


        for rect in rects:
            self.autolabel(rect)

        self.curax.legend(loc = 4)
        if figname:
            self.savefig(figname)

    ######################
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

        # perf configure file format
        # datafile  label   groupname
        #grp_size = len(overall_time)/2
        groupname = []
        for id in range(len(overall_time)):
            if not overall_time[id][2] in groupname:
                groupname.append( overall_time[id][2] )

        grp_size = len(groupname)
        rects = []
        N = len(overall_time) / len(groupname)
        ind = np.arange(N) + 0.10
        width = 1. / grp_size - 0.20

        for idx in range(grp_size):
            logger.info('val=%d, label=%s', overall_time[idx][0], overall_time[idx][1])
            grp_data = ( overall_time[idx][0], overall_time[idx+grp_size][0] )
            logger.info('val = %s, label=%s', grp_data, overall_time[idx][1])
            # ax.bar(ind + width*idx, overall_time[idx][0], width, label = overall_time[idx][1])
            rects.append(self.curax.bar(ind + width*idx, grp_data, width, color=self.colors[idx], label = overall_time[idx][1]))

        self.curax.set_ylabel('Overall Execution Time (s)')
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
            self.savefig(figname)

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

    def plot_accuracy_itertime(self, figname, conf):
        return self.plot_accuracy(3, figname, conf)



    def plot_accuracy(self, plottype, figname, conf):
        """
        get accuracy from .likelihood, and itertime from .runtime[3:]

        plottype:
            0   accuracy .vs. iternum
            1   accuracy .vs. traintime
            2   accuracy .vs. execution time
            3   accuracy .vs. itertime
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
            fname = name + '.iter-stat'
            dataflist.append(fname)
            fname = name + '.update-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist, False)

        accuracy = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
 
            lh_name = name + '.likelihood'
            runtime_name = name + '.runtime-stat'
            itertime_name = name + '.iter-stat'
            update_name = name + '.update-stat'
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

            itertimeMat = np.cumsum(self.perfdata[itertime_name][2,:]) / 1000.

            # convert iteration index number into real iternumber
            iterIdx = self.perfdata[lh_name][:,0].astype(int) 
            if self.perfdata[update_name] is not None:
                realIterId = self.perfdata[update_name][5][iterIdx -1 ]
            else:
                realIterId = iterIdx

            accuracy.append((iterIdx -1, 
                        self.perfdata[runtime_name][2,2:] + offset,
                        self.perfdata[lh_name][:,1], label, itertimeMat,
                        realIterId))

        #fig, ax = plt.subplots()

        #grp_size = len(accuracy)/2
        # data is two group, one in ib, other in eth
        curveData = []

        # limit x to the shortest iternumber among the curves
        grp_size = len(accuracy)
        _draw_all_iters_ = True
        if _draw_all_iters_ == True:
            iternum = None
        else:
            iternum = 999999
            for idx in range(grp_size):
                _iternum = accuracy[idx][0].shape[0]
                iternum = min(iternum, _iternum)

        logger.info('shortest iternum = %s', iternum)


        #setup the line style and mark, colors, etc
        colors = self.colors
        lines = self.lines

        if 'lines' in conf:
            lines = conf['lines']
        if 'colors' in conf:
            colors = conf['colors']

        _trace_shortest_x = 1e+24
        for idx in range(grp_size):
            if plottype == 0:
                #x = accuracy[idx][5][:iternum]
                x = accuracy[idx][5][:iternum] * 29911407874

                #self.curax.plot(x, accuracy[idx][2], self.colors_orig[idx]+self.marker[idx]+'-', label = accuracy[idx][3])
#self.curax.plot(x, accuracy[idx][2][:iternum], colors[idx]+lines[idx], label = accuracy[idx][3][:iternum])
                self.curax.plot(x, accuracy[idx][2][:iternum], lines[idx], color=colors[idx], label = accuracy[idx][3][:iternum])

                # save the lines in this figure for stop critierion analysis
                #curveData.append( (accuracy[idx][3], x, accuracy[idx][2]) )

            elif plottype ==3:
                x = accuracy[idx][0][:iternum]

                #convert iternum to runtime
                x = accuracy[idx][4][x ]
#self.curax.plot(x, accuracy[idx][2][:iternum], colors[idx]+lines[idx], label = accuracy[idx][3][:iternum])
                self.curax.plot(x, accuracy[idx][2][:iternum], lines[idx], color=colors[idx],label = accuracy[idx][3][:iternum])
            else:
                x = accuracy[idx][0][:iternum]
                #convert iternum to runtime
                x = accuracy[idx][1][x]
#self.curax.plot(x, accuracy[idx][2][:iternum], colors[idx]+lines[idx], label = accuracy[idx][3][:iternum])
                self.curax.plot(x, accuracy[idx][2][:iternum], lines[idx], color=colors[idx], label = accuracy[idx][3][:iternum])

            # trace on the x
            logger.info('_trace_shortest_x = %s, x[-1]=%s', _trace_shortest_x, x[-1])
            _trace_shortest_x = min(_trace_shortest_x, x[-1])

        # set the x limit by _trace_shortest_x
        if self.use_shortest_x:
            self.curax.set_xlim(0, _trace_shortest_x)
        logger.info('_trace_shortest_x = %s', _trace_shortest_x)
        #add xlim and ylim by conf
        if 'xlim' in conf:
            if _trace_shortest_x >0 and _trace_shortest_x > conf['xlim']:
                self.curax.set_xlim(0, conf['xlim'])
        if 'ylim_h' in conf:
            self.curax.set_ylim(conf['ylim_l'], conf['ylim_h'])



        #self.curax.set_ylabel('Model Perplexity')
        self.curax.set_ylabel('Model Log-likelihood')
        if plottype == 0:
            #self.curax.set_xlabel('Epoch Number')
            self.curax.set_xlabel('Model Update Count')
        elif plottype == 1:
            self.curax.set_xlabel('Training Time (s)')
        elif plottype == 2:
            self.curax.set_xlabel('Execution Time (s)')
        elif plottype ==3:
            #self.curax.set_xlabel('Iteration Time (s)')
            self.curax.set_xlabel('Training Time (s)')


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
            self.savefig(figname)

        #curveData for convergelevel analysis
        #self.analysis('convergelevel', curveData)

    ###############################################

    def plot_overhead_top(self, figname, conf):
        return self.plot_overhead(0, figname, conf)

    def plot_overhead_end(self, figname, conf):
        return self.plot_overhead(1, figname, conf)

    def plot_overhead_all(self, figname, conf):
        return self.plot_overhead(2, figname, conf)

    def plot_overhead(self, plottype, figname, conf):
        """
        get overhead value from .iter-stat and .comput-stat
        plottype:
            0   ; top 10 iters in barchart
            1   ; tail 10 iters in barchart
            2   ; plot all in line

        """
        dataflist = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            dataflist.append(name + '.iter-stat')
            dataflist.append(name + '.comput-stat')
            dataflist.append(name + '.runtime-stat')

        self.perfdata.load(dataflist, False)

        iter_time = []
        compute_time = []
        execution_time = []

        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            #gname = tp[2]
            gname = tp[1]
 
            fname1 = name + '.iter-stat'
            fname2 = name + '.comput-stat'
            fname3 = name + '.runtime-stat'
            if self.perfdata[fname1] is None or self.perfdata[fname2] is None:
                continue
            else:
                iter_time.append((self.perfdata[fname1]/1000, label, gname))
                compute_time.append((self.perfdata[fname2]/1000, label, gname))
                # get execution time
                offset = self.perfdata[fname3][2,0] - self.perfdata[fname3][2,1] 
                execution_time.append((self.perfdata[fname3][2,2:] + offset, label, gname))

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
        curvnum = len(iter_time)
        for id in range(curvnum):
            if not iter_time[id][2] in groupname:
                groupname.append( iter_time[id][2] )

        grp_size = len(groupname)
        rects = []

        #iternum = compute_time[0][0][2].shape[0]
        # iternum may be different, e.g. enwiki-bigram petuum always fail in the middle iteration
        iternum = 999999
        for idx in range(grp_size):
            # there are zeros filled now
            #_iternum = compute_time[idx][0][2].shape[0]
            #if _iternum < iternum:
            #    iternum = _iternum
            _iternum = compute_time[idx][0][2].shape[0]
            _firstzero = np.argwhere( compute_time[idx][0][0] == 0.)
            if _firstzero.shape[0] > 0:
                logger.info('firstzero = %s, shape=%s', _firstzero[:1], _firstzero.shape)
                iternum = min(iternum, _iternum, _firstzero[0,0])
            else:
                iternum = min(iternum, _iternum)

        logger.info('shortest nonzero iternum = %s', iternum)

        if plottype == 2:
            N = compute_time[0][0][2].shape[0]
        else:
            N = compute_time[0][0][2][:10].shape[0]
        logger.info('N=%s', N)
        ind = np.arange(N)
        #width = 0.5       # the width of the bars
        width = 1. / grp_size - 0.05


        #setup the line style and mark, colors, etc
        colors = self.colors
        lines = self.lines

        if 'lines' in conf:
            lines = conf['lines']
        if 'colors' in conf:
            colors = conf['colors']

        _trace_shortest_x = 1e+12
        for idx in range(grp_size):
            if plottype == 2:
                grp_data = compute_time[idx][0][2]
                grp_data_err = compute_time[idx][0][3]
                #grp_data2 = iter_time[idx][0][2] - compute_time[idx][0][2]
                #grp_data2_err = iter_time[idx][0][3] - compute_time[idx][0][3]
                grp_data2 = iter_time[idx][0][2]
                grp_data2_err = iter_time[idx][0][3]
 
                #sample every 10 points

                ind = np.arange(grp_data.shape[0])
                #ind = np.arange(iternum)
                
                if False:   #  _use_sample_ == True:
                    grp_data = grp_data[0:-1:10]
                    grp_data2 = grp_data2[0:-1:10]
                    x = ind[0:-1:10]
                    logger.info('x.shape=%s, data.shape=%s', x.shape, grp_data.shape)
                else:
                    x = ind
                #p1 = self.curax.errorbar(ind, grp_data, color=self.colors[idx*2], yerr= grp_data_err, label = compute_time[idx][1] +'-compute')

                #p2 = self.curax.errorbar(ind, grp_data2, color=self.colors[idx*2+1], yerr= grp_data2_err, label = compute_time[idx][1]+'-overhead')
#                p1 = self.curax.plot(x, grp_data, color=self.colors[idx*2], label = compute_time[idx][1] +'-compute')

                #p2 = self.curax.plot(x, grp_data2, color=self.colors[idx*2+1], label = compute_time[idx][1]+'-overhead')

                # draw by iteration or execution time
                #self.curax.set_xlabel('iteration')
                x_int = x.astype(int)
                x = execution_time[idx][0][x_int]
                
                point_cnt = x.shape[0]

                #draw
#p1 = self.curax.plot(x, grp_data[:point_cnt], colors[idx*2]+lines[idx*2], label = compute_time[idx][1] +'-compute')
#               p2= self.curax.plot(x, grp_data2[:point_cnt], colors[idx*2+1]+lines[idx*2+1], label = compute_time[idx][1] +'-iter')
                p1 = self.curax.plot(x, grp_data[:point_cnt], lines[idx*2], color=colors[idx*2],label = compute_time[idx][1] +'-compute')
                p2= self.curax.plot(x, grp_data2[:point_cnt], lines[idx*2+1], color=colors[idx*2+1],label = compute_time[idx][1] +'-iter')


                _trace_shortest_x = min(_trace_shortest_x, x[-1])

                #self.curax.set_xticks(x)
                #self.curax.set_xticklabels([x+1 for x in range(N)])
                self.curax.set_xlabel('Execution Time (s)')

            else:
                grp_data = compute_time[idx][0][2]
                grp_data_err = compute_time[idx][0][3]
                grp_data2 = iter_time[idx][0][2] - compute_time[idx][0][2]
                grp_data2_err = iter_time[idx][0][3] - compute_time[idx][0][3]
            
                if plottype  == 0:
                    grp_data = grp_data[:10]
                    grp_data_err = grp_data_err[:10]
                    grp_data2 = grp_data2[:10]
                    grp_data2_err = grp_data2_err[:10]
                else:
                    # get the last 10 points
                    #grp_data = grp_data[-10:]
                    #grp_data_err = grp_data_err[-10:]
                    #grp_data2 = grp_data2[-10:]
                    #grp_data2_err = grp_data2_err[-10:]

                    grp_data = grp_data[iternum-10:iternum]
                    grp_data_err = grp_data_err[iternum-10:iternum]
                    grp_data2 = grp_data2[iternum-10:iternum]
                    grp_data2_err = grp_data2_err[iternum-10:iternum]

                p1 = self.curax.bar(ind + width*idx, grp_data, width, color=self.colors_stackbar[idx*2], yerr= grp_data_err, label = compute_time[idx][1] +'-compute')

                p2 = self.curax.bar(ind + width*idx, grp_data2, width, bottom = grp_data, color=self.colors_stackbar[idx*2+1], yerr= grp_data2_err, label = compute_time[idx][1]+'-overhead')

                rects.append((p1,p2))

                self.curax.set_xticks(ind+width)
                if plottype == 0:
                    self.curax.set_xticklabels([x+1 for x in range(N)])
                else:
                    self.curax.set_xticklabels([ iternum -N + x +1 for x in range(N)])

                self.curax.set_xlabel('Iteration')

        if plottype == 2:
            if self.use_shortest_x:
                self.curax.set_xlim(0, _trace_shortest_x)
                logger.info('_trace_shortest_x = %s', _trace_shortest_x)

        # all plots goes here
        self.curax.set_ylabel('ExecutionTime Per Iteration (s)')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Overhead of LDA Trainers')

        for rect in rects:
            self.autolabel_stack(rect)
        #add xlim and ylim by conf
        if 'xlim' in conf:
            if _trace_shortest_x >0 and _trace_shortest_x > conf['xlim']:
                self.curax.set_xlim(0, conf['xlim'])
        if 'ylim' in conf:
            self.curax.set_ylim(conf['ylim_l'], conf['ylim_h'])


        #ax.set_ylim(0, overall_time[0][0] * 2)
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        if figname:
            self.savefig(figname)

        #plt.show()

    #############################################
    def plot_loadbalance_iter(self, figname, conf):
        return self.plot_loadbalance(0, figname, conf)

    def plot_loadbalance_runtime(self, figname, conf):
        return self.plot_loadbalance(1, figname, conf)

    def plot_loadbalance_overalltime(self, figname, conf):
        return self.plot_loadbalance(2, figname, conf)

    def plot_loadbalance_itertime(self, figname, conf):
        return self.plot_loadbalance(3, figname, conf)

    def plot_loadbalance(self, plottype, figname, conf):
        """
        get loadbalance from .comput-stat, and itertime from .runtime[3:]

        plottype:
            0   loadbalance .vs. iternum
            1   loadbalance .vs. traintime
            2   loadbalance .vs. execution time
            3   loadbalance .vs. itertime
        """
        dataflist = []
        #for name,label in self.perfname:
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            fname = name + '.comput-stat'
            dataflist.append(fname)
            fname = name + '.runtime-stat'
            dataflist.append(fname)
            fname = name + '.iter-stat'
            dataflist.append(fname)
            fname = name + '.update-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist, False)

        accuracy = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
 
            lh_name = name + '.comput-stat'
            runtime_name = name + '.runtime-stat'
            itertime_name = name + '.iter-stat'
            update_name = name + '.update-stat'

            # code modified from plot_accuracy
            # change .comput-stat to .likelihood like format
            cvVector = self.perfdata[lh_name][3] / self.perfdata[lh_name][2]
            iterNumber = cvVector.shape[0]
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

            itertimeMat = np.cumsum(self.perfdata[itertime_name][2,:]) / 1000.

            # convert iteration index number into real iternumber
            iterIdx = np.arange(iterNumber)
            if self.perfdata[update_name] is not None:
                realIterId = self.perfdata[update_name][5][iterIdx]
            else:
                realIterId = iterIdx + 1

            accuracy.append((iterIdx, 
                        self.perfdata[runtime_name][2,2:] + offset,
                        cvVector, label, itertimeMat,
                        realIterId))

        #fig, ax = plt.subplots()
        #setup the line style and mark, colors, etc
        colors = self.colors
        lines = self.lines

        if 'lines' in conf:
            lines = conf['lines']
        if 'colors' in conf:
            colors = conf['colors']


        #grp_size = len(accuracy)/2
        # data is two group, one in ib, other in eth
        _trace_shortest_x = 1e+12

        grp_size = len(accuracy)
        for idx in range(grp_size):
            if plottype == 0:
                x = accuracy[idx][5]
                #self.curax.plot(x, accuracy[idx][2], self.colors_orig[idx]+self.marker[idx]+'-', label = accuracy[idx][3])
#self.curax.plot(x, accuracy[idx][2], colors[idx]+lines[idx], label = accuracy[idx][3])
                self.curax.plot(x, accuracy[idx][2], lines[idx], color=colors[idx], label = accuracy[idx][3])

                # save the lines in this figure for stop critierion analysis
                curveData.append( (accuracy[idx][3], x, accuracy[idx][2]) )

            elif plottype ==3:
                x = accuracy[idx][0]
                #convert iternum to runtime
                x = accuracy[idx][4][x ]
                self.curax.plot(x, accuracy[idx][2], lines[idx], color=colors[idx], label = accuracy[idx][3])
            else:
                x = accuracy[idx][0]
                #convert iternum to runtime
                x = accuracy[idx][1][x]
                self.curax.plot(x, accuracy[idx][2], lines[idx], color=colors[idx], label = accuracy[idx][3])
            
            _trace_shortest_x = min(_trace_shortest_x, x[-1])

        #self.curax.set_ylabel('Model Perplexity')
        if self.use_shortest_x:
            self.curax.set_xlim(0, _trace_shortest_x)
    
        self.curax.set_ylabel('CV of Computation Time')
        if plottype == 0:
            self.curax.set_xlabel('Iteration Number')
        elif plottype == 1:
            self.curax.set_xlabel('Training Time (s)')
        elif plottype == 2:
            self.curax.set_xlabel('Execution Time (s)')
        elif plottype ==3:
            #self.curax.set_xlabel('Iteration Time (s)')
            self.curax.set_xlabel('Training Time (s)')


        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('LDA Trainer Workload Balance')
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        #add xlim and ylim by conf
        if 'xlim' in conf:
            if _trace_shortest_x >0 and _trace_shortest_x > conf['xlim']:
                self.curax.set_xlim(0, conf['xlim'])
        if 'ylim' in conf:
            self.curax.set_ylim(conf['ylim_l'], conf['ylim_h'])


        if figname:
            #plt.savefig('full-'+figname)
            #self.curax.set_ylim(0, 350)
            #plt.savefig('tail-'+figname)
            self.savefig(figname)

    #############################################
    def plot_scalability(self, figname, conf):
        """
        updatecnt is related to the result of model convergence 
        updatecnt .vs. time is a linear curve
        here try to compare the scalability on updatecnt@10s

        each xxx_taskxthread.rmse held a updatecnt .vs. time curve
        polyfit it, and predict on updatecnt@10s
        output <task, updatecnt@10s>

        draw a curve for each group

        """

        #
        # normalize the performance of different trainer
        # 1. byfit means use func fit on the modelupdate.vs.time curve
        # and then align all the experiment to the same time value
        # 2. otherwise, assume the experiment runs under the same
        # total model updatecnt setting, such as set with same iternum
        #
        normalize_byfit = True
        use_x_logscale = False
        stop_threshold = 8000
        predict_pt =  8000

        dataflist = []
        groups={}
        for tp in self.perfname:
            name = tp[0] 
            label = tp[1]
            fname = name + '.runtime-stat'
            dataflist.append(fname)
            fname = name + '.update-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist, quit_on_fail=False)

        iterNumber = 10
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            #for simple, just write the tasknum here
            tasknum = tp[2]
            if label in groups:
                groups[label].append((name, tasknum))
            else:
                groups[label] = [(name,tasknum)]

        # twin plot the time/update count bar chart
        ax2 = self.curax.twinx()
        seq = 0
        width = 0.2
        curveCnt = len(groups.keys())
        maxX = 0
        rects = []
        for label in groups.keys():
            curve = []
            groupdata = groups[label]

            #
            # load data for this group <name, tasknum>
            #
            groupdata = sorted(groupdata, key = lambda item: item[1])

            _min_rowcnt = np.min([ self.perfdata[groupdata[idx][0] + '.runtime-stat'][2,2:].shape[0] for idx  in range(len(groupdata))])
            logger.info('min rowcnt=%s', _min_rowcnt)
            raw_timeout = [ self.perfdata[groupdata[idx][0] + '.runtime-stat'][2,2:2+_min_rowcnt]  for idx  in range(len(groupdata))]


            #updatecnt
            iterIdx = np.arange(_min_rowcnt)
            raw_updatecnt = []
            for idx in range(len(groupdata)):
                update_name = groupdata[idx][0] + '.update-stat'
                if self.perfdata[update_name] is not None:
                    realIterId = self.perfdata[update_name][4][iterIdx]
                else:
                    realIterId = (iterIdx + 1) * self.getTrainsetSize(groupdata[idx][0])

                updatecnt = realIterId 
                #logger.info('updatecnt: %s', updatecnt)
                raw_updatecnt.append(updatecnt)

            logger.info('groupdata = %s', groupdata)
            #logger.info('tiem_out= %s', raw_timeout)
            #logger.info('raw_updatecnt = %s', raw_updatecnt)

            countindex = []
            curcount = 1
            lasttasknum = groupdata[0][1]
            for idx in range(1,len(groupdata)+1):
                if idx != len(groupdata):
                    curtasknum = groupdata[idx][1]
                else:
                    curtasknum = -1

                if lasttasknum != curtasknum:
                    #save the last one
                    countindex.append((idx - curcount, idx, lasttasknum))
                    #reset
                    curcount = 1
                    lasttasknum = curtasknum
                else:
                    curcount += 1

            logger.info('countindex=%s', countindex)

            # do mean/std on countindex[start, end, tasknum]
            for idx in range(len(countindex)):
                item = countindex[idx]
                predict = []
                for lineid in range(item[0], item[1]):
                    updatecnt = raw_updatecnt[lineid]
                    timeout = raw_timeout[lineid]

                    # fit the curve
                    z = np.polyfit(timeout, updatecnt, 2)
                    predict.append( np.poly1d(z)(predict_pt) )
 
                    # add a item <tasknum, updatecnt@10s>
                curve.append([int(item[2]), np.mean(predict), np.std(predict)])
    

            logger.info('curves: %s', curve)

            mat = np.array(curve)
            #speed up = t1/tn
            #_x = np.arange(1, mat.shape[0]+1)
            if use_x_logscale:
                _x = np.log2(mat[:,0]).astype(np.int)
            else:
                _x = np.arange(mat[:,0].shape[0])


            #logger.info('mat = %s',mat)
            #logger.info('bar %s,%s,%s',_x, mat[:,0],mat[:,1])

            ### draw bar chart
            bars = self.curax.bar(_x - curveCnt*width*1./2  + seq*width, mat[:,1], width, color=self.colors_orig_shade[seq],yerr = mat[:,2])
            rects.append(bars)
            #if (mat[:,0][-1] > maxX):
            #    maxX = mat[:,0][-1]

            ### draw speedup line
            _y = mat[:,1] *1.0 / mat[0,1]
            plots = ax2.plot(_x , _y, self.colors_orig[seq]+'.-', label = label)
            for _p in range(_x.shape[0]):
                ax2.text(_x[_p] - 0.1, _y[_p]+0.003,'%.1f'%(_y[_p]))
            
            #go to next group
            seq += 1

        ### end draw
        self.curax.set_ylabel('Model Update Count@%ds'%predict_pt if normalize_byfit else
                "Training Time Per Iteration(s)")
        if use_x_logscale:
            _x = np.arange(maxX)
            self.curax.set_xticks(_x)
            self.curax.set_xticklabels(np.exp2(_x).astype(np.int))
        else:
            self.curax.set_xticks(_x)
            self.curax.set_xticklabels(mat[:,0].astype(np.int))
 
        self.curax.set_xlabel('Nodes Number')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('LDA Trainer Scalability')

        #finally , update the recs
        for rect in rects:
            self.autolabel(rect)

        ax2.set_ylabel('SpeedUp T(1)/T(N)' if use_x_logscale else 'SpeedUp')

        ax2.legend(loc = 0)

        if figname:
            self.savefig(figname)


    def plot_scalability_nomeanstd(self, figname, conf):
        """
        updatecnt is related to the result of model convergence 
        updatecnt .vs. time is a near-linear curve in the burn-in part
        here try to compare the scalability on updatecnt@1000s

        polyfit it, and predict on updatecnt@10s
        output <task, updatecnt@1000s>

        draw a curve for each group

        """

        #
        # normalize the performance of different trainer
        # 1. byfit means use func fit on the modelupdate.vs.time curve
        # and then align all the experiment to the same time value
        # 2. otherwise, assume the experiment runs under the same
        # total model updatecnt setting, such as set with same iternum
        #
        normalize_byfit = True
        use_x_logscale = False
        stop_threshold = 8000
        predict_point = 8000
    
        dataflist = []
        groups={}
        for tp in self.perfname:
            name = tp[0] 
            label = tp[1]
            fname = name + '.runtime-stat'
            dataflist.append(fname)
            fname = name + '.update-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist, quit_on_fail=False)

        iterNumber = 10
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            #for simple, just write the tasknum here
            tasknum = tp[2]
            if label in groups:
                groups[label].append((name, tasknum))
            else:
                groups[label] = [(name,tasknum)]


        # get the throughput data

        # twin plot the time/update count bar chart
        seq = 0
        width = 0.2
        curveCnt = len(groups.keys())
        maxX = 0
        rects = []
        for label in groups.keys():
            curve = []
            groupdata = groups[label]
            for idx in range(len(groupdata)):
                # get the data
                #pfdata = self.perfdata[groupdata[idx][0]]
                logger.debug('load data for %s, shape=', groupdata[idx][0])

                if normalize_byfit:
                    # updatecnt = self.perfdata[groupdata[idx][0] + '.update-stat'][5]
                    timeout = self.perfdata[groupdata[idx][0] + '.runtime-stat'][2,2:]
                    iterIdx = np.arange(timeout.shape[0])
                    update_name = groupdata[idx][0] + '.update-stat'
                    if self.perfdata[update_name] is not None:
                        realIterId = self.perfdata[update_name][4][iterIdx]
                    else:
                        realIterId = (iterIdx + 1) * self.getTrainsetSize(groupdata[idx][0])

                    updatecnt = realIterId 
                    logger.info('updatecnt: %s', updatecnt)
                    logger.info('timeout: %s', timeout)

                    #find stop at 1000s
                    stopat = np.sum(timeout < stop_threshold)
                    updatecnt = updatecnt[:stopat]
                    timeout = timeout[:stopat]
                    logger.info('updatecnt: %s', updatecnt)
                    logger.info('timeout: %s', timeout)


                    # fit the curve
                    z = np.polyfit(timeout, updatecnt, 2)
                    p = np.poly1d(z)
                    logger.info('polyfit all, z = %s, ratio=%f, val(4000)=%s', z, z[0]/z[1], p(predict_point))
                    # add a item <tasknum, updatecnt@10s>
                    curve.append([int(groupdata[idx][1]), p(predict_point)])

            mat = np.array(curve)
            #speed up = t1/tn
            #_x = np.arange(1, mat.shape[0]+1)
            
            #use log scale for thread number
            if use_x_logscale:
                _x = np.log2(mat[:,0]).astype(np.int)
            else:
                _x = np.arange(mat[:,0].shape[0])

            #logger.info('mat = %s',mat)
            #logger.info('bar %s,%s,%s',_x, mat[:,0],mat[:,1])
            #ax2.bar(mat[:,0]+seq*width, mat[:,1], width, color=self.colors_orig[seq])
            bars = self.curax.bar(_x - curveCnt*width*1./2  + seq*width, mat[:,1], width, color=self.colors_orig_shade[seq])
            rects.append(bars)
            seq += 1
            if (mat[:,0][-1] > maxX):
                maxX = mat[:,0][-1]

        # 
        self.curax.set_ylabel('Model Update Count@%ds'%predict_point if normalize_byfit else
                "Training Time Per Iteration(s)")
        if use_x_logscale:
            _x = np.arange(maxX)
            self.curax.set_xticks(_x)
            self.curax.set_xticklabels(np.exp2(_x).astype(np.int))
        else:
            self.curax.set_xticks(_x)
            self.curax.set_xticklabels(mat[:,0].astype(np.int))
 

        self.curax.set_xlabel('Nodes Number')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('LDA Trainer Scalability')


        # plot speedup, each group is a curve
        ax2 = self.curax.twinx()
        seq = 0
        for label in groups.keys():
            curve = []
            groupdata = groups[label]
            for idx in range(len(groupdata)):
                # get the data
                logger.debug('load data for %s, shape=', groupdata[idx][0])
                if normalize_byfit:
                    # updatecnt = self.perfdata[groupdata[idx][0] + '.update-stat'][5]
                    timeout = self.perfdata[groupdata[idx][0] + '.runtime-stat'][2,2:]
                    iterIdx = np.arange(timeout.shape[0])
                    update_name = groupdata[idx][0] + '.update-stat'
                    if self.perfdata[update_name] is not None:
                        realIterId = self.perfdata[update_name][4][iterIdx]
                    else:
                        realIterId = (iterIdx + 1) * self.getTrainsetSize(groupdata[idx][0])
                    updatecnt = realIterId
 

                    #find stop at 1000s
                    stopat = np.sum(timeout < stop_threshold)
                    updatecnt = updatecnt[:stopat]
                    timeout = timeout[:stopat]


                    # fit the curve
                    z = np.polyfit(timeout, updatecnt, 2)
                    p = np.poly1d(z)
                    logger.info('polyfit all, z = %s, ratio=%f, val(predict_point)=%s', z, z[0]/z[1], p(predict_point))
                    # add a item <tasknum, updatecnt@10s>
                    #curve.append([int(groupdata[idx][1]), p(predict_point)])
                    curve.append([int(groupdata[idx][1]), p(predict_point), p(1000), p(2000), p(8000),p(12000)])

            mat = np.array(curve)
            #speed up = t1/tn
            #self.curax.plot(mat[:,0], mat[0,1] *1.0 / mat[:,1], self.colors_orig[seq]+'.-', label = label)
            #_x = np.arange(1, mat.shape[0]+1)
            #_x = np.arange(mat.shape[0])
            if use_x_logscale:
                _x = np.log2(mat[:,0]).astype(np.int)
            else:
                #_x = mat[:,0]
                _x = np.arange(mat[:,0].shape[0])

            if normalize_byfit:
                logger.info('speedup at different time point: p(100)=%s, p(1000)=%s, p(2000)=%s, p(5000)=%s,p(6000)=%s', 
                    mat[:,2]*1.0/mat[0,2],
                    mat[:,1]*1.0/mat[0,1],
                    mat[:,3]*1.0/mat[0,3],
                    mat[:,4]*1.0/mat[0,4],
                    mat[:,5]*1.0/mat[0,5],
                    )


            #ax2.plot(_x + curveCnt*width*1./2, mat[0,1] *1.0 / mat[:,1], self.colors_orig[seq]+'.-', label = label)
            # plots = ax2.plot(_x , mat[:,1] *1.0 / mat[0,1], self.colors_orig[seq+1]+'.-', label = label)
            #_y = mat[0,1] *1.0 / mat[:,1]
            plots = ax2.plot(_x , mat[:,1] *1.0 / mat[0,1], self.colors_orig[seq]+'.-', label = label)
            _y = mat[:,1] *1.0 / mat[0,1]
            for _p in range(_x.shape[0]):
                #ax2.text(_x +0.2, mat[0,1] *1.0 / mat[:,1] - 0.2,  '%.1f'%(mat[0,1] *1.0 / mat[:,1]))
                ax2.text(_x[_p] - 0.1, _y[_p]+0.01,  '%.1f'%(_y[_p]))
            # rects.append(plots)

            seq += 1

        # 
        ax2.set_ylabel("SpeedUp")
        for rect in rects:
            self.autolabel(rect)

        ax2.legend(loc = 0)
        #for rect in rects:
            #self.autolabel(rect)

        if figname:
            self.savefig(figname)




    #############################################
    def plot_throughput_runtime(self, figname, conf):
        return self.plot_throughput(0, figname, conf)

    def plot_accthroughput_runtime(self, figname, conf):
        return self.plot_throughput(1, figname, conf)


    def plot_throughput(self, plottype, figname, conf):
        """
        throughput is the model update count/s
        acc_throughput is the accumulate update count by time

        plottype:
            0   throughput .vs. traintime   ; update throughput
            1   acc_throughput .vs. traintime  ; accumulate updates
        """
        dataflist = []
        #for name,label in self.perfname:
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            fname = name + '.comput-stat'
            dataflist.append(fname)
            fname = name + '.runtime-stat'
            dataflist.append(fname)
            fname = name + '.iter-stat'
            dataflist.append(fname)
            fname = name + '.update-stat'
            dataflist.append(fname)

        self.perfdata.load(dataflist, False)

        accuracy = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
 
            lh_name = name + '.comput-stat'
            runtime_name = name + '.runtime-stat'
            itertime_name = name + '.iter-stat'
            update_name = name + '.update-stat'

            # code modified from plot_accuracy
            # change .comput-stat to .likelihood like format
            cvVector = self.perfdata[lh_name][3] / self.perfdata[lh_name][2]
            iterNumber = cvVector.shape[0]
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

            itertimeMat = np.cumsum(self.perfdata[itertime_name][2,:]) / 1000.

            # convert iteration index number into real iternumber
            iterIdx = np.arange(iterNumber)
            if self.perfdata[update_name] is not None:
                realIterId = self.perfdata[update_name][5][iterIdx]
            else:
                realIterId = iterIdx + 1

            accuracy.append((iterIdx, 
                        self.perfdata[runtime_name][2,2:] + offset,
                        cvVector, label, itertimeMat,
                        realIterId))

        #fig, ax = plt.subplots()
        #setup the line style and mark, colors, etc
        colors = self.colors
        lines = self.lines
        lines2 = self.lines2

        if 'lines' in conf:
            lines = conf['lines']
        if 'colors' in conf:
            colors = conf['colors']


        #grp_size = len(accuracy)/2
        # data is two group, one in ib, other in eth
        _trace_shortest_x = 1e+12
        
        grp_size = len(accuracy)
        for idx in range(grp_size):
            if plottype == 1:
                x = accuracy[idx][0]
                #convert iternum to runtime
                x = accuracy[idx][1][x]
                y = np.cumsum(accuracy[idx][5])
                self.curax.plot(x, y, lines[idx], color=colors[idx], label = accuracy[idx][3])
            else:
                x = accuracy[idx][0]
                #convert iternum to runtime
                x = accuracy[idx][1][x]
                self.curax.plot(x, accuracy[idx][5], lines[idx], color=colors[idx], label = accuracy[idx][3])
            

                #try plotfit
                z = np.polyfit(x, accuracy[idx][5], 2)
                p = np.poly1d(z)
                self.curax.plot(x, p(x), lines2[idx], color=colors[idx], label = accuracy[idx][3])




            _trace_shortest_x = min(_trace_shortest_x, x[-1])

        #self.curax.set_ylabel('Model Perplexity')
        if self.use_shortest_x:
            self.curax.set_xlim(0, _trace_shortest_x)
    
        self.curax.set_xlabel('Training Time (s)')
        if plottype == 0:
            self.curax.set_ylabel('Throughput')
        elif plottype == 1:
            self.curax.set_ylabel('Accumulate Throughput')

        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('LDA Trainer Throughput')
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        #add xlim and ylim by conf
        if 'xlim' in conf:
            if _trace_shortest_x >0 and _trace_shortest_x > conf['xlim']:
                self.curax.set_xlim(0, conf['xlim'])
        if 'ylim' in conf:
            self.curax.set_ylim(conf['ylim_l'], conf['ylim_h'])


        if figname:
            #plt.savefig('full-'+figname)
            #self.curax.set_ylim(0, 350)
            #plt.savefig('tail-'+figname)
            self.savefig(figname)


    #############################################
    def plot_comm_breakdown_top(self, figname, conf):
        return self.plot_comm_breakdown(0, figname, conf)

    def plot_comm_breakdown_end(self, figname, conf):
        return self.plot_comm_breakdown(1, figname, conf)

    def plot_comm_breakdown_all(self, figname, conf):
        return self.plot_comm_breakdown(2, figname, conf)

    def plot_comm_iter(self, figname, conf):
        return self.plot_comm_breakdown(3, figname, conf)

    def plot_comm_breakdown(self, plottype, figname, conf):
        """
        get comm and compute value from .comm-stat and .comput-stat
        plottype:
            0   ; top
            1   ; end
            2   ; all
            3   ; no breakdown iteration time only
        """
        dataflist = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            dataflist.append(name + '.comm-stat')
            dataflist.append(name + '.comput-stat')
            dataflist.append(name + '.runtime-stat')

        self.perfdata.load(dataflist,False)

        comm_time = []
        compute_time = []
        execution_time = []

        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            gname = tp[1]
 
            fname1 = name + '.comm-stat'
            fname2 = name + '.comput-stat'
            fname3 = name + '.runtime-stat'
            if self.perfdata[fname1] is None or self.perfdata[fname2] is None:
                continue
            else:
 
                comm_time.append((self.perfdata[fname1]/1000, label, gname))
                compute_time.append((self.perfdata[fname2]/1000, label, gname))

                # get execution time
                offset = self.perfdata[fname3][2,0] - self.perfdata[fname3][2,1] 
                execution_time.append((self.perfdata[fname3][2,2:] + offset, label, gname))

 
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

        #iternum = compute_time[0][0][2].shape[0]
        # iternum may be different, e.g. enwiki-bigram petuum always fail in the middle iteration
        iternum = 999999
        for idx in range(grp_size):
            _iternum = compute_time[idx][0][2].shape[0]
            if _iternum < iternum:
                iternum = _iternum
        logger.info('shortest iternum = %s', iternum)

        if plottype >= 2:
            N = compute_time[0][0][2].shape[0]
        else:
            N = compute_time[0][0][2][:10].shape[0]
        logger.info('N=%s', N)
        ind = np.arange(N)
        #width = 0.45       # the width of the bars
        width = 1. / grp_size - 0.05

        for idx in range(grp_size):
            if plottype == 2:
                # get mean , std
                grp_data = compute_time[idx][0][2]
                grp_data_err = compute_time[idx][0][3]
                grp_data2 = comm_time[idx][0][2]
                grp_data2_err = comm_time[idx][0][3]

                #sample every 10 points
                x = ind[0:-1:10]
                grp_data = grp_data[0:-1:10]
                grp_data2 = grp_data2[0:-1:10]
                logger.info('x.shape=%s, data.shape=%s', x.shape, grp_data.shape)
                x_int = x.astype(int)
                x = execution_time[idx][0][x_int]
                
                #draw
                #p1 = self.curax.plot(x, grp_data, self.colors_orig[idx]+'.-', label = compute_time[idx][1] +'-compute')
                #p2 = self.curax.plot(x, grp_data2, self.colors_orig[idx]+'.--', label = comm_time[idx][1] +'-comm')
                p2 = self.curax.plot(x, grp_data2, self.colors_orig[idx]+'.-', label = comm_time[idx][1] +'-comm')

                self.curax.set_xlabel('Execution Time (s)')

            elif plottype == 3:
                # comm-iter
                # sync pass number can be less than computation iteration number, as in ylda
                # find the shortest sync pass num



                # get mean , std
                grp_data = compute_time[idx][0][2]
                grp_data_err = compute_time[idx][0][3]

                # min > 0 is the true pass number
                true_pass = comm_time[idx][0][0] > 0
                grp_data2 = comm_time[idx][0][2][true_pass]
                grp_data2_err = comm_time[idx][0][3][true_pass]

                #sample every 10 points
                _ind = np.arange(grp_data2.shape[0])
                x = _ind[0:-1:10]
                #grp_data = grp_data[0:-1:10]
                grp_data2 = grp_data2[0:-1:10]
                
                logger.info('x.shape=%s, data.shape=%s', x.shape, grp_data.shape)
                #draw
                p2 = self.curax.plot(x + 1 , grp_data2, self.colors_orig[idx]+'.-', label = comm_time[idx][1] +'-comm')

                self.curax.set_xlabel('Num. of Synchronization Passes')

            else:
                # get mean , std
                grp_data = compute_time[idx][0][2]
                grp_data_err = compute_time[idx][0][3]
                grp_data2 = comm_time[idx][0][2]
                grp_data2_err = comm_time[idx][0][3]
 
                if plottype  == 0:
                    grp_data = grp_data[:10]
                    grp_data_err = grp_data_err[:10]
                    grp_data2 = grp_data2[:10]
                    grp_data2_err = grp_data2_err[:10]
                else:
                    grp_data = grp_data[-10:]
                    grp_data_err = grp_data_err[-10:]
                    grp_data2 = grp_data2[-10:]
                    grp_data2_err = grp_data2_err[-10:]

                p1 = self.curax.bar(ind + width*idx, grp_data, width, color=self.colors_stackbar[idx*2], yerr= grp_data_err, label = compute_time[idx][1] +'-compute')
                p2 = self.curax.bar(ind + width*idx, grp_data2, width, bottom = grp_data, color=self.colors_stackbar[idx*2+1], yerr= grp_data2_err, label = compute_time[idx][1]+'-comm')

                rects.append((p1,p2))

                self.curax.set_xticks(ind+width)
                if plottype == 0:
                    self.curax.set_xticklabels([x+1 for x in range(N)])
                else:
                    self.curax.set_xticklabels([ iternum -N + x +1 for x in range(N)])

                self.curax.set_xlabel('Iteration')


        # all plots goes here
        if plottype == 3:
            self.curax.set_ylabel('ExecutionTime Per SyncPass (s)')
        else:
            self.curax.set_ylabel('ExecutionTime Per Iteration (s)')

        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Communication and Computation time breakdown of LDA Trainers')

        for rect in rects:
            self.autolabel_stack(rect)

        #ax.set_ylim(0, overall_time[0][0] * 2)
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        if figname:
            self.savefig(figname)

        #plt.show()

    ################################
    def plot_iter_trend_top(self, figname, conf):
        return self.plot_iter_trend(0, figname, conf)

    def plot_iter_trend_end(self, figname, conf):
        return self.plot_iter_trend(1, figname, conf)

    def plot_iter_trend_all(self, figname, conf):
        return self.plot_iter_trend(2, figname, conf)

    def plot_iter_trend(self, plottype, figname, conf):
        """
        get iter value from .iter-stat
        plottype:
            0   ; top
            1   ; end
            2   ; all
        """
        dataflist = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            dataflist.append(name + '.iter-stat')
            dataflist.append(name + '.runtime-stat')

        self.perfdata.load(dataflist,False)

        iter_time = []
        execution_time = []

        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            gname = tp[1]
 
            fname1 = name + '.iter-stat'
            fname3 = name + '.runtime-stat'
            if self.perfdata[fname1] is None :
                continue
            else:
 
                iter_time.append((self.perfdata[fname1]/1000, label, gname))

                # get execution time
                offset = self.perfdata[fname3][2,0] - self.perfdata[fname3][2,1] 
                execution_time.append((self.perfdata[fname3][2,2:] + offset, label, gname))

 
        #
        # data is in groups
        #
        
        #code mofidy based on comm_breakdown
        comm_time = iter_time
        compute_time = iter_time

        # draw a bar stacked
        groupname = []
        for id in range(len(comm_time)):
            if not comm_time[id][2] in groupname:
                groupname.append( comm_time[id][2] )

        grp_size = len(groupname)
        rects = []


        # iternum may be different, e.g. enwiki-bigram petuum always fail in the middle iteration
        iternum = 999999
        for idx in range(grp_size):
            _iternum = compute_time[idx][0][2].shape[0]
            if _iternum < iternum:
                iternum = _iternum
        logger.info('shortest iternum = %s', iternum)

        if plottype == 2:
            N = compute_time[0][0][2].shape[0]
        else:
            N = compute_time[0][0][2][:10].shape[0]
        logger.info('N=%s', N)
        ind = np.arange(N)
        #width = 0.45       # the width of the bars
        width = 1. / grp_size - 0.05

        for idx in range(grp_size):
            if plottype == 2:
                # get mean , std
                grp_data = compute_time[idx][0][2]
                grp_data_err = compute_time[idx][0][3]
                grp_data2 = comm_time[idx][0][2]
                grp_data2_err = comm_time[idx][0][3]

                #sample every 10 points
                x = ind[0:-1:10]
                grp_data = grp_data[0:-1:10]
                grp_data2 = grp_data2[0:-1:10]
                logger.info('x.shape=%s, data.shape=%s', x.shape, grp_data.shape)
                x_int = x.astype(int)
                
                if grp_data.shape[0] < x.shape[0]:
                    x = execution_time[idx][0][x_int[:grp_data.shape[0]]]
                else:
                    x = execution_time[idx][0][x_int]
                
                #draw
                p1 = self.curax.plot(x, grp_data, self.colors_orig[idx]+'.-', label = compute_time[idx][1] +'-iter')
                #p2 = self.curax.plot(x, grp_data2, self.colors_orig[idx]+'.--', label = comm_time[idx][1] +'-comm')

                self.curax.set_xlabel('Execution Time (s)')

            else:
                # get mean , std
                grp_data = compute_time[idx][0][2]
                grp_data_err = compute_time[idx][0][3]
                grp_data2 = comm_time[idx][0][2]
                grp_data2_err = comm_time[idx][0][3]
 
                if plottype  == 0:
                    grp_data = grp_data[:10]
                    grp_data_err = grp_data_err[:10]
                    grp_data2 = grp_data2[:10]
                    grp_data2_err = grp_data2_err[:10]
                else:
                    # get the last 10 points
                    #grp_data = grp_data[-10:]
                    #grp_data_err = grp_data_err[-10:]
                    #grp_data2 = grp_data2[-10:]
                    #grp_data2_err = grp_data2_err[-10:]

                    grp_data = grp_data[iternum-10:iternum]
                    grp_data_err = grp_data_err[iternum-10:iternum]
                    grp_data2 = grp_data2[iternum-10:iternum]
                    grp_data2_err = grp_data2_err[iternum-10:iternum]

                #p1 = self.curax.bar(ind + width*idx, grp_data, width, color=self.colors_stackbar[idx*2], yerr= grp_data_err, label = compute_time[idx][1] +'-compute')
                #p2 = self.curax.bar(ind + width*idx, grp_data2, width, bottom = grp_data, color=self.colors_stackbar[idx*2+1], yerr= grp_data2_err, label = compute_time[idx][1]+'-comm')

                #rects.append((p1,p2))
                p1 = self.curax.bar(ind + width*idx, grp_data, width, color=self.colors_stackbar[idx], yerr= grp_data_err, label = compute_time[idx][1] +'-iter')
                rects.append(p1)

                self.curax.set_xticks(ind+width)
                if plottype == 0:
                    self.curax.set_xticklabels([x+1 for x in range(N)])
                else:
                    self.curax.set_xticklabels([ iternum -N + x +1 for x in range(N)])

                self.curax.set_xlabel('Iteration')


        # all plots goes here
        self.curax.set_ylabel('ExecutionTime Per Iteration (s)')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Communication and Computation time breakdown of LDA Trainers')

        for rect in rects:
            self.autolabel_stack(rect)

        #ax.set_ylim(0, overall_time[0][0] * 2)
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        if figname:
            self.savefig(figname)

        #plt.show()


    ######################################################
    def plot_network(self, figname, conf):
        return self.plot_system(0, figname, conf)
    def plot_freemem(self, figname, conf):
        return self.plot_system(1, figname, conf)
    def plot_cpu(self, figname, conf):
        return self.plot_system(2, figname, conf)

    def plot_system(self, plottype, figname, conf):
        """
        get system perf data from monitor stat files
        
        plottype:
            0   ; network
            1   ; freemem
            2   ; cpu

        """
        stat_name=['rx_ok','tx_ok','freemem','us','sy']
        dataflist = []
        #for name,label in self.perfname:
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            for sname in stat_name:
                fname = name + '.' + sname + '-stat'
                dataflist.append(fname)

        self.perfdata.load(dataflist, False)

        data = {}
        labels = []
        for sname in stat_name:
            data[sname] = []

        for tp in self.perfname:
            name = tp[0]
            load_fail = False
            for sname in stat_name:
                fname = name + '.' + sname + '-stat'
                if self.perfdata[fname] is None:
                    load_fail = True
                    break
                
                if sname =='freemem':
                    # use min value
                    data[sname].append(self.perfdata[fname][0,:])
                else:
                    # use max value
                    data[sname].append(self.perfdata[fname][1,:])

            if not load_fail:
                labels.append(tp[1])
        #begin to plot
        sampler = DataSampler()
        sample_span = 50

        grp_size = len(labels)
        for idx in range(grp_size):
            if plottype == 0:
                # draw network in/out
                y_in = data['rx_ok'][idx]
                y_out = data['tx_ok'][idx]
                
                y_in = sampler.sample_max(y_in,  sample_span)
                y_out = sampler.sample_max(y_out,  sample_span)
                y_out = -1 * y_out

                x = np.arange(y_in.shape[0]) *  sample_span

                self.curax.plot(x, y_in, self.colors_orig[idx*2]+'.-', label = labels[idx]+'-in')
                self.curax.plot(x, y_out, self.colors_orig[idx*2 +1]+'.-', label = labels[idx]+'-out')
            elif plottype ==1:
                # draw freememe
                y = data['freemem'][idx]

                y = sampler.sample_max(y,  sample_span)
                x = np.arange(y.shape[0]) *  sample_span


                self.curax.plot(x, y, self.colors_orig[idx]+'.-', label = labels[idx])
            else:
                #draw cpu
                y_us = data['us'][idx]
                y_sy = data['sy'][idx]


                y_us = sampler.sample_max(y_us,  sample_span)
                y_sy = sampler.sample_max(y_sy,  sample_span)
                x = np.arange(y_us.shape[0]) *  sample_span


                self.curax.plot(x, y_us, self.colors_orig[idx*2]+'.-', label = labels[idx]+'-us')
                self.curax.plot(x, y_sy, self.colors_orig[idx*2 +1]+'.-', label = labels[idx]+'-sy')

        #
        self.curax.set_xlabel('time (s)')
        if plottype == 0:
            self.curax.set_ylabel('Networking In/Out (MB/s)')
        elif plottype == 1:
            self.curax.set_ylabel('Free Memeory (GB)')
        elif plottype == 2:
            self.curax.set_ylabel('CPU Utilization')


        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('System Performance')
        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        
        if figname:
            #plt.savefig('full-'+figname)
            #self.curax.set_ylim(0, 350)
            #plt.savefig('tail-'+figname)
            self.savefig(figname)

        #plt.show()

    ######################################3
    def plot_model_zipf(self, figname, conf):
        """
        refer to zipf.py

        """
        dataflist = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            dataflist.append(name)

        self.perfdata.load(dataflist)

        split_data = []

        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            gname = tp[1]
            
            # rank, freq
            split_data.append((self.perfdata[name], label, gname))

        # plot in logx
        for idx in range(len(split_data)):
            rank = split_data[idx][0][:,0]
            freq = split_data[idx][0][:,1]

            # sample data from the 1M dict
            rank = np.hstack((rank[:3000], rank[3000:30000:500], rank[30000:-1:5000]))
            freq = np.hstack((freq[:3000], freq[3000:30000:500], freq[30000:-1:5000]))
 
            #
            # draw2() in zipf.py
            #
            lfreq = np.log10(np.array(freq))
            lrank = np.log10(np.array(rank))
            logger.debug('freq=%s, log(freq)=%s', freq[:10], lfreq[:10])

            # fit the zipf law curve?
            z = np.polyfit(lrank, lfreq, 1)
            p = np.poly1d(z)
            logger.info('polyfit all, z = %s, ratio=%f', z, z[0]/z[1])

            idx2=np.where(lrank<np.log10(3000))
            z2 = np.polyfit(lrank[idx2], lfreq[idx2], 1)
            p2 = np.poly1d(z2)
            logger.info('polyfit 3..8, z = %s, ratio=%f', z2, z2[0]/z2[1])

            xp = np.linspace(0, lrank[-1], 100)
            self.curax.set_xscale("log", nonposx='clip')
            self.curax.set_yscale("log", nonposx='clip')

            self.curax.plot(rank, freq, self.colors_orig[idx]+'.', label = split_data[idx][1])
            label=r'$y=10^{%.1f}x^{%.1f}$'%(z2[1], z2[0])
            self.curax.plot(10**xp, 10**p2(xp),'--', label=label)
            label=r'$y=10^{%.1f}x^{%.1f}$'%(z[1], z[0])
            #self.curax.plot(10**xp, 10**p(xp), '-',label=label)
 
            self.curax.set_xlabel('Word Rank')


        # all plots goes here
        self.curax.set_ylabel('Word Frequency')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Zipf Distribution')

        #for rect in rects:
        #    self.autolabel_stack(rect)

        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        #self.curax.legend(loc = 1)
        self.curax.legend(loc = 0)
        if figname:
            self.savefig(figname)

    def plot_model_split(self, figname, conf):
        dataflist = []
        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            dataflist.append(name)

        self.perfdata.load(dataflist)

        split_data = []

        for tp in self.perfname:
            name = tp[0]
            label = tp[1]
            gname = tp[1]
            
            # split number, docno, vocabsize,  wordcnt
            split_data.append((self.perfdata[name], label, gname))

        # plot in logx
        for idx in range(len(split_data)):
            x = split_data[idx][0][:,0]
            y = split_data[idx][0][:,2] *1.0/ split_data[idx][0][0,2]
            
            #draw

            self.curax.set_ylim(0, 1.2)
            self.curax.set_xscale("log", nonposx='clip')
            p1 = self.curax.plot(x, y, self.colors_orig[idx]+'o-', label = split_data[idx][1])

            self.curax.set_xlabel('Document Collection Partition Number')


        # all plots goes here
        self.curax.set_ylabel('Vocabulary Size of Partition (\%)')
        if 'title' in conf:
            self.curax.set_title(conf['title'])
        else:
            self.curax.set_title('Vocabulary Size Nonlinear Decrease Over Doc Partition')

        #for rect in rects:
        #    self.autolabel_stack(rect)

        #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
        self.curax.legend(loc = 0)
        if figname:
            self.savefig(figname)

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

