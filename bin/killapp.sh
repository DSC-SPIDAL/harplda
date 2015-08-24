#!/bin/bash

if [ $# -ne 1 ]; then
    echo 'Usage: killapp.sh <app name>'
    exit -1
fi

# Getting the PID of the process
APP=$1
PID=`pgrep $APP`

if [ "$?" != "0" ] ; then
    echo "$APP not found, quit"
    exit -2
fi

# Number of seconds to wait before using "kill -9"
WAIT_SECONDS=10

# Counter to keep count of how many seconds have passed
count=0

while kill $PID > /dev/null
do
    # Wait for one second
    sleep 1
    # Increment the second counter
    ((count++))

    # Has the process been killed? If so, exit the loop.
    if ! ps -p $PID > /dev/null ; then
        break
    fi

    # Have we exceeded $WAIT_SECONDS? If so, kill the process with "kill -9"
    # and exit the loop
    if [ $count -gt $WAIT_SECONDS ]; then
        kill -9 $PID
        break
    fi
done
echo "$APP Process $PID has been killed after $count seconds."
