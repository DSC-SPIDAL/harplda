cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda511 /tmp/lda true true 2
cexec monitor.sh stop lda511
monitor.sh collect lda511
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda512 /tmp/lda true true 4
cexec monitor.sh stop lda512
monitor.sh collect lda512
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /lda513 /tmp/lda true true 8
cexec monitor.sh stop lda513
monitor.sh collect lda513
collect_log.sh auto
