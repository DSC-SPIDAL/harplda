#!/bin/bash
homedir=/tmp/hpda/test/
bindir=$homedir/warplda/bin
dataroot=$homedir/dataset/


#
# init
#
init()
{
    #set alpha=50/K
    alpha=50
#alpha=`echo "scale=4; 50/$topic" | bc`
#    echo "init:set alpha to 50/K = $alpha"
    datadir=$dataroot/$dataset/warplda-$nodes/train

    case $dataset in
        nytimes)
            #alpha=0.1
            beta=0.01
            num_vocabs=111400
            max_doc=300000
            data_cap=800
            ;;
        pubmed2m)
            #alpha=0.1
            beta=0.01
            num_vocabs=144400
            max_doc=2100000
            data_cap=1500
            ;;
        pubmed)
            #alpha=0.1
            beta=0.01
            num_vocabs=144400
            max_doc=8300000
            data_cap=6200
            ;;
        *) echo "unkown dataset: $dataset"; help; exit 1;;
    esac
}


# 4. Run LightLDA
runwarplda()
{
    cmd="$bindir/warplda --niter $iter --mh $mh_step --prefix $datadir"
    echo "Start: $cmd"

#$bindir/lightlda.new -num_vocabs $num_vocabs -num_topics $topic -num_iterations $iter -alpha $alpha -beta $beta -mh_steps $mh_step -num_local_workers $threads -num_blocks 1 -max_num_document $max_doc -input_dir $datadir -data_capacity $data_cap  | tee $logfile
    
    logfile="warplda_"$dataset"_t"$topic"_"$nodes"x"$threads"_i"$iter"_"$alpha"_"$beta"_"$mh_step"_$1.log"
    if [ -f $logfile ] ; then
        echo "$logfile exist, skip this test"
    else
        export OMP_NUM_THREADS=$threads
        #$bindir/warplda --niter $iter --mh $mh_step --prefix $datadir --dumpmodel false --beta $beta --alpha $alpha --dumpz false -k $topic | tee $logfile
        $bindir/warplda --niter $iter --mh $mh_step --prefix $datadir --beta $beta --alpha $alpha --k $topic | tee $logfile
    fi
}

#
# main
#
if [ $# -eq 0 ]; then
    echo "runwarplda.sh <dataset> <iters> <topics> <nodes> <threads> <mh_steps> <runid>"
else
    dataset=$1
    iter=$2
    topic=$3
    nodes=$4
    threads=$5
    mh_step=$6
    runid=$7

    echo $dataset

    if [ -z $thread ]; then
        thread=1
    fi
    if [ -z $iter ] ; then
        iter=100
    fi
    if [ -z $topic ] ; then
        topic=1000
    fi
    if [ -z $nodes ] ; then
        nodes=1
    fi
    if [ -z $mh_step ] ; then
        mh_step=1
    fi
    if [ -z "$dataset" ] ; then
        dataset=nytimes
    fi
    if [ -z "$runid" ] ; then
        runid=`date +%m%d%H%M%S`
    fi


    init

    # run experiments
    runwarplda $runid
fi

