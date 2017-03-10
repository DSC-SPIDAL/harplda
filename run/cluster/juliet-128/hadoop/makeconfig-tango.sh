_hostname=`hostname`
_ip=`python -c "import socket, sys; print socket.gethostbyname(\"$_hostname\")"`
echo $_ip 
ibname=`echo $_ip | sed "s/172\.16\.2\./cc/g" -`
ibname=$ibname"-opa"
echo $ibname
sed "s/__HOSTNAME__/$ibname/g" yarn-site-tango.xml >yarn-site.xml
