#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo "usage: make_formatter.sh <hostname file>"
    exit 
fi


server_id=1

for host in ${hosts[*]}; do
    echo "echo \"run formatter on $host\"" >  run_formatter.$host
    cmd="cd $work"
    echo $cmd >> run_formatter.$host
    cmd="for f in \`ls "$datadir$host"\` ;  do cat "$datadir$host"/\$f >>input.ylda ; done "
    echo $cmd >>  run_formatter.$host

    echo "cd $ylda && source $ylda/setLibVars.sh" >> run_formatter.$host
    cmd="cd $work && cat input.ylda | $ylda/formatter"
    echo $cmd >> run_formatter.$host
    ((server_id++))
done


