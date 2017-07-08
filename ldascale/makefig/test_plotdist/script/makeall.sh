python ~/hpda/lda-test/src/analysis/fitcurve.py --draw speedup distenwiki_1K_8x16.conf 
python ~/hpda/lda-test/src/analysis/fitcurve.py --draw speedup distenwiki_10K_8x16.conf 
mkdir overhead
cd overhead/
cp /tmp/hpda//test/experiments/logs/2_dist_enwiki/lightlda/light_enwiki_10k/lightlda_enwiki_t10000_8x16_i300_.00500000_0.01_4_0613.log .
cp /tmp/hpda//test/experiments/logs/2_dist_enwiki/nomadlda/nomad_enwiki_mvapich2/nomadlda_enwiki_t10000_8x16_i20_50_0.01_t500_l2_L2_0613-noreid-threadlog-mvapich2.log .
cp /tmp/hpda/test/experiments/results/2_dist_enwiki/nomadlda/nomadlda_enwiki_t10000_8x16_i20_50_0.01_t500_l2_L2_0613-noreid-threadlog-mvapich2.*time .
cp /tmp/hpda/test/experiments/results/2_dist_enwiki/lightlda//lightlda_enwiki_t10000_8x16_i300_.00500000_0.01_4_0613.*time .
cp /tmp/hpda/test/experiments/results/2_dist_enwiki/harplda/harp_enwiki_j128_8x16_k10000_*.*time .
python ~/hpda/lda-test/src/analysis/analy_threadlog.py lightlda lightlda_enwiki_t10000_8x16_i300_.00500000_0.01_4_0613.log 
python ~/hpda/lda-test/src/analysis/analy_threadlog.py nomadlda nomadlda_enwiki_t10000_8x16_i20_50_0.01_t500_l2_L2_0613-noreid-threadlog-mvapich2.log
python ~/hpda/lda-test/src/analysis/analy_threadlog.py harp harp_enwiki_j128_8x16_k10000_notimer_l100_h100_r2_exp2dist-noreid.itertime 
python ~/hpda/lda-test/src/analysis/analy_threadlog.py harp harp_enwiki_j128_8x16_k10000_timer_l40_h80_r2_exp2dist-noreid.itertime 
cp * /tmp/hpda/test/experiments/results/test_distcv/
cd ..
