work1
=========

change the output log 
+ add timelog
+ add time-1, time-2, since the training time reported by the code is much less than the real value.
  by checking the source, time = training time(timeout setting), time-1 = time + overhead of lh calc
  and there is a all_reduce of Nwt in the lh calc code, it's time consuming

  anyway, need Nwt all keep in one node's memory is the fatal error for nomadlda code.


[2017-05-12 22:04:43] iter 128 time 50.02 totaltime 6446 time-1 289.9 time-2 7.812 eplasetime 4.149e+04 training-LL -1.61489e+11 Nwt 1706712543064 avg 57.0589 Nt 578223 nxt 30x30, throughput 4.620397e+04
after14889/14929 33358/51632 33418/746204 33067/278 33158/7323 33323/6280 33151/7036 33090/13081 33529/5999 33248/10036 33142/10971 33176/10462 33191/11728 33407/16543 33306/6619 32933/7160 33391/11343 33524/0 33
221/0 33091/0 33139/0 33398/8778 33471/7699 33570/7358 33530/0 33408/3463 33740/10304 33824/11292 33456/2258 11128/11158 


