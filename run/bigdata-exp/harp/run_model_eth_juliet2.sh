#cexec monitor.sh start eth0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda311 /tmp/lda true
#cexec monitor.sh stop lda311
#monitor.sh collect lda311
#cexec monitor.sh start eth0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda312 /tmp/lda true true
#cexec monitor.sh stop lda312
#monitor.sh collect lda312
#cexec monitor.sh start eth0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda313 /tmp/lda true false
#cexec monitor.sh stop lda313
#monitor.sh collect lda313
#cexec monitor.sh start eth0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /new-clueweb/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda411 /tmp/lda true
#cexec monitor.sh stop lda411
#monitor.sh collect lda411
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda412 /tmp/lda true true
cexec monitor.sh stop lda412
monitor.sh collect lda412
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda413 /tmp/lda true false
cexec monitor.sh stop lda413
monitor.sh collect lda413
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda311 /tmp/lda true
cexec monitor.sh stop lda311
monitor.sh collect lda311
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda312 /tmp/lda true true
cexec monitor.sh stop lda312
monitor.sh collect lda312
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda313 /tmp/lda true false
cexec monitor.sh stop lda313
monitor.sh collect lda313
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /new-clueweb/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda411 /tmp/lda true
cexec monitor.sh stop lda411
monitor.sh collect lda411
collect_log.sh auto