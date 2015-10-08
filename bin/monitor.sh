#!/bin/sh

#
# usage: monitor <eth0|ib0> <time> <logfile>
#
help(){
cat <<EOF
    Monitor netstat and vmstat, logging into /dev/shm.
    usage: monitor.sh <start|stop|collect> <eth0|ib0>|<logname>

    Example:
        monitor.sh start eth0  ; this start monitor.sh on network interface eth0
        monitor.sh stop        ; this stop the current monitor
        monitor.sh stop  application-1991 ; this stop the current monitor, and rename the logfile suffix with application-1991

    Run on Cluster:
        * start and stop is the same, run on headnode with cexec
        cexec monitor.sh start eth0
        cexec monitor.sh stop
        cexec monitor.sh stop application-1991

        * collect logfiles from nodes, don't use cexec, run on head node only.
        monitor.sh collect application-1991 ; this collect all logs with suffix application-1991, save them to /mnt/vol1/monitorlog 

EOF
}

sharedir="/mnt/vol1/monitorlog"

CMD=$1
case $CMD in
    start)
        shift
        interface=$1
        echo "start monitor on $interface"
        #as long as 100 hours?
        time=360000
        #save log to shm, no disk i/o involved
        logfile=/dev/shm/monitor.log
        
        #save the last log files
        if [ -f $logfile.vmstat ] ; then
            date=`date +%Y%m%d%H%M%S`
            mv $logfile.vmstat $logfile.vmstat.$date
            mv $logfile.netstat $logfile.netstat.$date
        fi

        # run command at background
        vmstat -t 1 $time 1>>$logfile.vmstat &
        netstat -c -I=$interface  1>>$logfile.netstat &
    ;;

    stop)
        echo "stop monitor"
        killall vmstat
        killall netstat
        
        if [ $# -eq '2' ]; then
            date=$2
            logfile=/dev/shm/monitor.log
            mv $logfile.vmstat $logfile.vmstat.$date
            mv $logfile.netstat $logfile.netstat.$date
        fi
    ;;
    
    collect)
        if [ $# -eq '2' ]; then
            date=.$2
            mkdir -p $sharedir/$2
        fi
        logfile=/dev/shm/monitor.log
        
        # concurrent scp from slaves will be out of service of sshd
        #scp $logfile.vmstat$date $sharedir/monitor.log.vmstat$date.$HOSTNAME
        #scp $logfile.netstat$date $sharedir/monitor.log.netstat$date.$HOSTNAME

        # try sequential copy from headnode
        # get slaves from $C3_CONF
        slaves=`cexec hostname | grep ^[a-zA-Z]`
        for s in $slaves; do
            scp $s:$logfile.vmstat$date $sharedir/$2/monitor.log.vmstat$date.$s
            scp $s:$logfile.netstat$date $sharedir/$2/monitor.log.netstat$date.$s
        done
    ;;

    *) echo "Unrecognized command: $CMD"; help; exit 1;;
esac

 



