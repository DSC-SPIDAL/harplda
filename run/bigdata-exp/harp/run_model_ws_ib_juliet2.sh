cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 100 40 /ldarttws2226 true 2
cexec monitor.sh stop ldarttws2226
monitor.sh collect ldarttws2226
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 100 40 /ldarttws2217 true 2
cexec monitor.sh stop ldarttws2217
monitor.sh collect ldarttws2217
collect_log.sh auto

