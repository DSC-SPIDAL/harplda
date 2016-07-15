cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 100 40 /ldarttws2121 true 2
cexec monitor.sh stop ldarttws2121
monitor.sh collect ldarttws2121
collect_log.sh auto
cexec monitor.sh start eth0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /enwiki/ 10000 0.01 0.01 200 1000000 100 40 /ldarttws2111 true 2
cexec monitor.sh stop ldarttws2111
monitor.sh collect ldarttws2111
collect_log.sh auto
