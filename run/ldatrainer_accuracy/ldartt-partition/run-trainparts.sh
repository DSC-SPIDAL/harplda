appdir=~/hpda/harp2-project/harp2-app/build/
date
output=/user/pb/lda/ldartt-pubmed2m-0.5kpart
#hadoop fs -rm -f -r $output/output
hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /user/pb/data/pubmed-2M/split 1000 0.05 0.01 1000 1000000 500 10 10 $output /mnt/disk1/pb/tmp/ld True
hadoop fs -copyToLocal $output .
date

output=/user/pb/lda/ldartt-pubmed2m-1kpart
#hadoop fs -rm -f -r $output/output
hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /user/pb/data/pubmed-2M/split 1000 0.05 0.01 1000 1000000 1000 10 10 $output /mnt/disk1/pb/tmp/ld True
hadoop fs -copyToLocal $output .
date

output=/user/pb/lda/ldartt-pubmed2m-5kpart
#hadoop fs -rm -f -r $output/output
hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /user/pb/data/pubmed-2M/split 1000 0.05 0.01 1000 1000000 5000 10 10 $output /mnt/disk1/pb/tmp/ld True
hadoop fs -copyToLocal $output .
date

output=/user/pb/lda/ldartt-pubmed2m-50kpart
#hadoop fs -rm -f -r $output/output
hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /user/pb/data/pubmed-2M/split 1000 0.05 0.01 1000 1000000 50000 10 10 $output /mnt/disk1/pb/tmp/ld True
hadoop fs -copyToLocal $output .
date


