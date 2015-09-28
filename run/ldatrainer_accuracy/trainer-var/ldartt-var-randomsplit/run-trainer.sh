appdir=~/hpda/harp2-project/harp2-app/build/

#explist="2 3 4 5 6 7 8 9 10"
explist="2 3 4 5 6 7 8 9 "

for expid in $explist; do
    echo $expid

    date
    hdfsdir=/user/pb/lda
    output=$hdfsdir/ldartt-pubmed2m-var-$expid
    hadoop fs -rm -f -r $output/output
    if [ -d ldartt-pubmed2m-var-$expid ] ; then
        rm -rf ldartt-pubmed2m-var-$expid
    fi

    # run trainer
    hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /user/pb/data/pubmed-2M/split 1000 0.05 0.01 1000 1000000 10000 10 10 $output /mnt/disk1/pb/tmp/ld True
    
    # check result
    hadoop fs -copyToLocal $output .
    date
done
