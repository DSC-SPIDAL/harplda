
dirs=(nytimes pubmed enwiki)

for dir in ${dirs[*]}; do
    grep $dir list.txt |grep k1000_  >1_basic_1x1_"$dir"_1k.conf
    grep $dir list.txt |grep t1000_  >>1_basic_1x1_"$dir"_1k.conf
    grep $dir list.txt |grep k10000_  >1_basic_1x1_"$dir"_10k.conf
    grep $dir list.txt |grep t10000_  >>1_basic_1x1_"$dir"_10k.conf
done

    grep enwiki list.txt |grep 5000_ |sort >1_basic_1x1_enwiki_5k.conf
