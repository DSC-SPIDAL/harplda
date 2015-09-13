ylda=/scratch/pengb/ylda
work=/scratch/pengb/hpda/test/work

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo 'get server host from slaves'
    hosts=(`cat slaves`)
fi

topics=1000
iter=1000
alpha=50
beta=0.01
threads=12

server_list=`cat server.list`
server_id=1

for host in ${hosts[*]}; do
    echo "echo \"run learntopics on madrid-00$server_id\"" >  run_lda.madrid-00$server_id
    echo "cd $ylda && source $ylda/setLibVars.sh" >> run_lda.madrid-00$server_id
    cmd="cd $work && nohup $ylda/learntopics --topics=$topics --iter=$iter --servers=$server_list --alpha=$alpha --beta=$beta  --optimizestats=5000 --samplerthreads=$threads --chkptdir="/tmp" --chkptinterval=10 &"
    echo $cmd >> run_lda.madrid-00$server_id
    ((server_id++))
done

