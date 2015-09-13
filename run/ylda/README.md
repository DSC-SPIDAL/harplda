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
