trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

#sh runpetuum.sh juliet-100 enwiki eth0 101
#sh runpetuum.sh juliet-100 enwiki ib0 101
#sh runpetuum.sh juliet-100 clueweb ib0 101
#sh runpetuum.sh juliet-100 clueweb eth0 101
#sh runpetuum.sh juliet-100 enwiki eth0 102
#sh runpetuum.sh juliet-100 enwiki ib0 102
#sh runpetuum.sh juliet-100 clueweb ib0 102
#sh runpetuum.sh juliet-100 clueweb eth0 102
sh runpetuum.sh juliet-100 enwiki-bigram ib0 1k-1
sleep 30
sh runpetuum.sh juliet-100 enwiki-bigram ib0 1k-2
