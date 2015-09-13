ylda=/scratch/pengb/ylda
work=/scratch/pengb/hpda/test/work

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo 'get server host from slaves'
    hosts=(`cat slaves`)
fi

server_id=1

datadir=/scratch/pengb/hpda/test/pubmed2m/
for host in ${hosts[*]}; do
    echo "echo \"run formatter on madrid-00$server_id\"" >  run_formatter.madrid-00$server_id
    cmd="cd $work"
    echo $cmd >> run_formatter.madrid-00$server_id
    cmd="for f in \`ls "$datadir$host"\` ;  do cat "$datadir$host"/\$f >>input.ylda ; done "
    echo $cmd >>  run_formatter.madrid-00$server_id

    echo "cd $ylda && source $ylda/setLibVars.sh" >> run_formatter.madrid-00$server_id
    cmd="cd $work && cat input.ylda | $ylda/formatter"
    echo $cmd >> run_formatter.madrid-00$server_id
    ((server_id++))
done


