cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda111 /tmp/lda true
cexec monitor.sh stop lda111
monitor.sh collect lda111
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda112 /tmp/lda true true 2
cexec monitor.sh stop lda112
monitor.sh collect lda112
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda113 /tmp/lda true false 2
cexec monitor.sh stop lda113
monitor.sh collect lda113
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldartt.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda211 /tmp/lda true
cexec monitor.sh stop lda211
monitor.sh collect lda211
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda212 /tmp/lda true true 2
cexec monitor.sh stop lda212
monitor.sh collect lda212
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 30 64 /lda213 /tmp/lda true false 2
cexec monitor.sh stop lda213
monitor.sh collect lda213
collect_log.sh auto
