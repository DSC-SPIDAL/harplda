#!/bin/bash

CurDir=$(pwd)

#
# init
#
init()
{
    case $trainer in
        petuum)
            binname="ldall"
            lib_path=$HOME/share/lib/petuum/
            src_path=$HOME/hpda/petuum/strads/
            appname=petuumlda
            ;;
        nomadlda)
            binname="f+nomad-lda"
            #lib_path="$HOME/share/lib;$HOME/share/lib/openmpi"
            lib_path=$HOME/share/lib
            src_path=$HOME/hpda/lda-test/tool/nomadlda/nomad-lda-exp-0.2/
            appname=nomadlda
            ;;
        warplda)
            binname=ldall
            lib_path=/N/u/fg474admin/share/lib/petuum/
            src_path=/N/u/fg474admin/hpda/petuum/strads/
            appname=petuum
            ;;
        *) echo "unkown dataset: $dataset"; help; exit 1;;
    esac

    get_pname

}

#
# get pid
#
get_pname()
{
## get the yarn chiild process name
#pname=$(ps -ef | grep "ldall" | awk '{ print $2 }' | head -1)
echo "ps -ef | gawk '{print $2, $8}' |grep $binname | gawk '{ print $2 }' | head -1"

pname=$(ps -ef | gawk '{print $2, $8}' |grep $binname | gawk '{ print $1}' | head -1)

echo "get pname: "$pname
}


#
# run vtune
#
run_vtune()
{
    resdir=/scratch/vtuneres/
    if [ ! -d $resdir ] ; then
        mkdir -p $resdir
        chmod g+w $resdir
    fi
    ## specify the collect type

    ## action
    # action=collect
    # action=collect-with

    ## collect type supported on haswell
    #type=general-exploration
    # hotspots
    # general-exploration
    # advanced-hotspots
    # runsa
    # advanced-hotspots    Advanced Hotspots
    # concurrency          Concurrency
    # cpugpu-concurrency   CPU/GPU Concurrency
    # general-exploration  General Exploration
    # hotspots             Basic Hotspots
    # locksandwaits        Locks and Waits
    # memory-access        Memory Access
    # tsx-exploration      TSX Exploration
    # tsx-hotspots         TSX Hotspots

    #check type
    alltype=(general-exploration hotspots general-exploration advanced-hotspots advanced-hotspots
            concurrency
        cpugpu-concurrency
        general-exploration
        hotspots
        locksandwaits
        memory-access
        tsx-exploration
        tsx-hotspots
        runsa_avx
        runsa_cache
        )

    found=0
    for tt in ${alltype[*]}; do
        if [[ "$type" == "$tt" ]]; then
            found=1
        fi
    done
    if [ $found -eq 0 ] ; then
        echo "$type not support by vtune yet, quit"
        return
    fi

    ## knob option
    knob_runsa_cache=MEM_LOAD_UOPS_RETIRED.L1_HIT,MEM_LOAD_UOPS_RETIRED.L2_HIT,MEM_LOAD_UOPS_RETIRED.L3_HIT,MEM_LOAD_UOPS_RETIRED.L1_MISS,MEM_LOAD_UOPS_RETIRED.L2_MISS,MEM_LOAD_UOPS_RETIRED.L3_MISS
    knob_runsa_avx=INST_RETIRED.ANY,UOPS_EXECUTED.CORE,UOPS_RETIRED.ALL_PS,MEM_UOPS_RETIRED.ALL_LOADS_PS,MEM_UOPS_RETIRED.ALL_STORES_PS,AVX_INSTS.ALL


    ## name and result path
    obj=R-$appname-$action-$runid
    resDir=$resdir/$obj
    
    ## if res already existed remove that
    rm -rf $resDir
    
    ## mode: auto, native, mixed
    mode=auto
    ## genearated data size (MB), 0 is unlimited
    dataLimit=0
    ## time limit unit time of training time per iteration
    #sec=180
    ## search path
    #path_daal=/N/u/fg474admin/lc37/Lib/DAAL2017/__release_lnx/daal/lib/intel64_lin
    #path_tbb=/opt/intel/compilers_and_libraries_2016/linux/tbb/lib/intel64_lin/gcc4.4
    #path_daal_misc=/N/u/fg474admin/lc37/Lib/DAAL2017/daal-misc/lib
    #src_path_daal=/N/u/fg474admin/lc37/Lib/DAAL2017/daal
    #lib_petuum_path=/N/u/fg474admin/share/lib/petuum/
    #src_petuum_path=/N/u/fg474admin/hpda/petuum/strads/
    
    ## start vtune command line tool 
    #cmd="amplxe-cl -$action $type 
    cmd="-mrte-mode=$mode \
        -data-limit=$dataLimit \
        -duration=$sec \
        -r $resDir \
        -search-dir $lib_path \
        -source-search-dir $src_path "
    cmdtail="-target-pid $pname "

    # -k event_config=$knob_runsa_cache \
    #amplxe-cl -collect $action \
    #    -mrte-mode=$mode \
    #    -data-limit=$dataLimit \
    #    -duration=$sec \
    #    -r $resDir \
    #    -search-dir $lib_path \
    #    -source-search-dir $src_path \
    #    -target-pid $pname

    # check action
    case $type in
        runsa_avx)
            cmd="amplxe-cl -collect-with runsa -knob event-config=$knob_runsa_avx $cmd"
            ;;
        runsa_cache)
            cmd="amplxe-cl -collect-with runsa -knob event-config=$knob_runsa_cache $cmd"
            ;;
        *)
            echo "standard type: $type"
            cmd="amplxe-cl -collect $type $cmd"
            ;;
    esac
    cmd=$cmd" "$cmdtail

    #finally, let's run
    echo $cmd
    `$cmd`
}

#
# main
#
if [ $# -eq 0 ]; then
    echo "amplxe-collect.sh <trainer> <type> <secs> <runid>"
else
    trainer=$1
    type=$2
    sec=$3
    runid=$4

    echo $trainer

    if [ -z "$type" ] ; then
        type=general-exploration
    fi

    if [ -z "$sec" ] ; then
        sec=180
    fi

    if [ -z "$runid" ] ; then
        runid=`date +%m%d%H%M%S`
    fi

    init

    # run experiments
    run_vtune
fi





