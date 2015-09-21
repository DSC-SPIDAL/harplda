appdir=~/hpda/harp2-project/harp2-app/build/
input=/user/pengb/data/pubmed-2M
date
output=/user/pengb/lda/ldartt-pubmed2m-30-64
#hadoop fs -rm -f -r $output/output
hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher $input 1000 0.05 0.01 1000 1000000 100000 30 64 $output /mnt/vol1/pengb/tmp/ True
hadoop fs -copyToLocal $output .
date

output=/user/pengb/lda/ldartt-pubmed2m-30-32
#hadoop fs -rm -f -r $output/output
hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher $input 1000 0.05 0.01 1000 1000000 100000 30 32 $output /mnt/vol1/pengb/tmp/ True
hadoop fs -copyToLocal $output .
date

output=/user/pengb/lda/ldartt-pubmed2m-30-16
#hadoop fs -rm -f -r $output/output
hadoop jar $appdir/harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher $input 1000 0.05 0.01 1000 1000000 100000 30 16 $output /mnt/vol1/pengb/tmp/ True
hadoop fs -copyToLocal $output .
date




