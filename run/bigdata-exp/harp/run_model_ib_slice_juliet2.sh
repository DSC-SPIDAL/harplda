cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda521 /tmp/lda true true 2
cexec monitor.sh stop lda521
monitor.sh collect lda521
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda522 /tmp/lda true true 4
cexec monitor.sh stop lda522
monitor.sh collect lda522
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda523 /tmp/lda true true 8
cexec monitor.sh stop lda523
monitor.sh collect lda523
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda524 /tmp/lda true false 8
cexec monitor.sh stop lda524
monitor.sh collect lda524
collect_log.sh auto
