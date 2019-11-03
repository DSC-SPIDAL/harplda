
dirs=(nytimes pubmed enwiki)

for dir in ${dirs[*]}; do
    grep $dir list.txt |grep 1000_ |sort >1_basic_single_"$dir"_1k.conf
    grep $dir list.txt |grep 10000_ |sort >1_basic_single_"$dir"_10k.conf
done

