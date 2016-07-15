cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb/ 10000 0.01 0.01 10 1000000 500000 30 64 /lda220 /tmp/lda true true
cexec monitor.sh stop lda22-ib
monitor.sh collect lda22-ib
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb/ 10000 0.01 0.01 10 1000000 500000 30 64 /lda230 /tmp/lda true false
cexec monitor.sh stop lda23-ib
monitor.sh collect lda23-ib
