# squared exponential/gaussian kernel, also linear kernel
from sklearn import svm
from learning import processdata
import random
import numpy as np

n = 16
m = 5

myX, Y = processdata.trainingCustomFeatures()
nnX, Y = processdata.trainingInceptionFeatures()

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

def oneshot():
	trainops = [[0], [1], [2], [3], [4]]
	testops = [[1,2,3,4], [0,2,3,4], [0,1,3,4], [0,1,2,4], [0,1,2,3]]
	return maketraintest(nnX, Y, trainops, testops), maketraintest(myX, Y, trainops, testops)

def twoshot():
	trainops = [[0,1], [0,2], [0,3], [0,4], [1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
	testops = [[2,3,4], [1,3,4], [1,2,4], [1,2,3], [0,3,4], [0,2,4], [0,2,3], [0,1,4], [0,1,3], [0,1,2]]
	return maketraintest(nnX, Y, trainops, testops), maketraintest(myX, Y, trainops, testops)

def threeshot():
	trainops = [[2,3,4], [1,3,4], [1,2,4], [1,2,3], [0,3,4], [0,2,4], [0,2,3], [0,1,4], [0,1,3], [0,1,2]]
	testops = [[0,1], [0,2], [0,3], [0,4], [1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
	return maketraintest(nnX, Y, trainops, testops), maketraintest(myX, Y, trainops, testops)

def fourshot():
	trainops = [[1,2,3,4], [0,2,3,4], [0,1,3,4], [0,1,2,4], [0,1,2,3]]
	testops = [[0], [1], [2], [3], [4]]
	return maketraintest(nnX, Y, trainops, testops), maketraintest(myX, Y, trainops, testops)

def run(trainsize):
	nndata = None
	mydata = None
	if trainsize == 1:
		nndata, mydata = oneshot()
	if trainsize == 2:
		nndata, mydata = twoshot()
	if trainsize == 3:
		nndata, mydata = threeshot()
	if trainsize == 4:
		nndata, mydata = fourshot()