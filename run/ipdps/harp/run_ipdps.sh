#application_1476393948100_0026	90	20	LDA	with timer tuning	1000
#application_1476393948100_0027	60	30	LDA	with timer tuning	1000
#application_1476393948100_0032	25	40	LDA	with timer tuning	1000
#application_1476393948100_0033	50	40	LDA	with timer tuning	1000
#application_1476393948100_0034	75	40	LDA	with timer tuning	1000


#sh ./analy_harp.sh /lda2540t application_1476393948100_0032 harp_clueweb30b_25x40_ipdps_0032
#sh ./analy_harp.sh /lda5040t application_1476393948100_0033 harp_clueweb30b_50x40_ipdps_0033
#sh ./analy_harp.sh /lda7540t application_1476393948100_0034 harp_clueweb30b_75x40_ipdps_0034
#sh ./analy_harp.sh /lda6030t application_1476393948100_0027 harp_clueweb30b_60x30_ipdps_0027
#sh ./analy_harp.sh /lda9020t application_1476393948100_0026 harp_clueweb30b_90x20_ipdps_0026
#sh ./analy_harp.sh /lda6020t application_1476393948100_0045 harp_clueweb30b_60x20_ipdps_0045
#sh ./analy_harp.sh /lda3020t application_1476393948100_0044 harp_clueweb30b_30x20_ipdps_0044
#sh ./analy_harp.sh /lda4520t application_1476814563991_0003  harp_clueweb30b_45x20_ipdps_0003
#sh ./analy_harp.sh /lda3020t1 application_1476814563991_0009  harp_clueweb30b_30x20_ipdps_0009
#sh ./analy_harp.sh /lda6020t1 application_1476814563991_0010  harp_clueweb30b_60x20_ipdps_0010
#sh ./analy_harp.sh /lda6020t2 application_1476814563991_0016  harp_clueweb30b_60x20_ipdps_0016
#sh ./analy_harp.sh /lda3020t2 application_1476814563991_0023  harp_clueweb30b_30x20_ipdps_0023
#sh ./analy_harp.sh /lda4520t2 application_1476814563991_0024  harp_clueweb30b_45x20_ipdps_0024

export TESTSET=clueweb-1M
#sh ./analy_harp.sh /lda3030clueweb application_1477146975236_0003  harp_clueweb30b_30x30_hsw72_ipdps_0003

sh ./analy_harp.sh /lda6020n    application_1477256680355_0001 harp_clueweb30b_60x20_hsw72_ipdps_N0001

sh ./analy_harp.sh /lda6020n1   application_1477256680355_0002 harp_clueweb30b_60x20_hsw72_ipdps_N0002

            
sh ./analy_harp.sh /lda3020t3   application_1477256680355_0005 harp_clueweb30b_30x20_hsw72_ipdps_N0005

sh ./analy_harp.sh /lda4520t3   application_1477256680355_0006 harp_clueweb30b_45x20_hsw72_ipdps_N0006

sh ./analy_harp.sh /lda6020t3   application_1477256680355_0007 harp_clueweb30b_60x20_hsw72_ipdps_N0007


#export TESTSET=enwiki-1M
#sh ./analy_harp.sh /lda3030enwiki application_1477146975236_0006  harp_enwiki_10x30_hsw72_ipdps_0006


