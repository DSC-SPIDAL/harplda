appdir=~/hpda/harp2-project/harp2-app/build/

explist="1 2 3 4 5"

for expid in $explist; do
    echo $expid

    date
    hdfsdir=/user/pb/lda
    output=$hdfsdir/ldalgs-pubmed2m-var-$expid
    hadoop fs -rm -f -r $output/output
    if [ -d ldalgs-pubmed2m-var-$expid ] ; then
        rm -rf ldalgs-pubmed2m-var-$expid
    fi

    # run trainer
    hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /user/pb/data/pubmed-2M/split 1000 0.05 0.01 1000 1000000 100000 10 10 $output /mnt/disk1/pb/tmp/ld True
    
    # check result
    hadoop fs -copyToLocal $output .
    date
done

sh run_eval.sh
