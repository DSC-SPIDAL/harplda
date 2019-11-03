confs=(8)

for pat in ${confs[*]}; do
grep " $pat" list.txt > bigram_test_"$pat".conf
grep harp bigram_test_"$pat".conf > bigram_test_"$pat"_harp.conf
done

grep harp list.txt > bigram_test_harp_scale.conf
