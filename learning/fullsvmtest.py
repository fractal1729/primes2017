from learning import svmtest
import numpy as np

num_trials = 100

sm1, dm1, m1, tm1 = svmtest.runmany(1,num_trials)
sm2, dm2, m2, tm2 = svmtest.runmany(2,num_trials)
sm3, dm3, m3, tm3 = svmtest.runmany(3,num_trials)
sm4, dm4, m4, tm4 = svmtest.runmany(4,num_trials)
sn1, n1, dn1, tn1 = svmtest.runmany(1,num_trials,'nn')
sn2, n2, dn2, tn2 = svmtest.runmany(2,num_trials,'nn')
sn3, n3, dn3, tn3 = svmtest.runmany(3,num_trials,'nn')
sn4, n4, dn4, tn4 = svmtest.runmany(4,num_trials,'nn')

compscores = np.array([np.average(sm1), np.average(sm2), np.average(sm3), np.average(sm4)])
comptimes = np.array([tm1, tm2, tm3, tm4])
incscores = np.array([np.average(sn1), np.average(sn2), np.average(sn3), np.average(sn4)])
inctimes = np.array([tn1, tn2, tn3, tn4])
m = np.array([m1, m2, m3, m4])
n = np.array([n1, n2, n3, n4])
sm = np.array([sm1, sm2, sm3, sm4])
sn = np.array([sn1, sn2, sn3, sn4])

summary = np.array([compscores, comptimes, incscores, inctimes])
detailed = np.array([m, n, sm, sn])
np.save("learning/svmtestsummary", summary)
np.save("learning/svmtestdetailed", detailed)