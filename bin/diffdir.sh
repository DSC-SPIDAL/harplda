#!/bin/sh

if [ $# -ne "2" ] ; then
    echo "Usage: diffdir <srcdir> <dstdir>"
    exit 0
fi

diff -rq $1 $2 |grep diff | awk '{print "cp ",$2,$4}'
