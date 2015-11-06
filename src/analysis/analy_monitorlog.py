#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Analysis the log file of performance monitor

input:
    performance monitor's log dir

format: 
    filename:
        monitor.log.netstat.$appname.j-046
        monitor.log.vmstat.$appname.j-046

    netstat:  Rx-OK $4, Tx-OK $8  
        Kernel Interface table
        Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg 
        eth0       1500   0 1003849731      0      0      0 1007094096      0      0      0 BMRU

    vmstat:  $4: free mem, $13 : us, $14 cs,$15 id, $16 wa
        procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu------ ---timestamp---
        r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
        2  0      0 128485192 165120 1628116    0    0     0     0    0    0  7  0 93  0  0    2015-10-15 07:35:36 EDT
        0  0      0 128485880 165120 1628124    0    0     0    28  429  555  0  0 100  0  0   2015-10-15 07:35:37 EDT

        CPU
        The cpu section reports on the use of the system’s CPU resources. The columns in this section always add to 100 and reflect “percentage of available time”.
        The us column reports the amount of time that the processor spends on userland tasks, or all non-kernel processes. The sy column reports the amount of time that the processor spends on kernel related tasks. The id column reports the amount of time that the processor spends idle. The wa column reports the amount of time that the processor spends waiting for IO operations to complete before being able to continue processing tasks.

Usage: 
    analy_monitorlog <logdir> <node id>

