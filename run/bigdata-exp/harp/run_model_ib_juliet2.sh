#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 lda /tmp/lda false
#collect_log.sh auto
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 50 40 lda /tmp/lda false
#collect_log.sh auto
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 lda /tmp/lda false true
#collect_log.sh auto
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 50 40 lda /tmp/lda false true
#collect_log.sh auto
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 50 40 lda /tmp/lda false
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda321 /tmp/lda true
#cexec monitor.sh stop lda321
#monitor.sh collect lda321
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda322 /tmp/lda true true
#cexec monitor.sh stop lda322
#monitor.sh collect lda322
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda323 /tmp/lda true false
#cexec monitor.sh stop lda323
#monitor.sh collect lda323
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /new-clueweb/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda421 /tmp/lda true
#cexec monitor.sh stop lda421
#monitor.sh collect lda421
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda422 /tmp/lda true true
#cexec monitor.sh stop lda422
#monitor.sh collect lda422
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda423 /tmp/lda true false
#cexec monitor.sh stop lda423
#monitor.sh collect lda423
#collect_log.sh auto
#hadoop fs -mkdir /new-clueweb2
#hadoop fs -put /mnt/vol1/clueweb-10b-split/* /new-clueweb2/
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda4211 /tmp/lda true
#cexec monitor.sh stop lda4211
#monitor.sh collect lda4211
#collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda4221 /tmp/lda true true
cexec monitor.sh stop lda4221
monitor.sh collect lda4221
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda4231 /tmp/lda true false
cexec monitor.sh stop lda4231
monitor.sh collect lda4231
collect_log.sh auto
