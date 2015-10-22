 for d in `ls`; do if [ -d $d ] ; then python ~/hpda/lda-test/src/analysis/analy_timelog.py harp $d; fi ; done
 for f in `ls *.computetime`; do diff $f ~/hpda/lda-test/run/harp_juliet/timelog/$f; done
 for f in `ls *.comput-stat`; do diff $f ~/hpda/lda-test/run/harp_juliet/timelog/$f; done
 for f in `ls *.commtime`; do diff $f ~/hpda/lda-test/run/harp_juliet/timelog/$f; done
 for f in `ls *.itertime`; do diff $f ~/hpda/lda-test/run/harp_juliet/timelog/$f; done
 cp lda*.* ~/hpda/lda-test/run/harp_juliet/timelog/
