#confs=(newlda_pubmed2m newlda_nytimes newlda_enwiki)

#for confname in ${confs[*]}: do
confname=$1

grep "1x1_" "$confname"_scale.conf >"$confname"_1x1.conf
grep "1x2_" "$confname"_scale.conf >"$confname"_1x2.conf
grep "1x4_" "$confname"_scale.conf >"$confname"_1x4.conf
grep "1x8_" "$confname"_scale.conf >"$confname"_1x8.conf
grep "1x16_" "$confname"_scale.conf >"$confname"_1x16.conf
grep "1x32_" "$confname"_scale.conf >"$confname"_1x32.conf

#done


#
#grep "1x1_" newlda_nytimes_scale.conf >newlda_nytimes_1x1.conf
#grep "1x2_" newlda_nytimes_scale.conf >newlda_nytimes_1x2.conf
#grep "1x4_" newlda_nytimes_scale.conf >newlda_nytimes_1x4.conf
#grep "1x8_" newlda_nytimes_scale.conf >newlda_nytimes_1x8.conf
#grep "1x16_" newlda_nytimes_scale.conf >newlda_nytimes_1x16.conf
#grep "1x32_" newlda_nytimes_scale.conf >newlda_nytimes_1x32.conf
