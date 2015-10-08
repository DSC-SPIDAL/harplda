#!/bin/sh

#
# usage: monitor <eth0|ib0> <time> <logfile>
#
help(){
cat <<EOF
    Monitor netstat and vmstat, logging into /dev/shm.
    usage: monitor <start|stop> <eth0|ib0>|<logname>

    Example:
        monitor start eth0  ; this start monitor on network interface eth0
        monitor stop        ; this stop the current monitor
        monitor stop  application-1991 ; this stop the current monitor, and rename the logfile suffix with application-1991

EOF
}

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

    *) echo "Unrecognized command: $CMD"; help; exit 1;;
esac

 



