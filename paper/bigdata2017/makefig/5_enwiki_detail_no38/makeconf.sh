#confs=("2x4_" "2x16_" "4x4_" "4x16_" "8x4_" "8x16_")
confs=(1 2 4 8)

for pat in ${confs[*]}; do
grep " $pat" list.txt > enwiki_detail_"$pat".conf
done

cp list.txt enwiki_detail_scale.conf
