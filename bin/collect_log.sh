#!/bin/sh

trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM
#
#
help(){
cat <<EOF
    usage: collect_log.sh <logname>
        * collect logfiles from nodes, don't use cexec, run on head node only.
        collect_log.sh application-1991 ; this collect all logs for appid=application-1991, save them to /mnt/vol1/hadooplog 
        collect_log.sh auto ; this collect all logs for the last appid, save them to /mnt/vol1/hadooplog 

EOF
}

#detct cluster
hostid=`hostname | grep -c "^t"`
if [ $hostid -eq "1" ] ; then
    # tango
    localdir="/scratch/logs/userlogs"
    sharedir="/scratch/hadooplog"
    resourcemanager="t-006"
else
    #juliet
    localdir="/scratch/logs/userlogs"
    sharedir="/mnt/vol1/hadooplog"
    resourcemanager="j-128"
fi


if [ $# -ne '1' ] ; then
    help
    exit 0
fi

name=`grep -Po "APPID=(.*)\t" /scratch/logs/yarn-fg474admin-resourcemanager-$resourcemanager.log | grep -Po "application_(.*)" |uniq | tail -n 1`
echo 'found the last appname=$name'


if [ "$1" == "auto" ] ; then
    appname=$name
else
    appname=$1
fi

echo "collect log for $appname"
mkdir -p $sharedir/$appname

# try sequential copy from headnode
# get slaves from $C3_CONF
slaves=`cexec hostname | grep ^[a-zA-Z]`
for s in $slaves; do
    scp -r $s:$localdir/$appname $sharedir
done

