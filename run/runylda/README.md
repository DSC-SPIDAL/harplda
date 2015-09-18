Run YLDA on Madrid cluster
===========================

cd ~/hpda/test/ylda

1. dist trainset
    $lda-test/bin/distrib <srcdir> <destdir> <slaves>
    !!! use absolute dir path
    
    cd pubmed2m
    ~/hpda/lda-test/bin/distrib `pwd`/raw /scratch/pengb/hpda/test/pubmed2m ../script/slaves
    
2. formatter
    cd formatter
    
    sh ../make_formatter.sh
    cpush * /scratch/pengb/hpda/test/bin
    
    cexec 'rm /scratch/pengb/hpda/test/work/*'
    cexec 'ls /scratch/pengb/hpda/test/work/'
    cexec 'sh /scratch/pengb/hpda/test/bin/run_formatter.$HOSTNAME'

3. DM_Server
    cd runserver
    sh ../make_runserver.sh ../script/slaves
    cpush * /scratch/pengb/hpda/test/bin
    
    cexec "sh /scratch/pengb/hpda/test/bin/killapp.sh DM_Server"
    cexec 'sh /scratch/pengb/hpda/test/bin/run_server.$HOSTNAME'
    
4. run learntopics

    cd learner/
    cp ../runserver/server.list .
    sh ../make_lda.sh ../script/slaves
    cpush * /scratch/pengb/hpda/test/bin
    cexec 'sh /scratch/pengb/hpda/test/bin/run_lda.$HOSTNAME'


Run YLDA on Julet cluster
=============================
working dir = ~/hpda/test/ylda

### 1. data

cd enwiki-1M
~/hpda/lda-test/bin/distrib `pwd`/raw /mnt/vol1/pengb/hpda/test/ylda/enwiki-1M ../conf/juliet.hostname

### 2. data formatter

sh ../scripts/make_formatter.sh ../conf/juliet.hostname
cpush * /mnt/vol1/pengb/hpda/test/bin
cexec 'sh  "/mnt/vol1/pengb/hpda/test/bin/run_formatter."$HOSTNAME'

### 3. DM_Server

cd runserver
sh ../scripts/make_runserver.sh ../conf/juliet.hostname ../conf/juliet.ip
cpush * /mnt/vol1/pengb/hpda/test/bin
cexec 'sh  "/mnt/vol1/pengb/hpda/test/bin/run_server."$HOSTNAME'

### 4. run learntopics

cd learner/
cp ../runserver/server.list .
sh ../scripts/make_lda.sh ../conf/juliet.hostname 1000
cpush * /mnt/vol1/pengb/hpda/test/bin
date && cexec 'sh  "/mnt/vol1/pengb/hpda/test/bin/run_lda."$HOSTNAME' && date

### 5. collect global dict and model
cd global_dict
sh ../scripts/build_gdict.sh ../conf/juliet.hostname

cd modeldump
sh ../scripts/make_modeldump.sh ../conf/juliet.hostname
cpush * /mnt/vol1/pengb/hpda/test/bin
cexec 'sh  "/mnt/vol1/pengb/hpda/test/bin/run_modeldump."$HOSTNAME'

cd global_model
sh ../scripts/build_gmodel.sh ../conf/juliet.hostname

### 6. close up
cd interval_model
sh ../scripts/build_intervalmodel.sh ../conf/juliet.hostname

cexec "sh /mnt/vol1/pengb/hpda/test/bin/killapp.sh DM_Server"

### 7. prepare for new experiments
cexec "cd /mnt/vol1/pengb/hpda/test/ylda && mv work work-####SAVENAME####"
cexec "cd /mnt/vol1/pengb/hpda/test/ylda && mkdir work"
cexec "cd /mnt/vol1/pengb/hpda/test/ylda && cp input/* work"



