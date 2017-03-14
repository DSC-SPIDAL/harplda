#!/bin/bash
#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config

installfiles="learntopics formatter DM_Server Merge_Dictionaries Merge_Topic_Counts"

if [ -z "${ylda+xxx}" ]; then
    echo "ylda not set yet, quit...."
    exit 
fi

#check current directory for installfiles
for f in $installfiles; do
    if [ ! -f $f ] ; then
        echo "$f not found, quit..."
        exit -1
    fi
done

#install the files
echo "cp $installfiles $ylda"
cp $installfiles $ylda

# cpush if you need
echo "cd $ylda && cpush $installfiles `pwd`"

echo 'bye~'

