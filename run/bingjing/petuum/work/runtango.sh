sh runpetuum.sh tango-2 enwiki-1M ib0 A60-2

sed 's/threads=60/threads=90/g' conf/cluster_config.enwiki-1M.tango-2 >.sed
mv .sed conf/cluster_config.enwiki-1M.tango-2 
sh runpetuum.sh tango-2 enwiki-1M ib0 A90

# run 60 for a long task

sed 's/threads=90/threads=60/g' conf/cluster_config.enwiki-1M.tango-2 >.sed
sed 's/iter=5/iter=100/g' .sed >.sed.1
mv .sed.1 conf/cluster_config.enwiki-1M.tango-2 

sh runpetuum.sh tango-2 enwiki-1M ib0 B60

#python ~/hpda/lda-test/src/analysis/analy_timelog.py petuum-run petuum-tango-2-enwiki-1M-ib0-A45
