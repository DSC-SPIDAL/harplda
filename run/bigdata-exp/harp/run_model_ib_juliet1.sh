cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda121 /tmp/lda true
cexec monitor.sh stop lda121
monitor.sh collect lda121
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda122 /tmp/lda true true 2
cexec monitor.sh stop lda122
monitor.sh collect lda122
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda123 /tmp/lda true false 2
cexec monitor.sh stop lda123
monitor.sh collect lda123
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda221 /tmp/lda true
cexec monitor.sh stop lda221
monitor.sh collect lda221
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda222 /tmp/lda true true 2
cexec monitor.sh stop lda222
monitor.sh collect lda222
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda223 /tmp/lda true false 2
cexec monitor.sh stop lda223
monitor.sh collect lda223
collect_log.sh auto
