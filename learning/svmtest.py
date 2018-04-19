# squared exponential/gaussian kernel, also linear kernel
from sklearn import svm
from learning import processdata
import sys
import random
import numpy as np
import time

n = 19
m = 5

myX, Y = processdata.trainingCustomFeatures()
nnX, Y = processdata.trainingInceptionFeatures()

myX = myX[np.concatenate(np.array([np.arange(0,50), np.arange(55,60), np.arange(65, 105)]))]
nnX = nnX[np.concatenate(np.array([np.arange(0,50), np.arange(55,60), np.arange(65, 105)]))]

bothX = np.concatenate((myX, nnX), axis=1)

numcorrect = {}
numtotal = {}

def initcounters():
	for i in range(n*m):
		numcorrect[sum(myX[i])] = 0
		numcorrect[sum(nnX[i])] = 0
		numtotal[sum(myX[i])] = 0
		numtotal[sum(nnX[i])] = 0

def accuracydata():
	mycor = []
	nncor = []
	mytot = []
	nntot = []
	for i in range(n*m):
		mycor += [numcorrect[sum(myX[i])]]
		nncor += [numcorrect[sum(nnX[i])]]
		if numtotal[sum(myX[i])] > 0:
			mytot += [numtotal[sum(myX[i])]]
		else:
			mytot += [-1]
		if numtotal[sum(nnX[i])] > 0:
			nntot += [numtotal[sum(nnX[i])]]
		else:
			nntot += [-1]
	mycor = np.array(mycor)
	nncor = np.array(nncor)
	mytot = np.array(mytot)
	nntot = np.array(nntot)
	return nncor.astype(np.float64)/nntot, mycor.astype(np.float64)/mytot

def maketraintest(X, Y, trainops, testops):
	trainX = []
	trainY = []
	testX = []
	testY = []
	for i in range(n):
		j = random.randint(0, len(trainops)-1)
		trainX += [X[m*i+k] for k in trainops[j]]
		trainY += [Y[m*i+k] for k in trainops[j]]
		testX += [X[m*i+k] for k in testops[j]]
		testY += [Y[m*i+k] for k in testops[j]]
	return np.array(trainX), np.array(trainY), np.array(testX), np.array(testY)

def oneshot(X, Y):
	trainops = [[0], [1], [2], [3], [4]]
	testops = [[1,2,3,4], [0,2,3,4], [0,1,3,4], [0,1,2,4], [0,1,2,3]]
	return maketraintest(X, Y, trainops, testops)

def twoshot(X, Y):
	trainops = [[0,1], [0,2], [0,3], [0,4], [1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
	testops = [[2,3,4], [1,3,4], [1,2,4], [1,2,3], [0,3,4], [0,2,4], [0,2,3], [0,1,4], [0,1,3], [0,1,2]]
	return maketraintest(X, Y, trainops, testops)

def threeshot(X, Y):
	trainops = [[2,3,4], [1,3,4], [1,2,4], [1,2,3], [0,3,4], [0,2,4], [0,2,3], [0,1,4], [0,1,3], [0,1,2]]
	testops = [[0,1], [0,2], [0,3], [0,4], [1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
	return maketraintest(X, Y, trainops, testops)

def fourshot(X, Y):
	trainops = [[1,2,3,4], [0,2,3,4], [0,1,3,4], [0,1,2,4], [0,1,2,3]]
	testops = [[0], [1], [2], [3], [4]]
	return maketraintest(X, Y, trainops, testops)

def run(trainsize, X, Y, method='linear'):
	data = None
	if trainsize == 1:
		data = oneshot(X, Y)
	if trainsize == 2:
		data = twoshot(X, Y)
	if trainsize == 3:
		data = threeshot(X, Y)
	if trainsize == 4:
		data = fourshot(X, Y)
	trainX, trainY, testX, testY = data
	clf = svm.LinearSVC()
	if method == 'rbf':
		clf = svm.SVC(decision_function_shape='ovo')
	clf.fit(trainX, trainY)
	pred = clf.predict(testX)
	numright = 0
	for i in range(len(testY)):
		numtotal[sum(testX[i])] += 1
		if pred[i] == testY[i]:
			numright += 1
			numcorrect[sum(testX[i])] += 1
	return float(numright)/len(testY)

def runmany(trainsize, numiter=50, dataset='my', method='linear'):
	initcounters()
	X = myX
	if dataset == 'nn':
		X = nnX
	if dataset == 'both':
		X = bothX
	s = []
	start = time.time()
	for i in range(numiter):
		s += [run(trainsize, X, Y, method=method)]
		sys.stdout.write("\r"+str(i)+" of "+str(numiter)+" complete.   ")
		sys.stdout.flush()
	print ""
	end = time.time()
	runtime = end-start
	nnresults, myresults = accuracydata()
	return s, nnresults, myresults, runtime

# if __name__ == '__main__':
# 	run(1, nnX, Y)