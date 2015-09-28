yarn application --list > list
apps=`cut -f 1 list | grep -P "^app*"`

for app in $apps; do
    
    cmd="yarn application --kill $app"
    echo $cmd
    $cmd
done
