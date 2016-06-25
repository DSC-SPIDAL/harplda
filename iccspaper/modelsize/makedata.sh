sed 's/[a-zA-Z:,_]//g' $1 | sed '/^\s*$/d' >$1.txt
