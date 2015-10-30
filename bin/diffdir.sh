#!/bin/sh

help(){
    echo "Usage: diffdir <-diff|-cp|-rcp> <srcdir> <dstdir>"
}

case $1 in
    -diff)
        shift
        diff -rq $1 $2 |grep diff | awk '{print "diff ",$2,$4}'
        ;;
    -cp)
        shift
        diff -rq $1 $2 |grep diff | awk '{print "cp ",$2,$4}'
        ;;
    -rcp)
        shift
        diff -rq $1 $2 |grep diff | awk '{print "cp ",$4,$2}'
        ;;
    *) echo "Unrecognized command: $CMD"; help; exit 1;;
esac