"""

import sys,os,re
import datetime
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Svg')
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class MonitorLog():
    def __init__(self):
        pass

    def load_log(self, logdir):
        netstat = self.load_netstat_log(logdir)
        vmstat = self.load_vmstat_log(logdir)

        #combine the data
        #appname , nodeid, rx_ok, tx_ok, us, cs, id, wa
        row1 = len(netstat)
        row2 = len(vmstat)
        if row1 != row2:
            logger.error('node number mismatch, netstat row=%s, vmstat row=%s', row1, row2)
            return

        for idx in range(row1):
            if netstat[idx][1] != vmstat[idx][1]:
                # nodeid mismatch
                logger.error('node number mismatch, netstat nodeid=%s, vmstat nodeid=%s', netstat[idx][1], vmstat[idx][1])
                return


        timespan = 999999999
        for idx in range(row1):
            # get the shortest length, in (s) 
            _timespan = min(len(netstat[idx][2]), len(netstat[idx][3]), len(vmstat[idx][2]), len(vmstat[idx][3]), len(vmstat[idx][4]), len(vmstat[idx][5]))
            #logger.debug('timespan=%d, %d, %d, %d, %d, %d', len(netstat[idx][2]), len(netstat[idx][3]), len(vmstat[idx][2]), len(vmstat[idx][3]), len(vmstat[idx][4]), len(vmstat[idx][5]))

            #logger.info('timespan on node %s = %d', netstat[idx][1], timespan)

            if _timespan < timespan:
                timespan = _timespan

        logger.info('shortest timespan = %d', timespan)

        # make the matrix[nodeid, type, data[0...timespan]]
        matrix = np.zeros((row1, 6, timespan))
        mtu = netstat[0][4][0]
        for idx in range(row1):
            matrix[idx,0] = np.array(netstat[idx][2][:timespan])
            matrix[idx,1] = np.array(netstat[idx][3][:timespan])
            matrix[idx,2] = np.array(vmstat[idx][2][:timespan])
            matrix[idx,3] = np.array(vmstat[idx][3][:timespan])
            matrix[idx,4] = np.array(vmstat[idx][4][:timespan])
            matrix[idx,5] = np.array(vmstat[idx][5][:timespan])
        
        # dealwith rx_ok and tx_ok, convert to MB/s
        for idx in range(timespan-1, 1, -1):
            matrix[:,0,idx] = (matrix[:,0,idx] - matrix[:,0,idx-1]) * mtu / (1024*1024.)
            matrix[:,1,idx] = (matrix[:,1,idx] - matrix[:,1,idx-1]) * mtu / (1024*1024.)

        #clear the first two column
        matrix[:,0,:2] = np.zeros((row1,2))
        matrix[:,1,:2] = np.zeros((row1,2))

        # dealwith freemem, B to MB
        matrix[:,2,:] = matrix[:,2,:] / (1024*1024.)

        #min, max, mean, std analysis
        idname=['rx_ok','tx_ok','freemem','us','sy','idle','wa']
        for id in range(6):
            statMatrix = np.zeros((4, timespan))
            statMatrix[0] = np.min(matrix[:,id,:], axis=0)
            statMatrix[1] = np.max(matrix[:,id,:], axis=0)
            statMatrix[2] = np.mean(matrix[:,id,:], axis=0)
            statMatrix[3] = np.std(matrix[:,id,:], axis=0)

            #save and skip first 10 data points
            fname = netstat[0][0] + '.' + idname[id] + '-stat'
            np.savetxt(fname, statMatrix[:,10:], fmt='%.02f')


        #save matrix
        #for idx in range(row1):
        #    fname = "monitor." + netstat[idx][0] + '.' + netstat[idx][1]
        #    np.savetxt(fname, matrix[idx,:,10:], fmt="%.02f")


        return matrix, netstat[:][1]

    def load_netstat_log(self, logdir, filename='monitor.log.netstat'):
        netstat = []
        for dirpath, dnames, fnames in os.walk(logdir):
            for f in fnames:
                if f.startswith(filename):
                    #decode the appname and nodeid
                    m = re.match(filename + '\.(.*)\.(j-[0-9]*)',f)
                    if not m:
                        logger.error('filename format error, f=%s', f)
                        continue
                    appname = m.group(1)
                    nodeid = m.group(2)
                    
                    #logger.info('load log from %s, appname=%s, nodeid=%s', dirpath+'/'+f, appname, nodeid)


                    #load data
                    with open(dirpath + '/' + f, 'r') as logf:
                        rx_ok = []
                        tx_ok = []
                        mtu = []
                        for line in logf:
                            if line.startswith('eth') or line.startswith('ib'):
                                items = line.split()
                                rx_ok.append(long(items[3]))
                                tx_ok.append(long(items[7]))
                                mtu.append(int(items[1]))

                        netstat.append((appname, nodeid, rx_ok, tx_ok, mtu))

        if not netstat:
            logger.error('%s/%s load data failed', dirpath, f)
            return None

        # sort by nodeid
        nodenum = len(netstat)
        netstat =  sorted(netstat, key = lambda modeltp : modeltp[1])
        logger.info('appname = %s, total %d nodes', appname, nodenum)

        logger.debug('netstat data = %s', netstat[0][2][:10])
 
        #min, max, mean analysis
        # mean/std of compute, comm, iter restured
        #statMatrix = np.zeros((4, iternum))
        #statMatrix[0] = rawdata[:,4]
        #statMatrix[1] = rawdata[:,4]
        #statMatrix[2] = rawdata[:,4]
        #np.savetxt(appdir + '.comput-stat', statMatrix,fmt='%.2f')

        return netstat

    def load_vmstat_log(self, logdir, filename='monitor.log.vmstat'):
        vmstat = []
        for dirpath, dnames, fnames in os.walk(logdir):
            for f in fnames:
                if f.startswith(filename):
                    #decode the appname and nodeid
                    m = re.match(filename + '\.(.*)\.(j-[0-9]*)',f)
                    if not m:
                        logger.error('filename format error, f=%s', f)
                        continue
                    appname = m.group(1)
                    nodeid = m.group(2)

                    #logger.info('load log from %s, appname=%s, nodeid=%s', dirpath+'/'+f, appname, nodeid)
                    #load data
                    with open(dirpath + '/' + f, 'r') as logf:
                        free_mem = []
                        _us = []
                        _sy = []
                        _idle = []
                        _wa = []

                        for line in logf:
                            # last timestamp EDT, EST, etc
                            if line.endswith('T\n'):
                                items = line.split()
                                free_mem.append(long(items[3]))
                                _us.append(long(items[12]))
                                _sy.append(long(items[13]))
                                _idle.append(long(items[14]))
                                _wa.append(long(items[15]))

                                #logger.debug('items=%s, %s, %s, %s', items[3], items[12], items[13], items[14])

                        vmstat.append((appname, nodeid, free_mem, _us, _sy, _idle, _wa))

        if not vmstat:
            logger.error('%s/%s load data failed', dirpath, f)
            return None

        # sort by nodeid
        nodenum = len(vmstat)
        vmstat =  sorted(vmstat, key = lambda modeltp : modeltp[1])
        logger.info('appname=%s, total %d nodes', appname, nodenum)
 
        logger.debug('vmstat data = %s', vmstat[0][2][:10])

        #min, max, mean analysis
        # mean/std of compute, comm, iter restured
        #statMatrix = np.zeros((4, iternum))
        #statMatrix[0] = rawdata[:,4]
        #statMatrix[1] = rawdata[:,4]
        #statMatrix[2] = rawdata[:,4]
        #np.savetxt(appdir + '.comput-stat', statMatrix,fmt='%.2f')

        return vmstat
 
def draw_mvmatrix(mv_matrix, trainer, fig, show = False):
    logger.info('draw the mean-var figure')

    row , col = mv_matrix.shape
    x = np.arange(1, col + 1 )

    plt.title('Performance of LDA Trainers')
    plt.xlabel('Iteration Number')
    plt.ylabel('Elapsed Millis')

    plt.errorbar(x, mv_matrix[0], mv_matrix[1] ,label=trainer + ' compute')
    plt.errorbar(x, mv_matrix[2], mv_matrix[3] ,label=trainer + ' comm')

    plt.legend()

    plt.savefig(fig)
    if show:
        plt.show()

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

if __name__ == "__main__":
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    # logging configure
    import logging.config
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 2:
        logger.error(globals()['__doc__'] % locals())
        sys.exit(1)

    # check the path
    logdir = sys.argv[1]
    if len(sys.argv) > 2:
        nodeid = sys.argv[2]

    logAnalizer = MonitorLog()

    logAnalizer.load_log(logdir)





