#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /ldalgs2221 /tmp/lda true true 2 2
#cexec monitor.sh stop ldalgs2221
#monitor.sh collect ldalgs2221
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /enwiki-bigram-100/ 500 0.01 0.01 100 1000000 100 40 /ldarttws2232 true 2
#cexec monitor.sh stop ldarttws2232
#monitor.sh collect ldarttws2232
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /gutenberg-100 10000 0.01 0.01 100 1000000 100 40 /ldarttws2242 true 2
#cexec monitor.sh stop ldarttws2242
#monitor.sh collect ldarttws2242
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttlgs.LDALauncher /gutenberg-100 10000 0.01 0.01 100 1000000 100 40 /ldartt2242 true 2 1 0 true
#cexec monitor.sh stop ldartt2242
#monitor.sh collect ldartt2242
#collect_log.sh auto
#cexec monitor.sh start ib0
#hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /ldalgs2222 /tmp/lda true true 2 4
#cexec monitor.sh stop ldalgs2222
#monitor.sh collect ldalgs2222
#collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldalgs.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 500000 100 40 /ldalgs2223 /tmp/lda true true 2 4
cexec monitor.sh stop ldalgs2223
monitor.sh collect ldalgs2223
collect_log.sh auto

