cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /user/fg474admin/data/enwiki-30 10000 0.01 0.01 200 1000000 30 64 /ldaw1211 true 2
cexec monitor.sh stop ldaw1211
monitor.sh collect ldaw1211
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /user/fg474admin/data/enwiki-30 10000 0.01 0.01 200 1000000 30 64 /ldaw1212 true 2
cexec monitor.sh stop ldaw1212
monitor.sh collect ldaw1212
collect_log.sh auto
cexec monitor.sh start ib0
hadoop jar harp2-app-hadoop-2.6.0.jar edu.iu.ldarttws.LDALauncher /new-clueweb2/ 10000 0.01 0.01 200 1000000 30 64 /ldaw1221 true 2
cexec monitor.sh stop ldaw1221
monitor.sh collect ldaw1221
collect_log.sh auto
