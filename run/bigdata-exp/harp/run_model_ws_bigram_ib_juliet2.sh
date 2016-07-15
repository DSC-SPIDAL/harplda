#hadoop fs -put /mnt/vol2/pengb/hpda/test/bigram/hdfs/enwiki-bigram-100  /
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /enwiki-bigram-100/ 500 0.01 0.01 100 1000000 100 40 /ldarttws2231 true 2
#cexec monitor.sh stop ldarttws2231
#monitor.sh collect ldarttws2231
#collect_log.sh auto
#hadoop fs -put /mnt/vol2/pengb/hpda/test/gutenberg/hdfs/gutenberg-100 /
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /gutenberg-100 10000 0.01 0.01 100 1000000 100 40 /ldarttws2241 true 2
#cexec monitor.sh stop ldarttws2241
#monitor.sh collect ldarttws2241
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttlgs.LDALauncher /gutenberg-100 10000 0.01 0.01 100 1000000 100 40 /ldartt2241 true 2 1 0 true
#cexec monitor.sh stop ldartt2241
#monitor.sh collect ldartt2241
#collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /gutenberg-100 20000 0.01 0.01 100 1000000 100 40 /ldarttws2242 true 1
cexec monitor.sh stop ldarttws2242
monitor.sh collect ldarttws2242
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttlgs.LDALauncher /gutenberg-100 20000 0.01 0.01 100 1000000 100 40 /ldartt2242 true 1 1 0 true
cexec monitor.sh stop ldartt2242
monitor.sh collect ldartt2242
collect_log.sh auto
